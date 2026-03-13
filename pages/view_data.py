import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

##########################################################################################
################################## CHARGEMENT DES DATA ###################################
##########################################################################################
@st.cache_data
def load_data():
    CSV_untouch = pd.read_csv('CSV_Cleaned.csv')
    return CSV_untouch

@st.cache_data
def compute_stats(df):

    listeaisle = df["aisle"].value_counts()

    listedep = df["department"].value_counts()

    listeheure = df["order_hour_of_day"].round().value_counts().sort_index()

    listejour = df["days_since_prior_order"].round().value_counts().sort_index()

    return listeaisle, listedep, listeheure, listejour

CSV_untouch = load_data()

listeaisle, listedep, listeheure, listejour = compute_stats(CSV_untouch)

##########################################################################################
###################################### Graphiques ########################################
##########################################################################################


######################################################
#################### GRAPH 01 Q02 ####################
######################################################

st.write("### Which aisle and departement have the most (less) preoducts")

fig2 = px.bar(
    x=listeaisle.index,
    y=listeaisle.values,
    height=600
)

fig2.update_layout(
    xaxis_title="Catégorie de produits",
    yaxis_title="Nombre d'occurrence"
)

######################################################
#################### GRAPH 02 Q02 ####################
######################################################

fig3 = px.bar(
    x=listedep.index,
    y=listedep.values,
    height=600
)

fig3.update_layout(
    xaxis_title="Catégorie de produits",
    yaxis_title="Nombre d'occurrence"
)

######################################################
#################### GRAPH 01 & 02 ###################
######################################################

fig2_col, fig3_col = st.columns(2)
with fig2_col:
    st.plotly_chart(fig2)

with fig3_col:
    st.plotly_chart(fig3)

######################################################
#################### GRAPH 03 Q04 ####################
######################################################
st.write("### When and how do custormers usually order")
DF = round(CSV_untouch["order_hour_of_day"], 0)

fig4 = px.bar(
    x=listeheure.index,
    y=listeheure.values,
    height=600
)

fig4.update_layout(
    xaxis_title="Heures de la journée",
    yaxis_title="Nombre d'achat"
)

######################################################
#################### GRAPH 04 Q04 ####################
######################################################

DF = round(CSV_untouch["days_since_prior_order"], 0)

fig5 = px.bar(
    x=listejour.index,
    y=listejour.values,
    height=600
)

fig5.update_layout(
    xaxis_title="Combien de jours depuis les dernières courses",
    yaxis_title="Nombre d'achat"
)



######################################################
#################### GRAPH 03 & 04 ###################
######################################################

fig4_col, fig5_col = st.columns(2)
with fig4_col:
    st.plotly_chart(fig4)

with fig5_col:
    st.plotly_chart(fig5)


######################################################
#################### GRAPH 05 Q05 ####################
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
#################### GRAPH 06 Q06 ####################
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