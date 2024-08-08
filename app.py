# required packages
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(layout="wide")

# custom functions
def fetch_data(country):
    url = f'https://data.worldbank.org/country/{country}'
    page = requests.get(url)
    contents = BeautifulSoup(page.text, 'html.parser')
    indicator_items = contents.select('.indicator-item')

    dt = {country: {}}
    for i in indicator_items:
        type = i.find('h1').text.strip()

        i_inner = i.find_all(class_='indicator-item__inner')
        for ii in i_inner:
            name = ii.find('div', class_='indicator-item__title')
            value = ii.find('div', class_='indicator-item__data-info')
            year = ii.find('p', class_='indicator-item__data-info-year')
            href = ii.find('a')
            
            name = '' if name is None else name.text.strip()
            value = 'No data available' if value is None else value.text.strip()
            year = '' if year is None else year.text.strip()
            href = '' if href is None else f"https://data.worldbank.org{href.get('href')}"

            if name in ['GDP (current US$)current US$constant US$current LCUconstant LCU', 'GDP per capita (current US$)current US$constant US$current LCUconstant LCU']:
                    name = name[:name.find('$')].strip()+'$)'
            
            dt[country][name] = {'type': type, 'value': value, 'year': year, 'href': href}

    return(dt)

# df = fetch_data('afghanistan')
# df = {}
# for country in ["Afghanistan", "Algeria", "Andorra", "American-Samoa"]:
#     df.update(fetch_data(country))

def display_data(df, category):
    text = ""

    for cnt in df.keys():
        sub_df = df[cnt]
        
        if (len(df.keys())) > 1:
            text = f"{text}<div><h4 class='country-name'>{cnt}</h4>"
        else:
            text = f"{text}<div>"

        text = f"{text}<ul>"

        for ind in sub_df.keys():
            if sub_df[ind]['type'] == category:
            
                name = f"<span class='indicator-name'>{ind}</span>"
                year = f"<span class='year'>{sub_df[ind]['year']}</span>"
                value = sub_df[ind]['value']
                href = sub_df[ind]['href']
                
                source = f"[<span class='href'><a href='{href}'>source</a></span>]" if value != "No data available" else ''
                value = f"<span class='value'>{value}</span>" if value != "No data available" else "<span class='no-data'>No data available</span>"

                text = f"{text} <li>{name} {source}<br>{value} {year if value != 'No data available' else ''} </li>"

        text = f"{text}</ul></div>"
    
    return(text)

# display_data(df, 'Social')
# display_data({'Afghanistan': df['Afghanistan']}, 'Social')

# custom styling
st.markdown(
    """
    <style>
    .box {
        max-height: 40vh;
        overflow-y: auto;
    }

    .value {
        font-size: 24px;
        font-weight: bold;
    }
    
    .no-data {
        color: orange;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

box = """
    <div class="box">
        {content}
    </div>
"""

# streamlit

countries_page = requests.get('https://data.worldbank.org/country')
countries_contents = BeautifulSoup(countries_page.text, 'html.parser')
countries = countries_contents.select('section.nav-item > ul > li')
countries = [country.text.strip() for country in countries]

col1, col2, col3 = st.columns([2, 3, 2])
with col2:
    countries = st.multiselect('', countries,  key='countries')
    countries = [country.replace(" ", "-") for country in countries]
    fetch_btn = st.button("Fetch")

if fetch_btn and len(countries)>0:
    
    df = {}
    for country in countries:
        df.update(fetch_data(country))
    
    # st.json(df)

    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            with st.expander('Social', expanded=True):
                # st.markdown(display_data(df, 'Social'), unsafe_allow_html=True)
                st.markdown(f"<div class='box'>{display_data(df, 'Social')}</div>", unsafe_allow_html=True)

        with st.container():
            with st.expander('Environment', expanded=True):
                st.markdown(f"<div class='box'>{display_data(df, 'Environment')}</div>", unsafe_allow_html=True)

    with col2:
        with st.container():
            with st.expander('Economic', expanded=True):
                st.markdown(f"<div class='box'>{display_data(df, 'Economic')}</div>", unsafe_allow_html=True)
        
        with st.container():
            with st.expander('Institutions', expanded=True):
                st.markdown(f"<div class='box'>{display_data(df, 'Institutions')}</div>", unsafe_allow_html=True)

else:
    with st.expander('', expanded=True):
        st.markdown(
            """
            Hello, my name is Fahim.\n
            I have developed this app for learning purposes only.
            It takes a country name (or two countries for comparison purposes) as input and returns the most recent values of social, economic, and environmental indicators from the World Bank (https://data.worldbank.org/country).\n
            The source code is publicly available on my [GitHub](https://github.com/Fahim-Ahmad/wb_indicators) account for anyone who is interested.
            """
        )

# execute 'streamlit run app.py' in terminal to run the app
# execute 'pip freeze > requirements.txt' to generate the requirements file