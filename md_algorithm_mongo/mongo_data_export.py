from mongo_utils import MongoDBHandler
from datetime import datetime

'''
MongoDB에 저장된 데이터를 추출하는 코드 (현재 해당 데스크탑이 없어 MongoDB 사용 불가능)
'''

if __name__ == "__main__":

    db_name = "accident_data"
    collection_name = "accidents"

    mongo_handler = MongoDBHandler(db_name, collection_name)

    query = {}
    projection = {
        "출생년도" : 1,
        "발생시간" : 1,
        "발생일자" : 1,
        "근무일수": 1,
        "공사규모" :1 , 
        "_id" : 0
    }

    non_accident_data = mongo_handler.fetch_data(query, projection)
    
    # 데이터 저장 
    today = datetime.now().strftime("%Y%m%d")
    output_file = f"./md_algorithm_mongo/data/accidents_{today}.csv"
    non_accident_data.to_csv(output_file, index=False)

    # mongoDB 연결 보기
    mongo_handler.close_connetion()
