# Import python packages
import streamlit
from snowflake.snowpark.functions import col

# Write directly to the app
streamlit.title("Customize Your Smoothie :cup_with_straw:")
streamlit.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)


#import streamlit as st

name_on_order = streamlit.text_input("Name on Smoothie: ")
streamlit.write("The name on your Smoothie will be: ", name_on_order)


#option = st.selectbox(
 #   "What is your favorite fuit?",
  #  ("Banana", "Strawberries", "Peaches"),
#)

#st.write("Your favorite fuit is:", option)


cnx=streamlit.connection("snowflake")
session=cnx.session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe,use_container_width=True);

ingredients_list=streamlit.multiselect('Choose up to 5 ingredients:',my_dataframe,max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' '

    streamlit.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert=streamlit.button('Submit order')


    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        streamlit.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")


import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response.json())
