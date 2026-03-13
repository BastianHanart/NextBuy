import pandas as pd
import streamlit as st
import joblib 

#################################################################################################################################
#################################################################################################################################
### On vient mettre les différents élément dans le cache de Streamlit pour éviter les longues attentes et les ralentissements ###
#################################################################################################################################
#################################################################################################################################

# Chargement de tous le dataset qui va se faire qu'une seule fois au début
@st.cache_data
def load_data():
    CSV_untouch = pd.read_csv('CSV_Cleaned.csv')
    return CSV_untouch

# Groupement des données par nom
@st.cache_data
def compute_product_stats(df):
    CSV_Clean = df.groupby(["product_name"]).agg(
        {"add_to_cart_order": "mean"}
    )
    CSV_Clean = CSV_Clean.reset_index()
    CSV_Clean = CSV_Clean.sort_values(by=["add_to_cart_order"])
    return CSV_Clean

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

CSV_untouch = load_data()

CSV_Clean = compute_product_stats(CSV_untouch)
DF = CSV_Clean.head(180)

dictionnaire_panier = joblib.load("Model_IA/Emplacement_panier_Model")
dictionnaire_heure = joblib.load("Model_IA/Meilleure_Heure_Model")
dictionnaire_rachat = joblib.load("Model_IA/Prct_rachat_Model")

######################################################
################# Pourcentage rachat #################
######################################################

Pourcentage_rachat = compute_repurchase(CSV_untouch)

######################################################
################# Recherche produits #################
######################################################


liste_produit = get_product_list(CSV_untouch)

check = st.multiselect("Rechercher produits :", liste_produit)


######################################################
################## Tableau produits ##################
######################################################

l, r = st.columns([3, 1])
l.subheader("📊 Data")

# tt les datas pour le graph comme dans view data
if check:  # si au moins un produit est sélectionné
    df_filtered = CSV_untouch[CSV_untouch["product_name"].isin(check)]

    dataf = (
        df_filtered.groupby("product_name")
        .agg(prct_rachat=("reordered", "mean"),
            # meilleure_heure=(CSV_untouch.columns[1], "max"),
            # meilleur_jour=(CSV_untouch.columns[2], "max"),
            # meilleur_item_avec=(CSV_untouch.columns[5], "first"),
            # emplacement_panier=(CSV_untouch.columns[6], "first"),
            # quantite_ecoulee=("product_name", "sum")
            )
        .reset_index()
    )

    # transformer en %
    dataf["prct_rachat"] = dataf["product_name"].map(dictionnaire_rachat) * 100
    dataf["nb_achats"] = 500 / len(CSV_untouch["user_id"].unique())
    dataf["meilleur_moment"] = dataf["product_name"].map(dictionnaire_heure)
    dataf["quantite_ecoulee"] = 1589 / len(CSV_untouch["product_name"])
    dataf["emplacement_panier"] = dataf["product_name"].map(dictionnaire_panier)
    
    st.write("len(CSV_untouch['user_id'])", len(CSV_untouch["user_id"].unique()))
    st.write("len(CSV_untouch['product_name'])", len(CSV_untouch["product_name"]))
    

    # ajouter le pourcentage de rachat


    ######################################################
    ####################### Scores #######################
    ######################################################

    poids = {"prct_rachat": 0.4,
             "nb_achats": 0.1,
             "quantite_ecoulee": 0.3,
             "emplacement_panier": 0.2}
    calculpoids = 0

    for k, j in poids.items():
        calculpoids += dataf[k] * j
    dataf["score"] = calculpoids

    dataf["nb_achats"] = dataf["nb_achats"] * len(CSV_untouch["user_id"].unique())
    dataf["quantite_ecoulee"] = dataf["quantite_ecoulee"] * len(CSV_untouch["product_name"])

    st.dataframe(dataf, use_container_width=True, hide_index=True)

else:
    st.dataframe([], use_container_width=True)