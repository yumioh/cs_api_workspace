import pandas as pd
from datetime import datetime
from accident_categorizer import AccidentCategorizer

'''
출생년도 : 나이로 수정
발생일자 : 사고날짜 
근무일수 : 근무경력으로 변경
발생일자 : 요일 추출
'''

df = pd.read_csv("./md_algorithm_mongo/data/accidents_20241212.csv", index_col=None)

#이상치제거 : CSI 사고 데이터 삭제 : 약 27000건
df = df.dropna(axis=0)

#제거 후 KOSHA 데이터 수 : 62277건
# print(df.isnull().sum())
# print(df.info())

#나이 추출
df["출생년도"]= df["출생년도"].astype(str).str.split(".").str[0]
df["나이"] = datetime.today().year - df["출생년도"].astype(int)
df = df[(df["나이"] >= 15) & (df["나이"] <= 100)]

#월 및 요일 추출
df["발생일자"] = pd.to_datetime(df["발생일자"]).dt.strftime("%Y-%m-%d")
df["발생월"] = pd.to_datetime(df["발생일자"]).dt.month
df["발생요일"] = pd.to_datetime(df["발생일자"]).dt.weekday 
df["발생시간"] = df["발생시간"].str.replace("시", "").astype(int)
 
# 컬럼명 변경
df = df.rename(columns={"근무일수" : "근무경력"})

# 근무경력 카테고리화
df["근무경력"] = df["근무경력"].apply(AccidentCategorizer.categrize_service_year)

# 공사규모 카테고리화
df["공사규모"] = df["공사규모"].apply(AccidentCategorizer.categorize_scale_kosha)

# 발생시간 카테고리화
df["발생시간"] = df["발생시간"].apply(AccidentCategorizer.categorize_time_range)

df[["나이","발생일자","발생시간","근무경력","공사규모","발생요일","발생월"]].to_csv("./md_algorithm_mongo/data/accidents_preprocessing.csv", index=None)



