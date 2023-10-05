import pandas as pd
import pandas_datareader.data as pdr
import streamlit as st
import locale
import plotly.express as px
import plotly as pl
import openai
import requests
import json
from streamlit_extras.metric_cards import style_metric_cards



#load dataframe
@st.cache_data
def load_data() -> pd.DataFrame:
    dataframe = pd.read_csv("movies.csv")
    dataframe.rename(
        columns={
            'revenue':'Box Office', 
            'title':'Title',
            'genres':'Gender',
            'original_language':'Language',
            'overview':'Overview',
            'popularity':'Popularity',
            'production_companies':'Production Companies',
            'release_date':'Release Date',
            'budget':'Budget',
            'runtime':'Runtime',
            'tagline':'Tagline',
            'vote_average':'Vote Average',
            'vote_count':'Vote Count',
            }, 
            inplace = True)
    
    dataframe['Balance'] = dataframe['Box Office'] - dataframe['Budget']

    dataframe.fillna('',inplace=True)
    null_value=dataframe[(dataframe['Gender']=='') & (dataframe['Overview']=='')].index
    dataframe.drop(null_value,inplace=True)

    # delete all the duplicated rows
    dataframe.isnull().sum()
    dataframe.drop_duplicates(inplace=True)

    # ignore repeated movies
    dataframe[['Title','Release Date']].duplicated().sum()
    dataframe.drop_duplicates(subset=['Title','Release Date'],inplace=True)

    # considering genres and overviews as the key predict, we fill up the null value
    dataframe.fillna('',inplace=True)
    null_value=dataframe[(dataframe['Gender']=='') & (dataframe['Overview']=='')].index
    dataframe.drop(null_value,inplace=True)
    dataframe['Gender']=dataframe['Gender'].apply(lambda i:' '.join(i.split('-'))) #remove "-"
    dataframe['Production Companies']=dataframe['Production Companies'].apply(lambda i:' '.join(i.split('-'))) #remove "-"

    return dataframe.head(200)

def build_where_clause(filter_results: dict) -> str:
    clause_list = list()
    for column in FILTER_LIST:
        if filter_results[column] != []:
            clause_list.append(f"`{column}` in {filter_results[column]}")
    
    clause_treated = str(clause_list) \
                        .replace('", "',' & ')[1:-1] \
                        .replace('[','(') \
                        .replace(']',')')
    return clause_treated

def set_sidebar(
    
    dataframe: pd.DataFrame = None, 
    filtered: pd.DataFrame = None) -> dict:

    st.sidebar.title("Filter Select: ")
        
    if filtered is None:
        df = dataframe
    else:
        df = filtered
    filter_results = dict()
    for i, name in enumerate(FILTER_LIST):
        component = st.sidebar.multiselect(
            key=i,
            label=name,
            options=df[name].unique(),
            help=f"Select a {name}"
        )
        filter_results.update({str(name) : component})


    return filter_results



def build_visualizations(dataframe: pd.DataFrame):
    col1, col2,  = st.columns([4,1])
    with col1:
        st.header(":bar_chart: Movies")
    
        
    #KPI´S
    total_movies = len(dataframe["Title"].unique())
    total_genres = len(dataframe["Gender"].unique())
    vote_average = round(dataframe["Vote Average"].mean(),2)
    total_budget = (
        float(round(dataframe['Budget'].sum()))
    )
    total_box_office = (
        float(round(dataframe['Box Office'].sum()))
    )
    total_balance = (
        dataframe.groupby("Title").head(10)
    )


    col1, col2, col3 = st.columns(3)
    locale.setlocale(locale.LC_MONETARY, 'en_US.UTF-8')
    col1.metric(
        label="Movies Total",
        value=total_movies, 
        )
    col2.metric(
        label="Total Genres", 
        value=total_genres, 
        )
    col3.metric(
        label="Total Budgets", 
        value=f"{locale.currency( total_budget, grouping=True)}",
        )
    style_metric_cards()

    col1, col2, col3 = st.columns(3)
    balance=float(total_box_office - total_budget)

    col1.metric(
        label="Total Box Office",
        value=f"{locale.currency( total_box_office,grouping=True)}",
        )
    col2.metric(
        label="Balance",
        value=f"{locale.currency(balance,grouping=True)}",
        )
    col3.metric(
        label="Vote Average",
        value=vote_average,
        )
    
#graphs
    fig_total_budget = px.bar(
        total_balance.head(10),
        x='Budget',
        y="Title",
        color='Title'
    )
    fig_total_box_office = px.area(
        dataframe.head(10),
        y='Box Office',
        x='Gender',
        color='Gender'
        
    )
    fig_votes = px.scatter(
        dataframe.head(20),
        y='Vote Count',
        x='Vote Average',
        color='Title',
        size='Vote Count'
    )
    fig_title_gen = px.treemap(
        dataframe.head(200),
        path=['Title'],
        values="Balance"
    )



    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(fig_total_budget)
    with coluna2:    
        st.plotly_chart(fig_total_box_office)

    coluna1, coluna2 = st.columns(2)
    with coluna1:
        st.plotly_chart(fig_votes)
    with coluna2:    
        st.plotly_chart(fig_title_gen)


    st.dataframe(dataframe.head(20))
    
def hide_syle():
    style = """
        <style>
            #MainMenu {visibility: ;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)


def main(dataframe):
    
    filter_results = set_sidebar(dataframe=dataframe)
    # print("STATE HERE", filter_results)
    filter_pattern = build_where_clause(filter_results=filter_results)
    # print("FILTER PATTERN", filter_pattern)
    df_selection = dataframe.query(
        expr=eval(filter_pattern),
        engine='python'
    ) if filter_pattern else dataframe
    
    build_visualizations(dataframe=df_selection)
    #hide_syle()

if __name__ == "__main__":
    st.set_page_config(
        page_title="Movie Analytics", 
        page_icon=":bar_chart:",
        layout="wide"
    )

    FILTER_LIST = ["Gender","Production Companies"]

    dataframe = load_data()
    main(dataframe=dataframe)