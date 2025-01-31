from dataclasses import dataclass
import streamlit as st

@dataclass
class Point:
    x: int
    y: int

def move_point():
    st.session_state.point.x += 1
    point.x += 1


point = Point(10,10)
if 'point' not in st.session_state:
    st.session_state.point = Point(0,0)

st.info('### Session state')
st.info(point)
st.code(str(st.session_state), language=None)
st.button('Move point', on_click=move_point)
