import streamlit as st
import cv2
import numpy as np

def cartoonize_image(image, level):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a median blur to reduce noise in the image
    gray = cv2.medianBlur(gray, 3)

    # Apply edge detection to extract the edges in the image
    edges = cv2.Laplacian(gray, cv2.CV_8U, ksize=5)

    # Threshold the edges to create a binary image
    ret, mask = cv2.threshold(edges, level, 255, cv2.THRESH_BINARY_INV)

    # Apply a bilateral filter to smoothen the image while preserving edges
    bilateral = cv2.bilateralFilter(image, 9, 75, 75)

    # Convert the image to an RGB format
    cartoon_rgb = cv2.cvtColor(bilateral, cv2.COLOR_BGR2RGB)

    # Apply the mask to the image to create the cartoon effect with proper RGB colors
    cartoon = cv2.bitwise_and(cartoon_rgb, cartoon_rgb, mask=mask)

    return cartoon

st.title("Anime-Style Cartoon Converter")
st.set_option('deprecation.showfileUploaderEncoding', False)

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    st.image(image, caption='Original Image', use_column_width=True)

    level = st.slider('Cartoon Level', 1, 100, 25)

    if st.button('Cartoonize'):
        cartoon = cartoonize_image(image, level)
        st.image(cartoon, caption='Cartoon Image', use_column_width=True)
