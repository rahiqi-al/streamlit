import streamlit as st
from extract_data import data
from config.config import config
from components import * 
from graph import *
from extract_orm import extract_orm
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,relationship, sessionmaker 


def app():
    st.set_page_config(page_title='AVITO DASHBOARD')

    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; ">
        <h1 style="text-align: center;">Real Estate Dashboard: Interactive Data Exploration and Analysis for Avito Listings</h1>
    </div>
    """, unsafe_allow_html=True)


    engine=create_engine(config.database_url)
    Base = declarative_base()
    Session=sessionmaker(bind=engine)
    session=Session()

    df=data(session)


    #print(df)
    #print(df.info())

    min_price,max_price,min_rooms,max_rooms,min_baths,max_bath,ville,equipements,start_date,end_date = sidebar_creation(df)


    
    choice = st.selectbox('Explore and Filter Data',['show original data','filter  original data'])
    if st.button('show' if choice== 'show original data' else 'filter  original data') :
        if choice == 'show original data':

            show_df(df,config.describe_array,'non filtered df')

            st.subheader("Chart of Number of annonces per City : ")
            bar(df)

            #st.subheader("Property Locations on Map :")
            #map(df)

            st.subheader("Chart of Price Distribution :")
            chart_price_distribution(df)

            #st.subheader("Chart of Price Range by City :")
            #chart_price_range_by_city(df)

            st.subheader("Chart of Equipment Distribution :")
            chart_equipement_distribution(df)

            st.subheader("Chart of average Rooms and Bathrooms per City :")
            chart_averege_rooms_baths_city(df)

            st.subheader("Chart of anoonces Over Time :")
            chart_annonces_over_time(df)

            st.subheader("Chart of Surface Area vs Price :")
            chart_of_surface_erea_vs_price(df)



        else:
            filtered_df = extract_orm(session,Base,engine,min_price,max_price,min_rooms,max_rooms,min_baths,max_bath,ville,equipements,start_date,end_date)
            
            #filtered_df = df[(df['price']>=min_price)&(df['price']<=max_price)&(df['nb_rooms']>=min_rooms)&(df['nb_rooms']<=max_rooms)&(df['nb_baths']>=min_baths) &(df['nb_baths']<=max_bath)&(df['datetime'].dt.date>=start_date)&(df['datetime'].dt.date<=end_date)&(df['ville_name']==ville)&(df['equipement_name'].isin(equipements) | (len(equipements) == 0))]"""
            
            

            show_df(filtered_df,config.describe_array,'filtred df')

            st.subheader("Chart of Number of annonces per City :")
            chart_number_annoonces_city(filtered_df)

            st.subheader("Property Locations on Map :")
            chart_propety_location_on_map(filtered_df)

            st.subheader("Chart of Price Distribution :")
            chart_price_distribution(df)

            st.subheader("Chart of Price Range by City :")
            chart_price_range_by_city(filtered_df)

            st.subheader("Chart of Equipment Distribution :" )
            chart_equipement_distribution(filtered_df)

            st.subheader("Chart of average Rooms and Bathrooms per City :")
            chart_averege_rooms_baths_city(filtered_df)

            st.subheader("Chart of anoonces Over Time :")
            chart_annonces_over_time(filtered_df)

            st.subheader("Chart of Surface Area vs Price :")
            chart_of_surface_erea_vs_price(filtered_df)



    else:
        st.write('waiting for your choice....')




if  __name__=='__main__':
    app()
