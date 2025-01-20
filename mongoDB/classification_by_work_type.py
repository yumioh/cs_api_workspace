from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# 데이터 로드
csi_gongjong = pd.read_excel('./mongoDB/data/사고비사고데이터 공종별_항목정리.xlsx', sheet_name="CSI 공종항목")
riskzero_categories = pd.read_excel('./mongoDB/data/사고비사고데이터 공종별_항목정리.xlsx', sheet_name="리스크제로 공종별항목")

print(csi_gongjong.head())

# 특정 열 선택
csi_gongjong_list = csi_gongjong["공종_중분류"].tolist()  # "공종" 열 이름 확인 필요
riskzero_list = riskzero_categories["공종"].tolist()  # "공종_중분류" 열 이름 확인 필요

# 고유값 추출
unique_gongjong = list(set(csi_gongjong_list))

# TF-IDF 벡터화
vectorizer = TfidfVectorizer(min_df=1)
unique_gongjong_vectors = vectorizer.fit_transform(unique_gongjong)
middle_vectors = vectorizer.transform(riskzero_list)

# 유사도 계산
similarity_matrix = cosine_similarity(unique_gongjong_vectors, middle_vectors)

# 매핑
mapped_unique_categories = []
for i in range(similarity_matrix.shape[0]):
    best_match_idx = similarity_matrix[i].argmax()
    mapped_unique_categories.append(riskzero_list[best_match_idx])

# 원본 데이터로 복원
mapped_categories = [mapped_unique_categories[unique_gongjong.index(item)] for item in csi_gongjong_list]

# 결과 출력
result = pd.DataFrame({"공종_중분류": csi_gongjong_list, "공종": mapped_categories})
print(result)

# 결과 저장
result.to_excel('./mongoDB/data/공종_중분류_매핑결과.xlsx', index=False)
