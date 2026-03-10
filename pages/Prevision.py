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
################# Recherche produits #################
######################################################


liste_produit = sorted(
    list(set(CSV_untouch["product_name"].unique()))
)

st.multiselect("Rechercher produits :", liste_produit)