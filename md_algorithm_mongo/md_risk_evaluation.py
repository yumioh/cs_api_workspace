import pandas as pd
import csv
from math_utils import MathUtils
import numpy as np
import math

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

#비사고 데이터를 사고 확률이 낮은 데이터로 변환하여, 공분산 계산시 기준 데이터로 활용
robust_cov_df = pd.DataFrame({
    "근무경력" : np.random.randint(1,3,size=len(non_accidents)), # 2~3년 미만, 3~4년 미만, 4~5년 미만, 
    "공사규모 " : np.random.randint(1,2, size=len(non_accidents)), #500인 이상
    "나이" : np.random.randint(2,3, size=len(non_accidents)), #30세 미만
    "발생시간" : np.random.randint(1,4, size=len(non_accidents)) # 02~04시, 04~06시, 20~22시, 22~24시 
})

# robust_cov_df = pd.DataFrame({
#     "근무경력" : np.random.randint(7,8, size=len(non_accidents)), #5년 이상
#     "공사규모 " : np.random.randint(1,4, size=len(non_accidents)), # 전체
#     "나이" : np.random.randint(2,3, size=len(non_accidents)), 
#     "발생시간" : np.random.randint(1,4, size=len(non_accidents))
# })

#print(robust_cov_df.head())

robust_cov = MathUtils.robust_cov(robust_cov_df)
print("사고 확률이 낮은 데이터 robust_cov 평균 : ", robust_cov.mean()) #0.0575483857632976

#사고데이터 Mahalnobis
accident_list = []
for value in accidents.values:
    accident_data = MathUtils.calc_mahalanobis(value, robust_cov_df, robust_cov)
    accident_list.append(accident_data)

#파일 저장
with open("./md_algorithm_mongo/data/accident_mahal.csv","w") as file :
    writer = csv.writer(file)
    for item in accident_list:
        writer.writerow([item])

#비사고데이터 Mahalnobis
non_accident_list = []
for value in non_accidents.values:
    non_accident_data = MathUtils.calc_mahalanobis(value, robust_cov_df, robust_cov)
    non_accident_list.append(non_accident_data)

#파일 저장
with open("./md_algorithm_mongo/data/non_accident_mahal.csv", "w", newline='') as file:
    writer = csv.writer(file)
    for item in non_accident_list:
        writer.writerow([item])


print("--------------------이상치 제거-------------------")

# 사고 데이터 MD값 이상치 제거 
accident_df = pd.Series(accident_list)

accident_zscores = MathUtils.z_scores(accident_df)
# print(accident_zscores.head())
accident = accident_df[accident_zscores.abs() <= 1.96]
print("사고 데이터 z-score 값 : ")
print(accident.head())
print("Maximum distance of accident: ", max(accident)) #1251.3725698935
print("Minimum distance of accident: ", min(accident)) #510.3150165561739

#비사고데이터 MD값 이상치 제거 
non_accident_df = pd.Series(non_accident_list)
non_accident_zscores = MathUtils.z_scores(non_accident_df)
# print(non_accident_zscores.head())
non_accident = non_accident_df[non_accident_zscores.abs() <= 1.96]
print("비사고 데이터 z-score 값 : ")
print(non_accident.head())

print("Maximum distance of non_accident : ", max(non_accident)) #359.16982248852685
print("Minimum distance of non_accident : ", min(non_accident)) #4.406839395246572

# 분포가 95%에 해당하는 사고 비사고 데이터 MD값만 저장
accident.to_csv("./md_algorithm_mongo/data/accident_md.csv", index = None)
non_accident.to_csv("./md_algorithm_mongo/data/non_accident_md.csv", index = None)

print("--------------------정규화(MD->normalize)-------------------")
# 데이터 프레임의 결합 순서가 다를 경우 minmax의 결과값이 달라짐 
# 결합의 순서에 따라 데이터의 최소값과 최대값이 달라질수 있고, 이는 스켈링 결과에 영향을 미침

#사고 데이터 정규화
accident_normalized = MathUtils.minmaxscaling(accident, non_accident)
print("accident 정규화 : ")
print(accident_normalized.head())
accident_normalized.to_csv("./md_algorithm_mongo/data/accident_normalized.csv", index = None)

#비사고 데이터 정규화
non_accident_normalized = MathUtils.minmaxscaling(non_accident, accident)
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
accident_log_normalized = MathUtils.minmaxscaling(accident_log, non_accident_log)
print("accident 정규화 : ")
print(accident_log_normalized.head())
accident_log_normalized.to_csv("./md_algorithm_mongo/data/accident_log_normalized.csv", index = None)

#비사고 log 데이터 정규화
non_accident_log_normalized = MathUtils.minmaxscaling(non_accident_log, accident_log)
print("non_accident 정규화 : ")
print(non_accident_log_normalized.head())
non_accident_log_normalized.to_csv("./md_algorithm_mongo/data/non_accident_log_normalized.csv", index = None)


import matplotlib.pyplot as plt

plt.hist(accident_list, bins=30, alpha=0.5, label="Accidents")
plt.hist(non_accident_list, bins=30, alpha=0.5, label="Non-Accidents")
plt.legend()
plt.title("Mahalanobis Distance Distribution")
plt.show()

# 사고 데이터 평균 벡터
accident_mean = accidents.mean()
print("사고 데이터 평균:")
print(accident_mean)

# 비사고 데이터 평균 벡터
non_accident_mean = non_accidents.mean()
print("비사고 데이터 평균:")
print(non_accident_mean)

# 차이 계산
mean_difference = accident_mean - non_accident_mean
print("평균 벡터 차이:")
print(mean_difference)