import streamlit as st
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key="AIzaSyBVDDB6cRhJjlcrQNir6wDg2sQmfJpK4lw")

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

def calculate_calories(weight, height, age, gender, goal, target_change_kg, weeks, activity_level):
    # BMR Calculation
    if gender == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    # Activity level multiplier
    activity_multipliers = {
        'sedentary': 1.2,
        'slightly active': 1.375,
        'moderately active': 1.55,
        'very active': 1.725,
        'super active': 1.9
    }
    tdee = bmr * activity_multipliers[activity_level]

    # Adjust TDEE for weight goal
    if goal == 'lose':
        tdee_goal = tdee - (500 * target_change_kg / weeks)
    elif goal == 'gain':
        tdee_goal = tdee + (500 * target_change_kg / weeks)
    else: # maintain
        tdee_goal = tdee

    # Macronutrient distribution
    protein_grams_per_kg = 1.0 # average requirement
    protein_calories = protein_grams_per_kg * weight * 4
    fat_calories = tdee_goal * 0.25 # 25% of total calories
    carb_calories = tdee_goal - protein_calories - fat_calories

    protein_grams = protein_calories / 4
    fat_grams = fat_calories / 9
    carb_grams = carb_calories / 4

    return {
        'calories': tdee_goal,
        'protein': protein_grams,
        'fat': fat_grams,
        'carbs': carb_grams
    }

st.title("Ovqat kaloriyasini aniqlash by Shaxzod AI :)")

weight = st.number_input('Weight (kg)', min_value=0, value=70)
height = st.number_input('Height (cm)', min_value=0, value=175)
age = st.number_input('Age (years)', min_value=0, value=25)
gender = st.selectbox('Gender', options=['male', 'female'])
goal = st.selectbox('Goal', options=['lose', 'gain', 'maintain'])
target_change_kg = st.number_input('Target Change (kg)', value=5)
weeks = st.number_input('Weeks', value=10)
activity_level = st.selectbox('Activity Level', options=['sedentary', 'slightly active', 'moderately active', 'very active', 'super active'])
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

if st.button('Calculate'):
    result = calculate_calories(weight, height, age, gender, goal, target_change_kg, weeks, activity_level)
    st.write('Calories: {:.2f}'.format(result['calories']))
    st.write('Protein: {:.2f} grams'.format(result['protein']))
    st.write('Fat: {:.2f} grams'.format(result['fat']))
    st.write('Carbs: {:.2f} grams'.format(result['carbs']))

submit=st.button("Kaloriylarni ko'rsatish")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----


"""

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("Natija")
    st.write(response)
