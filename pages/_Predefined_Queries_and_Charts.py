import streamlit as st
from dbutil import run_query
import matplotlib.pyplot as plt


st.title("SQL Insights Dashboard")

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

# Add section selector
query_type = st.sidebar.radio(
    "Select Query Type:",
    ("Predefined Queries", "User-Defined Queries")
)


#COMMON VISUALIZATION FUNCTIONS
def show_bar_chart(df, x_col, y_col, title):
    fig, ax = plt.subplots()
    ax.bar(df[x_col], df[y_col])
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_title(title)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)


def show_pie_chart(df, label_col, value_col, title):
    fig, ax = plt.subplots()
    ax.pie(df[value_col], labels=df[label_col], autopct='%1.1f%%')
    ax.set_title(title)
    st.pyplot(fig)


#PREDEFINED QUERIES
if query_type == "Predefined Queries":

    with st.expander("1. How many food providers and receivers are there in each city?"):
        if st.button("Run Query 1"):
            q = """
            SELECT 
                City,
                COUNT(DISTINCT Provider_ID) AS Total_Providers,
                COUNT(DISTINCT Receiver_ID) AS Total_Receivers
            FROM (
                SELECT City, Provider_ID, NULL AS Receiver_ID FROM Providers
                UNION ALL
                SELECT City, NULL AS Provider_ID, Receiver_ID FROM Receivers
            ) AS combined
            GROUP BY City;
            """
            df = run_query(q)
            st.dataframe(df)

    with st.expander("2. Which type of food provider contributes the most food?"):
        if st.button("Run Query 2"):
            q = """
            SELECT Provider_Type, SUM(Quantity) AS Total_Quantity
            FROM FoodListings
            GROUP BY Provider_Type
            ORDER BY Total_Quantity DESC
            LIMIT 4;
            """
            df = run_query(q)
            st.dataframe(df)
            show_bar_chart(df, 'Provider_Type', 'Total_Quantity', 'Food Contribution by Provider Type')

    with st.expander("3. What is the contact information of food providers in a specific city?"):
        city = st.text_input("Enter City Name:")
        if st.button("Run Query 3"):
            q = "SELECT Name, Type, Contact, Address FROM Providers WHERE City = %s;"
            df = run_query(q, (city,))
            st.dataframe(df)

    with st.expander("4. Which receivers have claimed the most food?"):
        if st.button("Run Query 4"):
            q = """
            SELECT Receivers.Name, COUNT(Claims.Claim_ID) AS Total_Claims
            FROM Claims
            JOIN Receivers ON Claims.Receiver_ID = Receivers.Receiver_ID
            GROUP BY Receivers.Name
            ORDER BY Total_Claims DESC;
            """
            df = run_query(q)
            st.dataframe(df)

    with st.expander("5. What is the total quantity of food available from all providers?"):
        if st.button("Run Query 5"):
            q = "SELECT SUM(Quantity) AS Total_Food_Quantity FROM FoodListings;"
            df = run_query(q)
            st.dataframe(df)

    with st.expander("6. Which city has the highest number of food listings?"):
        if st.button("Run Query 6"):
            q = """
            SELECT Location AS City, COUNT(Food_ID) AS Total_Listings
            FROM FoodListings
            GROUP BY Location
            ORDER BY Total_Listings DESC
            LIMIT 1;
            """
            df = run_query(q)
            st.dataframe(df)

    with st.expander("7. What are the most commonly available food types?"):
        if st.button("Run Query 7"):
            q = """
            SELECT Food_Type, COUNT(*) AS Count
            FROM FoodListings
            GROUP BY Food_Type
            ORDER BY Count DESC;
            """
            df = run_query(q)
            st.dataframe(df)

    with st.expander("8. How many food claims have been made for each food item?"):
        if st.button("Run Query 8"):
            q = """
            SELECT f.Food_Name, COUNT(c.Claim_ID) AS Total_Claims
            FROM Claims c
            JOIN FoodListings f ON c.Food_ID = f.Food_ID
            GROUP BY f.Food_Name
            ORDER BY Total_Claims DESC;
            """
            df = run_query(q)
            st.dataframe(df)
            show_bar_chart(df.head(10), 'Food_Name', 'Total_Claims', 'Claims per Food Item')

    with st.expander("9. Which provider has had the highest number of successful food claims?"):
        if st.button("Run Query 9"):
            q = """
            SELECT p.Name AS Provider_Name, COUNT(c.Claim_ID) AS Successful_Claims
            FROM Claims c
            JOIN FoodListings f ON c.Food_ID = f.Food_ID
            JOIN Providers p ON f.Provider_ID = p.Provider_ID
            WHERE c.Status = 'Completed'
            GROUP BY p.Name
            ORDER BY Successful_Claims DESC
            LIMIT 1;
            """
            df = run_query(q)
            st.dataframe(df)

    with st.expander("10. What percentage of food claims are Completed vs Pending vs Cancelled?"):
        if st.button("Run Query 10"):
            q = """
            SELECT Status, COUNT(*) AS Count
            FROM Claims
            GROUP BY Status;
            """
            df = run_query(q)
            st.dataframe(df)
            show_pie_chart(df, 'Status', 'Count', 'Claim Status Distribution')

    with st.expander("11. What is the average quantity of food claimed per receiver?"):
        if st.button("Run Query 11"):
            q = """
            SELECT r.Name AS Receiver_Name, ROUND(AVG(f.Quantity),2) AS Avg_Quantity_Claimed
            FROM Claims c
            JOIN FoodListings f ON c.Food_ID = f.Food_ID
            JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID
            GROUP BY r.Name
            ORDER BY Avg_Quantity_Claimed DESC;
            """
            df = run_query(q)
            st.dataframe(df)
            show_bar_chart(df.head(10), 'Receiver_Name', 'Avg_Quantity_Claimed', 'Average Quantity Claimed per Receiver')

    with st.expander("12. Which meal type is claimed the most?"):
        if st.button("Run Query 12"):
            q = """
            SELECT f.Meal_Type, COUNT(c.Claim_ID) AS Total_Claims
            FROM Claims c
            JOIN FoodListings f ON c.Food_ID = f.Food_ID
            GROUP BY f.Meal_Type
            ORDER BY Total_Claims DESC;
            """
            df = run_query(q)
            st.dataframe(df)
            show_bar_chart(df, 'Meal_Type', 'Total_Claims', 'Most Claimed Meal Type')

    with st.expander("13. What is the total quantity of food donated by each provider?"):
        if st.button("Run Query 13"):
            q = """
            SELECT p.Name AS Provider_Name, SUM(f.Quantity) AS Total_Quantity
            FROM FoodListings f
            JOIN Providers p ON f.Provider_ID = p.Provider_ID
            GROUP BY p.Name
            ORDER BY Total_Quantity DESC;
            """
            df = run_query(q)
            st.dataframe(df)

    with st.expander("14. Which cities have the highest number of completed claims?"):
        if st.button("Run Query 14"):
            q = """
            SELECT p.City, COUNT(c.Claim_ID) AS Completed_Claims
            FROM Claims c
            JOIN FoodListings f ON c.Food_ID = f.Food_ID
            JOIN Providers p ON f.Provider_ID = p.Provider_ID
            WHERE c.Status = 'Completed'
            GROUP BY p.City
            ORDER BY Completed_Claims DESC;
            """
            df = run_query(q)
            st.dataframe(df)

    with st.expander("15. Which food type has the highest average quantity donated per listing?"):
        if st.button("Run Query 15"):
            q = """
            SELECT Food_Type, ROUND(AVG(Quantity),2) AS Avg_Quantity
            FROM FoodListings
            GROUP BY Food_Type
            ORDER BY Avg_Quantity DESC;
            """
            df = run_query(q)
            st.dataframe(df)
            show_bar_chart(df, 'Food_Type', 'Avg_Quantity', 'Average Quantity per Food Type')


#USER-DEFINED QUERIES
else:

    with st.expander("16. Which city has the highest number of food providers?"):
        if st.button("Run Query 16"):
            q = """
            SELECT City, COUNT(*) AS Total_Providers
            FROM Providers
            GROUP BY City
            ORDER BY Total_Providers DESC
            LIMIT 1;
            """
            df = run_query(q)
            st.dataframe(df)

    with st.expander("17. How many food items are near expiry (within next 7 days)?"):
        if st.button("Run Query 17"):
            q = """
            SELECT Food_Name, Expiry_Date, DATEDIFF(Expiry_Date, CURDATE()) AS Days_Left
            FROM FoodListings
            WHERE Expiry_Date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY);
            """
            df = run_query(q)
            st.dataframe(df)

    with st.expander("18. Which city generates the most food claims?"):
        if st.button("Run Query 18"):
            q = """
            SELECT r.City, COUNT(c.Claim_ID) AS Total_Claims
            FROM Claims c
            JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID
            GROUP BY r.City
            ORDER BY Total_Claims DESC;
            """
            df = run_query(q)
            st.dataframe(df)

    with st.expander("19. How many claims are still pending per city?"):
        if st.button("Run Query 19"):
            q = """
            SELECT r.City, COUNT(c.Claim_ID) AS Pending_Claims
            FROM Claims c
            JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID
            WHERE c.Status = 'Pending'
            GROUP BY r.City
            ORDER BY Pending_Claims DESC;
            """
            df = run_query(q)
            st.dataframe(df)

    with st.expander("20. Monthly trend of food donations"):
        if st.button("Run Query 20"):
            query20="""SELECT DATE_FORMAT(Expiry_Date, '%%Y-%%m') AS Month,
           SUM(Quantity) AS Total_Donations
           FROM FoodListings
           GROUP BY Month
           ORDER BY Month;"""
            df = run_query(query20)
            st.dataframe(df)

    with st.expander("21. Which receiver type has the most claims?"):
        if st.button("Run Query 21"):
            q = """
            SELECT r.Type AS Receiver_Type, COUNT(c.Claim_ID) AS Total_Claims
            FROM Claims c
            JOIN Receivers r ON c.Receiver_ID = r.Receiver_ID
            GROUP BY r.Type
            ORDER BY Total_Claims DESC;
            """
            df = run_query(q)
            st.dataframe(df)
            show_bar_chart(df, 'Receiver_Type', 'Total_Claims', 'Claims by Receiver Type')

    with st.expander("22. Average number of food listings per provider"):
        if st.button("Run Query 22"):
            q = """
            SELECT p.Name AS Provider_Name, COUNT(f.Food_ID) AS Total_Listings,
                   AVG(f.Quantity) AS Avg_Quantity_Per_Listing
            FROM Providers p
            LEFT JOIN FoodListings f ON p.Provider_ID = f.Provider_ID
            GROUP BY p.Name
            ORDER BY Total_Listings DESC;
            """
            df = run_query(q)
            st.dataframe(df)

    with st.expander("23. Do cities with more providers have fewer pending claims?"):
        if st.button("Run Query 23"):
            q = """
            SELECT p.City, COUNT(DISTINCT p.Provider_ID) AS Providers,
                   SUM(CASE WHEN c.Status = 'Pending' THEN 1 ELSE 0 END) AS Pending_Claims
            FROM Providers p
            LEFT JOIN FoodListings f ON p.Provider_ID = f.Provider_ID
            LEFT JOIN Claims c ON f.Food_ID = c.Food_ID
            GROUP BY p.City
            ORDER BY Providers DESC;
            """
            df = run_query(q)
            st.dataframe(df)

    with st.expander("24. Which cities have the highest number of completed food claims?"):
        if st.button("Run Query 24"):
            q = """
            SELECT f.Location AS City, COUNT(c.Claim_ID) AS Completed_Claims
            FROM Claims c
            JOIN FoodListings f ON c.Food_ID = f.Food_ID
            WHERE c.Status = 'Completed'
            GROUP BY f.Location
            ORDER BY Completed_Claims DESC;
            """
            df = run_query(q)
            st.dataframe(df)

    with st.expander("25. Which food type has the highest average quantity donated per listing?"):
        if st.button("Run Query 25"):
            q = """
            SELECT Food_Type, ROUND(AVG(Quantity), 2) AS Avg_Quantity_Donated
            FROM FoodListings
            GROUP BY Food_Type
            ORDER BY Avg_Quantity_Donated DESC;
            """
            df = run_query(q)
            st.dataframe(df)
            show_bar_chart(df, 'Food_Type', 'Avg_Quantity_Donated', 'Avg Quantity per Food Type')
