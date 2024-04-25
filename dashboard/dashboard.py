import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
day_df = pd.read_csv("./day_clean.csv")
day_ori = pd.read_csv("../data/day.csv")

# rental bike amount based on weather
grouped = day_df.groupby("weathersit")
grouped_sum = grouped['cnt'].sum()
weathersit_grouped = grouped_sum.sort_values(ascending=False).reset_index()

# rental bike amount based on season
grouped = day_df.groupby("season")
grouped_sum = grouped['cnt'].sum()
season_grouped = grouped_sum.sort_values(ascending=False).reset_index()

pivot_week = day_df.pivot_table(index='weekday', values=['casual', 'registered'], aggfunc='sum')

# Dashboard set up
st.title('Proyek Analisis Data: Bike Sharing Dataset')
st.write(
    """
- Nama: Sayyidan Muhamad Ikhsan
- Email: sayyidan.xyz@gmail.com
- ID Dicoding: sayyidan-i
    """
)
st.subheader('Pertanyaan Bisnis')
st.write(
    """
1. Do people tend to rent bikes more on clear days compared to rainy or snow days?
2. In which season where demand significantly increases?
3. What are the weekly variations in bike rental demand, and how do these patterns differ across different user type (casual and registered)?
    """
)
st.subheader('Data Overview')
st.write('#### Original Data')
st.write(day_ori.head())

st.write('#### Cleaned Data')
st.write(day_df.head())


st.header('Data Visualization')
st.write('#### Rent Bike Demand by Weather')

# create bar chart to see the rent demand based on weather situation

fig1, ax1 = plt.subplots(figsize=(3,4))
sns.barplot(x="weathersit", y="cnt", data=weathersit_grouped, palette=["pink", "lightgrey", "lightgrey"], hue='weathersit', legend=False)
ax1.set_xlabel('Weather')
ax1.set_ylabel('Demand')
ax1.set_title('Bike Rental Demand Based on Weather', fontsize=10)
st.pyplot(fig1)

st.write('#### Rent Bike Demand by Season')

# create bar chart to see the rent demand based on season

fig2, ax2 = plt.subplots(figsize=(3,4))
sns.barplot(x="season", y="cnt", data=season_grouped, palette=["pink", "lightgrey", "lightgrey", "lightgrey"], order=['Spring', 'Summer', 'Fall', 'Winter'], hue='season', legend=False)
ax2.set_xlabel('Season')
ax2.set_ylabel('Demand')
ax2.set_title('Bike Rental Demand Based on Season', fontsize=10)
st.pyplot(fig2)

st.write('#### Weekly Variations in Bike Rental Demand by User Type')

# create bar chart to see the rent demaand variations weekly

melted_df = day_df.melt(id_vars='weekday', value_vars=['casual', 'registered'], var_name='User Type', value_name='Demand')

fig, ax = plt.subplots(figsize=(8,4))
sns.boxplot(x="weekday", y='Demand', data=melted_df, palette=["red", "blue"], order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], hue='User Type')
ax.set_xlabel('Day')
ax.set_ylabel('Bike Rental Demand')
ax.set_title('Weekly Variations in Bike Rental Demand by User Type', fontsize=10)
st.pyplot(fig)

# Define custom order for weekdays
custom_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Reorder the index of the pivot table
pivot_week = pivot_week.reindex(custom_order)

# Plotting
fig3, ax3 = plt.subplots(figsize=(8,4))

# Plot for casual users
ax3.plot(pivot_week.index, pivot_week['casual'], marker='o', label='casual', color='skyblue')

# Plot for registered users
ax3.plot(pivot_week.index, pivot_week['registered'], marker='o', label='registered', color='orange')

# Adding labels and title
ax3.set_xlabel('Day')
ax3.set_ylabel('Bike Rental Demand')
ax3.set_title('Weekly Variations in Bike Rental Demand by User Type')
ax3.legend()
st.pyplot(fig3)
