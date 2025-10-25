import streamlit as st
from dbutil import run_query

st.title("Overview — Food Donations")


dfp = run_query("SELECT COUNT(*) AS Providers FROM Providers;")
dfr = run_query("SELECT COUNT(*) AS Receivers FROM Receivers;")
dff = run_query("SELECT COUNT(*) AS FoodListings FROM FoodListings;")
dfc = run_query("SELECT COUNT(*) AS Claims FROM Claims;")

cols = st.columns(4)
cols[0].metric("Providers", int(dfp['Providers'][0]))
cols[1].metric("Receivers", int(dfr['Receivers'][0]))
cols[2].metric("Food Listings", int(dff['FoodListings'][0]))
cols[3].metric("Claims", int(dfc['Claims'][0]))

st.subheader("Sample Records")
st.markdown("**Providers**")
st.dataframe(run_query("SELECT * FROM Providers LIMIT 5;"), use_container_width=True)
st.markdown("**Receivers**")
st.dataframe(run_query("SELECT * FROM Receivers LIMIT 5;"), use_container_width=True)
st.markdown("**Food Listings**")
st.dataframe(run_query("SELECT * FROM FoodListings LIMIT 5;"), use_container_width=True)
st.markdown("**Claims**")
st.dataframe(run_query("SELECT * FROM Claims LIMIT 5;"), use_container_width=True)
