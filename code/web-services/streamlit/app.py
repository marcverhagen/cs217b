import streamlit as st
import pandas as pd
import numpy as np

from model import graph

st.sidebar.markdown('# Letters')
letter = st.sidebar.radio('Pick a letter', ['a', 'b', 'c'])
st.sidebar.info(f'Selected: {letter}')

st.markdown('### Text and Animals')

text  = "Nothing was going on at auntie Bibby's house and then... Ding Dong."
txt = st.text_area('Text to analyze', text)
if st.button('run'):
    st.info(txt.lower())

'---'

if st.button('Show Animals'):
    left, _spacer, right = st.columns([10,1,10])
    left.write('Here is what we have in the zoo')
    table_data = pd.DataFrame(['koalas','ole','dingos', 'rabbits'],[14,5,6,22])
    left.table(table_data)
    left.write('... with an unrelated chart')
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
    left.area_chart(chart_data)
    right.write('And here is an unrelated graph')
    right.graphviz_chart(graph)

