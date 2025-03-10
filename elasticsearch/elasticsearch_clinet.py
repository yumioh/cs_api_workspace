from elasticsearch import Elasticsearch
from datetime import datetime

# Elasticsearch 클라이언트 연결
# Elasticsearch IP: 192.168.0.203 port : 9200
es = Elasticsearch(["http://192.168.0.203:9200"])

# try:
#     # 연결 확인
#     info = es.info()
#     print("연결 성공!", info)
    
#     #데이터 넣기 
#     doc = {
#         "name" : "taylor",
#         "age" : 67,
#         "email" : "taylor@gamil.com",
#         "created_at" : datetime.now().strftime("%Y-%m-%d")
#     }
    
#     es.index(index="riskzero", document=doc)
    
#     #모든 문서 조회
#     # data = es.search(index="riskzero", query={"match_all": {}})
#     # print("검색 결과:", data)
    
#     #cat API를 활용해 인덱스 리스트 확인
#     # es.cat.indices() 클러스터 내의 모든 인덱스를 조회하는 기능
#     # green : 모든 샤드 정상적으로 할당, yellow : 기본 샤드는 정상적으로 작동, 복제 샤드는 일부 또는 전부 할당되지 않음. red : 일부 기본 샤드가 손실실
#     data = es.cat.indices()
#     print(data)
       
# except Exception as e:
#     print("오류 발생:", e)
    
# 문서 색인(데이터 저장 및 추가) : PUT
def index_document(index_name, doc_id=None, body=None):
    if body is None:
        raise ValueError("body는 None이 될 수 없습니다.")
    
    try:
        response = es.index(index=index_name, id=doc_id if doc_id else None, document=body)
        print("문서 색인 성공 : ", response)
        return response
    except Exception as e :
        print(f"문서 색인 중 오류 발생 : ", {e})
        return None
    
    
    
# document = {
#     "name": "james",
#     "age": 30,
#     "email": "john@example.com",
#     "created_at" : datetime.now().strftime("%Y-%m-%d")
# }

# result = index_document("riskzero", body=document)

    
    
# 데이터 조회 
def get_document(index_name, doc_id=None, body=None) :
    if body is None:
        raise ValueError("body는 None이 될 수 없습니다.")
    
    try:
        response = es.get(index=index_name, id=doc_id if doc_id else None, document=body)
        return response
    
    except Exception as e :
        print(f"문서 색인 중 오류 발생 : ", {e})
        return None

document = {
        "query": {
            "bool": {
            "must": [
                { "match": { "name": "juelly" } }
            ],
            "should": [
                { "term": { "email": "risk" } }
            ],
            "filter": [
                { "range": { "age": { "gte": 18, "lte": 30 } } }
            ]
            }
        }     
    }
   

result = get_document("riskzero", body=document)
print(result)