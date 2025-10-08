def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','region','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally["total"]=medal_tally["Gold"]+medal_tally["Bronze"]+medal_tally["Silver"]
    medal_tally["Gold"]=medal_tally["Gold"].astype(int)
    medal_tally["Silver"]=medal_tally["Silver"].astype(int)
    medal_tally["Bronze"]=medal_tally["Bronze"].astype(int)
    return medal_tally

def year_country_list(df):
    year= df["Year"].unique().tolist()
    year.sort()
    year.insert(0,'overall')
    country= df["region"].dropna().unique().tolist()
    country.sort()
    country.insert(0,'overall')
    return year, country

def fetch_tadal_tally(df,year, country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','region','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if country=="overall" and year=="overall":
        md=medal_df
    if country!="overall" and year=="overall":
        md=medal_df[medal_df["region"]==country]
    if country=="overall" and year!="overall":
        flag=1
        md=medal_df[medal_df["Year"]==(year)]
    if country!="overall" and year!="overall":
        md = medal_df[(medal_df["region"] == country) & (medal_df["Year"] == int(year))]
    if flag==1:
             x=md.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    else:
             x=md.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x["total"]=x["Gold"]+x["Bronze"]+x["Silver"]

    x["Gold"]=x["Gold"].astype(int)
    x["Silver"]=x["Silver"].astype(int)
    x["Bronze"]=x["Bronze"].astype(int)
    return x


def nation_over_time(df,col):
         nation_over_year=df.drop_duplicates(["Year",col])["Year"].value_counts().reset_index().sort_values("Year")
         nation_over_year = nation_over_year.rename(columns={"count": col})
         return nation_over_year


def most_successfull(df, Sport):
    # Drop rows without medals
    tem_df = df.dropna(subset=['Medal'])
    
    # Filter by sport if not Overall
    if Sport != "Overall":
        tem_df = tem_df[tem_df["Sport"] == Sport]   # ✅ make sure column name is "Sport"
    
    # Count medals per athlete
    top = (
        tem_df["Name"]
        .value_counts()
        .reset_index()
        .rename(columns={"Name": "Name", "count": "Medals"})   # rename count → Medals
        .head(15)
    )
    
    # Merge with original df to add Sport & region info
    x = (
        top.merge(df, on="Name", how="left")[["Name", "Medals", "Sport", "region"]]
        .drop_duplicates("Name")
    )
    
    return x

def country_wise_medal_tally(df, region ):
     tempdf=df.dropna(subset=['Medal'])
     tempdf.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
     x_file=tempdf[tempdf['region']==region]
     a=x_file.groupby('Year').count()['Medal'].reset_index()
     return a
def country_wise_heatmap(df, region ):
     tempdf=df.dropna(subset=['Medal'])
     tempdf.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
     x_file=tempdf[tempdf['region']==region]
     pvt= x_file.pivot_table(index='Sport',columns="Year",values='Medal',aggfunc='count')
     return pvt


     # top 10 atheletes from region region
def most_successfull_countrywise(df, country):
    # Drop rows without medals
    tem_df = df.dropna(subset=['Medal'])



    
    # Filter by sport if not Overall
   
    tem_df = tem_df[tem_df["region"]== country]  # ✅ make sure column name is "Sport"
    
    # Count medals per athlete
    top = (
        tem_df["Name"]
        .value_counts()
        .reset_index()
        .rename(columns={"Name": "Name", "count": "Medals"})   # rename count → Medals
        .head(10)
    )
    
    # Merge with original df to add Sport & region info
    x = (
        top.merge(df, on="Name", how="left")[["Name", "Medals", "Sport"]]
        .drop_duplicates("Name")
    )
    
    return x


def weight_height(df,sports):
     athelete_df = df.drop_duplicates(subset=['Name', 'region'])
     athelete_df['Medal'].fillna("No Medal",inplace=True)
     if sports!="Overall":
       temp_df=athelete_df[athelete_df['Sport']==sports]
       return temp_df
     else:
       return  athelete_df
     


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final