import streamlit as st
import pandas as pd
from PIL import Image
import base64
import matplotlib.pyplot as plt
import seaborn as sns


# Adding the title and favicon
im = Image.open("images/favicon.ico")
st.set_page_config(
    page_title="Maveric IQ - IPM Demo",
    page_icon=im,
    layout="wide",
)

st.title("Maveric IQ - IPM  Demo")

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

ipm_logo = add_logo(logo_path="images/IPM logo.png", width=200, height=60)
st.sidebar.image( ipm_logo)

maveric_logo = add_logo(logo_path="images/MIQ-Logo.png", width=200, height=110)
st.sidebar.image( maveric_logo)

# Data parsing and showing it on the webpage.

def scrub_data():
    data = pd.read_excel("client_data.xlsx")
    data["date"] = pd.to_datetime(data['date'])
    data["datetime"] =  data['date'] + pd.to_timedelta(data['period'].str.split('-').str[0] + ':00')
    data.set_index('datetime', inplace=True)

    daily_data = data.resample('D').sum(numeric_only=True)
    monthly_data = data.resample('ME').sum(numeric_only=True)
    bi_monthly_data = data.resample('2ME').sum(numeric_only=True)
    return data, daily_data, monthly_data, bi_monthly_data

data, daily_data, monthly_data, bi_monthly_data = scrub_data()

def line_plots():
    fig = plt.figure(figsize=(14, 7))

    # Daily consumption
    plt.subplot(3, 1, 1)
    sns.lineplot(data=daily_data, x=daily_data.index, y='consumption（kWh）')
    plt.title('Daily Consumption')
    plt.xlabel('Date')
    plt.ylabel('Consumption (kWh)')

    # Monthly consumption
    plt.subplot(3, 1, 2)
    sns.lineplot(data=monthly_data, x=monthly_data.index, y='consumption（kWh）')
    plt.title('Monthly Consumption')
    plt.xlabel('Date')
    plt.ylabel('Consumption (kWh)')

    # Bi-monthly consumption
    plt.subplot(3, 1, 3)
    sns.lineplot(data=bi_monthly_data, x=bi_monthly_data.index, y='consumption（kWh）')
    plt.title('Bi-Monthly Consumption')
    plt.xlabel('Date')
    plt.ylabel('Consumption (kWh)')

    plt.tight_layout()
    st.pyplot(fig)

st.subheader("Cumulative Daily, Monthly and Bi-Monthly Consumption")
line_plots()


def spread_outlines():
    # Spread and outlier of data
    fig = plt.figure(figsize=(14, 7))
    sns.boxplot(x=monthly_data.index, y='consumption（kWh）', data=monthly_data)
    plt.title('Montly Consumption Distribution')
    plt.xlabel('Date')
    plt.ylabel('Consumption (kWh)')
    st.pyplot(fig)

st.subheader("Spread and Outliers in the Data (if any)")
spread_outlines()

def pie_chart():
    fig = plt.figure(figsize=(30, 25))
    daily_sum = daily_data['consumption（kWh）'].sum()
    daily_data['percentage'] = (daily_data['consumption（kWh）'] / daily_sum) * 100
    plt.pie(daily_data['percentage'], labels=daily_data.index, autopct='%1.1f%%')
    plt.title('Daily Consumption Proportion')
    st.pyplot(fig)

st.subheader("Daily Consumption Proportion")
pie_chart()

def pie_chart_monthly():
    fig = plt.figure(figsize=(20, 7))
    monthly_sum = monthly_data['consumption（kWh）'].sum()
    monthly_data['percentage'] = (monthly_data['consumption（kWh）'] / monthly_sum) * 100
    plt.pie(monthly_data['percentage'], labels=monthly_data.index, autopct='%1.3f%%')
    plt.title('Monthly Consumption Proportion')
    st.pyplot(fig)

st.subheader("Monthly Consumption Proportion")
pie_chart_monthly()

def consumption_scatter_plot():
    fig = plt.figure(figsize=(14, 7))
    sns.scatterplot(x='date', y='consumption（kWh）', data=data)
    plt.title('Consumption Scatter Plot')
    plt.xlabel('Date')
    plt.ylabel('Consumption (kWh)')
    st.pyplot(fig)

st.subheader("Consumption Scatter Plot")
consumption_scatter_plot() 

def daily_consumption_area_chart():
    fig = plt.figure(figsize=(14, 7))
    plt.fill_between(daily_data.index, daily_data['consumption（kWh）'], color="green", alpha=0.4)
    plt.plot(daily_data.index, daily_data['consumption（kWh）'], color="Slateblue", alpha=0.6)
    plt.title('Daily Consumption Area Chart')
    plt.xlabel('Date')
    plt.ylabel('Consumption (kWh)')
    st.pyplot(fig)

st.subheader("Daily Consumption Area Chart")
daily_consumption_area_chart()

def monthly_consumption_area_chart():
    fig = plt.figure(figsize=(14, 7))
    plt.fill_between(monthly_data.index, monthly_data['consumption（kWh）'], color="green", alpha=0.4)
    plt.plot(monthly_data.index, monthly_data['consumption（kWh）'], color="Slateblue", alpha=0.6)
    plt.title('Monthly Consumption Area Chart')
    plt.xlabel('Date')
    plt.ylabel('Consumption (kWh)')
    st.pyplot(fig)

st.subheader("Monthly Consumption Area Chart")
monthly_consumption_area_chart()



