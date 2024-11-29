from sqlalchemy import create_engine, text 
from sqlalchemy.orm import  sessionmaker
from dotenv import load_dotenv
import os
from config.config import config
import pandas as pd


def extract_data(query,columns,session):
   

    result = session.execute(text(query))
    rows = result.fetchall()

    return pd.DataFrame(rows,columns=columns)


def merge(df_a,df_v,df_aq,df_equi):

    df_annonce_ville = pd.merge(df_a, df_v ,left_on= 'city_id' ,right_on= 'id_ville' ,how='left')
    df_annonce_ville_aq = pd.merge(df_annonce_ville, df_aq,left_on= 'id_annonces' ,right_on= 'annonce_id' ,how='left')
    df_annonce_ville_aq_equi = pd.merge(df_annonce_ville_aq, df_equi,left_on= 'equipement_id' ,right_on= 'id_equipement' ,how='left')
    df_annonce_ville_aq_equi['price']=pd.to_numeric(df_annonce_ville_aq_equi['price'])
    return df_annonce_ville_aq_equi.drop(['city_id', 'id_ville','annonce_id', 'equipement_id', 'id_equipement'],axis=1)




def data(session):
    

    df_annonces = extract_data(config.queries_annonce,config.column_annonce,session)
    df_villes = extract_data(config.queries_ville,config.column_ville,session)
    df_equipements = extract_data(config.queries_equipement,config.column_equipement,session)
    df_aq = extract_data(config.queries_aq,config.column_aq,session)

    #print(df_annonces.head(5),df_aq,df_equipements,df_villes)
    return merge(df_annonces,df_villes,df_aq,df_equipements)



    

    
   
    
    















