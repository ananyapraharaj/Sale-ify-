import requests
import streamlit as st
import pickle
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(
    page_title="Sale-ify",
    page_icon="🏷️",
    layout="wide",
)

def v_spacer(height, sb=False) -> None:
    for _ in range(height):
        if sb:
            st.sidebar.write('\n')
        else:
            st.write('\n')

st.sidebar.header("Walthrough and More about us!")
st.sidebar.write("Use this page as your **'how to use'** guide, as we walk you through the steps of use. We'll also give you a sneak peak of a little more on us and our thought process behind the working of this product and its future upscaling potential.")

st.header("Walkthough!")
st.subheader("Lead Default Probability:")
st.write("**1. Dataset Curation:**")
st.write("**About Dataset** - Personal Loan product is an unsecured loan therefore it is vital to assess the risk of the customers by checking their credit worthiness. This must be done to prevent loan defaults. The objective is to build a Risk model using the dataset which will assess the risk of a customer defaulting after cross-selling the Personal Loan.")
st.write("The source of the defaulter prediction dataset is TVS itself, further adding a layer of data reusability, ensuring that we can make the most out of the curated data, and enhancing customer retention. This can further be extended to customer acquisition, where, with the availability of the required parameters/guesstimates to get the possibility of being a loan defaulter for a given individual or lead.")

df=pd.read_csv("Data/TVS.csv")

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')
csv=convert_df(df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="TVS.csv",
    mime='text/csv',
)

v_spacer(2)
st.write("**2. Predictive Model:**")
st.write("**Working** - Using effective classifiers that perfrom well on model evaluation parameters, we have determined the 6 most important parameters for the determination of a possible defaulter.")

v_spacer(2)
st.write("**3. User Feedback:**")
st.write("**Real-Time Analytics:** Sale-ify's commitment to empowering your lead generation efforts goes beyond just identifying potential customers. We provide you with a robust real-time analytics suite that serves as your compass in the dynamic world of loan marketing.")

v_spacer(2)
st.write("**4. AI Based Communication:**")
st.write(" Test out your pre-sales chatbot tool, **(on the sidebar of the 'Home' page)** to help you better assist customer queries! It works on Question-Answer AI based models. This is exactly how the bot interacts with your potential leads! **For the final product, this could be deployed on the customer side and provide feedback on the company's side to better fit to each consumer individually!**")

v_spacer(4)
st.warning(
    "Please note that this website is but the prototype ans we're currently working on an endpoint website with consumer side and company side authentication, that provides better insights and analytics on an individual level!"
)

v_spacer(12,sb=True)
st.sidebar.success("Welcome to the prototype!")
st.sidebar.write("Feel free to send in your suggestions to us at - omkaramlankrishna@gmail.com")