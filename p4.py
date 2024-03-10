import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to convert Kelvin to Fahrenheit
def kelvin_to_fahrenheit(K):
    return (K - 273.15) * 9/5 + 32

# Load the dataset
@st.cache
def load_data():
    df = pd.read_csv('./weather - 286_40.75_t2m_1d.csv')
    df['time'] = pd.to_datetime(df['time'])
    df['Ftemp'] = kelvin_to_fahrenheit(df['Ktemp'])
    return df

df = load_data().copy()

# Part A: Monthly Average Temperature Visualization
st.title('Monthly Average Temperature Visualization')
selected_year = st.slider('Select a year', min_value=int(df['time'].dt.year.min()), max_value=int(df['time'].dt.year.max()), value=int(df['time'].dt.year.min()))

# Filter data for the selected year
df_year = df[df['time'].dt.year == selected_year]

# Calculate monthly average temperature
monthly_avg_temp = df_year.groupby(df_year['time'].dt.month)['Ftemp'].mean().reset_index()

# Plot
fig, ax = plt.subplots()
ax.plot(monthly_avg_temp['time'].values, monthly_avg_temp['Ftemp'].values, marker='o', linestyle='-')
ax.set_xlabel('Month')
ax.set_ylabel('Average Temperature (°F)')
ax.set_title(f'Average Monthly Temperature for {selected_year}')
st.pyplot(fig)

# Part B: First Year with Average Temperature Above 55°F
st.header('First Year with Average Temperature Above 55°F')

# Calculate yearly average temperature
yearly_avg_temp = df.groupby(df['time'].dt.year)['Ftemp'].mean()
first_warm_year = yearly_avg_temp[yearly_avg_temp > 55].index[0]

st.write(f'The first year when the average temperature exceeded 55°F at Cornell Tech was {first_warm_year}.')

# Part C: Creative Visualization

# Load the sea level data
@st.cache
def load_sea_level_data():
    sea_level_df = pd.read_csv('sealevel.csv')
    # Assume 'GMSL_GIA' is the column with GIA applied sea level variation
    sea_level_df['Year'] = pd.to_numeric(sea_level_df['Year'], errors='coerce')
    yearly_sea_level = sea_level_df.groupby('Year')['GMSL_GIA'].mean().reset_index()  # Use the correct sea level column
    return yearly_sea_level

yearly_sea_level = load_sea_level_data().copy()

# Ensure the temperature data has a year column to merge on
df['Year'] = df['time'].dt.year
yearly_avg_temp = df.groupby('Year')['Ftemp'].mean().reset_index()

# Merge the two datasets
combined_df = pd.merge(yearly_avg_temp, yearly_sea_level, on='Year')

# Filter the combined dataset to include years from 1995 to 2020
combined_df = combined_df[(combined_df['Year'] >= 1995) & (combined_df['Year'] <= 2020)]

# Plotting
st.header('Yearly Average Temperature vs. Average Sea Level (GIA applied) from 1995 to 2020')

# Define the figure size
fig, ax1 = plt.subplots(figsize=(14, 6))  # Increase figure width for better readability

years = combined_df['Year'].values
temp = combined_df['Ftemp'].values
sea_level = combined_df['GMSL_GIA'].values

color = 'tab:red'
ax1.set_xlabel('Year')
ax1.set_ylabel('Avg Temperature (°F)', color=color)
ax1.plot(years, temp, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:blue'
ax2.set_ylabel('Average Sea Level Change (mm)', color=color)
ax2.plot(years, sea_level, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('Yearly Average Temperature vs. Average Sea Level Change (GIA applied) from 1995 to 2020')
st.pyplot(fig)

st.write('This visualization shows the yearly average temperature in comparison to the average sea level change from 1995 to 2020, providing insights into potential correlations between global warming and sea level rise.')
