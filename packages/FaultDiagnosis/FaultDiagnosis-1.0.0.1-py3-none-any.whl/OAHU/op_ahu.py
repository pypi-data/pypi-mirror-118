
from matplotlib import font_manager, rc
rc('font', family=font_manager.FontProperties(fname="\c:/Windows/Fonts/malgun.ttf").get_name())
fontprop = font_manager.FontProperties(fname="\c:/Windows/Fonts/malgunbd.ttf", size=12)

import pandas as pd
import numpy as np
import joblib
from sklearn import ensemble
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, precision_score, recall_score, confusion_matrix
from scipy.stats import wasserstein_distance
from scipy.stats import energy_distance
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import csv
import matplotlib.pylab as plot
import pymssql
import datetime as dt

import warnings
warnings.filterwarnings('ignore')
#warnings.filterwarnings(action='ignore')

# 냉방, 난방 구분
def air_condition(file_name):
    file_name = file_name.lower()
    if (file_name.__contains__("cooling")):
        air_condition = "cooling"
    else:
        air_condition = "heating"
    return air_condition

# MSSQL 접속
def conn():
    db = pymssql.connect(host="192.168.11.55", user="sunghan", password="Sunghan!2345", database='sunghan', charset='UTF8') #charset='EUC-KR'
    return db

# 공조기 장비기본 정보 조회
def ahu_info(EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo):
    db = conn()
    cursor = db.cursor()
    sql = "SELECT  ColdSupplySetupTemp, HeatSupplySetupTemp, SupplyAirVolume, OutdoorAirVolume, ExhaustAirVolume FROM T_AHU_INFO \
                     WHERE EquipmentClassCode = %s AND EquipmentNo = %d AND SiteCode = %s \
                       AND BuildingNo = %s AND ZoneNo = %d"
    val = (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo)
    cursor.execute(sql, val)

    # 실행문 조회
    all_row = cursor.fetchall()

    ColdSupplySetupTemp = all_row[0][0]
    HeatSupplySetupTemp = all_row[0][1]
    SupplyAirVolume = all_row[0][2]
    OutdoorAirVolume = all_row[0][3]
    ExhaustAirVolume = all_row[0][4]

    #print("all_row:",all_row)
    cursor.close()
    db.close()

    return ColdSupplySetupTemp, HeatSupplySetupTemp, SupplyAirVolume, OutdoorAirVolume, ExhaustAirVolume

def op_normal_predict(op_file_path, op_file_name, start_date, end_date):
    aircondition = air_condition(op_file_name)

    fault_data = pd.read_csv(op_file_path + op_file_name, header=0, encoding='latin-1', delimiter=',', quoting=3)
    fault_data = fault_data.query(start_date + '<= DATE <=' + end_date)

    sa_set_temp_c, sa_set_temp_h, sa_flow, oa_flow, ea_flow = ahu_info('AHU', 12, 'GGTMC042', 'M', 11)
    if (aircondition == "cooling"):
        sa_set_temp = sa_set_temp_c

    if (aircondition == "heating"):
        sa_set_temp = sa_set_temp_h
        #sa_set_temp = 18.33  # DB

    sa_flow_rating = sa_flow
    oa_flow_rating = oa_flow
    ea_flow_rating = ea_flow
    ra_flow_rating = sa_flow_rating - oa_flow_rating + ea_flow_rating

    fault_data['OA-TEMP'] = fault_data['OA-TEMP'] / sa_set_temp
    fault_data['SA-TEMP'] = fault_data['SA-TEMP'] / sa_set_temp
    fault_data['MA-TEMP'] = fault_data['MA-TEMP'] / sa_set_temp
    fault_data['RA-TEMP'] = fault_data['RA-TEMP'] / sa_set_temp
    fault_data['SA-FLOW'] = fault_data['SA-FLOW'] / sa_flow_rating
    fault_data['OA-FLOW'] = fault_data['OA-FLOW'] / oa_flow_rating
    fault_data['RA-FLOW'] = fault_data['RA-FLOW'] / ra_flow_rating
    fault_data['SA-REH'] = fault_data['SA-REH'] / 100
    fault_data['RA-REH'] = fault_data['RA-REH'] / 100
    fault_data['OA-DAMPER'] = fault_data['OA-DAMPER'] / 100
    fault_data['RA-DAMPER'] = fault_data['RA-DAMPER'] / 100
    fault_data['EA-DAMPER'] = fault_data['EA-DAMPER'] / 100
    fault_data['COOLC-VLV'] = fault_data['COOLC-VLV'] / 100
    fault_data['HEATC-VLV'] = fault_data['HEATC-VLV'] / 100

    if (aircondition == "cooling"):
        columns_customed = ['OA-TEMP', 'SA-TEMP', 'MA-TEMP', 'RA-TEMP', 'COOLC-VLV', 'SA-FLOW', 'OA-FLOW', 'OA-DAMPER',
                            'SF-POWER']

    if (aircondition == "heating"):
        columns_customed = ['OA-TEMP', 'SA-TEMP', 'MA-TEMP', 'RA-TEMP', 'HEATC-VLV', 'SA-FLOW', 'OA-FLOW', 'OA-DAMPER',
                            'SF-POWER']

    fault_predict = fault_data[columns_customed]

    print('fault_predict:', len(fault_predict))

    dataset = fault_predict.values
    X_pred1 = dataset[:, 0:-1]
    Y_pred1 = dataset[:, -1]
    predict_len = Y_pred1.size

    if (aircondition == "cooling"):
        afaultRFModel = joblib.load("./KSB-cooling-regression.pkl")

    if (aircondition == "heating"):
        afaultRFModel = joblib.load("./KSB-heating-regression.pkl")

    Y_prediction2 = afaultRFModel.predict(X_pred1).flatten()

    mbe = (np.sum(Y_prediction2) - np.sum(Y_pred1)) / predict_len
    mae = mean_absolute_error(Y_prediction2, Y_pred1)
    mse = mean_squared_error(Y_prediction2, Y_pred1)
    rmse = np.sqrt(mse)
    mean = np.mean(Y_pred1)
    cvmbe = mbe / np.mean(Y_pred1)
    cvmae = mae / np.mean(Y_pred1)
    cvrmse = rmse / np.mean(Y_pred1)

    # R2
    r2 = r2_score(Y_pred1, Y_prediction2)

    # Wasserstein 거리
    wsd = wasserstein_distance(Y_pred1, Y_prediction2)

    # Energy거리
    cramerd = energy_distance(Y_pred1, Y_prediction2)

    # 출력
    print('예측 Cv(RMSE) % ; ' + str(cvrmse * 100))
    print('와서스타인변동계수;' + str(wsd / mean * 100))
    print('에너지거리변동계수;' + str(cramerd / mean * 100) + '\n')
    print('실측 평균 :       ' + str(mean))
    print('예측 MBE :        ' + str(mbe))
    print('예측 MAE :        ' + str(mae))
    print('예측 MSE :        ' + str(mse))
    print('예측 RMSE :       ' + str(rmse))
    print('예측 R2 % ;       ' + str(r2 * 100))
    print('예측 Cv(MBE) % ;  ' + str(cvmbe * 100))
    print('예측 Cv(MAE) % ;  ' + str(cvmae * 100))
    print('와서스테인거리;   ' + str(wsd))
    print('에너지거리;        ' + str(cramerd))

    plt.figure(figsize=(12, 5))
    plt.plot(np.arange(predict_len), Y_prediction2, 'g', label="예측 급기팬 전력량")
    plt.plot(np.arange(predict_len), Y_pred1, 'b', label="실측 급기팬 전력량")
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plt.legend()
    plt.show()

    for i in range(0, predict_len, 100):
        label = Y_pred1[i]
        prediction = Y_prediction2[i]
        #print("실측 {:.3f}     예측 {:.3f}".format(label, prediction))

    return fault_predict, Y_pred1, Y_prediction2, aircondition


# (4) 최적 다항 회귀모델 생성(KSB 회귀모델에 운용공조기의 10일치 정상데이터 사용하여 산출된 예측치 사용)
#     운영 공조기 보정 데이터 생성
def op_best_poly_reg_model(op_file_path, op_file_name, fault_predict, Y_pred1, Y_prediction2, aircondition):
    Y_fanpower = fault_predict['SF-POWER'].values
    print("load Y_fanpower:", Y_fanpower)

    size = len(Y_fanpower)
    print('Y_fanpower size:', size)

    rmses = []
    degrees = np.arange(1, 5)
    min_rmse, min_deg = 1e10, 0

    ###------------------------------------------------------------------------------------------
    ### 운용공조기 정상상태 보정 급기팬 전력량 산출
    ### (최적다항 회귀모델에 운용공조기 정상상태 실측 급기팬 전력량을 적용)
    ###------------------------------------------------------------------------------------------

    x_train, x_test, y_train, y_test = train_test_split(Y_pred1.reshape(-1, 1), Y_prediction2, test_size=0.3)

    for deg in degrees:

        # Train features
        poly_features = PolynomialFeatures(degree=deg, include_bias=False)
        x_poly_train = poly_features.fit_transform(x_train)

        # Linear regression
        poly_reg = LinearRegression()
        poly_reg.fit(x_poly_train, y_train)

        # Compare with test data
        x_poly_test = poly_features.fit_transform(x_test)
        poly_predict = poly_reg.predict(x_poly_test)
        poly_mse = mean_squared_error(y_test, poly_predict)
        poly_rmse = np.sqrt(poly_mse)
        rmses.append(poly_rmse)

        print('------------------------------')
        print('deg:', deg)
        print('min_rmse:', min_rmse)
        print('poly_rmse:', poly_rmse)
        print('min_deg:', min_deg)

        # Cross-validation of degree
        if min_rmse > poly_rmse:
            min_rmse = poly_rmse
            best_poly_reg = poly_reg
            min_deg = deg

        print('min_deg:', min_deg)

    """
    # degree 저장
    if (aircondition == 'cooling'):
        f = open("./cooling_degree.csv", 'w', newline='')
        wr = csv.writer(f)
        wr.writerow([str(min_deg)])
        f.close()
    if (aircondition == 'heating'):
        f = open("./heating_degree.csv", 'w', newline='')
        wr = csv.writer(f)
        wr.writerow([str(min_deg)])
        f.close()
    """

    # 모델 저장하기
    # (4) 최적 다항 회귀모델 저장
    if (aircondition == 'cooling'):
        joblib.dump(best_poly_reg, "./KSB-cooling-polynomial.pkl")

    if (aircondition == 'heating'):
        joblib.dump(best_poly_reg, "./KSB-heating-polynomial.pkl")

    # Plot and present results
    coef = best_poly_reg.coef_
    print('Best degree {} with RMSE {}, Coefficient id {}'.format(min_deg, min_rmse, coef))

    fig = plot.figure()
    plt.plot(degrees, rmses)
    plt.yscale('log')
    plt.xlabel('Degree')
    plt.ylabel('RMSE')

    # (5) 운용공조기 정상상태 보정 급기팬 전력량 산출
    plt.figure(figsize=(12, 5))
    plt.plot(y_test, 'b', label="기존 실측 급기팬 전력량")
    plt.plot(poly_predict, 'g', label="기존 실측에 대한 예측 급기팬 전력량")
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plt.legend()
    plt.show()

    best_poly_features = PolynomialFeatures(degree=min_deg, include_bias=False)
    Y_poly_pred = best_poly_features.fit_transform(Y_pred1.reshape(-1, 1))
    Y_fanpower = best_poly_features.fit_transform(Y_fanpower.reshape(-1, 1))

    # fault new data 저장
    # 정상 유형 보정 급기팬 전력량 (SAFpower2)
    fanpower_adj = pd.DataFrame(best_poly_reg.predict(Y_fanpower))
    print('fanpower_adj.size:', fanpower_adj.size)
    print('fanpower_adj:', fanpower_adj)

    fault_new_data = fault_predict
    fault_new_data = fault_new_data.reset_index()
    fault_new_data['SF-POWER-ADJ'] = fanpower_adj

    # path = "./ASH-CoolingFinal-adj.csv"
    op_file_name = op_file_name.partition('.')
    op_adj_file_name = op_file_name[0] + '-adj' + op_file_name[1] + op_file_name[2]
    print('op_adj_file_name:', op_adj_file_name)

    fault_new_data.to_csv(op_file_path + op_adj_file_name, index=False)

    plot.figure(figsize=(12, 5))
    plot.plot(y_test, 'b', label="다항 실측 급기팬 전력량")
    plot.plot(poly_predict, 'r', label="다항 예측 급기팬 전력량")
    plot.plot(Y_pred1, 'c', label="보정 실측 급기팬 전력량")
    plot.plot(fanpower_adj, 'g', label="보정 급기팬 전력량")

    plot.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plot.legend()
    plot.show()

    ###------------------------------------------------------------------------------------------
    ### (6) 운용 공조기 정상 유형 회귀모델 저장 (운용공조기 보정 정상 데이터 10일치 사용)
    ###------------------------------------------------------------------------------------------

    df_fault = fault_new_data
    print("df_fault 크기", len(df_fault))

    if (aircondition == "cooling"):
        columns_customed = ['OA-TEMP', 'SA-TEMP', 'MA-TEMP', 'RA-TEMP', 'COOLC-VLV', 'SA-FLOW', 'OA-FLOW', 'OA-DAMPER',
                            'SF-POWER-ADJ']

    if (aircondition == "heating"):
        columns_customed = ['OA-TEMP', 'SA-TEMP', 'MA-TEMP', 'RA-TEMP', 'HEATC-VLV', 'SA-FLOW', 'OA-FLOW', 'OA-DAMPER',
                            'SF-POWER-ADJ']

    df_fault = df_fault[columns_customed]
    faultNames = np.array(df_fault.keys())

    dataset = df_fault.values
    X = dataset[:, 0:-1]
    Y = dataset[:, -1]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

    # train random forest at a range of ensemble sizes in order to see how the mse changes
    iTrees = 500
    depth = None
    maxFeat = 4  # try tweaking
    bfaultRFModel = ensemble.RandomForestRegressor(n_estimators=iTrees, max_depth=depth, max_features=maxFeat,
                                                   oob_score=False, random_state=42, n_jobs=-1)

    bfaultRFModel.fit(X_train, Y_train)

    # 모델 저장하기
    if (aircondition == 'cooling'):
        joblib.dump(bfaultRFModel, "./AHU-cooling-regression.pkl")

    if (aircondition == 'heating'):
        joblib.dump(bfaultRFModel, "./AHU-heating-regression.pkl")

    # Accumulate mse on test set
    # 정상 유형 추정 급기팬 전력량 (SAFpower3)
    # (7) 운용공조기 정상상태 추정 급기팬 전력량 산출(SAFpower3) : Y_prediction
    Y_prediction = bfaultRFModel.predict(X_test)
    print('Y_prediction :', Y_prediction)
    print('Y_test :', Y_test)

    test_len = Y_test.size
    print("test_len", test_len)
    mbe = (np.sum(Y_prediction) - np.sum(Y_test)) / test_len
    mae = mean_absolute_error(Y_prediction, Y_test)
    mse = mean_squared_error(Y_prediction, Y_test)
    rmse = np.sqrt(mse)
    mean = np.mean(Y_test)
    cvmbe = mbe / np.mean(Y_test)
    cvmae = mae / np.mean(Y_test)
    cvrmse = rmse / np.mean(Y_test)

    fanpower_capacity = 1

    # R2
    r2 = r2_score(Y_test, Y_prediction)

    # Wasserstein 거리
    wsd = wasserstein_distance(Y_test * fanpower_capacity, Y_prediction * fanpower_capacity)

    # Wasswerstein 거리는 주변분포가 주어져 있을 때, 이 두개의 분포를 주변분포로 하는 결합분포 중에서
    # E를 가장 작게 하는 분포를 골랐을 때, p의 기대값

    # Energy거리
    cramerd = energy_distance(Y_test * fanpower_capacity, Y_prediction * fanpower_capacity)

    s_cvrmse = round(((cvrmse * 100) * 2), 3)
    s_wsd = round((((wsd / mean) * 100) * 2), 4)
    s_cramerd = round((((cramerd / mean) * 100) * 2), 4)

    print('유사도 Cv(RMSE) % ;   ' + str(s_cvrmse))
    print('유사도 와서스타인변동계수; ' + str(s_wsd))
    print('유사도 에너지거리변동계수; ' + str(s_cramerd))

    ### 공조기 유사도 기준 입력
    ### T_AHU_CRITERIA_SIMILARITY_INFO start
    db = conn()
    cursor = db.cursor()

    if (aircondition == 'cooling'):
        CoolHeatInd = '1'
    if (aircondition == 'heating'):
        CoolHeatInd = '2'

    poly_degree = str(min_deg)
    dt_now = dt.datetime.now()
    sdate = dt_now.strftime("%Y%m%d %H:%M:%S")
    print("sdate, min_deg:", sdate, type(poly_degree), poly_degree, CoolHeatInd, s_cvrmse, s_wsd, s_cramerd)

    sql = "INSERT INTO T_AHU_CRITERIA_SIMILARITY_INFO (EquipmentClassCode, EquipmentNo, SiteCode, BuildingNo, ZoneNo, CoolHeatingIndication, CvRMSE, WassersteinDistance, EnergyDistance, PolyDegree, SaveTime) VALUES (%s, %d, %s, %s, %d, %s, %d, %d, %d, %d, %s)"
    val = ('AHU', 12, 'GGTMC042', 'M', 11, CoolHeatInd, s_cvrmse, s_wsd, s_cramerd, poly_degree, sdate)

    cursor.execute(sql, val)
    db.commit()
    print(cursor.rowcount, "개의 레코드가 입력되었습니다.")

    cursor.close()    
    db.close()
    ### T_AHU_CRITERIA_SIMILARITY_INFO end

    # 출력
    print('시험 Cv(RMSE) % ;   ' + str(cvrmse * 100))
    print('와서스타인변동계수; ' + str((wsd / mean) * 100))
    print('에너지거리변동계수; ' + str((cramerd / mean) * 100) + '\n')
    print('행 갯수 :           ' + str(len(df_fault)))
    print('실측 평균 :         ' + str(mean))
    print('시험 MBE :          ' + str(mbe))
    print('시험 MAE :          ' + str(mae))
    print('시험 MSE :          ' + str(mse))
    print('시험 RMSE :         ' + str(rmse))
    print('시험 R2 % ;         ' + str(r2 * 100))
    print('시험 Cv(MBE) % ;    ' + str(cvmbe * 100))
    print('시험 Cv(MAE) % ;    ' + str(cvmae * 100))
    print('와서스타인거리;     ' + str(wsd))
    print('에너지거리;         ' + str(cramerd))

    # normalize by max importance
    featureImportance = bfaultRFModel.feature_importances_
    print('featureImportance:', featureImportance)
    print('featureImportance.max():', featureImportance.max())
    featureImportance = featureImportance / featureImportance.max()
    sorted_idx = np.argsort(featureImportance)
    print('sorted_idx.shape[0]:', sorted_idx.shape[0])
    print('featureImportance:', featureImportance[sorted_idx])
    barPos = np.arange(sorted_idx.shape[0])
    barPos = np.arange(sorted_idx.shape[0]) + .5

    print('faultNames:', faultNames[sorted_idx])
    plot.barh(barPos, featureImportance[sorted_idx], align='center')
    plot.yticks(barPos, faultNames[sorted_idx])
    plot.xlabel('특성 중요도', fontproperties=fontprop)
    plot.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plot.show()

    plot.figure(figsize=(12, 5))
    plot.plot(Y_test, 'b-+', label="실측 급기팬 전력량")
    plot.plot(Y_prediction, 'g--', label="예측 급기팬 전력량")
    plot.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.1)
    plot.legend()
    plot.show()

    for i in range(test_len):
        label = Y_test[i]
        prediction = Y_prediction[i]
        # print("실측:  {:.5f}, 예측: {:.5f}".format(label, prediction))


################################################################################################

"""
sa_set_temp_c, sa_set_temp_h, sa_flow_rating, oa_flow_rating, ea_flow_rating = ahu_info('AHU', 12, 'GGTMC042', 'M', 11)
print("ahu info :", sa_set_temp_c, sa_set_temp_h, sa_flow_rating, oa_flow_rating, ea_flow_rating)
"""
start_date = '20200806'
end_date = '20200815'
op_file_path = './'
op_file_name = 'ASH-CoolingFinal-original.csv'
# aircondition = air_condition(op_file_name)

fault_predict, Y_pred1, Y_prediction2, aircondition = op_normal_predict(op_file_path, op_file_name, start_date, end_date)
op_best_poly_reg_model(op_file_path, op_file_name, fault_predict, Y_pred1, Y_prediction2, aircondition)
