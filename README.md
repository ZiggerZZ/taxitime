# Taxi time prediction for Airplanes

The goal of this project is to find a model that will accurately estimate taxi-time of arrivals for a given airport. Taxi-time is the time it takes for an airplane that has landed to arrive at its designated stand. This repository contains the initial preprocessing of the data, the data exploration and the training of the models. 

## Preprocessing

This directory contains the files with the code that preprocesses the raw input data. There are 4 main files:

* [Aircraft Data Processing](preprocessing/aircraft_preprocessing.py): Preprocesses aircraft data and outputs treated data in data/aircraft_data.csv 
* [Airport Data Processing](preprocessing/airport_preprocessing.py): Preprocesses airport data and outputs treated data in data/airport_data.csv
* [Weather Data Processing](preprocessing/weather_preprocessing.py): Preprocesses weather data and outputs treated data in data/weather_data.csv
* [Merge Input Data](preprocessing/merge_all.py): To be run after preprocessing files to merge the three datasets into one large dataframe, output in data/complete_data.csv

## EDA

[EDA](EDA_v2.ipynb): Contains our Exploratory Data Analysis with some of the visuals used in our presentation.

## Training

[Training Experiments](Training_Experiments.ipynb): This is our notebook that we used for testing different models and saving their results. The results in our slides correspond with the work in this file.

[Fuzzy Time Series](fuzzy_time_series/univariate.ipynb): This is the file with the implementation of the fuzzy rules

