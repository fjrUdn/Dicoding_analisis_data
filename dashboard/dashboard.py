import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime
from pathlib import Path

def create_by_season(df):
    byseason_df = df.groupby(by='season')['cnt'].sum().sort_values(ascending=False).reset_index()
    byseason_df.rename(columns={
        'cnt': 'sum'
    })

    return byseason_df

def create_by_year(df):
    byyear_df = df.groupby(by='yr')['cnt'].sum().sort_values(ascending=False).reset_index()
    byyear_df.rename(columns={
        'cnt': 'sum'
    })

    return byyear_df

def create_by_month(df):
    bymonth_df = df.groupby(by='mnth')['cnt'].sum().sort_values(ascending=False).reset_index()
    bymonth_df.rename(columns={
        'cnt': 'sum',
        'mnth': 'month'
    })

    return bymonth_df

def create_by_day(df):
    byday_df = df.groupby(by='weekday')['cnt'].sum().sort_values(ascending=False).reset_index()
    byday_df.rename(columns={
        'cnt': 'sum'
    })

    return byday_df

def create_by_daily(df):
    bydaily_df = df.groupby(by='dteday')['cnt'].sum().reset_index()

    return bydaily_df

def season(df):
    st.subheader("Best and Worst Performing Season by Number of Sharing Bike\n\n")
 
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
    
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    sns.barplot(x="cnt", y="season", data=df, palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Best Performing Season", loc="center", fontsize=50)
    ax[0].tick_params(axis='y', labelsize=35)
    ax[0].tick_params(axis='x', labelsize=30)
    ax[0].get_xaxis().get_major_formatter().set_scientific(False)
    
    sns.barplot(x="cnt", y="season", data=df.sort_values(by="cnt", ascending=False), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Performing Season", loc="center", fontsize=50)
    ax[1].tick_params(axis='y', labelsize=35)
    ax[1].tick_params(axis='x', labelsize=30)
    ax[1].get_xaxis().get_major_formatter().set_scientific(False)
    
    st.pyplot(fig)

def year(df):
    st.subheader("Customer Demographics")
 
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(20, 10))

        colors = ["#D3D3D3", "#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
        sns.barplot(
            y="cnt", 
            x="yr",
            data=df.sort_values(by="yr", ascending=False),
            palette=colors,
            ax=ax
        )
        ax.set_title("Number of Customer by Year", loc="center", fontsize=50)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.tick_params(axis='x', labelsize=35)
        ax.tick_params(axis='y', labelsize=30)
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(20, 10))
        
        colors = ["#90CAF9"]
    
        sns.barplot(
            y="cnt", 
            x="weekday",
            data=df,
            palette=colors,
            ax=ax
        )
        ax.set_title("Number of Customer by Day", loc="center", fontsize=50)
        ax.set_ylabel(None)
        ax.set_xlabel(None)
        ax.tick_params(axis='x', labelsize=35)
        ax.tick_params(axis='y', labelsize=30)
        st.pyplot(fig)

def month(df):
    plt.figure(figsize=(10, 5))

    colors = ["#72BCD4"]
    sns.barplot(
        y="cnt",
        x="mnth",
        palette=colors,
        data=df,
    )
    plt.title("Number of Bike Sharing by Month", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis="x", labelsize=12)
    st.pyplot(plt)

def day(df):
    st.subheader('Daily Orders')
 
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        df["dteday"],
        df["cnt"],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    
    st.pyplot(fig)

    col1, col2 = st.columns(2)
    
    with col1:
        total_orders = df.cnt.sum()
        format_angka = "{:,}".format(total_orders)
        st.metric("Total orders", value=format_angka)


if __name__ == "__main__":
    sns.set(style="dark")

    st.header("Bike Sharing Dashboard :bike:")

    main_df = pd.read_csv('Data/day_clean.csv')

    datetime_columns = ["dteday"]
    main_df.sort_values(by="dteday", inplace=True)
    main_df.reset_index(inplace=True)
    
    for column in datetime_columns:
        main_df[column] = pd.to_datetime(main_df[column])

    min_date = main_df["dteday"].min()
    max_date = main_df["dteday"].max()
    
    with st.sidebar:
        # Menambahkan logo perusahaan
        st.image("logo.jpg")

        # Mengambil start_date & end_date dari date_input
        start_date, end_date = st.date_input(
            label='Rentang Waktu',min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )
    main_df_filter = main_df[(main_df["dteday"] >= str(start_date)) & 
                (main_df["dteday"] <= str(end_date))]
    
    df_season = create_by_season(main_df_filter)
    df_year = create_by_year(main_df_filter)
    df_month = create_by_month(main_df_filter)
    df_daily = create_by_daily(main_df_filter)

    day(df_daily)
    season(df_season)
    year(main_df_filter)
    month(df_month)

