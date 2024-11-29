import yaml
import os
from dotenv import load_dotenv


load_dotenv()

class config():

    with open('config/config.yml','r') as file :
        config_data=yaml.load(file , Loader=yaml.FullLoader)
    

    queries_annonce =config_data['QUERIES']['table_anoonces']
    queries_ville =config_data['QUERIES']['table_villes']
    queries_aq =config_data['QUERIES']['table_annonce_equipement']
    queries_equipement =config_data['QUERIES']['table_equipements']

    column_annonce =config_data['COLUMNS']['columns_annonces']
    column_ville =config_data['COLUMNS']['columns_villes']
    column_aq =config_data['COLUMNS']['columns_annonce_equipement']
    column_equipement =config_data['COLUMNS']['columns_equipement']
    describe_array =config_data['COLUMNS']['describe_array']



    database_url= os.getenv('DATABASE_URL')


config=config()






