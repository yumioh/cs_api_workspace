import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from accident_categorizer import AccidentCategorizer
from sklearn.preprocessing import LabelEncoder


accident_data = pd.read_excel("./md_algorithm_mongo/data/accident_cases_kosha.xlsx", sheet_name='case')

accident_data = accident_data[["시행업체(회사명)","사업소명(현장명)","공사규모","출생년도","발생시간","발생일자","근무일수","사고 유형","재해 형태","재해규모","기인물"]]
accident_data = accident_data.dropna()

print(accident_data.head())

accident_data["발생시간"] = accident_data["발생시간"].str.replace("시", "").astype(float)

accident_data["근무일수"] = accident_data["근무일수"].apply(AccidentCategorizer.categrize_service_year)

accident_data["공사규모"] = accident_data["공사규모"].apply(AccidentCategorizer.categorize_scale_kosha)

accident_data['발생년도'] = accident_data['발생일자'].dt.year.astype(float)
accident_data['발생월'] = accident_data['발생일자'].dt.month.astype(float)
accident_data['발생일'] = accident_data['발생일자'].dt.day.astype(float)
accident_data['발생요일'] = accident_data['발생일자'].dt.weekday.astype(float)

#사업소명 
freq = accident_data['재해규모'].value_counts() / len(accident_data)
accident_data['재해규모'] = accident_data['재해규모'].map(freq)

#사고유형
freq = accident_data['사고 유형'].value_counts() / len(accident_data)
accident_data['사고 유형'] = accident_data['사고 유형'].map(freq)

freq = accident_data['기인물'].value_counts() / len(accident_data)
accident_data['기인물'] = accident_data['기인물'].map(freq)

#사고유형에 순서가 없고 단순히 구분만 필요한 경우
encoder = LabelEncoder()
accident_data['시행업체(회사명)'] = encoder.fit_transform(accident_data['시행업체(회사명)'])
accident_data['사업소명(현장명)'] = encoder.fit_transform(accident_data['사업소명(현장명)'])
accident_data['재해 형태'] = encoder.fit_transform(accident_data['재해 형태'])

print(accident_data.head())

numerical_columns = accident_data.select_dtypes(include=['float64', 'int64'])
print(numerical_columns.info())

# Drop columns with too many NaN values (threshold: at least 50% non-NaN values)
threshold = len(numerical_columns) * 0.3
filtered_numerical = numerical_columns.dropna(axis=1, thresh=threshold)

#결측값 채우기
processed_numerical = numerical_columns.fillna(numerical_columns.mean())

# 피어슨 상관계수 계산
correlation_matrix = processed_numerical.corr()

plt.rc("font", family="Malgun Gothic")
sns.set_theme(font="Malgun Gothic", rc={"axes.unicode_minus": False}, style='white')

plt.figure(figsize=(15, 10))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', linewidths=.5, annot_kws={"size": 4}, cmap='RdYlBu_r')
plt.xticks(fontsize=8)
plt.yticks(fontsize=8)
plt.title('Pearson Correlation Heatmap for Accident Data')
plt.savefig('./md_algorithm_mongo/data/img/clustermap_pearson_correlation.png')
plt.show(block=False)
plt.show()
