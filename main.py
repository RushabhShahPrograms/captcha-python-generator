import streamlit as st
from captcha.image import ImageCaptcha
from PIL import Image
import random
import string
import io
import time

# generate a random captcha text of len=4 combination of lowercase alphabet plus numerics
def generate_captcha_text(length=4):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

# generate captcha image
def generate_captcha_image(captcha_text):
    image_captcha = ImageCaptcha()
    captcha_image = image_captcha.generate_image(captcha_text)
    return captcha_image

# refresh the captcha
def refresh_captcha():
    st.session_state.captcha_text = generate_captcha_text()
    st.session_state.captcha_time = time.time()

# Streamlit interface
st.title("Captcha Generator")

# inputs
name = st.text_input("Enter your name:")
phone = st.text_input("Enter your phone number:")

# refresh captcha
if 'captcha_text' not in st.session_state or 'captcha_time' not in st.session_state:
    refresh_captcha()

# Check if captcha is expired (valid till 10 seconds)
if time.time() - st.session_state.captcha_time > 10:
    st.warning("Captcha expired, generating a new one.")
    refresh_captcha()

# Generate captcha image
captcha_image = generate_captcha_image(st.session_state.captcha_text)
buf = io.BytesIO()
captcha_image.save(buf, format='PNG')
buf.seek(0)

st.image(buf, caption='Please enter the text above')

user_captcha = st.text_input("Enter the captcha text:")

# Refresh captcha button
if st.button("Refresh Captcha"):
    refresh_captcha()
    st.experimental_rerun()

# Login button
if st.button("Login"):
    if user_captcha == st.session_state.captcha_text:
        st.success("You are logged in!")
        # refresh_captcha()
    else:
        st.error("Incorrect captcha, please try again.")
        refresh_captcha()