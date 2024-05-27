import qrcode
from io import BytesIO
import streamlit as st
from streamlit_lottie import st_lottie
import json
import wifi_qrcode_generator.generator
from datetime import datetime


# Function to load and display the lottie file
def display_lottiefile(filename):
    # Load the lottie file
    with open(filename, "r") as f:
        lottie_file = json.load(f)
    st_lottie(lottie_file, speed=1, reverse=False, loop=True, quality="high", height=150, width=300, key=None)


# Function to generate text/URL based qrcode
def text_qr_code_generator(qrdata):
    img = qrcode.make(qrdata)
    byte_arr = BytesIO()
    img.save(byte_arr)
    return byte_arr.getvalue()  # Get the byte contents


# Function to generate Wi-Fi password based qrcode. Using this qrcode, password remain hidden and one can connect
# the Wi-Fi network after qrcode scanning
def wifi_qr_code_generator(wifissid, wifipassword):
    qr_code = wifi_qrcode_generator.generator.wifi_qrcode(
        ssid=wifissid, hidden=False, authentication_type='WPA', password=wifipassword)
    img = qr_code.make_image()
    byte_arr = BytesIO()
    img.save(byte_arr)
    return byte_arr.getvalue()  # Get the byte contents


# --- PAGE SETUP ---
# Initialize streamlit app
page_title = "QR Code Generator"
page_icon = "🔢"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout="centered")

# Display the lottie file
display_lottiefile("qr_code_lottie.json")

# Sidebar configuration
st.sidebar.title('Configuration')
st.sidebar.header('Select the QR Code Type')
option = st.sidebar.selectbox('Select the QR code Type', ('Text/URL', 'Wifi Password'), label_visibility='collapsed')

# Initialize variables
qr_data = ''
button_enabled = False
wifi_ssid = ''
wifi_password = ''
if "byte_contents" not in st.session_state:
    st.session_state.byte_contents = None

# Main page configuration
st.title("QR Code Generator")
st.write(":blue[***Quick and easy way to generate QR Codes.***]")
st.subheader(f'Enter {option} for QR Code:')

if option == 'Text/URL':
    qr_data = st.text_input('Enter text/url for QR Code:', label_visibility='collapsed')
    button_enabled = True if qr_data != '' else False
elif option == 'Wifi Password':
    wifi_ssid = st.text_input('Enter Wifi SSID:')
    wifi_password = st.text_input('Enter Wifi Password:', type='password')
    button_enabled = True if wifi_ssid != '' and wifi_password != '' else False

generate = st.button("Generate QR Code", type="primary", disabled=not button_enabled)

if generate:
    if option == 'Text/URL':
        st.session_state.byte_contents = text_qr_code_generator(qr_data)
    elif option == 'Wifi Password':
        st.session_state.byte_contents = wifi_qr_code_generator(wifi_ssid, wifi_password)

if st.session_state.byte_contents is not None:
    st.subheader('Generated QR Code:')
    with st.container(border=True):
        st.image(st.session_state.byte_contents)
        current_time = datetime.now().strftime('%H%M%S')
        st.download_button(label="Download QR Image", type="primary",
                           data=st.session_state.byte_contents,
                           file_name=f"{current_time}_qr_code.png",
                           mime="image/png")
