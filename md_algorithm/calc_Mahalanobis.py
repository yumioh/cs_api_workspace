import pandas as pd
import math
import sys, os
import csv
import matplotlib.pyplot as plt
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import math_utils


#공분산에 해당하는 데이터 
gh_df = pd.read_csv("./md_algorithm/data/gh_categorize.csv")
kosha_df = pd.read_csv("./md_algorithm/data/kosha_categorize.csv")

# GH DATA
#공사규모, 발생시간 행의 값이 동일하여 역행렬 불가능
#공사규모(대,특대,중), 발생시간(1,2,3), 나이(35~38세) 랜덤으로 넣기

#TODO 해당하는 열의 랜덤화 하여 넣기 

#gh_data = gh_df[["공사규모","발생시간","근무경력","나이","월별","요일별"]]
gh_data = gh_df[["근무경력","나이","월별","요일별"]]
print("gh data : ", gh_data.shape)

# 근무경력 5년 이상 나이  50세 이하로 FILTERING
filtered_gh = gh_data[gh_data["근무경력"] >= 7]
filtered_gh = filtered_gh[gh_data["나이"] <= 50]

filtered_gh.to_csv("./md_algorithm/data/filtered_gh.csv", encoding="utf-8")
print("filtered gh data : ", filtered_gh.shape)

# KOSHA DATA
# kosha_data = kosha_df[["공사규모","발생시간","근무경력","나이","월별","요일별"]]
kosha_data = kosha_df[["근무경력","나이","월별","요일별"]]
print("kosha data : ", kosha_data.shape)

print("-------------------kosha Mahalanobis 구하기--------------------")

# 비교할 기본값 filtered gh data
test_robust_cov = math_utils.robust_cov(filtered_gh)

kosha_list = []
for kosha_value in kosha_data.values:
    kosha_data = math_utils.calculateMahalanobis(kosha_value, filtered_gh.values, test_robust_cov)
    kosha_list.append(kosha_data)
    ##kosha_value :  1
    ##filtered_gh.values :  [ 8 47  5  3]


print("kosha Mahalanobis data :", kosha_list)

#LIST 파일 저장
with open("./md_algorithm/data/kosha_Mahal_list.csv","w") as file :
    writer = csv.writer(file)
    for item in kosha_list:
        writer.writerow([item])


print("-------------------gh Mahalanobis 구하기--------------------")

gh_list = []
for gh_value in gh_data.values:
    gh_data = math_utils.calculateMahalanobis(gh_value, filtered_gh.values, test_robust_cov)
    gh_list.append(gh_data)

print("gh Mahalanobis data :", gh_list)


#LIST 파일 저장
with open("./md_algorithm/data/gh_Mahal_list.csv", "w", newline='') as file:
    writer = csv.writer(file)
    for item in gh_list:
        writer.writerow([item])

#MIN & MAX
print("Maximum distance of KOSHA : ", max(kosha_list))
print("Maximum distance of KOSHA : ", min(kosha_list))

print("Minimum distance of GH : ", max(gh_list))
print("Minimum distance of GH : ", min(gh_list))

#gh & kosha Data merge
merged_list = []
merged_list.extend(gh_list)
merged_list.extend(kosha_list)

log_list = []
for step in merged_list:
    log_list.append(math.log(step))

print("Maximum log : ", max(log_list))
print("Minimum log : ", min(log_list))

# 파이썬에서 exp 함수가 처리할 수 있는 최대 값
MAX_EXP = 709  
exp_list = []
for step in merged_list:
    if step > MAX_EXP:
        step = MAX_EXP  # 최대값으로 제한
    exp_list.append(math.exp(step))

print("Maximum exp : ", max(exp_list))
print("Minimum exp : ", min(exp_list))
