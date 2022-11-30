import streamlit as st
import time
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#this is the header

st.set_page_config(page_title='Payment Detail Report',  layout='wide', page_icon=':ambulance:')

st.title("Project Knight - Payment Detail Report")
st.markdown("Last Update Date: 2022-11-29")


## Data

with st.spinner('Updating Report...'):
    #Metrics setting and rendering

    lowercase = lambda x: str(x).lower()
    pay_df = pd.read_excel('source/pl_paymenet_date_snapshot_.xlsx',sheet_name = 'Sheet1')    
    pay_df.rename(lowercase, axis='columns', inplace=True)

    #Format datetime to date
    pay_df['snapshot_createdate'] = pd.to_datetime(pay_df['snapshot_createdate']).dt.date
    pay_df['c_actdate'] = pd.to_datetime(pay_df['c_actdate']).dt.date

    exp_df = pay_df['snapshot_createdate'].sort_values(ascending=False).unique().tolist()
    print(exp_df)
    sel_date = st.selectbox('Snapshot Date',exp_df)
    pay_df = pay_df[pay_df['snapshot_createdate']<= sel_date]

    item_count_df = pay_df.groupby(['item'],as_index=False).size().groupby(level=0).max() 
    print(item_count_df)
    #Create the count card
    m1,m2,m3,m4,m5,m6,m7,m8  = st.columns((0.5,1,1,1,1,1,1,1))
    m1.write('')
    if len(item_count_df)>0:m2.metric(label='Number for '+item_count_df.loc[0]['item'],value=int(item_count_df.loc[0]['size']),delta='')
    if len(item_count_df)>1:m3.metric(label='Number for '+item_count_df.loc[1]['item'],value=int(item_count_df.loc[1]['size']),delta='')
    if len(item_count_df)>2:m4.metric(label='Number for '+item_count_df.loc[2]['item'],value=int(item_count_df.loc[2]['size']),delta='')
    if len(item_count_df)>3:m5.metric(label='Number for '+item_count_df.loc[3]['item'],value=int(item_count_df.loc[3]['size']),delta='')
    if len(item_count_df)>4:m6.metric(label='Number for '+item_count_df.loc[4]['item'],value=int(item_count_df.loc[4]['size']),delta='')
    if len(item_count_df)>5:m7.metric(label='Number for '+item_count_df.loc[5]['item'],value=int(item_count_df.loc[5]['size']),delta='')
    if len(item_count_df)>6:m8.metric(label='Number for '+item_count_df.loc[6]['item'],value=int(item_count_df.loc[6]['size']),delta='')
    m1.write('')

    #Number of last 10 payment date count

    g1, g2 = st.columns((1,1))

    last_py_date_count_df = pay_df.groupby(['c_actdate'],as_index=False).size().groupby(level=0).max().sort_values(by=['c_actdate'],ascending=False).head(10)
    #last_py_date_count_df['day'] = pd.to_datetime(pay_df['c_actdate']).dt.month
    last_py_date_count_df = last_py_date_count_df.set_axis(['Active Date','Count'], axis=1, inplace=False)
    print(last_py_date_count_df)
    fig = px.bar(last_py_date_count_df, x = 'Active Date', y='Count', template = 'seaborn')
    fig.update_traces(marker_color='#264653')
    fig.update_layout(title_text="Number of Last 10 Days Payment",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title="Count", xaxis_title="Active Date")
    
    g1.plotly_chart(fig, use_container_width=True) 

    last_py_date_amt_df = pay_df.groupby(['c_actdate'],as_index=False)['amount'].sum().groupby(level=0).max().sort_values(by=['c_actdate'],ascending=False).head(10)
    #last_py_date_amt_df['amount'] = last_py_date_amt_df['amount'].apply(lambda x: "${:.1f}k".format((x/1000)))    
    #last_py_date_amt_df['amount'] = last_py_date_amt_df["amount"].map('{:.2f}'.format)
    last_py_date_amt_df = last_py_date_amt_df.set_axis(['Active Date','Amount'],axis=1, inplace = False)
    
    print(last_py_date_amt_df)
    fag = px.bar(last_py_date_amt_df, x = 'Active Date', y='Amount', template = 'seaborn')
    fag.update_traces(marker_color='#7A9E9F')
    fag.update_layout(title_text="Last 10 Days Payment Amount",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title="Amount", xaxis_title="Active Date")
    fag.update_yaxes( # the y-axis is in dollars
        tickprefix="$"
    )
    g2.plotly_chart(fag, use_container_width=True) 

    today_df = pay_df[pay_df['snapshot_createdate'] == sel_date]
    today_df['status'] = []
    yes_date = pd.to_datetime(sel_date) - pd.DateOffset(1)
    yes_df = pay_df[pay_df['snapshot_createdate'] == yes_date]
    yes_df['status'] = []

    #Check yesterday's find are records, today's canot nout find are records
    for index,row in yes_df.iterrows():
        gidpy = row['gidpy'] 
        t_record = today_df.loc[today_df['gidpy']==gidpy]


    

