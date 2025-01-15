import pandas as pd
import datetime as dt
import sys, os # add the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import category_utils

'''
전처리한 데이터 카테고리화 
 - 근속년수
 - 날짜 
 - 나이
 - 공사규모
 - 발생시간
'''

gh_file_path = "./md_algorithm/data/gh_preprocessing.csv"
kosha_file_path = "./md_algorithm/data/kosha_preprocessing.csv"
gh_save =  "./md_algorithm/data/gh_categorize.csv"
kosha_save =  "./md_algorithm/data/kosha_categorize.csv"

data = pd.read_csv(kosha_file_path)
print(data.head())
print(data.info())

#근속년수 카테고리화 
data["근무경력"] = data["근무경력"].str.replace(r"\s", "", regex=True)
print(data["근무경력"])
data["근무경력"] = data["근무경력"].apply(category_utils.categorize_service_years_num)
#print(data.head())

data["나이"] = data["나이"].astype(int).apply(category_utils.categorize_age_num)

# 시간 카테고리
data["발생시간"] = data["발생시간"].str.replace("시","")
data["발생시간"] = data["발생시간"].astype(int).apply(category_utils.categorize_time_num)
#print(data["발생시간"])

#공사 규모 => num
data["공사규모"] = data["공사규모"].str.replace(r"\s", "", regex=True)
data["공사규모"] = data["공사규모"].apply(category_utils.categorize_scale_num)

#요일별 => num
data["요일별"] = data["요일별"].apply(category_utils.categorize_day_num)

save_data = pd.DataFrame(data)
save_data.to_csv(kosha_save, encoding="utf-8-sig", index=False)

#파일 이름만 추출
file_name = os.path.basename(kosha_save)
print(f"{file_name} data : ", save_data.head())
print(f"{file_name} info : ", save_data.info())
