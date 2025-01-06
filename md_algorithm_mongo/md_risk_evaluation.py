import pandas as pd
import csv
from math_utils import MathUtils
import numpy as np

'''
MD값 계산 및 정규화
- 마할라노비스 거리(MD) 계산: 사고 및 비사고 데이터를 기반으로 공분산 행렬을 사용하여 MD값 계산.
- 데이터 정규화: 계산된 MD값에 Min-Max Scaling을 적용하여 값을 0과 1 사이로 정규화.
'''

#발생시간, 근무경력, 나이, 발생월을 변수로 선택
non_accidents_df = pd.read_csv("./md_algorithm_mongo/data/non_accidents_preprocessing.csv", encoding="utf-8")
accidents_df = pd.read_csv("./md_algorithm_mongo/data/accidents_preprocessing.csv", encoding="utf-8")

non_accidents = non_accidents_df[["근무경력","나이","공사규모","발생시간"]]
accidents = accidents_df[["근무경력","나이","공사규모","발생시간"]]

accidents_cov = MathUtils.robust_cov(accidents)
print("사고데이터 : ", accidents_cov)

non_accident_cov = MathUtils.robust_cov(non_accidents)
print("비사고데이터 : ", non_accident_cov)

#사고데이터 Mahalnobis
accident_list = []
for value in accidents.values:
    accident_data = MathUtils.calc_mahalanobis(value, accidents, accidents_cov)
    accident_list.append(accident_data)

print("Maximum distance of accident : ", max(accident_list)) # 69.7224181709437
print("Minimum distance of accident : ", min(accident_list)) # 0.27380826322991353

#파일 저장
with open("./md_algorithm_mongo/data/accident_mahal.csv","w") as file :
    writer = csv.writer(file)
    for item in accident_list:
        writer.writerow([item])

#비사고데이터 Mahalnobis
non_accident_list = []
for value in non_accidents.values:
    non_accident_data = MathUtils.calc_mahalanobis(value, non_accidents, non_accident_cov)
    non_accident_list.append(non_accident_data)

print("Maximum distance of non-accident : ", max(non_accident_list)) # 139.7352739733086
print("Minimum distance of nono-accident : ", min(non_accident_list)) # 0.14626488755019176

#파일 저장
with open("./md_algorithm_mongo/data/non_accident_mahal.csv", "w", newline='') as file:
    writer = csv.writer(file)
    for item in non_accident_list:
        writer.writerow([item])

# 사고, 비사고 데이터 합치기 => 데이터 분포를 알기 위함 
# merged_list = []
# merged_list.extend(accident_list)
# merged_list.extend(non_accident_list)

#print(merged_list)

# #log값 변환
# log_list = []
# for value in merged_list:
#     log_list.append(math.log(value))

# print("Maximum log : ", max(log_list))
# print("Minimum log : ", min(log_list))

# #지수값 값변환
# exp_list=[]
# for value in merged_list:
#     exp_list.append(math.exp(value))

# print("Maximum exp : ", max(exp_list))
# print("Minimum exp : ", min(exp_list))

# 사고 데이터 MD값 이상치 제거 
accident_df = pd.Series(accident_list)

accident_zscores = MathUtils.z_scores(accident_df)
# print(accident_zscores.head())
accident = accident_df[accident_zscores.abs() <= 1.96]
print("사고 데이터 z-score 값 : ")
print(accident.head())
print("Maximum distance of accident: ", max(accident)) # 19.917695010669433
print("Minimum distance of accident: ", min(accident)) # 0.27380826322991353

#비사고데이터 MD값 이상치 제거 
non_accident_df = pd.Series(non_accident_list)

non_accident_zscores = MathUtils.z_scores(non_accident_df)
# print(non_accident_zscores.head())
non_accident = non_accident_df[non_accident_zscores.abs() <= 1.96]
print("비사고 데이터 z-score 값 : ")
print(non_accident.head())
print("Maximum distance of accident : ", max(non_accident)) #52.09605332981937
print("Minimum distance of accident : ", min(non_accident)) #0.14626488755019176

# 분포가 95%에 해당하는 사고 비사고 데이터 MD값만 저장
accident.to_csv("./md_algorithm_mongo/data/accident_md.csv", index = None)
non_accident.to_csv("./md_algorithm_mongo/data/non_accident_md.csv", index = None)

print("--------------------정규화(MD->normalize)-------------------")
# 데이터 프레임의 결합 순서가 다를 경우 minmax의 결과값이 달라짐 
# 결합의 순서에 따라 데이터의 최소값과 최대값이 달라질수 있고, 이는 스켈링 결과에 영향을 미침

#사고 데이터 정규화
accident_normalized = MathUtils.minmaxscaling(accident)
print("accident 정규화 : ")
print(accident_normalized.head())
accident_normalized.to_csv("./md_algorithm_mongo/data/accident_normalized.csv", index = None)

#비사고 데이터 정규화
non_accident_normalized = MathUtils.minmaxscaling(non_accident)
print("non_accident 정규화 : ")
print(non_accident_normalized.head())
non_accident_normalized.to_csv("./md_algorithm_mongo/data/non_accident_normalized.csv", index = None)

print("-------------------(MD->logMD)-------------------")

accident_log = np.log(accident)
non_accident_log = np.log(non_accident)

accident_log.to_csv("./md_algorithm_mongo/data/accident_log.csv", index = None)
non_accident_log.to_csv("./md_algorithm_mongo/data/non_accident_log.csv", index = None)

print("accident_log : ")
print(accident_log)
print("non_accident_log : ")
print(non_accident_log)

print("--------------------정규화(logMD->normalize)-------------------")

# 사고 log 데이터 정규화
accident_log_normalized = MathUtils.minmaxscaling(accident_log)
print("accident 정규화 : ")
print(accident_log_normalized.head())
accident_log_normalized.to_csv("./md_algorithm_mongo/data/accident_log_normalized.csv", index = None)

#비사고 log 데이터 정규화
non_accident_log_normalized = MathUtils.minmaxscaling(non_accident_log)
print("non_accident 정규화 : ")
print(non_accident_log_normalized.head())
non_accident_log_normalized.to_csv("./md_algorithm_mongo/data/non_accident_log_normalized.csv", index = None)