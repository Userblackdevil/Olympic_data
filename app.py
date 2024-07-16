import plotly.figure_factory as ff
import streamlit as st
import pandas as pd
import numpy as np
import preprocessor,helper 
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import scipy

def add_local_background_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Path to your local background image
background_image_path = 'Olympic.jpg'

# Add background image
add_local_background_image(background_image_path)
df=pd.read_csv('athlete_events.csv')
region_df=pd.read_csv('noc_regions.csv')
df=preprocessor.preprocess(df,region_df)
st.sidebar.image('Olympic_1.jpg')
st.sidebar.header('Olympics Analysis')
user_menu=st.sidebar.radio('Select an Option',('Medal Tally','OverAll Analysis','Country-wise Analysis','Athlete wise analysis'))

# st.dataframe(df)
if user_menu =='Medal Tally':
    st.sidebar.header('Medal Tally')
    years,country=helper.country_year_list(df)
    Selected_year=st.sidebar.selectbox('Select Year',years)
    Selected_country=st.sidebar.selectbox('Select Country',country)
    medal_tally=helper.fetch_medal_tally(df,Selected_year,Selected_country) 
    if Selected_year=='OverAll' and Selected_country=='OverAll':
        st.title('OverAll Tally')
    if Selected_year !='OverAll' and Selected_country=='OverAll':
        st.title('Medal Tally'+str(Selected_year)+'Olympics')
    if Selected_year =='OverAll' and Selected_country !='OverAll':
        st.title('OverAll Performance of'+ ' '+Selected_country)
    if Selected_year != 'OverAll' and Selected_country!='OverAll':
        st.title('Performance of'+' '+Selected_country+' '+'in'+' '+str(Selected_year)+' '+'Olympics')
    st.table(medal_tally)

if user_menu == 'OverAll Analysis':
    editions=df['Year'].unique().shape[0]-1
    cities=df['City'].unique().shape[0]
    sports=df['Sport'].unique().shape[0]
    events=df['Event'].unique().shape[0]
    athletes=df['Name'].unique().shape[0]
    nations=df['region'].unique().shape[0]
    st.title('Top Statistics of Olympic')
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Edition')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)
    nations_over_time=helper.data_over_time(df,'region')
    # nations_over_time.rename(columns={'Edition':'Year','region':'No. of nations'})
    fig=px.line(nations_over_time,x='Edition',y='region')
    st.title('Participation of Nations over the Years')
    st.plotly_chart(fig)

    Events_over_time=helper.data_over_time(df,'Event')
    # Events_over_time.rename(columns={'Edition':'Year','Event':'No. of Games'},inplace=True)
    fig=px.line(Events_over_time,x='Edition',y='Event')
    st.title('No. of Games over the Years')
    st.plotly_chart(fig)
    athlete_over_time=helper.data_over_time(df,'Name')
    # athlete_over_time.rename(columns={'Edition':'Year','Name':'No. of Athletes'},inplace=True)
    fig=px.line(athlete_over_time,x='Edition',y='Name')
    st.title('No. of Atheletes over the Years')
    st.plotly_chart(fig)
    st.title('No. of Events Over time(Every Sports)')
    fig,ax=plt.subplots(figsize=(40,40))
    x=df.drop_duplicates(['Year','Sport','Event'])
    x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int)
    ax=sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)
    st.title('Most Successful Athletes')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'OverAll')
    selected_sport=st.selectbox('Select a Sport',sport_list)
    x=helper.most_successful(df,selected_sport)
    st.table(x)
if user_menu=='Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')
    country_list=df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox("Select a Country",country_list)
    yearwise=helper.yearwise_medal_tally(df,selected_country)
    fig=px.line(yearwise,x='Year',y='Medal')
    st.title(selected_country+' '+'Medal Tally Over Years')
    st.plotly_chart(fig)
    st.title(selected_country+' '+'Excel in the following Sports')
    pt=helper.country_event_heatmap(df,selected_country)
    fig,ax=plt.subplots(figsize=(30,30))
    ax=sns.heatmap(pt,annot=True)
    st.pyplot(fig)
    st.title("Top 10 Athletes of "+selected_country)
    top_athletes=helper.most_successful_athletes(df,selected_country)
    st.table(top_athletes)

if user_menu == 'Athlete wise analysis':
    athletes_df=df.drop_duplicates(subset=['Name','region'])
    x=athletes_df['Age'].dropna()
    x1=athletes_df[athletes_df['Medal']=='Gold']['Age'].dropna()
    x2=athletes_df[athletes_df['Medal']=='Silver']['Age'].dropna()
    x3=athletes_df[athletes_df['Medal']=='Bronze']['Age'].dropna()
    fig=ff.create_distplot([x,x1,x2,x3],['OverAll Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    # fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)
    famous_sports=['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
       'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
       'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
       'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Equestrianism',
       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
       'Tennis', 'Modern Pentathlon', 'Golf', 'Softball', 'Archery',
       'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
       'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining',
       'Beach Volleyball', 'Triathlon', 'Rugby', 'Lacrosse', 'Polo',
       'Cricket', 'Ice Hockey', 'Racquets', 'Motorboating', 'Croquet',
       'Figure Skating', 'Jeu De Paume', 'Roque', 'Basque Pelota',
       'Alpinism', 'Aeronautics']
    x = []
    name = []

    for sport in famous_sports:
        temp_df = athletes_df[athletes_df['Sport'] == sport]
        gold_medalist_ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        
        if len(gold_medalist_ages) > 1 and np.var(gold_medalist_ages) > 0:  # Check for sufficient data points and variance
            x.append(gold_medalist_ages)
            name.append(sport)

    if x:  # Ensure x is not empty before creating the plot
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False,width=800,height=500)
        st.title('Distribution of Age with respect to Sports and Gold Medalists')
        st.plotly_chart(fig)
    else:
        print("No data available to create the distribution plot.")
    st.title('Height VS Weight')
    sport_list=df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'OverAll')
    selected_sport=st.selectbox('Select a Sport',sport_list)
    temp_df=helper.weight_height(df,selected_sport)
    fig,ax=plt.subplots()
    ax=sns.scatterplot(data=temp_df,x='Weight',y='Height',hue='Medal',style='Sex',s=80)
   
    st.pyplot(fig)
    st.title('Men VS Women Participation over the Years')
    final=helper.men_women(df)
    fig=px.line(final,x='Year',y=['Male','Female'])
    st.plotly_chart(fig)