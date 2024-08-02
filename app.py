import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(layout="wide")

countries_page = requests.get('https://data.worldbank.org/country')
countries_contents = BeautifulSoup(countries_page.text, 'html.parser')
countries = countries_contents.select('section.nav-item > ul > li')
countries = [country.text.strip() for country in countries]

def fetch_data(url):

    dt = {
    # Social
    'Poverty headcount ratio at $2.15 a day (2017 PPP) (% of population)' : {'type': 'Social', 'value': '', 'year': '', 'href': ''},
    'Life expectancy at birth, total (years)' : {'type': 'Social', 'value': '', 'year': '', 'href': ''},
    'Population, total' : {'type': 'Social', 'value': '', 'year': '', 'href': ''},
    'Population growth (annual %)' : {'type': 'Social', 'value': '', 'year': '', 'href': ''},
    'Net migration' : {'type': 'Social', 'value': '', 'year': '', 'href': ''},
    'Human Capital Index (HCI) (scale 0-1)' : {'type': 'Social', 'value': '', 'year': '', 'href': ''},

    # 'Economic'
    'GDP (current US$)': {'type': 'Economic', 'value': '', 'year': '', 'href': ''},
    'GDP per capita (current US$)' : {'type': 'Economic', 'value': '', 'year': '', 'href': ''},
    'GDP growth (annual %)' : {'type': 'Economic', 'value': '', 'year': '', 'href': ''},
    'Unemployment, total (% of total labor force) (modeled ILO estimate)' : {'type': 'Economic', 'value': '', 'year': '', 'href': ''},
    'Inflation, consumer prices (annual %)' : {'type': 'Economic', 'value': '', 'year': '', 'href': ''},
    'Personal remittances, received (% of GDP)' : {'type': 'Economic', 'value': '', 'year': '', 'href': ''},

    # 'Environment'
    'CO2 emissions (metric tons per capita)' : {'type': 'Environment', 'value': '', 'year': '', 'href':''},
    'Forest area (% of land area)' : {'type': 'Environment', 'value': '', 'year': '', 'href':''},
    'Access to electricity (% of population)' : {'type': 'Environment', 'value': '', 'year': '', 'href':''},
    'Annual freshwater withdrawals, total (% of internal resources)' : {'type': 'Environment', 'value': '', 'year': '', 'href':''},
    'Electricity production from renewable sources, excluding hydroelectric (% of total)' : {'type': 'Environment', 'value': '', 'year': '', 'href':''},
    'People using safely managed sanitation services (% of population)' : {'type': 'Environment', 'value': '', 'year': '', 'href':''},

    # 'Institutions'
    'Intentional homicides (per 100,000 people)': {'type': 'Institutions', 'value': '', 'year': '', 'href': ''},
    'Central government debt, total (% of GDP)': {'type': 'Institutions', 'value': '', 'year': '', 'href': ''},
    'Statistical performance indicators (SPI): Overall score (scale 0-100)': {'type': 'Institutions', 'value': '', 'year': '', 'href': ''},
    'Individuals using the Internet (% of population)': {'type': 'Institutions', 'year': '', 'value': '', 'href': ''},
    'Proportion of seats held by women in national parliaments (%)': {'type': 'Institutions', 'value': '', 'year': '', 'href': ''},
    'Foreign direct investment, net inflows (% of GDP)': {'type': 'Institutions', 'value': '', 'year': '', 'href': ''},
    }

    page = requests.get(url)
    contents = BeautifulSoup(page.text, 'html.parser')
    indicators = contents.select('.indicator-item > .indicator-item__wrapper > .indicator-item__inner')
    
    for i in indicators:
        indicator_name = i.find('div', class_='indicator-item__title')
        indicator_value = i.find('div', class_='indicator-item__data-info')
        indicator_year = i.find('p', class_='indicator-item__data-info-year')

        indicator_name = indicator_name.text.strip()
        indicator_value = 'No data available' if indicator_value is None else indicator_value.text.strip()
        indicator_year = None if indicator_year is None else indicator_year.text.strip()

        href = i.find('a').get('href')
        href = 'https://data.worldbank.org' + href

        if indicator_name in ['GDP (current US$)current US$constant US$current LCUconstant LCU', 'GDP per capita (current US$)current US$constant US$current LCUconstant LCU']:
            indicator_name = indicator_name[:indicator_name.find('$')].strip()+'$)'

        dt[indicator_name]['value'] = indicator_value
        dt[indicator_name]['year'] = indicator_year
        dt[indicator_name]['href'] = href

    return dt


def display_data(data, country, type):
    for ind in data[country]:
        if data[country][ind]['type'] == type:
            value = data[country][ind]['value']
            year = data[country][ind]['year']
            href = ' - [source](' + data[country][ind]['href'] + ')' if value != 'No data available' else ''
            
            st.markdown(f"- {ind} {href} \n {value} {'' if year is None else year}")

country1 = st.sidebar.selectbox("Please select a country name", countries, key='country1')
url1 = f"https://data.worldbank.org/country/{country1}"

compare_country = st.sidebar.checkbox('Compare Countries', value=False)

country2 = None
if compare_country:
    country2 = st.sidebar.selectbox("Please select a country name", countries, key='country2')
    url2 = f"https://data.worldbank.org/country/{country2}"


if st.sidebar.button("Submit"):
    data = {country1: ''}

    if country2:

        if country2 == country1:
            st.error('Please make sure to select two different country names')
        else:
            data[country1] = fetch_data(url1)
            data[country2] = fetch_data(url1)

            col1, col2 = st.columns(2)
            with col1:
                st.header(country1)

                st.subheader('Social')
                display_data(data, country1, 'Social')

                st.header('Environment')
                display_data(data, country1, 'Environment')

                st.header('Economic')
                display_data(data, country1, 'Economic')

                st.header('Institutions')
                display_data(data, country1, 'Institutions')
            with col2:
                st.header(country2)

                st.subheader('Social')
                display_data(data, country2, 'Social')

                st.header('Environment')
                display_data(data, country2, 'Environment')

                st.header('Economic')
                display_data(data, country2, 'Economic')

                st.header('Institutions')
                display_data(data, country2, 'Institutions')
            
            with st.expander('Data in json format:'):
                st.json(data)

    else:
        data[country1] = fetch_data(url1)

        col1, col2 = st.columns(2)

        with col1:
            st.header('Social')
            display_data(data, country1, 'Social')

            st.write('----------------------------------------------------------------')
            st.header('Environment')
            display_data(data, country1, 'Environment')

        with col2:
            st.header('Economic')
            display_data(data, country1, 'Economic')

            st.write('----------------------------------------------------------------')
            st.header('Institutions')
            display_data(data, country1, 'Institutions')
    
        with st.expander('Data in json format:'):
            st.json(data)

else:
    with st.expander('---', expanded=True):
        st.markdown(
            """
            I have developed this app for learning purposes only.\n
            It takes a country name (or two countries for comparison purposes) as input and returns the most recent values of social, economic, and environmental indicators from the World Bank (https://data.worldbank.org/country).\n
            The source code is publicly available on my [GitHub](https://github.com/Fahim-Ahmad/wb_indicators) account for anyone who is interested.
            """
        )

# execute 'streamlit run app.py' in terminal to run the app
# execute 'pip freeze > requirements.txt' to generate the requirements file