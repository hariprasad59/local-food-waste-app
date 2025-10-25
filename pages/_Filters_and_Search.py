import streamlit as st
from dbutil import run_query

st.markdown("""
    <style>
        body {
            background-color: #f0f5f5;
        }
        .stApp {
            background-color: #f0f5f5;
        }
    </style>
""", unsafe_allow_html=True)

#location
cities = run_query("SELECT DISTINCT City FROM Providers UNION SELECT DISTINCT City FROM Receivers;")
city_list = cities['City'].dropna().tolist() if not cities.empty else []

# Get providers
providers_df = run_query("SELECT Provider_ID, Name, City FROM Providers;")
provider_options = providers_df['Name'].tolist() if not providers_df.empty else []

# Get food types
food_types = run_query("SELECT DISTINCT Food_Type FROM FoodListings;")
food_type_options = food_types['Food_Type'].dropna().tolist() if not food_types.empty else []

# Dropdown filters
st.title("Filters & Search")
sel_city = st.selectbox("City (Provider or Receiver)", [None] + city_list)
sel_provider = st.selectbox("Provider", [None] + provider_options)
sel_food_type = st.selectbox("Food Type", [None] + food_type_options)

# Build dynamic query
query = """
    SELECT f.*, 
           p.Name AS Provider_Name, 
           p.Contact AS Provider_Contact, 
           p.City AS Provider_City 
    FROM FoodListings f 
    LEFT JOIN Providers p ON f.Provider_ID = p.Provider_ID
"""
where_clauses = []
params = []

if sel_city:
    where_clauses.append("(p.City = %s OR f.Location = %s)")
    params.extend([sel_city, sel_city])
if sel_provider:
    where_clauses.append("p.Name = %s")
    params.append(sel_provider)
if sel_food_type:
    where_clauses.append("f.Food_Type = %s")
    params.append(sel_food_type)

if where_clauses:
    query += " WHERE " + " AND ".join(where_clauses)

query += " ORDER BY f.Food_ID DESC LIMIT 200;"

# Display query (optional)
st.write("### Executed Query:")
st.code(query)

# Run and display results
df_results = run_query(query, params)
st.dataframe(df_results)

# Show contact details for selected provider
st.markdown("### Contact Providers / Receivers")
if not df_results.empty:
    selected = st.selectbox("Select provider to view contact", df_results['Provider_Name'].unique().tolist())
    provider_row = run_query("SELECT * FROM Providers WHERE Name = %s LIMIT 1;", (selected,))
    if not provider_row.empty:
        p = provider_row.iloc[0]
        st.write(f"**{p['Name']}**")
        st.write(p['Address'])
        st.write(f"Contact: {p['Contact']}")
