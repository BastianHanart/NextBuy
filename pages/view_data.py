import pandas as pd
import matplotlib.pyplot as plt
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
# st.write("### Which item do customers put in their cart first")
# fig1 = px.bar(
#     DF,
#     x="product_name",
#     y="add_to_cart_order",
#     height=750
# )

# fig1.update_layout(
#     xaxis_title="Nom du produit",
#     yaxis_title="Ordre d'ajout au panier"
# )

# st.plotly_chart(fig1)

######################################################
#################### GRAPH 02 Q02 ####################
######################################################

st.write("### Which aisle and departement have the most (less) preoducts")
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
st.write("### When and how do custormers usually order")
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
    xaxis_title="Heures de la journée",
    yaxis_title="Nombre d'achat"
)

######################################################
#################### GRAPH 05 Q04 ####################
######################################################

DF = round(CSV_untouch["days_since_prior_order"], 0)

listejour = {}

# On fait un boucle qui parcour tout DF, et on ajoute chaque nouvelle durée de temps en clé si elle n'existe pas, et on augmente sa valeur qui 
# correspond au nombre de fois ou cette durée apparait dans le CSV
for k in DF:
    if k not in listejour:
        listejour[k] = 1
    else:
        listejour[k] += 1

fig5 = px.bar(
    DF,
    x=listejour.keys(),
    y=listejour.values(),
    height=600
)

fig5.update_layout(
    xaxis_title="Combien de jours depuis les dernières courses",
    yaxis_title="Nombre d'achat"
)



######################################################
#################### GRAPH 04 & 05 ###################
######################################################

fig4_col, fig5_col = st.columns(2)
with fig4_col:
    st.plotly_chart(fig4)

with fig5_col:
    st.plotly_chart(fig5)


######################################################
#################### GRAPH 06 Q05 ####################
######################################################

st.write("### What time of day do most people buy food ?")
Bad_DEPARTEMENT = ['other', 'pets', 'personal care', 'house hold']
CSV_untouch = CSV_untouch.drop(CSV_untouch[CSV_untouch.department.isin(Bad_DEPARTEMENT)].index)
CSV_Clean = CSV_untouch.groupby(
    ["user_id"]
).agg(
    {
        "order_hour_of_day": "mean"
    }
)
DF = round(CSV_Clean, 0)

listeheure = {}
for k in DF["order_hour_of_day"]:
    if k not in listeheure:
        listeheure[k] = 1
    else:
        listeheure[k] += 1

fig6 = px.bar(
    DF,
    x=listeheure.keys(),
    y=listeheure.values(),
    height=600
)

fig6.update_layout(
    xaxis_title="Heur de la journée",
    yaxis_title="Nombre d'achat de nourriture"
)


st.plotly_chart(fig6)


######################################################
#################### GRAPH 07 Q06 ####################
######################################################


st.write("### What percentage of the same items do customers buy when they return to the store ?")

col1, col2, col3 = st.columns(3)
CSV_Clean = CSV_untouch.groupby("user_id").agg(
    nbr_unique=("product_name", "nunique"),
    total_achat=("product_name", "count")
)
DataFrameRachat = pd.DataFrame()
DataFrameRachat['tauxrachat%'] = ((CSV_Clean['total_achat'] - CSV_Clean['nbr_unique']) / CSV_Clean['total_achat']) * 100


Pourcentage_rachat = DataFrameRachat['tauxrachat%'].mean()


sizes = [Pourcentage_rachat, 100-Pourcentage_rachat]
labels = 'Rachat', 'Non rachat'

fig7, ax7 = plt.subplots(figsize=(4, 4))
ax7.pie(sizes, labels=labels, startangle=90, autopct='%1.1f%%')
ax7.axis("equal")

plt.title("Graphique pourcentage de rachat d'items")
col2.pyplot(fig7, use_container_width=False)