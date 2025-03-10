import numpy as np
from sklearn.metrics import accuracy_score

# 실제 예시 - 두 모델의 정확도가 다른 경우
# 가정: 모델 A의 정확도는 85%, 모델 B의 정확도는 70%

# 예시 데이터 생성
np.random.seed(42)  # 재현성을 위한 시드 설정
n_samples = 100
y_true = np.random.randint(0, 2, n_samples)  # 실제 레이블

# 모델 A - 85% 정확도를 가진 예측 만들기
model_A_preds = np.copy(y_true)
error_indices = np.random.choice(n_samples, int(n_samples * 0.15), replace=False)
for idx in error_indices:
    model_A_preds[idx] = 1 - model_A_preds[idx]  # 15%에 해당하는 예측을 반전시킴

# 모델 B - 70% 정확도를 가진 예측 만들기
model_B_preds = np.copy(y_true)
error_indices = np.random.choice(n_samples, int(n_samples * 0.30), replace=False)
for idx in error_indices:
    model_B_preds[idx] = 1 - model_B_preds[idx]  # 30%에 해당하는 예측을 반전시킴

# 각 모델의 정확도 확인
accuracy_A = accuracy_score(y_true, model_A_preds)
accuracy_B = accuracy_score(y_true, model_B_preds)

print(f"Model A 정확도: {accuracy_A:.4f}")  # 약 0.85
print(f"Model B 정확도: {accuracy_B:.4f}")  # 약 0.70
print(f"Total Model 정확도: {accuracy_A + accuracy_B}")

# 정확도 기반 가중치 계산
total_accuracy = accuracy_A + accuracy_B
weight_A = accuracy_A / total_accuracy
weight_B = accuracy_B / total_accuracy

print(f"Model A 가중치: {weight_A:.4f}")  # 약 0.5484
print(f"Model B 가중치: {weight_B:.4f}")  # 약 0.4516
print(f"Total Model 가중치: {weight_A + weight_B}")

# 예측 확률 생성 (예시를 위해 임의로 생성)
# 실제 예측과 일치하는 방향으로 확률값 생성
model_A_probs = np.zeros(n_samples)
for i in range(n_samples):
    if model_A_preds[i] == 1:
        model_A_probs[i] = np.random.uniform(0.5, 1.0)  # 1로 예측한 경우 0.5~1.0 사이의 확률
    else:
        model_A_probs[i] = np.random.uniform(0.0, 0.5)  # 0으로 예측한 경우 0.0~0.5 사이의 확률

model_B_probs = np.zeros(n_samples)
for i in range(n_samples):
    if model_B_preds[i] == 1:
        model_B_probs[i] = np.random.uniform(0.5, 1.0)
    else:
        model_B_probs[i] = np.random.uniform(0.0, 0.5)

# 가중 평균 앙상블 예측 확률
weighted_probs = (weight_A * model_A_probs) + (weight_B * model_B_probs)
weighted_preds = (weighted_probs >= 0.5).astype(int)

# 앙상블 모델의 정확도
ensemble_accuracy = accuracy_score(y_true, weighted_preds)
print(f"앙상블 모델 정확도: {ensemble_accuracy:.4f}")

""" Made by claude"""
"""
    가중치 계산 및 해석
    위 예시에서:
    
    모델 A의 정확도는 약 85%(0.85)
    모델 B의 정확도는 약 70%(0.70)
    총 정확도 합은 1.55(0.85 + 0.70)
    
    가중치 계산:
    
    모델 A의 가중치: 0.85 / 1.55 = 0.5484 (약 55%)
    모델 B의 가중치: 0.70 / 1.55 = 0.4516 (약 45%)
    
    이는 정확도가 더 높은 모델 A에 더 많은 가중치(약 55%)를 부여하고, 상대적으로 정확도가 낮은 모델 B에는 적은 가중치(약 45%)를 부여합니다. 정확도 차이가 클수록 가중치 차이도 커집니다.
    극단적인 예시
    만약 모델 간 정확도 차이가 더 크다면:
    
    모델 A 정확도: 0.95 (95%), 모델 B 정확도: 0.60 (60%)
    총 정확도 합: 1.55
    모델 A 가중치: 0.95 / 1.55 = 0.6129 (약 61%)
    모델 B 가중치: 0.60 / 1.55 = 0.3871 (약 39%)
    
    이처럼 정확도가 높은 모델에 더 많은 영향력을 부여함으로써, 앙상블 모델의 전체 정확도를 향상시킬 수 있습니다. 
"""
""" Reference URL : https://github.com/xbeat/Machine-Learning/blob/main/Advantages%20of%20Weighted%20Averaging%20in%20Ensemble%20Models.md """

