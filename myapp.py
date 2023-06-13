import streamlit as st
import requests
import PIL.Image
import io


st.title("Product Recommender")

product_id = st.text_input("Enter a product id")

if product_id:
    response = requests.get(f"http://localhost:8000/{product_id}")
    data = response.json()
    if "Error" in data:
        st.error(data["Error"])
    else:
        st.write(f"Recommendations for {product_id}:")
        for item in data:
            st.markdown(f"- {item['product_title']} ({item['similarity']})")

# Get the product title and category from the user
product_title = st.text_input("Enter a product title")
category = st.selectbox("Select a category", ["casual button down shirts", "other"])

# Define a variable that holds the URL of the default or placeholder image
default_image_url = "https://via.placeholder.com/200x200?text=No+Image"

if product_title and category:
    # Send a POST request to the FastAPI endpoint with the user input as JSON data
    response = requests.post(f"http://localhost:8000/{product_title}/{category}", json={"product_title": product_title, "category": category})
    data = response.json()
    if "Error" in data:
        st.error(data["Error"])
    else:
        st.write(f"Recommendations for {product_title} - {category}:")
        for item in data:
            # Check if the product_img_url field is present and valid
            if "imgurl" in item and item["imgurl"]:
                try:
                    # Get the image data from the product_img_url field
                    img_data = requests.get(item["imgurl"]).content
                    # Convert the image data to a bytes object
                    img_bytes = io.BytesIO(img_data)
                    # Open the image from the bytes object
                    img = PIL.Image.open(img_bytes)
                except Exception as e:
                    # If there is an exception, use the default or placeholder image instead
                    #st.warning(f"Failed to load or display image:")
                    img_data = requests.get(default_image_url).content
                    img_bytes = io.BytesIO(img_data)
                    img = PIL.Image.open(img_bytes)
            else:
                # If there is no valid product_img_url field, use the default or placeholder image instead
                st.error(f"No valid image URL found for {item['product_title']}")
                img_data = requests.get(default_image_url).content
                img_bytes = io.BytesIO(img_data)
                img = PIL.Image.open(img_bytes)
            # Display the image, title, and similarity score in a column layout
            col1, col2 = st.columns(2)
            with col1:
                st.image(img, width=200)
            with col2:
                st.markdown(f"- {item['product_title']} ({item['similarity']})")