import streamlit as st
import pandas as pd
import plotly.express as px
df = pd.read_csv('vehicles_us.csv')
## Data Cleaning
# Seperate model from make
df[['make', 'model']] = df['model'].str.split(' ', n=1, expand=True)
# Calculate the median model_year for each model
median_model_year = df.groupby('model')['model_year'].median().reset_index()
median_model_year.columns = ['model', 'median_model_year']
# Merge the median values back to the original DataFrame
df = df.merge(median_model_year, on='model', how='left')
# Fill missing values in model_year
df['model_year'].fillna(df['median_model_year'], inplace=True)
# Drop the temporary column
df.drop(columns=['median_model_year'], inplace=True)
# Calculate the median odometer for each combination of model_year and model
median_odometer = df.groupby(['model_year', 'model'])['odometer'].median().reset_index()
median_odometer.columns = ['model_year', 'model', 'median_odometer']
# Merge the median values back to the original DataFrame
df = df.merge(median_odometer, on=['model_year', 'model'], how='left')
# Fill missing values in odometer
df['odometer'].fillna(df['median_odometer'], inplace=True)
# Drop the temporary column
df.drop(columns=['median_odometer'], inplace=True)
# Calculate the median cylinders for each model
median_cylinders = df.groupby('model')['cylinders'].median().reset_index()
median_cylinders.columns = ['model', 'median_cylinders']
# Merge the median values back to the original DataFrame
df = df.merge(median_cylinders, on='model', how='left')
# Fill missing values in cylinders
df['cylinders'].fillna(df['median_cylinders'], inplace=True)
# Drop the temporary column
df.drop(columns=['median_cylinders'], inplace=True)
# Change Paint color
df['paint_color'].fillna(df['paint_color'].mode()[0], inplace=True)
# Change the mising is_4wd to be False
df['is_4wd'].fillna(0.0, inplace=True)
# Fill remaining NaNs in odometer with overall median
overall_median_odometer = df['odometer'].median()
df['odometer'].fillna(overall_median_odometer, inplace=True)
# Remove outliers from the 'price' column where price > 150000
df = df[df['price'] <= 100000]
# Remove outliers from the 'model_year' column where model_year < 1940
df = df[df['model_year'] >= 1940]
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

