from sklearn.covariance import MinCovDet
import numpy as np
import pandas as pd

class MathUtils:

    @staticmethod
    def robust_cov(data) :
        #2차원 행렬로 반환을 해야 공분산 계산이 가능
        #이상치를 배제한 후 데이터의 일부를 사용하여 공분산 행렬 계산
        #data = data.to_numpy()
        robust_cov = MinCovDet().fit(data)
        return robust_cov.covariance_
    

    #마할라노비스 거리 구하기
    def calc_mahalanobis(y=None, data=None, cov=None): 
        y_mu = y - np.mean(data, axis=0)  # 각 열(특성)의 평균으로 계산
        if cov is None:  
            cov = np.cov(data.T)  # 공분산 행렬 계산
        elif cov.ndim != 2:
            raise ValueError("Covariance matrix must be 2-dimensional")

        # 공분산 행렬의 역행렬 계산
        inv_covmat = np.linalg.pinv(cov)

        # 마할라노비스 거리 계산
        mahal = np.dot(y_mu, np.dot(inv_covmat, y_mu.T))
        #np.sqrt(mahal)
        return mahal
    
    # z값 계산
    def z_scores(df):
         return (df - df.mean()) / df.std()
    
    #minmaxscaling(정규화)
    def minmaxscaling(df1, df2):
    #최대, 최소값을 구하기 위하여 병합
        merged_df = pd.concat([df1, df2], axis=0)
        normalized_values = (df1 - merged_df.min()) / (merged_df.max() - merged_df.min())
        nor_df = pd.DataFrame()
        nor_df['normalized'] = normalized_values
        return nor_df
        

