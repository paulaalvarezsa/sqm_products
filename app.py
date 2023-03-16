import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_csv('data_clean.csv')

price_min_df = int(round(df.Precio.min(), 0))
price_max_df = int(round(df.Precio.max(), 0))

list_categories = ['Champú', 'Jabón']

# Filtro de precio en el sidebar
with st.sidebar:
    price_min, price_max = st.slider("Selecciona un rango de precios:", min_value=price_min_df, max_value=price_max_df, value=(price_min_df, price_max_df))

    # Filtro de orden en el sidebar
    order = st.selectbox("Selecciona un orden:", ["Ascendente", "Descendente"])

    # categories = st.multiselect('Selecciona varias etiquetas', list_categories)

# Filtro de cantidad en el sidebar
# with st.sidebar:
#     quantity = st.number_input("Selecciona una cantidad:", min_value=1, max_value=1000, value=10)

# Converting links to html tags
def path_to_image_html(path):
    return '<img src="' + path + '" width="60" >'

def process_url(url):
    return f'<a href={url}>Visita Página</a>'

@st.cache_resource
def convert_df(input_df, price_min, price_max, order):

    df = input_df.query(f'{price_min} < Precio < {price_max}')

    if order == 'Ascendente':
        df = df.sort_values(by='Precio', ascending=True)
    else:
        df = df.sort_values(by='Precio', ascending=False)

    df = df.set_index('Imagen')

    # mask_categories = df['Categoría'].isin(categories)
    # df = df[mask_categories].copy()

    df = df.to_html(escape=False, formatters={'__index__':path_to_image_html, 'URL': process_url})
    
     # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df

html = convert_df(df, price_min, price_max, order)

st.markdown(
    html,
    unsafe_allow_html=True
)


# Saving the dataframe as a webpage

# st.download_button(
#      label="Download data as HTML",
#      data=html,
#      file_name='output.html',
#      mime='text/html',
#  )