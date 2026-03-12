import pandas as pd
import streamlit as st


CSV_untouch = pd.read_csv('CSV_Cleaned.csv')
CSV_Clean = CSV_untouch.groupby(
    ["product_name"]
).agg(
    {
        "add_to_cart_order": "mean"
    }
)
CSV_Clean = CSV_Clean.reset_index()
CSV_Clean = CSV_Clean.sort_values(by=["add_to_cart_order"])
DF = CSV_Clean.head(180)

######################################################
################# Pourcentage rachat #################
######################################################


CSV_Clean = CSV_untouch.groupby("user_id").agg(
    nbr_unique=("product_name", "nunique"),
    total_achat=("product_name", "count")
)

DataFrameRachat = pd.DataFrame()
DataFrameRachat['tauxrachat%'] = ((CSV_Clean['total_achat'] - CSV_Clean['nbr_unique']) / CSV_Clean['total_achat']) * 100


Pourcentage_rachat = DataFrameRachat['tauxrachat%'].mean()

######################################################
################# Recherche produits #################
######################################################


liste_produit = sorted(
    list(set(CSV_untouch["product_name"].unique()))
)

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
        .agg(prct_rachat=("reordered", "mean"))
        .reset_index()
    )

    # transformer en %
    dataf["prct_rachat"] = dataf["prct_rachat"] * 100
            # nb_achats=(CSV_untouch.columns[4], "count"),
            # meilleure_heure=(CSV_untouch.columns[1], "max"),
            # meilleur_jour=(CSV_untouch.columns[2], "max"),
            # meilleur_item_avec=(CSV_untouch.columns[5], "first"),
            # emplacement_panier=(CSV_untouch.columns[6], "first"),
            # quantite_ecoulee=(CSV_untouch.columns[4], "sum"),

    # ajouter le pourcentage de rachat

    dataf.columns = [
        "Produit",
        "% Rachat",
        # "Nombre de fois achaté",
        # "Meilleure heures",
        # "Meilleur jour",
        # "Meilleur item avec",
        # "Emplacement panier",
        # "Quantité écoulé",
    ]

    st.dataframe(dataf, use_container_width=True, hide_index=True)

else:
    st.dataframe([], use_container_width=True)



# redirection vers page viewdata
# if st.button("Voir +", key="b2"):
#     st.switch_page("pages/view_data.py")