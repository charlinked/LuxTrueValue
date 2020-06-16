import streamlit as st
import pandas as pd
from xgboost import XGBRegressor 

#FRONT-END: INPUT - LAYOUT
#Welcome layout and message
st.write("Reveal your bag's true value with LuxTrueValue!!")
st.write('Just input the details of your bag below and LuxTrueValue will tell you the current resale value of your bag')
#get input from user
brand = st.selectbox('Brand',('CHANEL',''))
quilts = st.selectbox('Is your bag quilted?',('Yes','No'))
logo = st.selectbox('Visible logo present?',('Yes','No'))
chain = st.selectbox('Does your bag have leather interlaced chain straps?',('Yes','No'))
material =  st.selectbox('What material is your bag made out of?',('lambskin','caviar','patent','suede','tweed','fabric','exotic','synthetic'))
color = st.selectbox('color?',('Black','Red','Blue','Beige','Pink','metallic','green','brown'))
style = st.selectbox('What style is your bag',('Flap','Tote','Clutch','WOC','Backpack','canity_case','waist_bag','Crossbody','hand_bag','shoulder_bag'))
size =st.selectbox('What size is your bag',('mini','small','nedium','large','xlarge'))
acc = st.slider('How many of the original accessories do you still have? (dust bag, box, authenticity card)',0,6,(1))
year = st.selectbox('When was the bag produced?',('1980s','1990s','2000-2010','2010-2015','2015-2020'))
cond = st.selectbox('What is the condition of the bag?',('Fair','Good','Excellent','like_new'))
otherdef = st.selectbox('Does your bag have any of the following defects: Visible stains, rips, tears ,missing parts?',('Yes','No'))
odor = st.selectbox('Does your bag have an odor: musty, cigarette, perfume?',('Yes','No'))

#BACK-END: CONVERT INPUT - DO PREDICTIONS
#read in a template file to put in the user input
template = pd.read_csv('template.csv', index_col=0,header=0)

#functions to convert input
#binary input
def bininput(answ,colname):
    if answ == 'Yes':
        template[colname]=1
    else:
        template[colname]=0
#other input
col_list = list(template.columns)
def complete_cols(userinp):
    for i in range(0,len(col_list)):
        if userinp.lower() in str(col_list[i]):
            colname = str(col_list[i])
            template[colname] = 1 

#converting the binary input
bininput(quilts,'has_quilts')
bininput(logo,'has_logo')
bininput(chain,'has_chain')
bininput(otherdef,'other_defects')
bininput(odor,'has_smell')
complete_cols(material)
complete_cols(color)
complete_cols(style)
complete_cols(size)
complete_cols(year)
complete_cols(cond)
template['acc_included']=acc

#predict value
loaded_model = XGBRegressor(random_state=1)
loaded_model.load_model("xgb1_tunedCHANEL_alldata.model")
prediction = loaded_model.predict(template)
#FRONT-END: OUTPUT
st.write("The current resale value of this bag is: $")
st.write(prediction)