import pandas as pd
import datetime as dt
import sys, os # add the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import category_utils

''''
GH(비사고 데이터)
- 공사규모
- 날짜 => MON값만 추출하여 월값만 저장
- 요일 => 월,화,수,목,금으로 변경
- 출생년도 => 나이로 변경
- 발생시간 => 6시로 열추가 

'''

#GH 파일 데이터 들고 오기
#gh_df = pd.read_excel("./md_algorithm/data/gh_accident_cases_240924.xlsx")
gh_df = pd.read_excel("./md_algorithm/data/gh_accident_cases_240924.xlsx")
# print("GH 데이터 INFO :", gh_df.info())
print(gh_df.head())

print("이상치 제거 전 : ", gh_df.shape)

#year 추출
gh_df["출생년도"] = gh_df["출생년도"].astype(str).str.split("-").str[0]

#만나이 계산: 2024년 기준으로 출생년도에서 나이 계산
gh_df['나이'] = 2024 - gh_df["출생년도"].astype(int)
# print("GH 데이터 INFO :", gh_df.info())
# print("GH 데이터 나이 데이터 추가 : ", gh_df.head())

#월만 추출
gh_df["월별"]= pd.to_datetime(gh_df["날짜"]).dt.month
# print(gh_df.head())

#이상치 제거 
#나이 100세 이상 제외
gh_df = gh_df[gh_df.나이 <= 100]
gh_df = gh_df[gh_df.나이 >= 15]
gh_df = gh_df[gh_df["공사규모"] != "50인~99인"]

print("이상치 제거 후 :", gh_df.shape)
# #컬럼명 변경
gh_df.rename(columns={'경력일수':'근무경력'}, inplace=True)
# print(gh_df.head()

#요일 한글로 변경
gh_df["요일별"]= gh_df["요일"].apply(category_utils.day_to_korean)

gh_df[["공사규모","발생시간","근무경력","나이","월별","요일별"]].to_csv("./md_algorithm/data/gh_preprocessing.csv"
                                                   ,encoding="utf-8",index=False)
print("저장할 데이터 head :", gh_df)
print("저장할 데이터 shape :", gh_df.shape)
