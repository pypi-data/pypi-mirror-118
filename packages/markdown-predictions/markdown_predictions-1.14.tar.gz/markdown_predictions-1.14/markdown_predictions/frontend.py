import streamlit as st

import numpy as np
import pandas as pd
from markdown_predictions.trainer import get_data

'''
# Markdown Selection Tool
'''

file_csv = st.file_uploader("Upload your CSV here", type=([".csv"]))

if file_csv:
    # TODO: Replace with get_data function from markdown_predictions.trainer
    df = pd.read_csv(file_csv)
    df
    # TODO: Fill out remainng summary items once get_data is implemented
    st.text('CSV Summary')
    num_products = f'Number of products: {len(df)}'
    num_products

if st.button('Set Markdowns'):
    pass

number = st.number_input('Choose a markdown', min_value=0, max_value = 50, step=10, value=0)
st.write('The current number is ', number)
