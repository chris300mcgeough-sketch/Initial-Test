import streamlit as st 
st.title("Christophers Weebsite")
st.write("my first website")
name=st.text_input("Enter your name")

if name:
  st.success(f"Hello {name}")
