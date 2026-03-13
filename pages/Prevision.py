import pandas as pd
import streamlit as st
import joblib
import numpy as np

##########################################################################################
############################## Initialisation des données ################################
##########################################################################################

# On vient mettre toutes les tâches "longues" dans le cache de streamlit pour éviter de devoir charger tous les items tout le temps

# Chargement de tous le dataset qui va se faire qu'une seule fois au début
@st.cache_data
def load_data():
    CSV_untouch = pd.read_csv('CSV_Cleaned.csv')
    return CSV_untouch

# Groupement des données des nom des produits selon les acheteurs
@st.cache_data
def compute_repurchase(df):
    CSV_Clean = df.groupby("user_id").agg(
        nbr_unique=("product_name", "nunique"),
        total_achat=("product_name", "count")
    )

    taux = ((CSV_Clean['total_achat'] - CSV_Clean['nbr_unique']) / CSV_Clean['total_achat']) * 100
    return taux.mean()

# Classer les noms de produit par ordre alphabétique
@st.cache_data
def get_product_list(df):
    return sorted(df["product_name"].unique())

@st.cache_data
def compute_next_product(df):

    # Permet de connaitre l'objet le plus acheté après celui séléctionné
    df = CSV_untouch.sort_values(['order_id', 'add_to_cart_order'])
    df['produit_suivant'] = df['product_name'].shift(-1)
    df_seq = df[df['order_id'] == df['order_id'].shift(-1)]
    Duos = (
        df_seq.groupby(['product_name','produit_suivant'])
        .size()
        .reset_index(name="count")
    )
    Duos = Duos.sort_values("count", ascending=False).drop_duplicates("product_name")
    next_product_dict = dict(zip(Duos["product_name"], Duos["produit_suivant"]))
    

    return next_product_dict


CSV_untouch = load_data()

##########################################################################################
########################## Récupération prédictions modèles IA ###########################
##########################################################################################

dictionnaire_panier = joblib.load("Model_IA/Emplacement_panier_Model")
dictionnaire_heure = joblib.load("Model_IA/Meilleure_Heure_Model")
dictionnaire_jour = joblib.load("Model_IA/Meilleur Jour_Model")
dictionnaire_rachat = joblib.load("Model_IA/Prct_rachat_Model")
dictionnaire_ecoulé = joblib.load("Model_IA/Quantite_ecouler_Model")

##########################################################################################
################################### Pourcentage rachat ###################################
##########################################################################################

Pourcentage_rachat = compute_repurchase(CSV_untouch)

##########################################################################################
################################### Recherche produits ###################################
##########################################################################################


liste_produit = get_product_list(CSV_untouch)

check = st.multiselect("Rechercher produits :", liste_produit)


##########################################################################################
#################################### Tableau produits ####################################
##########################################################################################

st.subheader("📊 Data")

# Si il y a au moins un produit séléctionné, on fait un affichage détaillé
if check:

    ######################################################
    ############ Paramètres colonnes tableau #############
    ######################################################

    # On créer un filtre pour ne garder que les produit séléctionné, pour ne garder que ce qui nous intérésse
    df_filtered = CSV_untouch[CSV_untouch["product_name"].isin(check)]


    # On fait un groupby pour avoir le nb d'achateur unique de chaque produit
    dataf = (
        df_filtered.groupby("product_name")
        .agg(nb_achats=('user_id', "nunique")
            )
        .reset_index()
    )

    # On veut quand même obtenir les vrai quantité pour pouvoir faire une comparaison avec notre prédiction
    real_quantite = df_filtered.groupby("product_name")["product_name"].count()

    # Récupérer l'item souvent achtées ensuite
    next_product_dict = compute_next_product(CSV_untouch)
    
    jours_semaine = {0: "Lundi", 1: "Mardi", 2: "Mercredi", 3: "Jeudi", 4: "Vendredi", 5: "Samedi",6: "Dimanche"}

    ######################################################
    ################## Colonnes tableau ##################
    ######################################################

    dataf["Pourcentage de Rachat"] = dataf["product_name"].map(dictionnaire_rachat) * 100
    dataf["Prédiction quantité écoulée"] = round(dataf["product_name"].map(dictionnaire_ecoulé))
    dataf["Vrai quantité écoulée"] = dataf["product_name"].map(real_quantite)
    dataf["Meilleur moment de la journée"] = dataf["product_name"].map(dictionnaire_heure)
    dataf["Meilleur jour d'achat"] = dataf["product_name"].map(dictionnaire_jour)
    dataf["Meilleur jour d'achat"] = dataf["Meilleur jour d'achat"].map(jours_semaine)
    dataf["Emplacement dans le panier"] = round(dataf["product_name"].map(dictionnaire_panier))
    dataf["Item souvent acheté ensuite"] = dataf["product_name"].map(next_product_dict)

    ######################################################
    ####################### Scores #######################
    ######################################################

    dataf["Erreur quantité"] = abs(dataf["Prédiction quantité écoulée"] - dataf["Vrai quantité écoulée"])
    dataf["Score quantité"] = np.maximum(0, dataf["Prédiction quantité écoulée"] - dataf["Erreur quantité"])

    poids = {"Pourcentage de Rachat": 0.4,
             "nb_achats": 0.1,
             "Score quantité": 0.3,
             "Emplacement dans le panier": 0.2}
    calculpoids = 0

    for k, j in poids.items():
        calculpoids += dataf[k] * j
    dataf["Score / 100"] = calculpoids

    dataf = dataf.rename(columns={
        "product_name": "Nom du produit",
        "nb_achats": "Nombre d'acheteurs différents"
    })

    colonnes_a_afficher = ["Nom du produit", "Nombre d'acheteurs différents","Pourcentage de Rachat","Prédiction quantité écoulée","Vrai quantité écoulée","Meilleur moment de la journée","Meilleur jour d'achat","Emplacement dans le panier","Item souvent acheté ensuite","Score / 100"
]

    st.dataframe(dataf[colonnes_a_afficher], use_container_width=True, hide_index=True)


# Sinon on laisse un tableau vide
else:
    st.dataframe([], use_container_width=True)