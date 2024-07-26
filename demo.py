import streamlit as st
from PIL import Image

# Open the image from the specified path
image = Image.open('assets/box_demo.png')

st.image(image, caption='Coming soon', use_column_width=True)

st.write('This is a demo page. It will be updated soon.')