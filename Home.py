import requests
import streamlit as st
import pickle
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.set_page_config(
    page_title="Sale-ify",
    page_icon="🏷️",
    layout="wide",
)

model_pkl_file="RandomForest_6Params.pkl"
with open(model_pkl_file, 'rb') as file:  
    clf = pickle.load(file)

def v_spacer(height, sb=False) -> None:
    for _ in range(height):
        if sb:
            st.sidebar.write('\n')
        else:
            st.write('\n')

API_URL = "https://api-inference.huggingface.co/models/AdapterHub/bert-base-uncased-pf-drop"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
st.header("Sale-ify! 🏷️")
st.write("Welcome to Sale-ify! Sale-ify is a visionary website that aims to redefine the art of lead generation and presales automation for loan customers. Regardless of whether you operate as a lending institution, a mortgage broker, or a financial professional, Sale-ify is here to revolutionize your approach, making your daily operations more efficient and customer-centric. Our platform is meticulously designed to streamline your workflow, elevate customer engagement to new heights, and ultimately, propel your conversion rates to impressive levels.")
st.header("Key Features!")
st.write("**1. Lead Generation Excellence:** At the core of Sale-ify in lead generation lies our proprietary, state-of-the-art machine learning algorithms and data analytics. These cutting-edge technologies are meticulously crafted to redefine how you discover and engage potential loan customers, effectively becoming your most reliable ally in this competitive landscape.")
st.write("**2. Real-Time Analytics:** Sale-ify's commitment to empowering your lead generation efforts goes beyond just identifying potential customers. We provide you with a robust real-time analytics suite that serves as your compass in the dynamic world of loan marketing.")

st.sidebar.header("Test it out!")
st.sidebar.write("**Playground! -** Test out your pre-sales chatbot tool, to help you better assist customer queries! It works on Question-Answer AI based models. This is exactly how the bot interacts with your potential leads!")


question=st.sidebar.text_input(label="Enter your question.",value="What is EMI?")
output = query({
	"inputs": {
		"question": question,
		"context": "EMI stands for 'Equated Monthly Instalments'. The instalment comprises two components - the principal and the interest. EMIs provide you with the ease and benefit of paying back your loan in fixed monthly payments over a long period of time. To make changes to you contact or mailing details please mail a self-attested copy of any KYC document (as mentioned in the Eligibility and Documentation section) to helpdesk@tvscredit.com, or walk into any of our branches with your documents. You can update the mobile number linked to your TVS Credit loan account using any of the modes: TVS Credit Saathi App, TVS Credit website, TIA - the chatbot on our website, or, our official WhatsApp account: +91 638-517-2692. Your loan will be processed within 24 to 48 hours depending upon the documents and verification requirement. You need to visit a TVS Credit Two-Wheeler Dealership and ask for a TVS Credit representative, we will be happy to assist you with your loan requirement. You may also visit our website or social media pages and provide your contact details, post which our representative will get in touch with you shortly. You only have to submit your KYC documents along with bank details for loan approval. Until the loan is repaid, the vehicle will be hypothecated to TVS Credit. You can borrow up to 95 percent of on-road price of the vehicle (subject to applicable terms & conditions). We offer multiple tenure options ranging from 12 months to 48 months (subject to conditions)."
	},
})
out=output["answer"]
st.sidebar.success(out)
feedback=""
bool_conversation=st.sidebar.radio("Were your doubts resolved?",options=['Yes','No'],horizontal=True, index=1)
add_feedback=""
talk_rating=5
if bool_conversation=='Yes':
    talk_rating=st.sidebar.number_input("How would your rate this talk?",min_value=0,max_value=5)
    feedback=st.sidebar.text_input("How satisfied are you with the conversation?")
else:
    v_spacer(2,sb=True)
    st.sidebar.write("**We appreciate your feedback!**")
    st.sidebar.write(" Please do give us your valueable feedback after you close the conversation with our QnA model to help us enrich your experience further!")

v_spacer(4)
st.header("Lead Default Probability")
col1,col2=st.columns(2)
with col1:
	bounce_last12=st.number_input("Enter the number of times any payment has bounced in the past year.",min_value=0,max_value=1000)
	bounce_when_pay=st.number_input("Enter the number of times payment failed during loan repayment",min_value=0,max_value=1000)
	age_during_loan=st.number_input("Enter the age of applicant",min_value=18,max_value=100)
with col2:
	days_pass_30=st.number_input("Number of times the applicant defaulted in previous loans in the past 30 days in past 6 months.",min_value=0)
	days_pass_60=st.number_input("Number of times the applicant defaulted in previous loans in the past 60 days in past 6 months.",min_value=0)
	days_pass_90=st.number_input("Number of times the applicant defaulted in previous loans in the past 90 days in past 3 months.",min_value=0)
 
test_data = [[
            bounce_last12,
            bounce_when_pay,
            age_during_loan,
            days_pass_30,
            days_pass_60,
            days_pass_90
    ]]
lead_default=round(clf.predict_proba(test_data)[0][1]*100,2)
st.success("The possibility that this lead will be a defaulter is: "+str(lead_default)+"%")

st.subheader("Suggestion:")
if lead_default>50:
    st.error("**This is a high risk lead, it is advisable to follow other options.**")
elif lead_default>20:
    st.warning("**This is a mid risk lead, it is advisable to follow this lead if there aren't any better options.**")
elif lead_default>5:
    st.warning("**This is a fair lead, it is advisable to follow this lead.**")
else:
    st.success("**This is a strong lead to follow.**")
    
v_spacer(4)
st.header("Sentimental Analyser")
st.write("It is imperative to analyze how well your auto-talk tool functions. This portion makes use of NLP or Natural Language Processing to work on user feedback and conversation patterns to aid you in either setting up follow up conversations or in best case scenarios redirect them to the Sales team.")
# Create a SentimentIntensityAnalyzer object.
sid_obj = SentimentIntensityAnalyzer()
# polarity_scores method of SentimentIntensityAnalyzer
# object gives a sentiment dictionary.
# which contains pos, neg, neu, and compound scores.
sentiment_dict = sid_obj.polarity_scores(feedback)
v_spacer(1)
st.subheader("Based on the feeback sentence - ")
st.write("Sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
st.write("Sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
st.write("Sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
# decide sentiment as positive, negative and neutral
if sentiment_dict['compound'] >= 0.05 :
    st.write("**Sentence Overall Rated As Positive**")
elif sentiment_dict['compound'] <= - 0.05 :
    st.write("**Sentence Overall Rated As Negative**")
else :
    st.write("**Sentence Overall Rated As Neutral**")
v_spacer(3)
if feedback!="":
	score=(talk_rating*sentiment_dict['pos'] +(sentiment_dict['neu'])/5 - sentiment_dict['neg'])*100
else:
    score=talk_rating*20
st.subheader("Suggestions:")
st.write("Considering feedback and rating, the overall score = "+str(score))
if score>=75:
    st.success("It's a good time to schedule a sales call.")
elif score>=50:
    st.warning("More pre-sales human/AI conversations are needed.")
else:
    st.error("It's best to have human pre-sales calls. Customer is probably dissatisfied.")
    
dashboard={}

v_spacer(2)