from sklearn.covariance import EmpiricalCovariance, MinCovDet
import numpy as np
import csv
import pandas as pd

#covariance 계산 방법
#2차원 행렬로 반환해야 공분산 계산이 가능
#데이터에 이상치가 많을때 MinCovDet()
def robust_cov(df) :
    #이상치를 배제한 후 데이터의 일부를 사용하여 공분산 행렬을 계산
    robust_cov = MinCovDet().fit(df)
    return robust_cov.covariance_

#마할라노비스 거리 구하기
def calc_Mahalanobis(y=None, data=None, cov=None): 
  
    y_mu = y - np.mean(data, axis=0)  # 각 열(특성)의 평균으로 계산
    if cov is None:  
        cov = np.cov(data.T)
    else:
        cov = cov.T  # 공분산 계산

    # 공분산 행렬이 2차원인지 확인
    if cov.ndim == 1:
        raise ValueError("covariance matrix is 1-dimensional")

    # 공분산 행렬의 역행렬 계산
    inv_covmat = np.linalg.inv(cov)

    # 마할라노비스 거리 계산
    left = np.dot(y_mu, inv_covmat)
    mahal = np.dot(left, y_mu.T)
    
    return mahal

#colum별로 csv로 나눠서 저장
def save_mahalanobis_by_col(df, comparative_data, coulmns, cov, file_path) :
    for column in coulmns:
        data_list = []
        df_values = df[column].values #values 인덱스나 컬럼 이름 없이 순수한 데이터 값만 포함
        for value in df_values:
            mal_data = calc_Mahalanobis(value, comparative_data.values, cov)
            data_list.append(mal_data)

        #결과 파일 저장
        file_name = f"{file_path}/Mahal_{column}.csv"
        with open(file_name, "w", newline='') as file:
            writer = csv.writer(file)
            for item in data_list:
                writer.writerow([item])


#마할라로비스 계산한 결과값 하나의 데이터 프레임으로 저장
def calc_mahalanobis_df(df, comparative_data, columns, cov):
    results = pd.DataFrame() 
    for column in columns:
        data_list = []
        for value in df[column]:
            mal_data = calc_Mahalanobis(value, comparative_data.values, cov)
            data_list.append(mal_data)

        results[column] = data_list

    return results

#컬럼별 정규화 하기 
def normalize_columns(df, columns):
    results = pd.DataFrame()
    for column in columns:
        values = df[column]
        normalized_values = (values - values.min()) / (values.max() - values.min())
        results[column] = normalized_values
    return results

#정규화 하기
#최대 최소값을 구하기 위하여 gh와 kosha 데이터를 병합 
def normalize(df1, df2):
    #최대, 최소값을 구하기 위하여 병합
    merged_df = pd.concat([df1, df2], axis=0)
    normalized_values = (df1 - merged_df.min()) / (merged_df.max()-merged_df.min())
    nor_df = pd.DataFrame()
    nor_df['normalized'] = normalized_values
    print(nor_df[:10], nor_df.shape)
    return nor_df

 #이상치 제외한 데이터 반환 함수 
def remove_outliers(x,column):
    if column is None :
        data = x
    else :
        data = x[column]
    # Q1, Q3 계산
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    iqr = q3 - q1
    print("iqr : ", iqr)
    y = x[(data >= (q1 - 1.5*iqr)) & (data <= (q3 + 1.5*iqr))]
    print(f" 이상치 제거 후 데이터 {column} : ", y.shape)
    # column이 주어졌을 경우 해당 컬럼만 반환
    if column is None:
        return y
    else:
        return y[column] 
