## Programmer: Abe Mefleh

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## Read in the Industry.csv file

data = pd.read_csv('~/Desktop/Industry.csv')

## Strip out the workforce total rows and the year column

data = data[~data['Label (Grouping)'].str.contains('Civilian employed population 16 years and over')]
data = data.drop(columns=['Year'])

## Subset this data into 2D arrays representing each year (rows: industry, columns: county)

data_array = data.to_numpy()
industry_labels = data.iloc[:, 0].tolist()
years_data = [data.iloc[1 + 14 * chunk: 1 + 14 * (chunk + 1), 1:].to_numpy() for chunk in range(len(data) // 14)]

## Subset this data into 2D arrays representing each county (rows: industry, columns: year)

county_data = data_array[:, 1:].T

## For the output of #3, construct a 3D array where each layer is the next timestamp sequentially

spacetime_cube = np.stack(years_data, axis=2)

## The total number of workers in the state per industry per given year

total_workers_per_year = np.sum(spacetime_cube, axis=(0, 1))

## The average number of workers in the county per industry over the 12 year period

average_workers_per_county_industry = np.mean(spacetime_cube, axis=2)

## Choose a color combination (0 or 255 on a combination of scales). Take Cumberland County and a rural county of your choice

cumberland_county_data = county_data[2]
penobscot_county_data = county_data[10]

## Calculate the percentage of the labor force in that county by year that is in a particular industry

percentage_cumberland = (cumberland_county_data / np.sum(cumberland_county_data, axis=0))*100
percentage_penobscot = (penobscot_county_data / np.sum(penobscot_county_data, axis=0))*100

## Find the minimum and maximum by industry

min_percentage = min(np.min(percentage_cumberland), np.min(percentage_penobscot))
max_percentage = max(np.max(percentage_cumberland), np.max(percentage_penobscot))

## “Center” the field by placing it along the scale from its minimum to maximum

centered_cumberland = (percentage_cumberland - min_percentage) / (max_percentage - min_percentage)*255
centered_penobscot = (percentage_penobscot - min_percentage) / (max_percentage - min_percentage)*255

## Use that centered value to then shift the scale in one color dimension from 0 to 255

shifted_cumberland = centered_cumberland.astype(float)
shifted_penobscot = centered_penobscot.astype(float)

## Display the colors on an array grid

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.imshow(shifted_cumberland, cmap='viridis', interpolation='nearest', vmin=0, vmax=255)
plt.title('Cumberland County')
plt.colorbar()

plt.subplot(1, 2, 2)
plt.imshow(shifted_penobscot, cmap='viridis', interpolation='nearest', vmin=0, vmax=255)
plt.title('Penobscot County')
plt.colorbar()

plt.tight_layout()

## Saving visual to the desktop

plt.savefig('~/Desktop/visual.png')

## Do you notice any stark differences between the two counties?

## Using Boolean masking, identify any industries in the space time cube from #5 that are above the expected share of the workforce

expected_share = np.sum(spacetime_cube) / 13
above_expected_share = spacetime_cube > expected_share

with open('~/Desktop/answers.txt', 'w') as file:
    file.write('Total workers per year per industry:\n')
    file.write(np.array2string(total_workers_per_year))
    file.write('\n\nAverage workers per county per industry over the 12-year period:\n')
    file.write(np.array2string(average_workers_per_county_industry))
    file.write('\n\nExpected share of workforce:\n')
    file.write(str(expected_share))
    file.write('\n\nIndustries above expected share of workforce:\n')
    file.write(np.array2string(above_expected_share))
