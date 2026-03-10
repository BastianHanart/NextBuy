import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import plotly.express as px

######################################################
################ CHARGEMENT DES DATA #################
######################################################

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
#################### GRAPH 01 Q01 ####################
######################################################
st.write("### Quel article les clients mettent-ils en premier dans leur panier ?")
fig1 = px.bar(
    DF,
    x="product_name",
    y="add_to_cart_order",
    height=750
)

fig1.update_layout(
    xaxis_title="Nom du produit",
    yaxis_title="???"
)

st.plotly_chart(fig1)

######################################################
#################### GRAPH 02 Q02 ####################
######################################################

st.write("### Quel rayon et quel département contiennent le plus (le moins) de produits ?")
listeaisle = {}

for k in CSV_untouch["aisle"]:
    if k not in listeaisle:
         listeaisle[k] = 1
    else:
        listeaisle[k] += 1

        x_RESULT = listeaisle.keys()

fig2 = px.bar(
    DF,
    x=x_RESULT,
    y=listeaisle.values(),
    height=600
)

fig2.update_layout(
    xaxis_title="Catégorie de produits",
    yaxis_title="Nombre d'occurrence"
)



######################################################
#################### GRAPH 03 Q02 ####################
######################################################

listedep = {}
for k in CSV_untouch["department"]:
    if k not in listedep:
         listedep[k] = 1
    else:
        listedep[k] += 1

fig3 = px.bar(
    DF,
    x=listedep.keys(),
    y=listedep.values(),
    height=600
)

fig3.update_layout(
    xaxis_title="Catégorie de produits",
    yaxis_title="Nombre d'occurrence"
)

######################################################
#################### GRAPH 02 & 03 ###################
######################################################

fig2_col, fig3_col = st.columns(2)
with fig2_col:
    st.plotly_chart(fig2)

with fig3_col:
    st.plotly_chart(fig3)

######################################################
#################### GRAPH 04 Q04 ####################
######################################################
st.write("### Quand et comment les clients passent-ils généralement leurs commandes ?")
DF = round(CSV_untouch["order_hour_of_day"], 0)
listeheure = {}
for k in DF:
    if k not in listeheure:
         listeheure[k] = 1
    else:
        listeheure[k] += 1

fig4 = px.bar(
    DF,
    x=listeheure.keys(),
    y=listeheure.values(),
    height=600
)

fig4.update_layout(
    xaxis_title="Heur de la journée",
    yaxis_title="Nombre d'achat"
)

st.plotly_chart(fig4)

######################################################
#################### GRAPH 05 Q05 ####################
######################################################
# st.write("### Quel est l'horaire ou il y a le plus d'achat de nourriture")
# Bad_DEPARTEMENT = ['other', 'pets', 'personal care', 'house hold']
# CSV_untouch = CSV_untouch.drop(CSV_untouch[CSV_untouch.department.isin(Bad_DEPARTEMENT)].index)
# CSV_Clean = CSV_untouch.groupby(
#     ["user_id"]
# ).agg(
#     {
#         "order_hour_of_day": "mean"
#     }
# )
# DF = round(CSV_Clean, 0)

# listeheure = {}
# for k in DF["order_hour_of_day"]:
#     if k not in listeheure:
#         listeheure[k] = 1
#     else:
#         listeheure[k] += 1

# fig5 = px.bar(
#     DF,
#     x=listeheure.keys(),
#     y=listeheure.values(),
#     height=600
# )

# fig5.update_layout(
#     xaxis_title="Heur de la journée",
#     yaxis_title="Nombre d'achat de nourriture"
# )


# st.plotly_chart(fig5)


######################################################
#################### GRAPH 06 Q06 ####################
######################################################

# CSV_Clean = CSV_untouch.groupby(
#     ["user_id"]
# ).agg(
#     {
#         "days_since_prior_order": "mean"   
#     }
# )
# CSV_Clean = CSV_Clean.reset_index()

# DF = round(CSV_Clean, 0)

# listejour = {}

# for k in DF["days_since_prior_order"]:
#     if k not in listejour:
#         listejour[k] = 1
#     else:
#         listejour[k] += 1

# fig6 = px.bar(
#     DF,
#     x=listejour.keys(),
#     y=listejour.values(),
#     height=600
# )

# fig6.update_layout(
#     xaxis_title="Heur de la journée",
#     yaxis_title="Nombre d'achat"
# )

# st.plotly_chart(fig6)
