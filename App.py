import os
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from google import genai
from PIL import Image

# --- Activity 1: Load the Gemini Pro API and Configure ---
# Load Environment Variables
load_dotenv()

# Configure Google Generative AI
try:
    # Ensure the GOOGLE_API_KEY is available in the environment
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Error: GOOGLE_API_KEY not found in environment variables. Please check your .env file.")

    # Initialize the client
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

except Exception as e:
    st.error(f"Error configuring Google Generative AI: {e}")
    st.stop()


# --- Activity 3: Implement a function to read the Image and set the image format ---
def input_image_setup(uploaded_file):
    """
    Reads the uploaded image file and converts it into the format
    required for the Gemini Pro Vision model input.
    """
    if uploaded_file is not None:
        # Read the image as bytes
        bytes_data = uploaded_file.getvalue()

        # Open image using PIL to confirm it's a valid image
        try:
            Image.open(BytesIO(bytes_data))
        except IOError:
            st.error("Error: The uploaded file is not a valid image.")
            return None

        # Prepare the list of parts for the API call
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # e.g., "image/jpeg"
                "data": bytes_data,
            }
        ]
        return image_parts

    # Raising an error as described in the plan, though a Streamlit warning is friendlier
    raise FileNotFoundError("No file uploaded")


# --- Activity 2: Implement a function to get gemini response ---
def get_gemini_response(input_text, image_parts, prompt):
    """
    Interacts with the Gemini Pro Vision model to generate a description.
    """
    # Use gemini-pro-vision for multimodal input (text and image)
    model = genai.GenerativeModel("gemini-pro-vision")

    # The generate_content call expects a list of parts (text, image, prompt)
    # The input_text and prompt are also passed as strings in the list.
    response = model.generate_content([input_text, image_parts[0], prompt])

    return response.text


# --- Activity 4: Write a prompt for gemini model ---
# This detailed prompt is passed to the model along with the user's input text and image.
input_prompt = """
You are an expert Civil Engineer AI assistant. Analyze the provided image of a civil engineering structure.
Based on the image and the user's input text, provide a detailed description including the following elements:
1.  **Structure Type:** (e.g., residential building, beam bridge, truss, retaining wall)
2.  **Primary Materials Used:** (e.g., reinforced concrete, steel, brick, timber)
3.  **Key Structural Elements:** (e.g., columns, beams, trusses, foundation type if visible)
4.  **Construction Method/Phase:** (e.g., concrete pouring in progress, steel frame erection, completed structure)
5.  **Notable Features or Engineering Challenges:** (e.g., unique cantilever design, signs of corrosion, heavy-duty shoring)
Format your response clearly using bullet points for each section.
"""


# --- Milestone 4: Model Deployment (Activities 1 & 2) ---

# Initialize Streamlit App
st.set_page_config(page_title="Civil Engineering Insight Studio", layout="wide")
st.header("Civil Engineering Insight Studio")

# User Input Fields
input_text = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display Uploaded Image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit Button
submit = st.button("Describe Structure")

# Process User Input and Generate Description
if submit:
    if uploaded_file is not None:
        try:
            # Get image parts formatted for the model
            image_parts = input_image_setup(uploaded_file)

            if image_parts:
                with st.spinner("Analyzing structure and generating insight..."):
                    # Get response from the Gemini model
                    response = get_gemini_response(input_text, image_parts, input_prompt)

                st.subheader("Structural Description and Insight")
                st.write(response)

        except FileNotFoundError as e:
            st.warning(str(e))  # "No file uploaded"
        except Exception as e:
            st.error(f"An error occurred during content generation: {e}")

    else:
        st.warning("Please upload an image to describe the structure.")
