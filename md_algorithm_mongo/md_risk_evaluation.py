import pandas as pd
from math_utils import MathUtils

#발생시간, 근무경력, 나이, 발생월을 변수로 선택
non_accidents_df = pd.read_csv("./md_algorithm_mongo/data/non_accidents_preprocessing.csv", encoding="utf-8")
accidents_df = pd.read_csv("./md_algorithm_mongo/data/accidents_preprocessing.csv", encoding="utf-8")

non_accidents = non_accidents_df[["근무경력","나이","발생월","발생시간"]]
accidents = accidents_df[["근무경력","나이","발생월","발생시간"]]


accidents_cov = MathUtils.robust_cov(accidents)
print("사고데이터 : ", accidents_cov)

non_accident_cov = MathUtils.robust_cov(non_accidents)
print("비사고데이터 : ", non_accident_cov)

#사고데이터 Mahalnobis
accident_list = []
for value in accidents.values:
    accident_data = MathUtils.calc_Mahalanobis(value, accidents, accidents_cov)
    accident_list.append(accident_data)

#print(accident_list)

print("Maximum distance of accident : ", max(accident_list))
print("Maximum distance of accident : ", min(accident_list))