import streamlit as st
import pandas as pd
import numpy as np

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

def load_training_data():
    data = pd.read_excel('source/training_data.xlsx')
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
#data = load_data(10000)
data = load_training_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

"""
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')

hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=10, range=(0,10))[0]

st.bar_chart(hist_values)

hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)
"""

st.subheader('Number of company')

loan_amt = st.slider('Loan Amount',int(data['loanamt'].min()),int(data['loanamt'].max()),int(data['loanamt'].max()/2))
filtered_data = data[data['loanamt']>loan_amt]

company_rows = filtered_data['company'].unique().tolist()
for index,row in filtered_data.iterrows(): 
    filtered_data.at[index,'company'] = company_rows.index(row['company'])

comp_values = np.histogram(filtered_data['company'], bins=len(company_rows), range=(0,len(company_rows)))[0]


grah_df = pd.DataFrame(columns=["total","company"])
for index,row in filtered_data.iterrows(): 
    name =company_rows[row[0]]
    total = comp_values[row[0]]
    grah_df.loc[len(grah_df.index)] = [total,name]

grah_df = grah_df.drop_duplicates()

st.bar_chart(grah_df,x='company',y='total')
