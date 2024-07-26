import streamlit as st

pg = st.navigation([
    st.Page("app.py", title="Portfolio", icon=":material/home:"),
    st.Page("demo.py", title="Demo", icon=":material/deployed_code:"),
])
pg.run()

