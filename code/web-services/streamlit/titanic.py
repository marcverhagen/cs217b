import streamlit as st
import pandas as pd

st.set_page_config(layout='wide')

@st.cache_data
def load_data():
    return pd.read_csv(file)

file = "data/titanic.csv"
df = load_data()

minimum_age, maximum_age = st.sidebar.slider(
    'Select age range', 0.0, 100.0, (0.0, 100.0))
gender = st.sidebar.radio("Select gender", ['no selection', 'male', 'female'])
survived = st.sidebar.radio("Survived?", ['no selection', 'yes', 'no'])
pclass = st.sidebar.radio("Class", ['no selection', 'first', 'second', 'third'])

if minimum_age != 0 or maximum_age != 100:
    df = df.loc[df['Age'] >= minimum_age].loc[df['Age'] <= maximum_age]
if gender in ('male', 'female'):
    df = df.loc[df['Sex'] == gender]
if survived != 'no selection':
    df = df.loc[df['Survived'] == 1] if survived == 'yes' else df.loc[df['Survived'] == 0]
if pclass != 'no selection':
    mappings = {'first': 1, 'second': 2, 'third': 3}
    df = df.loc[df['Pclass'] == mappings[pclass]]


st.header('Titanic search')
st.info(f'Matching records: {len(df)}')
st.dataframe(df)
