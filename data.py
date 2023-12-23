import pandas as pd
import pymongo
import streamlit as st
import plotly.express as plt
from streamlit_option_menu import option_menu
from PIL import Image

icon = Image.open("air_bnb.png")
st.set_page_config(page_title="Airbnb Data Visualization",
                   page_icon=icon,
                   layout="wide",
                   initial_sidebar_state="expanded")

with st.sidebar:
    selected = option_menu(
                menu_title="Menu", 
                options=["Home", "Overview","Explore"],
                icons=["house","clipboard-data", "compass"],
                default_index=0,
                styles={"nav-link": {"--hover-color": "#00A699"},
                                   "nav-link-selected": {"background-color": "#FF5A5F"}}
                           )


client = pymongo.MongoClient(f"mongodb+srv://jaiganeshmohan:jaiganesh@cluster0.aadmud7.mongodb.net/?retryWrites=true&w=majority")
db = client.sample_airbnb
col = db.listingsAndReviews

df = pd.read_csv('Airbnb_data.csv')


col1, col2 = st.columns([0.13, 0.87], gap='small')
col1.image("air_bnb.png", width=200)
col2.title = '<p style="font-family:roboto; color:#00A699; font-size: 48px;">Welcome to AirBnB Dashboard</p>'
st.markdown(col2.title, unsafe_allow_html=True)


# HOME PAGE
if selected == "Home":
    
    st.markdown("__<p> Analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, "
        "develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, "
        "availability patterns, and location-based trends. </p>__",unsafe_allow_html=True)

    
# OVERVIEW PAGE
if selected == "Overview":

    selected_tab = option_menu(None, ["Airbnb Data", "Insights"],
                               default_index=0,
                               orientation="horizontal",
                               styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px","--hover-color": "#00A699"},
                                       "nav-link-selected": {"background-color": "#FF5A5F"}})


    if selected_tab == "Airbnb Data":
    
        if st.button("Click to view Airbnb Data"):
            st.write(df)

    if selected_tab == "Insights":

        country = st.sidebar.multiselect('Select a Country', sorted(df.Country.unique()))
        prop = st.sidebar.multiselect('Select Property_type', sorted(df.Property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type', sorted(df.Room_type.unique()))
        price = st.slider('Select Price', df.Price.min(), df.Price.max(), (df.Price.min(), df.Price.max()))

        query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'

        col1, col2 = st.columns(2, gap='medium')

        with col1:
            # TOP 10 PROPERTY TYPES BAR CHART
            df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(
                by='Listings', ascending=False)[:10]
                       
            fig = plt.bar(df1,
                         title='Top 10 Property Types',
                         x='Listings',
                         y='Property_type',
                         orientation='h',
                         color='Property_type',
                         color_continuous_scale=plt.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)

            # TOP 10 HOSTS BAR CHART
            df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings',
                                                                                                         ascending=False)[
                  :10]
            fig = plt.bar(df2,
                         title='Top 10 Hosts with Highest number of Listings',
                         x='Listings',
                         y='Host_name',
                         orientation='h',
                         color='Host_name',
                         color_continuous_scale=plt.colors.sequential.Agsunset)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
            df1 = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")
            fig = plt.pie(df1,
                         title='Total Listings in each Room types',
                         names='Room_type',
                         values='counts',
                         color_discrete_sequence=plt.colors.sequential.Rainbow
                         )
            fig.update_traces(textposition='outside', textinfo='value+label')
            st.plotly_chart(fig, use_container_width=True)

            # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
            country_df = df.query(query).groupby(['Country'], as_index=False)['Name'].count().rename(
                columns={'Name': 'Total_Listings'})
            fig = plt.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='Country',
                                locationmode='country names',
                                color='Total_Listings',
                                color_continuous_scale=plt.colors.sequential.Plasma
                                )
            st.plotly_chart(fig, use_container_width=True)

if selected == "Explore":
    
    a = '<p style="font-family:sans serif; color:#00A699; font-size: 30px;">Explore more about the Airbnb data...</p>'
    st.markdown(a, unsafe_allow_html=True)

    country = st.sidebar.multiselect('Select a Country', sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type', sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type', sorted(df.Room_type.unique()))
    price = st.slider('Select Price', df.Price.min(), df.Price.max(), (df.Price.min(), df.Price.max()))

    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'

    b = '<p style="font-family:sans serif; color:#00A699; font-size: 25px;"><em><b>Price Analysis</b></em></p>'
    st.markdown(b, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap='medium')

    with col1:
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(query).groupby('Room_type', as_index=False)['Price'].mean().sort_values(by='Price')
        fig = plt.bar(data_frame=pr_df,
                     x='Room_type',
                     y='Price',
                     color='Price',
                     title='Avg Price for each Room type'
                     )
        st.plotly_chart(fig, use_container_width=True)

        c = '<p style="font-family:sans serif; color:#00A699; font-size: 25px;"><em><b>Availability Analysis></b></em></p>'
        st.markdown(c, unsafe_allow_html=True)

        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = plt.box(data_frame=df.query(query),
                     x='Room_type',
                     y='Availability_365',
                     color='Room_type',
                     title='Availability by Room type'
                     )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # AVG PRICE IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country', as_index=False)['Price'].mean()
        fig = plt.scatter_geo(data_frame=country_df,
                             locations='Country',
                             color='Price',
                             hover_data=['Price'],
                             locationmode='country names',
                             size='Price',
                             title='Avg Price in each Country',
                             color_continuous_scale='agsunset'
                             )
        col2.plotly_chart(fig, use_container_width=True)

        # BLANK SPACE
        st.markdown("#   ")
        st.markdown("#   ")

        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country', as_index=False)['Availability_365'].mean()
        country_df.Availability_365 = country_df.Availability_365.astype(int)
        fig = plt.scatter_geo(data_frame=country_df,
                             locations='Country',
                             color='Availability_365',
                             hover_data=['Availability_365'],
                             locationmode='country names',
                             size='Availability_365',
                             title='Avg Availability in each Country',
                             color_continuous_scale='agsunset'
                             )
        st.plotly_chart(fig, use_container_width=True)
