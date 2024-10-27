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
df['Vehicle_Type'].unique()
df_recession = df[df['Recession'] == 1]
df_Mline = df_recession.groupby(['Year', 'Vehicle_Type'], as_index=False)['Automobile_Sales'].mean()
df_Mline.set_index('Year', inplace = True)
df_Mline = df_Mline.groupby(['Vehicle_Type'])['Automobile_Sales']
plt.figure(figsize=(10,6))
df_Mline.plot(kind = 'line')
plt.xlabel('Year')
plt.ylabel('Sales')
plt.title('Sales Trend Vehicle-wise during Recession')
plt.legend()
plt.show()

# Task 1.3. Create a visualization to compare the sales trend per vehicle type for a recession period with a non-recession period
df.columns
new_df = df.groupby('Recession')['Automobile_Sales'].mean().reset_index()
new_df.head()

plt.figure(figsize=(8,6))
sns.barplot(x='Recession', y='Automobile_Sales', hue='Recession', data = new_df)
plt.xlabel('Recession')
plt.ylabel('Mean Automobile Sales')
plt.title('Average Automobile Sales during Recession and Non-Recession')
plt.xticks(ticks=[0,1], labels=['Non-Recession', 'Recession'])
plt.show()

# Now you want to compare the sales of different vehicle types during a recession and non-recession perios
df_Tvehicles = df.groupby(['Recession', 'Vehicle_Type'], as_index=False)['Automobile_Sales'].mean()
df_Tvehicles.set_index('Recession', inplace=True)
plt.figure(figsize=(8,6))
sns.barplot(x='Recession', y='Automobile_Sales', hue='Vehicle_Type', data = df_Tvehicles)
plt.xlabel('Period')
plt.ylabel('Mean Automobile Sales')
plt.title('Vehicle-Wise Sales during Recession and Non-Recession Period')
plt.xticks(ticks=[0, 1], labels=['Non-Recession', 'Recession'])
plt.show()


# Task 1.4. Use a sub plotting to compare the variations in GDP during recession and non-recession period
# by developing line plots for each period
# How did the GDP vary over time during recession and non-recession periods?
df_gdp_recession = df[df['Recession'] == 1]
df_gdp_NonRecession = df[df['Recession'] == 0]

# Plots
fig = plt.figure(figsize=(12,8))
ax0 = fig.add_subplot(2,1,1)
ax1 =fig.add_subplot(2,1,2)

# Periodo de recesion
sns.lineplot(x = 'Year', y ='GDP', data = df_gdp_recession, ax = ax0)
ax0.set_xlabel('Year')
ax0.set_ylabel('GDP')
ax0.set_title('GDP Variation during Recession Period')

# Periodo de no recesión
sns.lineplot(x = 'Year', y ='GDP', data = df_gdp_NonRecession, ax = ax1)
ax0.set_xlabel('Year')
ax0.set_ylabel('GDP')
ax0.set_title('GDP Variation during Non Recession Period')

plt.tight_layout()
plt.show()

# Task 1.5. Bubble plot for displaying the impact of seasonality on Automobile Sales
non_rec_data = df[df['Recession'] == 0]
size = non_rec_data['Seasonality_Weight']
sns.scatterplot(data=non_rec_data, x='Month', y='Automobile_Sales', size = size, hue='Seasonality_Weight')
plt.xlabel('Month')
plt.ylabel('Automobile Sales')
plt.title('Seasonality impact on Automobile Sales')
plt.show()

rec_data = df[df['Recession'] == 1]
size = rec_data['Seasonality_Weight']
sns.scatterplot(data=rec_data, x='Month', y='Automobile_Sales', size = size, hue='Seasonality_Weight')
plt.xlabel('Month')
plt.ylabel('Automobile Sales')
plt.title('Seasonality impact on Automobile Sales')
plt.show()

# Task 1.6
rec_data = df[df['Recession'] == 1]

plt.scatter(rec_data['Consumer_Confidence'], rec_data['Automobile_Sales'])
plt.xlabel('Consumer Confidence')
plt.ylabel('Automobile Sales')
plt.title('Relationship between Consumer Confidence and Automobile Sales during Recession Period')
plt.show()

plt.scatter(rec_data['Price'], rec_data['Automobile_Sales'])
plt.xlabel('Price')
plt.ylabel('Automobile Sales')
plt.title('Relationship between Average Vehicle Price and Sales during Recessions')
plt.show()

# Task 1.7. Pie chart to display the portion of sdvertising expenditure of XYZAtomotives during recession and non-recession periods
advertising_recession = df[df['Recession'] == 1]
advertising_NonRecession = df[df['Recession'] == 0]

#Calculamos el total de gastos en propaganda para los tod periodos
advertising_recession_total = advertising_recession['Advertising_Expenditure'].sum()
advertising_NonRecession_total = advertising_NonRecession['Advertising_Expenditure'].sum()

plt.figure(figsize=(8,6))
labels=['Recession', 'Non-Recession']
sizes = [advertising_recession_total, advertising_NonRecession_total]
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Advertising Expenditure during Recession and Non-Recession Periods')
plt.show()

# Task 1.8. 
advertising_recession = df[df['Recession'] == 1]

VTexpenditure = advertising_recession.groupby('Vehicle_Type')['Advertising_Expenditure'].sum()
plt.figure(figsize=(10,8))
labels = VTexpenditure.index
sizes = VTexpenditure.values
plt.pie(sizes, labels=labels, autopct = '%1.1f%%', startangle=90)

plt.title('Share of Each Vehicle Type in Total Expenditure during Recessions')
plt.show()

# Task 1.9
recession_data = df[df['Recession'] == 1]
sns.lineplot(data = recession_data, x='unemployment_rate', y='Automobile_Sales', hue = 'Vehicle_Type',
            markers='o', err_style=None)
plt.ylim(0,850)
plt.legend(loc=(0.05,.3))
plt.title('Effect of Unemployment Rate on Vehicle Type and Sales')
plt.show()