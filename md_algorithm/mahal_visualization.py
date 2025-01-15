import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules import math_utils


print("-------------------gh vs kosah MD 박스플롯 그리기 --------------------")  

gh_md_df = pd.read_csv("./md_algorithm/data/gh_Mahal_list.csv", header = None)
kosha_md_df = pd.read_csv("./md_algorithm/data/kosha_Mahal_list.csv", header = None)

# MD값 이상치 제거 및 인덱스 리셋
outlier_gh_md = gh_md_df[(abs((gh_md_df[0] - gh_md_df[0].mean()) / gh_md_df[0].std()) > 1.96)].index
gh_md_filtered = gh_md_df.drop(outlier_gh_md)
gh_md_filtered.to_csv("./md_algorithm/data/gh_without_outline.csv",index = False)

outlier_kosha_md = kosha_md_df[(abs((kosha_md_df[0] - kosha_md_df[0].mean()) / kosha_md_df[0].std()) > 1.96)].index
kosha_md_filtered = kosha_md_df.drop(outlier_kosha_md)
kosha_md_filtered.to_csv("./md_algorithm/data/kosha_without_outline.csv",index = False)

# plt.boxplot([gh_md_filtered[0], kosha_md_filtered[0]]) 
# plt.title(f'GH vs KOSHA MD', fontdict={'weight': 'bold', 'size' : "20"}) #제목 및 라벨 설정
# plt.ylabel('Values')
# plt.xticks([1, 2], ['GH Data', 'KOSHA Data']) 
# plt.savefig(f"./md_algorithm/data/img/gh_kosha_boxplot.png")
# plt.show()

print("------------------- GH vs KOSHA 산점도 그리기 --------------------")

#오름차순으로 정렬 후 인덱스 재정렬
arranged_gh = gh_md_filtered.sort_values(by=0).reset_index(drop=True)
arranged_kosha = kosha_md_filtered.sort_values(by=0).reset_index(drop=True)
# print(arranged_gh.head())
# print(arranged_kosha.head())

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['boxplot.flierprops.markersize'] = 3
plt.scatter(arranged_gh.index, arranged_gh.iloc[:, 0], color="dodgerblue", label="GH",s=8)
plt.scatter(arranged_kosha.index, arranged_kosha.iloc[:, 0], color="coral", alpha=0.4, label="KOSHA", s=8)
plt.title(f"GH vs KOSHA (MD)",fontdict={'weight': 'bold', 'size' : "20"})
plt.xlabel("Index")
plt.ylabel("MD")
plt.legend()
plt.grid(True)
plt.savefig(f"./md_algorithm/data/img/scatter_gh_kosha.png")
plt.show()

print("------------------- GH vs KOSHA 로그 산점도 그리기 --------------------")

#오름차순으로 정렬 후 인덱스 재정렬
arranged_gh = gh_md_filtered.sort_values(by=0).reset_index(drop=True)
arranged_kosha = kosha_md_filtered.sort_values(by=0).reset_index(drop=True)
# print(arranged_gh.head())
# print(arranged_kosha.head())

#로그변환
log_arranged_gh = np.log(arranged_gh.iloc[:, 0])
log_arranged_kosha = np.log(arranged_kosha.iloc[:, 0])

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['boxplot.flierprops.markersize'] = 3
plt.scatter(log_arranged_gh.index, log_arranged_gh, color="dodgerblue", label="GH",s=8)
plt.scatter(log_arranged_kosha.index, log_arranged_kosha, color="coral", alpha=0.4, label="KOSHA", s=8)
plt.title(f"GH vs KOSHA 로그 (MD)",fontdict={'weight': 'bold', 'size' : "20"})
plt.xlabel("Index")
plt.ylabel("MD")
plt.grid(True)
plt.legend()
plt.savefig(f"./md_algorithm/data/img/scatter_gh_kosha_log.png")
plt.show()

print("------------------- GH vs KOSHA 정규화 산점도 그리기 --------------------")

#오름차순으로 정렬 후 인덱스 재정렬
gh_nor = pd.read_csv("./md_algorithm/data/gh_normalized.csv", )
kosah_nor = pd.read_csv("./md_algorithm/data/kosha_normalized.csv")
print(gh_nor)
print(gh_nor.index)

gh_nor_sorted = gh_nor.sort_values(by="normalized").reset_index(drop=True)
kosah_nor_sorted = kosah_nor.sort_values(by="normalized").reset_index(drop=True)

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['boxplot.flierprops.markersize'] = 3
plt.scatter(gh_nor.index, gh_nor, color="dodgerblue", label="GH",s=8)
plt.scatter(kosah_nor.index, kosah_nor, color="coral", alpha=0.4, label="KOSHA", s=8)
plt.title(f"정규화된 GH vs KOSHA (MD)",fontdict={'weight': 'bold', 'size' : "20"})
plt.xlabel("Index")
plt.ylabel("MD")
plt.grid(True)
plt.legend(loc='upper right')
plt.savefig(f"./md_algorithm/data/img/gh_kosha_normalized.png")
plt.show()

print("------------------- GH vs KOSHA 정규화 로그 산점도 그리기 --------------------")
# x축 : MD데이터 
# y축 : 정규화한 log(MD)

gh_log = pd.read_csv("./md_algorithm/data/gh_normalized_log.csv")
kosha_log = pd.read_csv("./md_algorithm/data/kosha_normalized_log.csv")

gh_outline_log = pd.read_csv("./md_algorithm/data/gh_outline_normalized_log.csv")
kosha_outline_log = pd.read_csv("./md_algorithm/data/kosha_outline_normalized_log.csv")

#오름차순으로 정렬 후 인덱스 재정렬
gh_normalized_log = gh_log.sort_values(by="normalized").reset_index(drop=True)
kosha_normalized_log = kosha_log.sort_values(by="normalized").reset_index(drop=True)

gh_normalized_log = gh_outline_log.sort_values(by="normalized").reset_index(drop=True)
kosha_normalized_log = kosha_outline_log.sort_values(by="normalized").reset_index(drop=True)

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['boxplot.flierprops.markersize'] = 3
plt.scatter(gh_normalized_log.index, gh_normalized_log, color="dodgerblue", label="GH",s=8)
plt.scatter(kosha_normalized_log.index, kosha_normalized_log, color="red", alpha=0.4, label="KOSHA", s=8)
# plt.title(f"정규화된 GH vs KOSHA (로그 MD)",fontdict={'weight': 'bold', 'size' : "20"})
plt.title(f"사고 vs 비사고 log(MD) 정규화한 산점도",fontdict={'weight': 'bold', 'size' : "20"})
plt.xlabel("Index")
plt.ylabel("Normalized Log MD")
plt.grid(True)
plt.legend(loc='upper right')
plt.savefig(f"./md_algorithm/data/img/gh_kosha_normalized_log.png")
plt.show()


print("-------------------kosha 박스플롯 그리기 --------------------")  

# columns = ["공사규모","발생시간","근무경력","나이"]

# kosha = pd.read_csv("./md_algorithm/data/kosha_mal_normalized.csv")
# kosha_md = kosha["normalized"]

# for column in columns : 
#     plt.rcParams['font.family'] ='Malgun Gothic'
#     plt.rcParams['axes.unicode_minus'] = False
#     plt.rcParams['boxplot.flierprops.markersize'] = 3
    
#     #boxplot 그리기
#     plt.boxplot([math_utils.remove_outliers(kosha,column),math_utils.remove_outliers(kosha_md,None)])
#     #제목 및 라벨 설정
#     plt.title(f'KOSHA {column}',fontdict={'weight': 'bold', 'size' : "20"})
#     plt.ylabel('Values')
#     plt.xticks([1, 2], ['KOSHA Data', 'MD Data']) 
#     plt.grid(True)
#     plt.savefig(f"./md_algorithm/data/img/kosha_boxplot_{column}.png")
#     plt.show()

print("-------------------gh 박스플롯 그리기 --------------------")  
# gh = pd.read_csv("./md_algorithm/data/gh_mal_normalized.csv")
# gh_md = gh["mahal"] 
# #rint("gh :", gh.describe())

# for column in columns : 
#     plt.rcParams['font.family'] ='Malgun Gothic'
#     plt.rcParams['axes.unicode_minus'] = False
#     plt.rcParams['boxplot.flierprops.markersize'] = 3
     
#     #boxplot 그리기
#     plt.boxplot([math_utils.remove_outliers(gh,column), math_utils.remove_outliers(gh_md, None)])
#     #제목 및 라벨 설정
#     plt.title(f'GH {column}', fontdict={'weight': 'bold', 'size' : "20"})
#     plt.ylabel('Values')
#     plt.xticks([1, 2], ['GH Data', 'MD Data']) 
#     plt.savefig(f"./md_algorithm/data/img/gh_boxplot_{column}.png")
#     plt.show()

print("-------------------GH DATA 산점도 그리기 --------------------")
# gh_accident_df = pd.read_csv("./md_algorithm/data/gh_preprocessing.csv")
# gh_md_df = pd.read_csv("./md_algorithm/data/gh_Mahal_list.csv", header = None)

# #x측 위험도 y측 md
# plt.figure()
# plt.scatter(gh_accident_df["위험도"], gh_md_df[0], color="skyblue", s=10)
# plt.title('GH 산점도', fontdict={'weight': 'bold', 'size' : "20"})
# plt.xlabel("GH 위험도", fontdict={'weight': 'bold', 'size' : "12"})
# plt.ylabel("MD값", fontdict={'weight': 'bold', 'size' : "12"})
# plt.savefig("./md_algorithm/data/img/gh_scatter.png")
# plt.show()

print("-------------------이상치 제거 전 GH KOSHA 항목별 산점도 그리기 --------------------")

# gh_df = pd.read_csv("./md_algorithm/data/gh_categorize_random.csv")
# kosha_df = pd.read_csv("./md_algorithm/data/kosha_categorize.csv")

# for column in columns:
#     plt.figure()
#     plt.scatter(gh_df[column], gh_md_df[0], color="purple", label="GH",s=10, marker="D")
#     plt.scatter(kosha_df[column], kosha_md_df[0], color="pink", alpha=0.4, label="KOSHA", s=10)
#     plt.title(f"{column} vs MD 거리 산점도",fontdict={'weight': 'bold', 'size' : "20"})
#     plt.xlabel(f'{column} 데이터')
#     plt.ylabel("MD 거리")
#     plt.legend()
#     plt.savefig(f"./md_algorithm/data/img/scatter_{column}.png")
#     plt.show()


print("-------------------이상치 제거 후 GH KOSHA 항목별 산점도 그리기 --------------------")

# print(gh_df.head())
# for column in columns:
    # 이상치 인덱스 추출 및 제거
    # outlier_gh = gh_df[(abs((gh_df[column] - gh_df[column].mean()) / gh_df[column].std()) > 1.96)].index
    # gh_df_filtered = gh_df.drop(outlier_gh).reset_index(drop=True)
    
    # outlier_kosha = kosha_df[(abs((kosha_df[column] - kosha_df[column].mean()) / kosha_df[column].std()) > 1.96)].index
    # kosha_df_filtered = kosha_df.drop(outlier_kosha).reset_index(drop=True)

    # # 데이터 길이 조정 x,y축 동일하게 함
    # min_len = min(len(gh_df_filtered[column]), len(gh_md_filtered))
    # data_x = gh_df_filtered[column].iloc[:min_len]
    # data_y = gh_md_filtered[0].iloc[:min_len]

    # min_len_2 = min(len(kosha_df_filtered[column]), len(kosha_md_filtered))
    # data_z = kosha_df_filtered[column].iloc[:min_len_2]
    # data_i = kosha_md_filtered[0].iloc[:min_len_2]
    
    # #산점도 x,y길이가 동일해야한다 
    # gh_df_filtered = math_utils.remove_outliers(gh_df,column)
    # gh_md_filtered = math_utils.remove_outliers(gh_md_df, None)
    # min_len = min(len(gh_df_filtered), len(gh_md_filtered))
    # data_x = gh_df_filtered.iloc[:min_len]
    # data_y = gh_md_filtered.iloc[:min_len]
    
    # kosha_df_filtered = math_utils.remove_outliers(kosha_df, column)
    # kosha_md_filtered = math_utils.remove_outliers(kosha_md_df, None)
    # min_len2 = min(len(kosha_df_filtered), len(kosha_md_filtered))
    # data_z = kosha_df_filtered.iloc[:min_len2]
    # data_i = kosha_md_filtered.iloc[:min_len2]

    # # 산점도 그리기
    # plt.scatter(data_x, data_y, color="green", label="GH", s=6, marker="*")
    # plt.scatter(data_z, data_i, color="orange", alpha=0.1, label="KOSHA", s=6)
    # plt.title(f"{column} vs MD 거리 산점도", fontdict={'weight': 'bold', 'size': 20})
    # plt.xlabel(f'{column} 데이터')
    # plt.ylabel("MD 거리")
    # plt.legend()
    # plt.savefig(f"./md_algorithm/data/img/scatter_outliner_{column}.png")
    # plt.show()


print("-------------------이상치 제거 전 GH KOSHA 항목별 산점도 그리기 --------------------")

# gh_df = pd.read_csv("./md_algorithm/data/gh_categorize_random.csv")
# kosha_df = pd.read_csv("./md_algorithm/data/kosha_categorize.csv")
# column = "나이"

# #categories = ["2~4시", "20~22시", "4~6시", "22~24시", "0~2시", "18~20시", "6~8시", "16~18시", "12~14시", "14~16시", "8~10시", "10~12시"]
# #categories = ["6개월미만","6개월~1년","1~2년","2~3년","3~4년","4~5년","5~10년","10년이상"]
# categories = ["10대","20대","30대","40대","50대","60대","70대","80대이상"]
# x_positions = range(2,len(categories)+2)  # x축 위치 (0, 1, 2, 3)

# plt.figure()
# plt.scatter(gh_df[column], gh_md_df[0], color="red", label="GH",s=10, marker="D")
# plt.scatter(kosha_df[column], kosha_md_df[0], color="dodgerblue", alpha=0.1, label="KOSHA", s=10)
# plt.title(f"{column} vs MD 거리 산점도",fontdict={'weight': 'bold', 'size' : "20"})
# plt.xlabel(f'{column} 데이터')
# plt.ylabel("MD 거리")
# plt.xticks(x_positions, categories, fontsize=8)
# plt.legend()
# plt.savefig(f"./md_algorithm/data/img/scatter_{column}_1.png")
# plt.show()


print("------------------- GH vs KOSHA 정규화 로그 산점도 그리기 --------------------")