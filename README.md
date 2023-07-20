<!-- ABOUT THE PROJECT -->
## About The Project - Australian Dollar ($AUD) movement

The purpose of this project is to demonstrate the end to end Extract, Transform, Load (ETL) process that is commonly used to build pipelines in data engineering. 

Daily foreign currency (FX) time series data was extracted from an API, data was then transformed using Pandas and then ultimately loaded into local Postgres for visulisation using Microsoft PowerBI.

Using the API from https://apilayer.com/ - I have extracted the 2022 DAILY value of the Australian dollar ($AUD) against five major currencies, they are:

- United States Dollar ($ USD)
- Euro (€ EUR)
- British Pound (£ GBP)
- Canadian Dollar ($ CAD)
- Hong Kong Dollar ($ HKD)

IMAGE

etl.py file represents the complete pipeline

<!-- LIBRARY TOOLKIT -->
## Library & Toolkit Used

-   Python Pandas
-   SQLAlchemy

<!-- TRANSFORMATION -->
## Data Transformations Performed

-   JSON normalisation 
-   Date format change
-   Renaming of data columns
-   Joining of Pandas Dataframes

<!-- VISULISATION -->
## Data Visualisation

PowerBI is connected to Postgres as a direct data source. 

Screenshot below plots the value of $1 Australian Dollar ($AUD) against USD, GBP and HKD.

IMAGE



