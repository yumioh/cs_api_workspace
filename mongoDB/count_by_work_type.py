import pandas as pd

# 데이터 로드
csi_work_type = pd.read_excel('./mongoDB/data/사고비사고데이터 공종별_항목정리.xlsx', sheet_name="CSI 공종항목")
riskzero_type = pd.read_excel('./mongoDB/data/사고비사고데이터 공종별_항목정리.xlsx', sheet_name="리스크제로 공종별항목")

def export_work_type(df, work_type, task_name, sheet_name) :
    df = df[[work_type, task_name]]
    print(df.head())
    
    df1 = pd.DataFrame(df[work_type].value_counts().to_dict().items(), columns=["공종", "갯수"])
    df2 = pd.DataFrame(df[task_name].value_counts().to_dict().items(), columns=["작업명", "갯수"])
    print(df1.head())
    print(df2.head())
    
    merged_df = pd.concat([df1, df2], axis=1)
    print(merged_df.head())
    merged_df.to_excel("./mongoDB/data/count_by_work_type.xlsx", index=False, sheet_name=sheet_name)
    
    
export_work_type(csi_work_type,"공종-대분류", "공종-중분류", "csi_work_type")
