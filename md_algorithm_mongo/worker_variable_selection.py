import pandas as pd
from scipy.stats import ttest_ind
from scipy.stats import mannwhitneyu
from statsmodels.multivariate.manova import MANOVA
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import xgboost as xgb


non_accidents_df = pd.read_csv("./md_algorithm_mongo/data/non_accidents_preprocessing.csv")
accidents_df = pd.read_csv("./md_algorithm_mongo/data/accidents_preprocessing.csv")

print(non_accidents_df.describe())
print(accidents_df.describe())
# print(non_accidents_df.head())

variables = ['나이', '근무경력', '발생시간', '공사규모', "발생월", "발생요일"]

#t검정 하기 : 두 집단의 평균 비교하여 유의미한 변수 추출
selected_vars = []
for var in variables:
    t_stat, p_value = ttest_ind(accidents_df[var], non_accidents_df[var], equal_var=False)
    if p_value < 0.05:  # 유의 수준 5%
        selected_vars.append(var)
        print(f"{var}: t-stat = {t_stat:.2f}, p-value = {p_value:.3f} (유의미)")
    else:
        print(f"{var}: t-stat = {t_stat:.2f}, p-value = {p_value:.3f} (유의미하지 않음)")

print("유의미한 변수:", selected_vars)


#윌콕스 부호 순위 검정 : 비모수검정으로 두 집단 간 순위 차이 비교
results = {}
for var in variables:
    try:
        # 두 그룹의 해당 변수 추출
        non_accident_group = non_accidents_df[var].dropna()
        accident_group = accidents_df[var].dropna()

        # Wilcoxon Rank-Sum Test
        stat, p = mannwhitneyu(non_accident_group, accident_group)
        results[var] = {'U-statistic': stat, 'p-value': p}

        # 결과 출력
        print(f"변수: {var}")
        print(f"U-statistic: {stat:.2f}, p-value: {p:.3f}")
        if p < 0.05:
            print("유의미한 차이가 있습니다.")
        else:
            print("유의미한 차이가 없습니다.")
    except KeyError:
        print(f"변수 '{var}'가 데이터에 없습니다.")
    except Exception as e:
        print(f"변수 '{var}' 처리 중 오류: {e}")


# 다변량 분석(MANOVA): 여러변수를 한번에 비교
combined_df = accidents_df.copy()
combined_df['사고여부'] = 1
non_accidents_df['사고여부'] = 0
combined_df = pd.concat([combined_df, non_accidents_df])

manova = MANOVA.from_formula(f"{'+'.join(variables)} ~ 사고여부", data=combined_df)
print(manova.mv_test())

#랜덤포레스트 : 사고/비사고 데이터를 예측하는데 기여도가 높은 변수 평가
X = combined_df[variables]
y = combined_df['사고여부']

# 랜덤포레스트 모델 학습
rf = RandomForestClassifier()
rf.fit(X, y)

# 변수 중요도 출력 
importances = rf.feature_importances_
for var, imp in zip(variables, importances):
    print(f"{var}: 중요도 = {imp:.3f}")

# [머신러닝] 
# LightGBM : Tree1이 예측하고 남은 잔차들을 Tree2, Tree3를 차례대로 지나가면서 줄여가는 것을 부스팅
# 각 Tree들을 weak learner라고 보면 된다. 가중치 부여를 통해 오류를 개선 
# 경사하강법 이용 즉, 손실함수를 최소화 하는 방향성을 갖고 가중치 값을 업데이트

print(combined_df.head())
x = combined_df.drop(columns=["사고여부"])
y = combined_df["사고여부"]

#데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# x_train : 입력 데이터  y_train:해당 데이터 라벨
train_data = lgb.Dataset(X_train, label=y_train)

#모델학습
params = {
        'objective': 'binary', # 이진분류 사고1, 비사고0
    'boosting_type': 'gbdt', # 일부 트리를 무작위로 제외해 과적합 방지
    'metric': 'binary_error', # 이진 분류에서의 오류율(실제값과 다른 비율)
    'verbose': -1 #출력 로그 최소화
}

# num_boost_round : 생성할 트리 개수 
lgb_model = lgb.train(params, train_data, num_boost_round=150)

# feature_importance : 변수 중요도 가져오는 함수 
# gain: 해당 변수가 트레에서 정보 이득을 얼마나 많이 가져오는지 측정 => 높은 값일 수록 모델이 해당 변수를 많이 사용
importance = lgb_model.feature_importance(importance_type='gain')
feature_names = X.columns

for name, imp in zip(feature_names, importance):
    print(f"{name}: 중요도 = {imp:.3f}")

#모델 학습
xgb_model = xgb.XGBRFClassifier()
xgb_model.fit(X_train, y_train)

#get_score(importance_type="gain") : 각 변수의 중요도 반환
xgb_importance = xgb_model.get_booster().get_score(importance_type="gain")
print("XGBoost 중요도 : ", xgb_importance)

#발생시간, 근무경력, 나이, 발생월을 변수로 선택
