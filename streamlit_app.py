import streamlit as st
import snowflake.connector
import pandas as pd

st.title("Tcuber's Amazing Athleisure Catalog")

# Connect to Snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()

# Run a Snowflake query and put it all in a variable called my_catalog
my_cur.execute("SELECT color_or_style FROM catalog_for_website")
my_catalog = my_cur.fetchall()

# Put the data into a dataframe
df = pd.DataFrame(my_catalog)

# Temp write the dataframe to the page so I can see what I am working with
# st.write(df)

# Put the first column into a list
color_list = df[0].values.tolist()
# print(color_list)

# Let's put a pick list here so they can pick the color
option = st.selectbox('Pick a sweatsuit color or style:', list(color_list))

# We'll build the image caption now, since we can
product_caption = 'Our warm, comfortable, ' + option + ' sweatsuit!'

# Use the option selected to go back and get all the info from the database
query = "SELECT direct_url, price, size_list, upsell_product_desc FROM catalog_for_website WHERE color_or_style = %s"
my_cur.execute(query, (option,))
df2 = my_cur.fetchone()

st.image(
    df2[0],
    width=400,
    caption=product_caption
)

st.write('Price: ', df2[1])
st.write('Sizes Available: ', df2[2])
st.write(df2[3])
