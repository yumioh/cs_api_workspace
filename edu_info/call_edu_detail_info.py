import requests
import os
from dotenv import load_dotenv
import pandas as pd

#call api key 
load_dotenv()
edu_api_key = os.getenv('EDU_API_KEYS')

params = {
    'serviceKey': edu_api_key,
    'pageNo': 1,
    'numOfRows': 100,
    'eduCategory' : 'CSI',
    'returnType': 'JSON'
}

#eduSeq 확인해보기 

url = "	https://api.csi.go.kr/api/service/edu/onlineEduInfo/1?"

res = requests.get(url, params)
print(res.text)
#edu_data = res.json()
#edu_items = edu_data['response']['body']['items']
#print(edu_items)
# edu_detail_df = pd.DataFrame(edu_items)
# edu_detail_df.index = edu_detail_df.index + 1
# print(edu_detail_df.head())

#save online edu list : 45
#edu_detail_df.to_csv('./edu_info/data/edu_details_info.csv', encoding="utf-8-sig")