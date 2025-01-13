import streamlit as st
import pandas as pd
import plotly.express as px
df = pd.read_csv('vehicles_us.csv')
## Data Cleaning
# Seperate model from make
df[['make', 'model']] = df['model'].str.split(' ', n=1, expand=True)
# Replace the quantitative columns missing data with the mean of the column
df['model_year'].fillna(df['model_year'].median(), inplace=True)
df['odometer'].fillna(df['odometer'].mean(), inplace=True)
# Replace the categorical columns missing data with the most frequent value (mode)
df['cylinders'].fillna(df['cylinders'].mode()[0], inplace=True)
df['paint_color'].fillna(df['paint_color'].mode()[0], inplace=True)
# Change the mising is_4wd to be False (0)
df['is_4wd'].fillna(0.0, inplace=True)

# Make a st header
st.header('Vehicles Simulator Data App')

# Plot Histogram with plotly.express
# Plot histogram of price
fig = px.histogram(df['price'], nbins=150,title='Price Distribution')
fig.update_xaxes(title='Price')
#fig.yaxes(title='Frequency')
st.plotly_chart(fig)
