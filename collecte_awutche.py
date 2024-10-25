import streamlit as st
import psycopg2
from io import BytesIO

# Configuration de la connexion à PostgreSQL
def create_connection():
    conn = psycopg2.connect(
        host='localhost',  # Remplacez par votre hôte
        database='AWU TCHE',  # Remplacez par le nom de votre base de données
        user='postgres',  # Remplacez par votre nom d'utilisateur
        password='admin'  # Remplacez par votre mot de passe
    )
    return conn

# Fonction pour insérer un propriétaire
def insert_owner(name):
    conn = create_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO public.owners (name) VALUES (%s) RETURNING id;", (name,))
            owner_id = cursor.fetchone()[0]
    return owner_id

# Fonction pour insérer une image
def insert_image(owner_id, image_front, image_side):
    conn = create_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO public.images (owner_id, image_front, image_side)
                VALUES (%s, %s, %s) RETURNING id;
            """, (owner_id, image_front, image_side))
            image_id = cursor.fetchone()[0]
    return image_id

# Fonction pour insérer des mesures
def insert_measurements(image_id, measurements):
    conn = create_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO public.measurements (image_id, carrure_dos, carrure_devant, hauteur_poitine, hauteur_sousein,
                    longueurtaille_devant, longueurtaille_dos, longueur_corsage, tour_encolure, tour_poitrine,
                    tour_sousein, tour_taille, tour_bassin, tour_hanche, longueurtaille_genoux,
                    longueurtaille_cheville, tour_bras, tour_poignet, longueur_bras)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (image_id, *measurements))

# Interface Streamlit
st.title("Upload d'Images et de Mesures")

# Variable d'état pour stocker owner_id
if 'owner_id' not in st.session_state:
    st.session_state.owner_id = None

# Formulaire pour ajouter un propriétaire
with st.form(key='owner_form'):
    owner_name = st.text_input("Nom du Propriétaire")
    submit_owner = st.form_submit_button("Ajouter Propriétaire")
    if submit_owner and owner_name:
        # Insérer le propriétaire et obtenir son ID
        st.session_state.owner_id = insert_owner(owner_name)
        st.success(f"Propriétaire ajouté avec l'ID : {st.session_state.owner_id}")

# Formulaire pour ajouter des images et des mesures
with st.form(key='image_measure_form'):
    image_front = st.file_uploader("Téléchargez l'Image de Face", type=["jpg", "png", "jpeg"])
    image_side = st.file_uploader("Téléchargez l'Image de Profil", type=["jpg", "png", "jpeg"])

    # Mesures
    carrure_dos = st.number_input("Carrure Dos", min_value=0.0)
    carrure_devant = st.number_input("Carrure Devant", min_value=0.0)
    hauteur_poitine = st.number_input("Hauteur Poitrine", min_value=0.0)
    hauteur_sousein = st.number_input("Hauteur Sous-Ein", min_value=0.0)
    longueurtaille_devant = st.number_input("Longueur Taille Devant", min_value=0.0)
    longueurtaille_dos = st.number_input("Longueur Taille Dos", min_value=0.0)
    longueur_corsage = st.number_input("Longueur Corsage", min_value=0.0)
    tour_encolure = st.number_input("Tour Encolure", min_value=0.0)
    tour_poitrine = st.number_input("Tour Poitrine", min_value=0.0)
    tour_sousein = st.number_input("Tour Sous-Ein", min_value=0.0)
    tour_taille = st.number_input("Tour Taille", min_value=0.0)
    tour_bassin = st.number_input("Tour Bassin", min_value=0.0)
    tour_hanche = st.number_input("Tour Hanche", min_value=0.0)
    longueurtaille_genoux = st.number_input("Longueur Taille Genoux", min_value=0.0)
    longueurtaille_cheville = st.number_input("Longueur Taille Cheville", min_value=0.0)
    tour_bras = st.number_input("Tour Bras", min_value=0.0)
    tour_poignet = st.number_input("Tour Poignet", min_value=0.0)
    longueur_bras = st.number_input("Longueur Bras", min_value=0.0)

    submit_image_measure = st.form_submit_button("Ajouter Images et Mesures")
    if submit_image_measure:
        # Vérifiez si owner_id est défini
        if st.session_state.owner_id is not None:
            if image_front and image_side:
                # Lire les images
                img_front = BytesIO(image_front.read())
                img_side = BytesIO(image_side.read())

                # Insérer les images et les mesures
                image_id = insert_image(st.session_state.owner_id, img_front.getvalue(), img_side.getvalue())
                measurements = (
                    carrure_dos, carrure_devant, hauteur_poitine, hauteur_sousein,
                    longueurtaille_devant, longueurtaille_dos, longueur_corsage, tour_encolure,
                    tour_poitrine, tour_sousein, tour_taille, tour_bassin, tour_hanche,
                    longueurtaille_genoux, longueurtaille_cheville, tour_bras, tour_poignet,
                    longueur_bras
                )
                insert_measurements(image_id, measurements)
                st.success("Images et Mesures ajoutées avec succès!")
            else:
                st.error("Veuillez télécharger les deux images.")
        else:
            st.error("Veuillez d'abord ajouter un propriétaire.")
