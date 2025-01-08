import pandas as pd
from datetime import datetime
from accident_categorizer import AccidentCategorizer
import random


'''
출력일자 : yyyy-mm-dd로 수정
요일 : 출력일자로 요일 추출
생년월일 : 나이
건설업근무경력 : 근무경력으로 컬럼 변경
현장규모 : 공사규모로 변경
발생시간 : 동일하게 8시로 변경

'''

df = pd.read_csv("./md_algorithm_mongo/data/non_accidents_20241212.csv", index_col=None)
print(df.info())

#결측치 제거 후 : 47424건
df = df.dropna(axis=0)
#print(df.info()) 

#나이 추출
df["나이"] = pd.to_datetime(df["생년월일"],errors="coerce")
df["나이"] = datetime.today().year - df["나이"].dt.year.fillna(0).astype(int)
df = df[(df["나이"] >= 15) & (df["나이"] <= 100)]


#발생일자,발생시간,발생요일,발생월 추가 
df["발생일자"] = pd.to_datetime(df["출역일자"]).dt.strftime("%Y-%m-%d")
df["발생월"] = pd.to_datetime(df["발생일자"]).dt.month
# 0:Mon, 1:Tue, .... 6:Sun
df["발생요일"] = pd.to_datetime(df["발생일자"]).dt.weekday 
# kosha 통계 기준으로 가장 사고가 적게 난 시간대  : 2~4시, 4~6시, 20~22시 랜덤화 해서 돌리기  
numbers = [2,3,4,5,6,20,21]
df["발생시간"] = random.choices(numbers, k=len(df))

#df["발생시간"] = df["발생시간"].str.replace("시", "").astype(int)

df["공사규모"] = pd.to_numeric(df["현장규모"].str.replace(",", "", regex=True)).astype(int)

df = df.rename(columns={"건설업근무경력" : "근무경력"})

#항목별 카테고리화
df["근무경력"] = df["근무경력"].apply(AccidentCategorizer.categrize_service_year)
df["발생시간"] = df["발생시간"].apply(AccidentCategorizer.categorize_time_range)
df["공사규모"] = df["공사규모"].apply(AccidentCategorizer.categorize_scale_number)
df["나이"] = df["나이"].apply(AccidentCategorizer.categorize_age_num)

df[["나이","발생일자","발생시간","근무경력","공사규모","발생요일","발생월"]].to_csv("./md_algorithm_mongo/data/non_accidents_preprocessing.csv", index=None)