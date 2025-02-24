from dotenv import load_dotenv

load_dotenv()

''''
- 이상치 제거 
- 정규화 
'''

class DataProcessor :

    @classmethod
    def remove_outliers_zcore(cls, df, col):
        std = df[col].std()
        z_scores = (df[col] - df[col].mean()) / df[col].std()
        if std == 0:
            return df
        return df[abs(z_scores) <= 1.96]
    
    @classmethod
    def remove_outliers_quantile(cls, df, col):
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1 #IQR
        lower_bound = q1 - 1.5*iqr
        upper_bound = q3 + 1.5*iqr
        print(df.head())
        return df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    
    def normalize(df, columns):
        for col in columns:
            col_min = df[col].min()
            col_max = df[col].max()
            df[col] = (df[col] - col_min) / (col_max - col_min)
        return df