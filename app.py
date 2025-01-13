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

# Make a checkbox using st.checkbox that changes the behavior of any of the above components
show_histogram = st.checkbox('Show Histogram')

# Plot Histogram with plotly.express
if show_histogram:
    fig = px.histogram(df, x='price', nbins=150, title='Price Distribution by Make', 
                       color='make', color_discrete_sequence=px.colors.qualitative.Set1)
    # Show the chart in Streamlit
    st.plotly_chart(fig)

# Plot a scatterplot in Streamlit
odometer_year = px.scatter(df, x='odometer', y='model_year', title='Odometer Reading by Year', color='make')
# Show the scatter plot in the Streamlit app
st.plotly_chart(odometer_year)

