import pandas as pd
import matplotlib.pyplot as plt
from data_processor import DataProcessor

accident_df = pd.read_csv("./md_algorithm_mongo/data/accidents_preprocessing.csv")
non_accident_df = pd.read_csv("./md_algorithm_mongo/data/non_accidents_preprocessing.csv")

accident_df = accident_df[['나이','발생시간','근무경력','공사규모','발생요일','발생월']]
non_accident_df = non_accident_df[['나이','발생시간','근무경력','공사규모','발생요일','발생월']]

# 기본 데이터 이상치 제거
for col in accident_df.columns:
    accident_df = DataProcessor.remove_outliers_zcore(accident_df, col)
    non_accident_df = DataProcessor.remove_outliers_zcore(non_accident_df, col)


for col in accident_df.columns:
    plt.rcParams['font.family'] ='Malgun Gothic'
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['boxplot.flierprops.markersize'] = 3

    data = [
        accident_df[col].dropna().tolist(),
        non_accident_df[col].dropna().tolist(),
    ]

    plt.figure(figsize=(5,4))
    plt.boxplot(data)
    plt.title(f'사고 vs 비사고 항목 비교 : {col}',fontdict={'weight': 'bold', 'size' : "15"})
    plt.ylabel('Values')
    plt.xticks([1, 2], ['Accident', 'Non-Accident'])
    plt.savefig(f"./md_algorithm_mongo/data/img/boxplot_comparison_{col}")
    plt.show()
