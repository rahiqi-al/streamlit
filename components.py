import streamlit as st
from extract_data import data
from config.config import config





def download_file(df,name):
    csv=df.to_csv(index=False)
    st.download_button(label='download csv',data=csv,file_name=name,mime='text/csv')

def sidebar_creation(df):
    st.sidebar.title('Filter the dataframe')
    min_price,max_price = st.sidebar.slider('prix',min_value=df['price'].min(),max_value=df['price'].max(),step=4,value=(df['price'].min(),df['price'].max()))
    min_rooms,max_rooms = st.sidebar.slider('nb rooms',min_value=df['nb_rooms'].min(),max_value=df['nb_rooms'].max(),value=(df['nb_rooms'].min(),df['nb_rooms'].max()))
    min_baths,max_bath = st.sidebar.slider('nb bath',min_value=df['nb_baths'].min(),max_value=df['nb_baths'].max(),value=(df['nb_baths'].min(),df['nb_baths'].max()))
    ville = st.sidebar.selectbox('ville',df['ville_name'].unique())
    equipements =st.sidebar.multiselect('equipements',df['equipement_name'].unique())
    start_date = st.sidebar.date_input('start date',min_value=df['datetime'].min(),max_value=df['datetime'].max(),value=df['datetime'].min())
    end_date = st.sidebar.date_input('end date',min_value=df['datetime'].min(),max_value=df['datetime'].max())

    return min_price,max_price,min_rooms,max_rooms,min_baths,max_bath,ville,equipements,start_date,end_date
    
def show_df(df,array,prompt):
    df = (df.groupby('link').apply(lambda group:group.drop_duplicates(subset='title'))).reset_index(drop=True)
    st.dataframe(df)
    st.subheader('Real Estate Listings Data Overview :')
    st.dataframe(df[array].describe())
    download_file(df, prompt)
