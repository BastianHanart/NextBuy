import streamlit as st

# ==================================================================
# Mise en page du site
# ==================================================================
#st.logo("logo.png", size="large")
st.set_page_config(layout="wide")



data_view = st.Page(
    page="pages/view_data.py",
    title="Exploration des données",
    default=True,
)
pg = st.navigation(pages=[data_view])
pg.run()


footer = """<style>
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: transparent;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Gabin Hannier | Louis Zoonekynd | Bastian Hanart<br>2026 - NEXTBUY - { EPITECH }</p>

</div>
"""
st.markdown(footer, unsafe_allow_html=True)
