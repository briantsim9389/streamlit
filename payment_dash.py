import streamlit as st
from st_aggrid import AgGrid
from st_aggrid.shared import JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date



#this is the header

st.set_page_config(page_title='Payment Detail Report',  layout='wide', page_icon=':moneybag:')

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
    pay_df['c_actdate'] = pd.to_datetime(pay_df['c_actdate']).dt.strftime('%Y-%m-%d')
    pay_df['c_expdate'] = pd.to_datetime(pay_df['c_expdate']).dt.strftime('%Y-%m-%d')

    exp_df = pay_df['snapshot_createdate'].sort_values(ascending=False).unique().tolist()
    print(exp_df)
    sel_date = st.selectbox('Snapshot Date',exp_df)
    pay_df = pay_df[pay_df['snapshot_createdate']<= sel_date]

    item_count_df = pay_df.groupby(['item'],as_index=False).size().groupby(level=0).max() 
    print(item_count_df)
    #Create the count card
    m1,m2,m3,m4,m5,m6,m7,m8  = st.columns((1,1,1,1,1,1,1,1))

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
    today_df=today_df.assign(status='')

    yes_date = pd.to_datetime(sel_date) - pd.DateOffset(1)
    yes_df = pay_df[pay_df['snapshot_createdate'] == yes_date]
    yes_df=yes_df.assign(status='')

    #The records are find in yesterday's, but not found today's
    filter1 = yes_df[~yes_df.gidpy.isin(today_df.gidpy)]
    filter1['status'] ='OLD'
    today_df = today_df.append(filter1)

    #The records are find in today's, but not found yesterday's
    filter2 = today_df[~today_df.gidpy.isin(yes_df.gidpy)]
    filter2['status'] ='NEW'
    today_df.update(filter2)

    filter3 = yes_df[yes_df.gidpy.isin(today_df.gidpy)]
    filter3.drop(['snapshot_key', 'snapshot_createdate'], axis=1)
    filter3 = filter3.drop(['snapshot_key', 'snapshot_createdate'], axis=1)

    filter4 = today_df[today_df.gidpy.isin(yes_df.gidpy)]
    filter4 = filter4.drop(['snapshot_key', 'snapshot_createdate'], axis=1)

    comparion = filter3.reset_index(drop=True).compare(filter4.reset_index(drop=True))

    #The records are find in today's and yesterday's but values not match
    filter5 = today_df.iloc[comparion.index]
    filter5['status'] = 'UPDATE'
    today_df.update(filter5)
    today_df = today_df.drop(['snapshot_key', 'snapshot_createdate','gidpy','gidcq','actdate','expdate'], axis=1)
    today_df['amount'] = today_df['amount'].apply(lambda x: "${:.1f}k".format((x/1000)))
    today_df['cheque_amount'] = today_df['cheque_amount'].apply(lambda x: "${:.1f}k".format((x/1000)))

    st.subheader("Payment Comparisons: "+str(sel_date)+" / "+str(yes_date))
    cellsytle_jscode = JsCode(
        """
        function(params) {
            if (params.data.status == 'NEW') {
                return {
                    'color': 'black',
                    'backgroundColor': 'paleturquoise'
                }
            } else if (params.data.status == 'OLD') {
                return {
                    'color': 'black',
                    'backgroundColor': 'lightgrey'
                }
            } else if (params.data.status == 'UPDATE') {
                return {
                    'color': 'black',
                    'backgroundColor': '#ED553B'
                }
            } else {
                return {
                    'color': 'black',
                    'backgroundColor': '#FFFFFF'
                }
            }
        };
        """
    )
    #['Loan No','Ref No.','Exp Date','Term','Amount','Item','Remark','Act Date','Cleared','Number','Bank','Cheque Amount','Cheque Remark','Status']
    gb = GridOptionsBuilder.from_dataframe(today_df)
    gb.configure_columns(
        (
            "loanid"
            ,"refno"
            ,"c_expdate"
            ,"term"
            ,"amount"
            ,"item"
            ,"remark"
            ,"c_actdate"
            ,"cleared"
            ,"number"
            ,"bank"
            ,"cheque_amount"
            ,"cheque_remark"
            ,"status"
        ),
        cellStyle=cellsytle_jscode,
    )
    gb.configure_pagination()
    gb.configure_columns(("account_name", "symbol"), pinned=True)
    gridOptions = gb.build()

    AgGrid(today_df, gridOptions=gridOptions, allow_unsafe_jscode=True,fit_columns_on_grid_load=True,height=600)

    @st.experimental_memo
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')


    csv = convert_df(today_df)

    st.download_button(
        "Press to Download",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
    )