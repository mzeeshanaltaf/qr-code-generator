import qrcode
from io import BytesIO
import streamlit as st
from streamlit_lottie import st_lottie
import json


# Function to load and display the lottie file
def display_lottiefile(filename):
    # Load the lottie file
    with open(filename, "r") as f:
        lottie_file = json.load(f)
    st_lottie(lottie_file, speed=1, reverse=False, loop=True, quality="high", height=150, width=300, key=None)


# --- PAGE SETUP ---
# Initialize streamlit app
page_title = "QR Code Generator"
page_icon = "🔢"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="centered")

# Display the lottie file
display_lottiefile("qr_code_lottie.json")

st.title("QR Code Generator")
st.write(":blue[***Quick and easy way to generate QR Codes.***]")
st.subheader('Enter text/url for QR Code:')
qr_data = st.text_input('Enter text/url for QR Code:', placeholder='E.g: www.google.com', label_visibility='collapsed')
generate = st.button("Generate QR Code", type="primary", disabled=not qr_data)

if generate:
    img = qrcode.make(qr_data)
    byte_arr = BytesIO()
    img.save(byte_arr)
    # Get the byte contents
    byte_contents = byte_arr.getvalue()
    # st.success('QR Code Generated Successfully')
    st.subheader('Generated QR Code:')
    with st.container(border=True):
        st.image(byte_contents)
        st.download_button(label="Download QR Image", type="primary",
                           data=byte_contents,
                           file_name="qr_code.png",
                           mime="image/png")
