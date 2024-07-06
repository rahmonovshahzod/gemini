import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# Configure the API key
genai.configure(api_key="AIzaSyAz1PAqnRfAlBoouXxKlUCobn3Fq4RcjUM")

# Define the GenerativeModel
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Streamlit app title
st.title("Yozishmalaringizni sun'iy idrok yordamida davom ettiring")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image
    img = Image.open(uploaded_file)

    # Display the uploaded image
    st.image(img, caption='Uploaded Image', use_column_width=True)

    # Send image and prompt to the Generative AI model
    prompt = "что я могу ей написать? дай мне такой ответ, чтобы ее приятно удивить, и чтобы она была еще лучшего мнения обо мне. пишите на узбекском."
    response = model.generate_content([prompt, img])

    # Display the result
    st.write("Generated Response:")
    st.write(response.text)


