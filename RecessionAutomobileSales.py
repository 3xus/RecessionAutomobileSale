# Importing Libraries
import numpy as np
import pandas as pd
import matplotlib as mpl 
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import requests
import io

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"

# Obtener el contenido de la URL
response = requests.get(URL)
response.raise_for_status()  # Asegura que la descarga fue exitosa

# Leer los datos en un DataFrame
text = io.StringIO(response.text)
df = pd.read_csv(text)

print('Data downloaded and read into a dataframe!')

df.describe()
df.columns

# Creating Visualizations for Data Analysis
# Task 1.1 Develop a Line Chart using the functionality of pandas
# to show how automobile sales fluctuate from year to year
df_line = df.groupby(df['Year'])['Automobile_Sales'].mean()
df_line

plt.figure(figsize=(10,6))
df_line.plot(kind = 'line')
plt.title('Mean Automobile Sales from 1980 to 2023')
plt.xlabel('Year')
plt.ylabel('Automobile Sales')
plt.xticks(ticks=df_line.index, rotation=80)
plt.text(1982.5, 650, '81-82 Recession')
plt.text(1991.5, 650, '89-92 Recession')
plt.text(2001.5, 650, '01 Recession')
plt.text(2009.5, 650, '09 Recession')
plt.legend()
plt.show()

# Task 1.2