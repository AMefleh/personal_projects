## Work of: Abdallah Al-Mefleh
## Description: This program takes in the births dataset, produced a list of descriptive statistics then produced two plots for each of the yearly, monthly and decennial data

# Importing relevant libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize
import calendar

# Reading dataset from csv file to pandas dataFrame and error handling
try:
    df = pd.read_csv('US_births_1994_2014_monthly.csv') # initial dataFrame with raw data
except pd.errors.EmptyDataError:
    print("Error: This CSV file is empty.")
except pd.errors.ParserError:
    print("Error: There was an issue parsing this CSV file. Please make sure it is a valid CSV file.")
except FileNotFoundError:
    print("Error: The file was not found.")
except Exception as e:
    print(f"Unexpected error: {e}")

# Checking if the dataFrame is empty
if df.empty:
    print("The dataframe is empty. Please check your input file.")


# Calculating and displaying descriptive statistics
descriptiveStats = df.drop(['year', 'month'], axis=1).describe().round(2) # using describe to get summarized statistics rounded to 2 decimal places, dropping year and months columns
descriptiveStats.loc['median'] = df['births'].median().round(2) # adding median as it is not included in describe function
descriptiveStats.loc['total'] = df['births'].sum().round(2) # addindg row for total number of births
print("Descriptive Statistics:")
print(descriptiveStats)

# Classifying the dataset: yearly, decennially, and by each month
yearlyData = df.groupby('year').sum() # grouping by year
decennialData = df.groupby(df['year'] // 10 * 10).sum() # grouping by decennium
monthlyData = df.groupby('month').sum() # grouping by month

## Visualizing the data with graphs/plots

## YEARLY DATA

# Plotting a bar chart for yearly data
# Using a color map for the bars based on number of births
cmap = cm.RdBu_r # red to blue color scale, reversed using _r
norm = Normalize(vmin=yearlyData['births'].min(), vmax=yearlyData['births'].max()) # setting the start and end points for the scale
colors = cmap(norm(yearlyData['births'])) # associating colors to number of births

plt.bar(yearlyData.index, yearlyData['births'], color = colors)
plt.title('Yearly Births in the United States (1994-2014)')
plt.xlabel('Year')
plt.ylabel('Number of Births (in Tens of Millions)')
plt.xticks(rotation=45) # tilting x-axis labels by 45 degrees
tickPositions = np.arange(1994, 2015, 2) # setting interval size to 1
plt.xticks(tickPositions)
plt.savefig('yearly_births_bar_chart.png') # saving figure
plt.show()

# Plotting a line chart for yearly data
plt.plot(yearlyData.index, yearlyData['births'])
plt.title('Yearly Births in the United States (1994-2014)')
plt.xlabel('Year')
plt.ylabel('Number of Births (in Tens of Millions)')
plt.xticks(rotation=45) # tilting x-axis labels by 45 degrees
tickPositions = np.arange(1994, 2015, 2) # setting interval size to 1
plt.xticks(tickPositions)
plt.savefig('yearly_births_line_chart.png')
plt.show()

## DECENNIAL DATA

# Plotting a bar chart for decennial data
# Splitting data into decades
decades = [f"{i}'s" for i in range(1990, 2020, 10)] # setting decades variable with interval size of 10 and adding 's to the end
barColors = ['blue', 'orange', 'green'] # setting colors

plt.bar(decennialData.index, decennialData['births'], width = 8, color = barColors)
plt.title('Decennial Births in the United States (1994-2014)')
plt.xlabel('Decennial')
plt.ylabel('Number of Births (in Tens of Millions)')
plt.xticks(decennialData.index, decades, rotation=45) # tilting x-axis labels by 45 degrees
plt.savefig('decennial_births_bar_chart.png')
plt.show()

# Plotting a pie chart for decennial data
plt.figure(figsize=(8, 8))
plt.pie(decennialData['births'], labels=decennialData.index, autopct='%1.1f%%', startangle=140) # assigning percentage of total months to each deacde
plt.title('Decennial Distribution of Births (1994-2014)')
plt.savefig('decennial_births_pie_chart.png')
plt.show()

## MONTHLY DATA

# Plotting a line chart for monthly data
monthNames = [calendar.month_name[i] for i in range(1, 13)] # replacing month numbers with month names

plt.plot(monthlyData.index, monthlyData['births'], marker='o', linestyle='-', color='blue')
plt.title('Total Births by Month in the United States (1994-2014)')
plt.xlabel('Month')
plt.ylabel('Number of Births (in Tens of Millions)')
plt.xticks(monthlyData.index, monthNames, rotation=45) # tilting x-axis labels by 45 degrees
plt.savefig('monthly_births_line_chart.png')
plt.show()

# Plotting a stem plot for monthly data
plt.figure(figsize=(10, 6))
plt.stem(monthlyData.index, monthlyData['births'], markerfmt='bo', linefmt='b-')
plt.title('Stem Plot of Total Births by Month in the United States (1994-2014)')
plt.xlabel('Month')
plt.ylabel('Number of Births (in Tens of Millions)')
plt.xticks(monthlyData.index, monthNames, rotation=45)  # tilting x-axis labels by 45 degrees
plt.savefig('monthly_births_stem_plot.png')
plt.show()

print("Data analysis completed.")
