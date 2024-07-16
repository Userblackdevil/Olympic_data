import numpy as np
def fetch_medal_tally(new_df,years,country):
    medal_df=new_df.drop_duplicates(subset=['Team','NOC','Games','City','Year','Sport','Event','Medal'])
    flag=0
    if years=='OverAll' and country=='OverAll':
        temp_df=medal_df
    if years=='OverAll' and country !='OverAll':
        flag=1
        temp_df=medal_df[medal_df['region']==country]
    if years !='OverAll' and country =='OverAll':
        temp_df=medal_df[medal_df['Year']== int(years)]
    if years !='OverAll' and country != 'OverAll':
        temp_df=medal_df[(medal_df['Year']==years) & (medal_df['region']==country)]
    if flag==1:
        x=temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x=temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
        
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

def medal_tally(new_df):
    medal_tally=new_df.drop_duplicates(subset=['Team','NOC','Games','City','Year','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    return medal_tally


def country_year_list(new_df):
    years=new_df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'OverAll')

    country=np.unique(new_df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'OverAll')
    return years,country
def data_over_time(new_df,col):
    nations_over_time=new_df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year':'Edition','count':col},inplace=True)
    return nations_over_time
def most_successful(new_df,Sport):
    temp_df=new_df.dropna(subset=['Medal'])
    if Sport !='OverAll':
        
        temp_df=temp_df[temp_df['Sport']==Sport]
        
    x=temp_df['Name'].value_counts().reset_index().head(15).merge(new_df,left_on='Name',right_on='Name',how='left')[['Name','count','region','Sport']].drop_duplicates('Name')
    x.rename(columns={'Name':'Name','count':'Medals'},inplace=True)
    return x
    
def yearwise_medal_tally(new_df,country):
    temp_df=new_df.dropna(subset='Medal')
    temp_df.drop_duplicates(subset=['Team','Games','NOC','Year','City','Sport','Event','Medal'],inplace=True)
    p_df=temp_df[temp_df['region']==country]
    final_df=p_df.groupby('Year').count()['Medal'].reset_index()
    return final_df
def country_event_heatmap(new_df,country):
    temp_df=new_df.dropna(subset='Medal')
    temp_df.drop_duplicates(subset=['Team','Games','NOC','Year','City','Sport','Event','Medal'],inplace=True)
    p_df=temp_df[temp_df['region']==country]
    pt=p_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype(int)
    return pt
def most_successful_athletes(new_df,country):
    temp_df=new_df.dropna(subset=['Medal'])
  
        
    temp_df=temp_df[temp_df['region']==country]
        
    x=temp_df['Name'].value_counts().reset_index().head(10).merge(new_df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport']].drop_duplicates('Name')
    x.rename(columns={'Name':'Name','count':'Medals'},inplace=True)
    return x
def weight_height(new_df,sport):
    athletes_df=new_df.drop_duplicates(subset=['Name','region'])
    athletes_df['Medal'].fillna('No medal',inplace=True)
    if sport !='OverAll':
        temp_df=athletes_df[athletes_df['Sport']==sport]
        return temp_df
    else:
        return athletes_df
def men_women(new_df):
    athletes_df=new_df.drop_duplicates(subset=['Name','region'])
    men=athletes_df[athletes_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women=athletes_df[athletes_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()
    final=men.merge(women,on='Year')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    return final
