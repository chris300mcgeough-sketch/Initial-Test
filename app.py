import streamlit as st 
st.title("Christophers Website")
st.write("my first website")
name=st.text_input("Enter your name")

if name:
  st.success(f"Hello {name}")
x=10
if x==10:
  st.write(x)
else:
  st.write("else")
