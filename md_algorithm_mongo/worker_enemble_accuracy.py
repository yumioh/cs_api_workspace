import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
근로자 MD, 공종별 MD를 통해 위험도 계산
- 비사고 데이터 : 정상 데이터, 사고 데이터 : 비정상 데이터로 가정
- Thredsold 그리기 : 비사고 데이터 기준으로 상한 임계값을 통해 기준선 그리기
- 모델 평가 하기 : 
    - 정상 데이터(non_accident)가 정상으로 분류되면 TP, 비정상으로 분류되면 FN, 
    - 비정상 데이터(accident)가 비정상으로 분류되면 TN, 정상으로 분류되면 FP
- 정확도 계산

'''

non_accident = pd.read_csv("./md_algorithm_mongo/data/non_accident_log_normalized.csv")
accident = pd.read_csv("./md_algorithm_mongo/data/accident_log_normalized.csv")
# non_accident = pd.read_csv("./md_algorithm_mongo/data/non_accident_normalized.csv")
# accident = pd.read_csv("./md_algorithm_mongo/data/accident_normalized.csv")

# IQR 계산
def remove_outliers_iqr(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data >= lower_bound) & (data <= upper_bound)]

# # lable 추가
# non_accident["label"] = "non_accident"
# accident["label"] = "accident"
# print(accident.head())

# 그래프를 그리기 전에 데이터의 순서를 정렬하여 분석 및 시각화할 때 더 명확하게 보이기 위함
# 오름차순으로 정렬하여 인덱스 재부여
non_accident = remove_outliers_iqr(non_accident["normalized"]).sort_values().reset_index(drop=True)
accident = remove_outliers_iqr(accident["normalized"]).sort_values().reset_index(drop=True)

#비사고 데이터의 평균 및 표준편차 구하기 
mu = np.mean(non_accident)
sigma = np.std(non_accident)
print(mu)
print(sigma)

#사고 데이터의 평균 및 표준편차 구하기 
accident_mu = np.mean(accident)
accident_sigma = np.std(accident)

# 임계값 설정
upper_threshold = mu + 2 * sigma
lower_threshold = mu - 2 * sigma
print("임계값 :", upper_threshold)
print(non_accident.max())

# 히스토그램
plt.hist(non_accident, bins=30, alpha=0.5, color="blue", density=True, label="Non-Accident Data")
plt.hist(accident, bins=30, alpha=0.5, color="red", density=True, label="Accident Data")
plt.show()

# plt.axvline(x=lower_threshold, color="red", linestyle="dashed", linewidth=2, label="lower")
# plt.axvline(x=upper_threshold, color="blue", linestyle="dashed", linewidth=2, label="upper")

# 산점도 그리기
plt.scatter(non_accident.index, non_accident, color="blue", s=8, label="비사고")
plt.scatter(accident.index, accident, color="red", s=8, label="사고")

# 임계값 그리기
plt.axhline(y=upper_threshold, color='red', linestyle='dashed', linewidth=2, label="Threshold")
#plt.axhline(y=lower_threshold, color='red', linestyle='dashed', linewidth=2, label="Threshold")
plt.show()

# plt.axvline(x=lower_threshold, color="red", linestyle="dashed", linewidth=2, label="Lower 3σ Threshold")
# plt.axvline(x=upper_threshold, color="green", linestyle="dashed", linewidth=2, label="Upper 3σ Threshold")

# plt.title(f"Histogram with 3σ Threshold")
# plt.ylabel("Density")
# plt.legend()
# plt.grid()

# plt.show()

print("-------------------분류 성능 평가--------------------")

# 분류 성능 평가
# 정상 데이터(non_accident)가 정상으로 분류되면 TP, 비정상으로 분류되면 FN
# 비정상 데이터(accident)가 비정상으로 분류되면 TN, 정상으로 분류되면 FP
non_accident_predictions = (non_accident >= lower_threshold) & (non_accident <= upper_threshold)
accident_predictions = (accident < lower_threshold) | (accident > upper_threshold)

TP = np.sum(non_accident_predictions)
FN = len(non_accident) - TP
TN = np.sum(accident_predictions)
FP = len(accident) - TN

# 정확도 계산
accuracy = (TP + TN) / (TP + TN + FP + FN)
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

print(f"TP: {TP}, FP: {FP}, TN: {TN}, FN: {FN}")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1_score:.4f}")










 