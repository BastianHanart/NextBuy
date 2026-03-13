import pandas as pd
import streamlit as st
import joblib 

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

# Classer les noms des nom de produit par ordre alphabétique
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
    
    ######################################################
    ################## Colonnes tableau ##################
    ######################################################

    dataf["prct_rachat"] = dataf["product_name"].map(dictionnaire_rachat) * 100
    dataf["meilleur_moment"] = dataf["product_name"].map(dictionnaire_heure)
    dataf["meilleur_jour"] = dataf["product_name"].map(dictionnaire_jour)
    dataf["Quantité écoulée prédite"] = round(dataf["product_name"].map(dictionnaire_ecoulé) / len(CSV_untouch["product_name"]))
    dataf["Vrai quantité écoulée"] = dataf["product_name"].map(real_quantite)
    dataf["emplacement_panier"] = dataf["product_name"].map(dictionnaire_panier)
    dataf["prochain item"] = dataf["product_name"].map(next_product_dict)

    ######################################################
    ####################### Scores #######################
    ######################################################

    poids = {"prct_rachat": 0.4,
             "nb_achats": 0.1,
             "Quantité écoulée prédite": 0.3,
             "emplacement_panier": 0.2}
    calculpoids = 0

    for k, j in poids.items():
        calculpoids += dataf[k] * j
    dataf["score"] = calculpoids
    dataf["Quantité écoulée prédite"] = round(dataf["product_name"].map(dictionnaire_ecoulé))

    st.dataframe(dataf, use_container_width=True, hide_index=True)


# Sinon on laisse un tableau vide
else:
    st.dataframe([], use_container_width=True)