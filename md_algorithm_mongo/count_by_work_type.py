import pandas as pd

data = pd.ExcelFile('./md_algorithm_mongo/data/사고비사고데이터 공종별_항목정리.xlsx')
print(data.sheet_names)

# with pd.ExcelWriter("./md_algorithm_mongo/data/count_by_work_type.xlsx") as writer:
#     for sheet_name in data.sheet_names:
#         df = pd.read_excel('./md_algorithm_mongo/data/사고비사고데이터 공종별_항목정리.xlsx', sheet_name=sheet_name)
#         df = df[["공종","작업명"]]
#         print(df.head())
        
#         df1 = pd.DataFrame(df["공종"].value_counts().to_dict().items(), columns=["공종", "갯수"])
#         df2 = pd.DataFrame(df["작업명"].value_counts().to_dict().items(), columns=["작업명", "갯수"])
#         print(df1.head())
#         print(df2.head())
        
#         merged_df = pd.concat([df1, df2], axis=1)
#         print(merged_df.head())

#         merged_df.to_excel(writer, sheet_name=sheet_name, index=False)
    
#     print("Done")

df = pd.read_excel('./md_algorithm_mongo/data/사고비사고데이터 공종별_항목정리.xlsx', sheet_name="CSI 공종항목")
df = df[["공종","작업명"]]
print(df.head())

with pd.ExcelWriter("./md_algorithm_mongo/data/count_by_csi_work_type.xlsx") as writer:
    for work_type in df["공종"].unique():
        filterd_df = df[df["공종"] == work_type]
        #공종 작업명으로 개수 구하기 
        result_df = filterd_df.groupby(["공종","작업명"]).size().reset_index(name="개수")
        # 총합계 행 추가
        total_sum = result_df["개수"].sum()
        total_row = pd.DataFrame([{"공종": "", "작업명": "총합계", "개수": total_sum}])
        result_df = pd.concat([result_df, total_row], ignore_index=True)
        
        result_df.to_excel(writer, sheet_name=work_type, index=False)
    
    print("Done")

