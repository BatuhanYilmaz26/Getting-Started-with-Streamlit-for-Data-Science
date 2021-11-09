import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from PIL import Image
import pickle


st.write("""
## Penguin Classifier
##### This app uses 6 inputs to predict the species of penguin using a model built on the Palmer's Penguins dataset.
##### Use the form below to get started! 
""")

penguin_df = pd.read_csv("BatuhanYilmaz26/Getting-Started-with-Streamlit-for-Data-Science/Chapter5/streamlit_sharing/penguins.csv/penguins.csv")
rf_pickle = open("random_forest_penguin.pickle", "rb")
map_pickle = open("output_penguin.pickle", "rb")
rfc = pickle.load(rf_pickle)
unique_penguin_mapping = pickle.load(map_pickle)
rf_pickle.close()
map_pickle.close()



with st.form("user_inputs"):
    island = st.selectbox(label="Penguin Island", 
        options=["Biscoe", "Dream", "Torgerson"])
    sex = st.selectbox(label="Sex", options=["Female", "Male"])
    bill_length = st.number_input(label="Bill Length (mm)", min_value=0)
    bill_depth = st.number_input(label="Bill Depth (mm)", min_value=0)
    flipper_length = st.number_input(label="Flipper Length (mm)", min_value=0)
    body_mass = st.number_input(label="Body Mass (g)", min_value=0)
    st.form_submit_button()

island_biscoe, island_dream, island_torgerson = 0, 0, 0
if island == "Biscoe":
    island_biscoe = 1
elif island == "Dream":
    island_dream = 1
elif island == "Torgerson":
    island_torgerson = 1

sex_female, sex_male = 0, 0
if sex == "Female":
    sex_female = 1
elif sex == "Male":
    sex_male = 1

#Now that we have the inputs with our new form, we need to create our prediction 
# and write the prediction to the user.
new_prediction = rfc.predict([[bill_length, bill_depth, flipper_length,
    body_mass, island_biscoe, island_dream, island_torgerson, sex_female, sex_male]])
prediction_species = unique_penguin_mapping[new_prediction][0]
st.write("""##### Predicting your penguins species...""")
st.write(f"#### We predict your penguin is of the {prediction_species} species.")
st.write("""
We used a machine learning (Random Forest) model to predict the species.\n
The features used in this prediction are ranked by relative importance below.
""")
image = Image.open("feature_importance.png")
st.image(image, caption="Feature Importance Graph")

st.write("""Below are the histograms for each continuous variable seperated by penguin species.\n
The vertical line represents your inputted value.""")
# Bill Length Histogram
fig, ax = plt.subplots()
ax = sns.displot(x=penguin_df["bill_length_mm"], hue=penguin_df["species"])
plt.axvline(bill_length)
plt.title("Bill Length by Species")
st.pyplot(ax)

# Bill Depth Histogram
fig2, ax2 = plt.subplots()
ax2 = sns.displot(x=penguin_df["bill_depth_mm"], hue=penguin_df["species"])
plt.axvline(bill_depth)
plt.title("Bill Depth by Species")
st.pyplot(ax2)

# Flipper Length Histogram
fig3, ax3 = plt.subplots()
ax3 = sns.displot(x=penguin_df["flipper_length_mm"], hue=penguin_df["species"])
plt.axvline(flipper_length)
plt.title("Flipper Length by Species")
st.pyplot(ax3)
