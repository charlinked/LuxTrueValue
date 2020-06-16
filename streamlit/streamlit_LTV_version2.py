import streamlit as st
import pandas as pd
from xgboost import XGBRegressor
from PIL import Image

#FRONT-END: INPUT - LAYOUT
#importing images
image_bags = Image.open('header.jpg')
im_quilts = Image.open('quilts.jpg')
im_straps = Image.open('straps.jpg')
im_material = Image.open('material.jpg')
im_style = Image.open('style.jpg')
im_condition = Image.open('condition.jpg')
#Welcome layout and message
st.image(image_bags)
#get input from user
brand = st.selectbox('Brand',('CHANEL',''))
quilts = st.selectbox('Is your bag quilted?',('Yes','No'))
st.image(im_quilts)
logo = st.selectbox('Is there a visible brand logo present on the bag?',('Yes','No'))
chain = st.selectbox('Does your bag have chain-linked straps?',('Yes','No'))
st.image(im_straps)
material =  st.selectbox('What material is your bag made out of?',('Lambskin','Caviar','Patent','Suede','Tweed','Fabric','Exotic','Synthetic','Fur'))
st.image(im_material)
color = st.selectbox('Color?',('Black','Red','Blue','Beige','Pink','White','Metallic','Green','Brown','Yellow','Orange','Multicolor','Grey'))
style = st.selectbox('What style is your bag?',('Flap','Tote','Clutch','WOC','Backpack','Vanity_case','Waist_bag','Crossbody','Hand_bag','Shoulder_bag'))
st.image(im_style)
size =st.selectbox('What size is your bag?',('Mini','Small','Medium','Large','Xlarge'))
acc = st.slider('How many of the original accessories do you still have? (dust bag, box, authenticity card, straps or pouches, etc.)',0,6,(1))
year = st.selectbox('When was the bag produced?',('1980s','1990s','2000-2010','2010-2015','2015-2020'))
cond = st.selectbox('What is the condition of the bag?',('Fair','Good','Excellent','Like_new'))
st.image(im_condition)
otherdef = st.selectbox('Does your bag have any of the following defects: Visible stains, rips, tears ,missing parts?',('Yes','No'))
odor = st.selectbox('Does your bag have a particular odor (such as a musty, cigarette, or perfume odor)?',('Yes','No'))

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
prediction = str(loaded_model.predict(template))
prediction = float((prediction.strip('[').replace('','')).strip(']').replace('',''))

#FRONT-END: OUTPUT
st.markdown("---")
st.header("The current resale value of this bag is:")
st.title(f'$%10.f'%prediction)