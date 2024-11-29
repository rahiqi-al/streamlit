import pandas as pd 
import matplotlib.pyplot as plt
from config.config import config
import streamlit as st
import folium
import seaborn as sns
from streamlit_folium import folium_static




def chart_number_annoonces_city(df):

    df = df.groupby('link').apply(lambda group:group.drop_duplicates(subset='title'))
 

    fig, ax = plt.subplots()
    ax.bar(df['ville_name'].value_counts().index, df['ville_name'].value_counts().values, color="skyblue")
    ax.set_title("Nombre d annonces par ville")
    ax.set_xlabel("Ville")
    ax.set_ylabel("Nombre d annonces")
    ax.set_xticklabels(df['ville_name'].value_counts().index, rotation=45)

    st.pyplot(fig)
    

def chart_propety_location_on_map(df):
    df = df.groupby('link').apply(lambda group:group.drop_duplicates(subset='title'))
    df = df['ville_name'].value_counts()
    coords = {
    "ville_name": ["Tanger", "Essaouira", "Casablanca", "Tangiers", "Fès", "Rabat", "Oujda", "Agadir", "Meknès", "Marrakech"],
    "latitude": [35.7595, 31.5125, 33.5731, 35.7595, 34.0331, 34.0209, 34.6814, 30.4278, 33.8935, 31.6295],
    "longitude": [-5.83395, -9.77, -7.5898, -5.83395, -5.0003, -6.8417, -1.9086, -9.5981, -5.5479, -7.9811]} 


    coords_df = pd.DataFrame(coords)

    final_df = pd.merge(df, coords_df, on="ville_name", how="left")

    # Create a map centered at the average latitude and longitude
    map_center = [final_df["latitude"].mean(), final_df["longitude"].mean()]
    map_object = folium.Map(location=map_center, zoom_start=6)

    # Add markers to the map
    for _, row in final_df.iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"{row['ville_name']}: {row['count']} annonces",
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(map_object)

    # Display map in Streamlit
    folium_static(map_object)

    
def chart_price_distribution(df):
    df = df.groupby('link').apply(lambda group:group.drop_duplicates(subset='title'))

    plt.figure(figsize=(15, 6))
    plt.hist(df['price'], bins=10, color='skyblue', edgecolor='black')
    plt.title("Répartition des prix")
    plt.xlabel("Prix")
    plt.ylabel("Fréquence")
    plt.grid(True)

    st.pyplot(plt)


def chart_price_range_by_city(df):
    df = df.groupby('link').apply(lambda group:group.drop_duplicates(subset='title'))
    df = df[['ville_name','price']]
    plt.figure(figsize=(35, 12))
    sns.boxplot(x='ville_name', y='price', data=df, palette='Set2')
    plt.title("Comparaison des gammes de prix par ville")
    plt.xlabel("Ville")
    plt.ylabel("Prix")
    st.pyplot(plt)


def chart_equipement_distribution(df):
    

    # Calculate the frequency of each equipment
    equipement_counts = pd.Series(df['equipement_name'].unique()).value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(equipement_counts, labels=equipement_counts.index, autopct='%1.1f%%', colors=['#66b3ff','#99ff99','#ffcc99','#ff6666'], startangle=90)
    plt.title("Répartition des équipements dans les annonces")

    st.pyplot(plt)


def chart_averege_rooms_baths_city(df):
    df = df.groupby('link').apply(lambda group:group.drop_duplicates(subset='title'))


    df = df[['nb_rooms','nb_baths','ville_name']]

    avg_rooms_bathrooms = df.groupby('ville_name')[['nb_rooms', 'nb_baths']].mean()

    # Plotting the bar chart
    avg_rooms_bathrooms.head(20).plot(kind='bar', figsize=(10, 6), color=['skyblue', 'salmon'])

    # Customize the chart
    plt.title("Nombre moyen de pièces et de salles de bain par ville")
    plt.xlabel("Ville")
    plt.ylabel("Moyenne")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Display the chart in Streamlit
    st.pyplot(plt)

    
def chart_annonces_over_time(df):
    df = df.groupby('link').apply(lambda group:group.drop_duplicates(subset='title'))

    
    df['datetime'] = pd.to_datetime(df['datetime']).dt.strftime('%Y-%m-%d')
    df = df.groupby('datetime').size()

    plt.figure(figsize=(10, 6))
    df.plot(kind='line', color='skyblue', marker='o')

    # Customize the chart
    plt.title("Évolution du nombre d'annonces publiées au fil du temps")
    plt.xlabel("Date")
    plt.ylabel("Nombre d'annonces")

    # Display the chart in Streamlit
    st.pyplot(plt)

    
def chart_of_surface_erea_vs_price(df):
    df = df.groupby('link').apply(lambda group: group.drop_duplicates(subset='title'))

    # Select the relevant columns for plotting
    df = df[['surface_area', 'price']]

    # Create the scatter plot
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.scatter(df['surface_area'], df['price'], color='blue', alpha=0.7)
    ax.set_title('Relation entre Surface et Prix')
    ax.set_xlabel('Surface (m²)')
    ax.set_ylabel('Prix (MAD)')
    ax.grid(True)

    # Display the plot in Streamlit
    st.pyplot(fig)


def map(df):
    df = df['ville_name'].value_counts()
    coords = {
        "ville_name": [
            "Casablanca", "Marrakech", "Tanger", "Agadir", "Rabat", "Temara", "Kénitra", "Mohammedia", "Salé", "El Jadida",
            "Fès", "Tétouan", "Meknès", "Martil", "Bouskoura", "Bouznika", "Urgent", "Saidia", "Had Soualem", "Sidi Rahal",
            "Mdiq", "Dar Bouazza", "Asilah", "Taza", "Sidi Allal El Bahraoui", "Settat", "Skhirat", "Khouribga", "Oued Laou",
            "Béni Mellal", "Tamesna", "Oujda", "Errahma", "Fquih Ben Saleh", "Nouaceur", "Safi", "Essaouira", "Larache",
            "El Mansouria", "Deroua", "Berrechid", "Tiznit", "Berkane", "Mediouna", "Nador", "Abdelghaya Souahel", "Taghazout",
            "Biougra", "Ifrane", "Khemisset", "Fnideq", "El Kelâa des Sraghna", "Sidi Bouknadel", "Tamensourt", "Ain Attig",
            "Al Hoceima", "Benslimane", "Zenata", "Guercif"
        ],
        "latitude": [
            33.5731, 31.5204, 35.7595, 30.4278, 34.0209, 33.9127, 34.2666, 33.6871, 34.0209, 33.2547,
            34.0331, 35.5897, 33.8974, 35.7475, 33.5255, 33.5289, 35.6305, 35.0919, 33.2485, 33.4137, 35.7918,
            33.6798, 35.7323, 33.9605, 33.7606, 33.2341, 33.5711, 32.9306, 33.6481, 32.8955, 33.5564,
            33.6244, 34.0209, 33.6093, 33.5911, 33.2162, 30.3086, 33.9050, 35.0736, 33.7003, 30.4972, 30.2667,
            33.5325, 32.9633, 31.7661, 35.3025, 33.9081, 33.5886, 34.0164, 33.5303, 33.3431
        ],
        "longitude": [
            -7.5898, -7.9811, -5.83395, -9.5981, -6.8417, -6.8997, -6.5777, -7.3805, -6.8294, -8.5366,
            -5.0003, -5.3757, -5.4191, -5.7511, -7.0291, -7.0613, -5.2959, -2.9261, -6.7539, -7.1111, -7.5897,
            -7.0959, -7.3755, -8.0913, -7.3583, -7.6083, -8.3291, -6.9182, -7.3152, -6.6041, -7.3245,
            -7.7184, -6.8417, -7.6149, -7.5517, -7.2843, -9.4249, -7.1280, -7.2294, -7.3999, -8.4980, -8.3786,
            -8.1821, -7.0714, -6.7115, -5.8721, -5.3791, -5.7070, -6.8412, -6.5282, -6.6837, -5.7795
        ]
    }




    coords_df = pd.DataFrame(coords)

    final_df = pd.merge(df, coords_df, on="ville_name", how="left")
    st.map(final_df)


def bar(df):
    df = df.groupby('link').apply(lambda group:group.drop_duplicates(subset='title'))
    df = df['ville_name'].value_counts()
   


    st.bar_chart(df)

