import pandas as pd

df = pd.read_excel("./md_algorithm_mongo/data/CSI_accident.xlsx", sheet_name="Sheet1")

print(df.head())

# 필요한 컬럼의 유니크 값 추출
unique_values = {
    "공종-중분류": df["공종 - 중분류"].dropna().unique(),
    "사고객체-대분류": df["사고객체 - 대분류"].dropna().unique(),
    "사고객체-중분류": df["사고객체 - 중분류"].dropna().unique(),
    "작업프로세스": df["작업프로세스"].dropna().unique()
}

# 데이터프레임 생성
unique_rows_df = df[['공종 - 중분류','작업프로세스']].drop_duplicates().dropna()
filtered_df = df.merge(unique_rows_df, on=['공종 - 중분류','작업프로세스'], how='inner')

filtered_unique_df = filtered_df.drop_duplicates(subset=['공종 - 중분류','작업프로세스'])

print(filtered_unique_df.head())

filtered_unique_df.to_excel("./md_algorithm_mongo/data/extract_unique_work_type.xlsx")

