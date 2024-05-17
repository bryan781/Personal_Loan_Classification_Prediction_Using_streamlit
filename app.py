import streamlit as st
import pandas as pd
import pickle
import numpy as np

#configure page
st.set_page_config('Personal Loan Prediction',page_icon=':moneybag:',layout='wide')

# configurasi header
style = '<style>h2 {text-align: center;} </style>'
st.markdown(style,unsafe_allow_html=True)

# Session state configuration
if 'submited' not in st.session_state:
    st.session_state['submited'] = False


#=========== Function
def load_model():
    with open('RFClassifier.sav','rb') as file:
        model = pickle.load(file)
        return model

def predict(data:pd.DataFrame):
    model=load_model()
    prob = model.predict_proba(data)
    prob = prob[:,1]

    return prob

#configure title
st.title('Personal Loan Prediction')

#create welcome message
st.write('Welcome to the Personal Loan Campaign Prediction Tool. This application helps banks and financial institutions determine the likelihood of customers accepting personal loan offers. Simply input the customer details below and get instant predictions.')

#create dividing line
st.divider()



with st.sidebar:
    st.header('Menu')
    st.button('Home',use_container_width=True)
    st.button('Setting',use_container_width=True)
    st.button('About',use_container_width=True)

#=======================================================main page
#create 2 columns with a medium gap between
left_panel, right_panel = st.columns(2,gap='medium')

#***************************************left_panel 
#left_panel header
left_panel.header('Information Panel')

#tabs
left_tab_1, left_tab_2= left_panel.tabs(['Overview','Benefits'])

#tab1 overview
#subheader
left_tab_1.write('lorem ipsum')

#tab2 Benefits
#subheader
left_tab_2.write('lorem ipsum')

#*******************************************************right_panel 
#header
right_panel.header('Prediction')
placeholder=right_panel.empty()
btn_placeholder= placeholder.container()
feature_container= placeholder.container()


feature_container.write('Personal Information')


cust_id=feature_container.text_input(label='Customer ID',label_visibility='collapsed',placeholder='Customer ID')

feature_left, feature_right = feature_container.columns(2)

#******************************************************** input columns

age =feature_left.number_input(label='Age',min_value= 17, max_value=75,step=5)
income = feature_left.number_input(label='Anual Income ($ thousands)',min_value= 1, max_value=1000,step=5)
fam_size = feature_left.number_input(label='Family Size',min_value=1,step=1)
prof_exp = feature_left.number_input(label='Profesional Experience (years)',min_value=0,step=1)
deposit_acc = feature_left.selectbox('Certificate Deposit Account',options=['yes','no'])
sec_acc = feature_left.selectbox('Have Security Account',options=['yes','no'])

edu = feature_right.selectbox(label='Education',options=['undergraduate','graduate','advanced/profesional'])
mortgage = feature_right.number_input('Mortgage Value of house ($ thousands)',min_value=0,step=5)
credit_card_spending = feature_right.number_input('Monthly Credit Card Spending ($ thousands)',min_value=0,step=2)
credit_card_acc = feature_right.selectbox('Have Credit Card Account',options=['yes','no'])
internet_bank = feature_right.selectbox('Using Internet Banking',options=['yes','no'])


#============================ submit btn
feature_container.divider()
btn_submit = feature_container.button('Submit!',use_container_width=True)


# Mapping
edu_map = {'undergraduate':1,'graduate':2,'advanced/profesional':3}
edu = edu_map[edu]

deposit_acc_map = {'no':0,'yes':1}
deposit_acc = deposit_acc_map[deposit_acc]

sec_acc_map = {'no':0,'yes':1}
sec_acc = sec_acc_map[sec_acc]

credit_card_acc_map = {'no':0,'yes':1}
credit_card_acc = credit_card_acc_map[credit_card_acc]

internet_bank_map = {'no':0,'yes':1}
internet_bank = internet_bank_map[internet_bank]

if btn_submit:
    st.session_state['submited'] = True


if st.session_state['submited']:
    df = pd.DataFrame([cust_id,age,income,fam_size,prof_exp,deposit_acc,sec_acc,edu,mortgage,credit_card_spending,credit_card_acc,internet_bank],
                      index=['Customer ID','Age','Income','Family','Experience',
                             'CD Account','Securities Account','Education','Mortgage'
                             ,'CCAvg','CreditCard','Online'],
                      columns=['Personal Information'])
    
    placeholder.dataframe(df,use_container_width=True)

    # btn_placeholder.empty()
    btn_cancel = right_panel.button('cancel',use_container_width=True)
    btn_predict = right_panel.button('predict',use_container_width=True)

    if btn_predict:
        df = df.T.drop('Customer ID',axis=1)
        prob = round(predict(df)[0]*100,2)
        right_panel.success(f'Customer with ID: {cust_id} has {prob}% chance to accpt the Personal loan offer')


    if btn_cancel:
        st.session_state['submited'] = False
        st.rerun()




st.divider()
st.write('This tool is designed for illustrative and professional use by financial advisors and should not be considered as personal financial advice. Contact a financial expert before making significant financial decisions.')