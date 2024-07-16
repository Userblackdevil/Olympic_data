import pandas as pd


def preprocess(df, region_df): 
    #filtering for summer olympics
    df=df[df['Season']=='Summer']
    df=df.merge(region_df,on='NOC',how='left')
    df.drop_duplicates(inplace=True)
    df=pd.concat([df,pd.get_dummies(df['Medal'],dtype=int)],axis=1)
    return df
    # df_trans=df.T
    # df_trans.drop_duplicates(inplace=True)
    # new_df=df_trans.T
    # return new_df
    duplicate_columns = df.columns[df.columns.duplicated()]
    new_df = df.drop(columns=duplicate_columns,inplace=True)
    return new_df
   