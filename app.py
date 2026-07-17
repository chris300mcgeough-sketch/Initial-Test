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


st.title("🍺 Christopher's Brewery Dashboard")

volume = st.slider("Today's Volume (HL)", 0, 10000, 5000)

st.metric(
    label="Production Volume",
    value=f"{volume:,} HL"
)

if volume >= 8000:
    st.success("Target achieved!")
else:
    st.warning("Below target.")
