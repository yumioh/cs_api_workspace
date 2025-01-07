import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
# plt.rcParams['boxplot.flierprops.markersize'] = 3

print("-------------------사고 vs 비사고 MD boxplot --------------------")  

accident_md = pd.read_csv("./md_algorithm_mongo/data/accident_md.csv", header = None)
non_accident_md = pd.read_csv("./md_algorithm_mongo/data/non_accident_md.csv", header = None)
#print(accident_md.head())

plt.boxplot([accident_md[0].tolist(), non_accident_md[0].tolist()]) 
plt.title(f'GH vs KOSHA MD', fontdict={'weight': 'bold', 'size' : "20"}) #제목 및 라벨 설정
plt.ylabel('Values')
plt.xticks([1, 2], ['accident', 'non_accident']) 
plt.savefig(f"./md_algorithm_mongo/data/img/MD_boxplot.png")
#plt.show()

print("-------------------사고 vs 비사고 MD 정규화 boxplot --------------------")  

accident_md = pd.read_csv("./md_algorithm_mongo/data/accident_normalized.csv")
non_accident_md = pd.read_csv("./md_algorithm_mongo/data/non_accident_normalized.csv")
print(accident_md.head())

# plt.boxplot([accident_md["normalized"].tolist(), non_accident_md["normalized"].tolist()]) 
# plt.title(f'GH vs KOSHA MD', fontdict={'weight': 'bold', 'size' : "20"}) #제목 및 라벨 설정
# plt.ylabel('Values')
# plt.xticks([1, 2], ['accident', 'non_accident']) 
# plt.savefig(f"./md_algorithm_mongo/data/img/MD_normalized_boxplot.png")
#plt.show()

print("-------------------사고 vs 비사고 MD 정규화 산점도--------------------")  

arranged_accident = accident_md["normalized"].sort_values().reset_index(drop=True)
arranged_non_accident = non_accident_md["normalized"].sort_values().reset_index(drop=True)

plt.scatter(arranged_accident.index, arranged_accident, color="dodgerblue", label="accident",s=8)
plt.scatter(arranged_non_accident.index, arranged_non_accident, color="orange", alpha=0.4, label="non_accident", s=8)
plt.title(f"사고 vs 비사고 정규화된 MD값 산점도",fontdict={'weight': 'bold', 'size' : "20"})
plt.xlabel("Index")
plt.ylabel("MD")
plt.grid(True)
plt.legend()
plt.savefig(f"./md_algorithm_mongo/data/img/scatter_md_normalized.png")
plt.show()


print("-------------------사고 vs 비사고 log(MD) 산점도--------------------")  

accident_log = pd.read_csv("./md_algorithm_mongo/data/accident_log.csv", header = None)
non_accident_log = pd.read_csv("./md_algorithm_mongo/data/non_accident_log.csv", header = None)


arranged_accident_log = accident_log[0].sort_values().reset_index(drop=True)
arranged_non_accident_log = non_accident_log[0].sort_values().reset_index(drop=True)

plt.scatter(arranged_accident_log.index, arranged_accident_log, color="dodgerblue", label="GH",s=8)
plt.scatter(arranged_non_accident_log.index, arranged_non_accident_log, color="red", alpha=0.4, label="KOSHA", s=8)
plt.title(f"사고 vs 비사고 log(MD)값 산점도",fontdict={'weight': 'bold', 'size' : "20"})
plt.xlabel("Index")
plt.ylabel("MD")
plt.grid(True)
plt.legend()
plt.savefig(f"./md_algorithm_mongo/data/img/scatter_logmd_normalized.png")
plt.show()