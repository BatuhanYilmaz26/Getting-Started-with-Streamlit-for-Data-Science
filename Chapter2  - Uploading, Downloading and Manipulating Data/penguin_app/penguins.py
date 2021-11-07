import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.write("""
# Palmer's Penguins 
### The first 5 rows in dataset """)

penguins_df = pd.read_csv("penguins.csv")
st.write(penguins_df.head())

st.write("#### Number of penguin species")
st.write(penguins_df["species"].value_counts())
# st.write("#### Is there any missing values?")
# st.write(penguins_df.isnull().sum())

st.write("""#### Use this Streamlit app to make your own scatterplot about penguins!""")
selected_species = st.selectbox("What species would you like to visualize?",
    ["Adelie", "Gentoo", "Chinstrap"])
selected_x_var = st.selectbox("What do you want the x variable to be?",
    ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])
selected_y_var = st.selectbox("What about the y variable?",
    ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

penguins_df = penguins_df[penguins_df["species"] == selected_species]

fig, ax = plt.subplots()
ax = sns.scatterplot(x = penguins_df[selected_x_var],
                     y = penguins_df[selected_y_var])
plt.xlabel(selected_x_var)
plt.ylabel(selected_y_var)
plt.title(f"Scatterplot of {selected_species} Penguins")
st.pyplot(fig)
