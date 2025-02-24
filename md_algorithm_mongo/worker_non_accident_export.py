from md_algorithm_mongo.mongo_utils import MongoDBHandler
from datetime import datetime


if __name__ == "__main__":

    db_name = "accident_data"
    collection_name = "non_accidents"

    mongo_handler = MongoDBHandler(db_name, collection_name)

    query = {}
    projection = {
        "생년월일" : 1,
        "나이" : 1,
        "건설업근무경력" : 1,
        "현장규모": 1,
        "출역일자" :1 , 
        "_id" : 0
    }

    non_accident_data = mongo_handler.fetch_data(query, projection)

    # 데이터 저장
    today = datetime.now().strftime("%Y%m%d")
    output_file = f"./md_algorithm_mongo/data/non_accidents_{today}.csv"
    non_accident_data.to_csv(output_file, index=False)

    # mongoDB 연결 보기
    mongo_handler.close_connetion()
    





