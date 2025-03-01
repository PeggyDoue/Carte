import streamlit as st
import pydeck as pdk
import pandas as pd
import geopandas as gpd
from io import StringIO
# Contenu principal de l'application
st.title("Application de visualisation de données géographiques")
st.write("Utilisez la barre latérale pour ajouter des données GeoJSON ou KML.")

# Utiliser la barre latérale pour les entrées utilisateur
st.sidebar.title("Accueil")
option = st.sidebar.selectbox(
    'Choisissez une option:',
    ['Données', 'Outils','Cartes']
)

# Afficher le choix de l'utilisateur
st.write('Vous avez choisi:', option)

# Afficher différentes fenêtres en fonction de l'option choisie
if option == 'Données':
    st.write("Contenu spécifique à Données")
elif option == 'Outils':
    st.write("Contenu spécifique à Outils")
elif option == 'Cartes':
    st.write("Contenu spécifique à Cartes")

# Fonction pour charger les données GeoJSON
def load_geojson(file):
    return gpd.read_file(file)

# Fonction pour charger les données KML
def load_kml(file):
    return gpd.read_file(file, driver='KML')

# Créer un onglet pour ajouter des données
st.sidebar.title("Ajouter des données")
data_type = st.sidebar.selectbox("Type de données", ["GeoJSON", "KML"])
uploaded_file = st.sidebar.file_uploader("Choisissez un fichier", type=["geojson", "kml"])

if uploaded_file is not None:
    if data_type == "GeoJSON":
        gdf = load_geojson(uploaded_file)
    elif data_type == "KML":
        gdf = load_kml(uploaded_file)

    # Afficher les données sur une carte
    layer = pdk.Layer(
        "GeoJsonLayer",
        gdf,
        pickable=True,
        stroked=False,
        filled=True,
        extruded=True,
        get_fill_color="[255, 255, 255, 200]",
        get_line_color=[255, 255, 255],
    )

    view_state = pdk.ViewState(
        latitude=gdf.geometry.centroid.y.mean(),
        longitude=gdf.geometry.centroid.x.mean(),
        zoom=10,
        pitch=50,
    )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{name}"}
    )

    st.pydeck_chart(r)
else:
    st.sidebar.info("Veuillez télécharger un fichier GeoJSON ou KML.")

# Exemple de données
data = pd.DataFrame({
    'lat': [5.3167, 7.6833, 6.8161, 6.8833, 4.7500, 9.4167, 7.4000, 6.1333, 6.7333, 5.8333],
    'lon': [-4.0333, -5.0167, -5.2742, -6.4500, -6.6333, -5.6167, -7.5500, -5.9333, -3.4833, -5.3667],
    'name': ['Abidjan', 'Bouaké', 'Yamoussoukro', 'Daloa', 'San-Pédro', 'Korhogo', 'Man', 'Gagnoa', 'Abengourou', 'Divo']
})
# Options pour les fonds de carte
basemap_options = {
    'Carte par défaut': 'mapbox://styles/mapbox/light-v9',
    'Satellite': 'mapbox://styles/mapbox/satellite-v9',
    'Extérieur': 'mapbox://styles/mapbox/outdoors-v11',
    'Noir & Blanc': 'mapbox://styles/mapbox/dark-v9'
}

# Choix du fond de carte par l'utilisateur
st.sidebar.title("Fonds de carte")
basemap_choice = st.sidebar.selectbox('Choisissez le fond de carte', list(basemap_options.keys()))
selected_basemap = basemap_options[basemap_choice]

# Définir la couche pour pydeck
layer = pdk.Layer(
    'ScatterplotLayer',
    data,
    get_position='[lon, lat]',
    get_color='[200, 30, 0, 160]',
    get_radius=200,
)

# Définir la vue initiale de la carte
view_state = pdk.ViewState(
    latitude=7.539989,
    longitude=-5.547080,
    zoom=1.5,
    pitch=0,
)

# Afficher la carte avec pydeck
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={'text': '{name}'}
))