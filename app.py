import streamlit as  st
import pandas as pd 
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
# Load your dataframes first
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')


# Pass the DataFrames, not strings
df = preprocessor.preprocess(df, region_df)
st.sidebar.title("Olympic Data Analysis")
st.sidebar.image(r"pngwing.com (1).png")

user_menu=st.sidebar.radio(
    'Select An Option',('Medal Tally','Overall Analysis','Country-wise Analysis'
,'Athlete-Wise Analysis')

)


if user_menu=="Medal Tally":
   st.sidebar.header("Medal Tally")
   
   year, country= helper.year_country_list(df)
   selected_year=st.sidebar.selectbox("YEAR",year)
   selected_country=st.sidebar.selectbox("COUNTRY",country)
   medal_tally=helper.fetch_tadal_tally(df,selected_year,selected_country)
   if selected_country=="overall" and selected_year=="overall":
      st.title("Overall Tally")
   if selected_country=="overall" and selected_year!="overall":
      st.title("Over All Performce In Year " + str(selected_year))
   if selected_country!="overall" and selected_year=="overall":
      st.title(str(selected_country + " Over All Performace"))
   if selected_country!="overall" and selected_year!="overall":
      st.title(str(selected_country)+ " Over All Performce In Year "+ str(selected_year))
   st.table(medal_tally)
if user_menu=="Overall Analysis":
   editions= df["Year"].unique().shape[0]-1
   cities= df["City"].unique().shape[0]
   sports=df["Sport"].unique().shape[0]
   events=df["Event"].unique().shape[0]
   athelets=df["Name"].unique().shape[0]
   nation=df["region"].unique().shape[0]
     


   st.title("Top Statistics")
   col1,col2,col3 = st.columns(3)

   with col1:
      st.subheader("Editions")
      st.title(editions)
   with col2:
      st.subheader("Cities")
      st.title(cities)
   with col3:
      st.subheader("Sports")
      st.title(sports)
   col1,col2,col3 = st.columns(3)
   with col1:
      st.subheader("Events")
      st.title(events)

   with col3:
      st.subheader("Atheletes")
      st.title(athelets)
   with col2:
      st.subheader("Nations")
      st.title(nation)
 
   n_o_v= helper.nation_over_time(df, "region")
   fig = px.line(n_o_v, x="Year", y="region")
   st.title("Participating Countries Over The Years")
   st.plotly_chart(fig)

   E_o_v= helper.nation_over_time(df, "Event")
   fig = px.line(E_o_v, x="Year", y="Event")
   st.title("Events Over The Years")
   st.plotly_chart(fig)

   A_o_v= helper.nation_over_time(df, "Name")
   fig = px.line(A_o_v, x="Year", y="Name")
   st.title("Athelets Over The Years")
   st.plotly_chart(fig)

   st.title("Numbers Of Events Over Time")
   fig, ax = plt.subplots(figsize=(20, 20),facecolor="#494848")

   x=df.drop_duplicates(["Year","Event","Sport"])
   ax=sns.heatmap(x.pivot_table(index="Sport",columns="Year",values="Event", aggfunc='count').fillna(0).astype("int32"),annot=True)
   ax.tick_params(axis='x', colors='white')
   ax.tick_params(axis='y', colors='white')

   st.pyplot(fig)


   st.title("Top Most Athelets")
   
   sprt=df["Sport"].dropna().unique().tolist()
   sprt.sort()
   sprt.insert(0,"Overall")
   selected_sport=st.selectbox("Sports Person",sprt)
   x=helper. most_successfull(df,selected_sport)
   st.table(x)


if user_menu=="Country-wise Analysis":
   st.sidebar.title("Country-wise Analysis")
   country_list=df['region'].dropna().unique().tolist()
   country_list.sort()
   selected_country=st.sidebar.selectbox("Country",country_list)
   c_w_a=helper.country_wise_medal_tally(df,selected_country)
   st.title(selected_country + ' Medal Tally Over The Year')
   if c_w_a.empty:
    st.warning(f"No medal data available for {selected_country}.")
   else:
    fig = px.line(c_w_a, x="Year", y="Medal")

    
    st.plotly_chart(fig)

#heatmap
   
   country_list=df['region'].dropna().unique().tolist()
   
   st.title(selected_country + " Excel In The Following Sports")
   pt=helper.country_wise_heatmap(df,selected_country)
   if pt.empty:
    st.warning(f"No medal data available for {selected_country}.")
   else:
    
    fig, ax = plt.subplots(figsize=(20, 20),facecolor="#494848")
    ax=sns.heatmap(pt.fillna(0),annot=True)
    ax.tick_params(axis='x', colors='white',labelsize=18)
    ax.tick_params(axis='y', colors='white',labelsize=18)

    st.pyplot(fig)

    st.title("Top 10 Atheletes Of "+selected_country)
    top10= helper.most_successfull_countrywise(df,selected_country)
    st.table(top10)

if user_menu == 'Athlete-Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)




    st.title('Height vs Weight')
    sprt=df["Sport"].dropna().unique().tolist()
    sprt.sort()
    sprt.insert(0,"Overall")
    selected_sport=st.selectbox("Sports",sprt)
    temp_df=helper.weight_height(df,selected_sport)
    
    fig, ax = plt.subplots()
    
    ax=sns.scatterplot(data=temp_df,x='Weight',y='Height',hue=temp_df['Medal'],style=temp_df["Sex"],s=100)
    st.pyplot(fig)




    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
