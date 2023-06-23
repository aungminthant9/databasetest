import streamlit as st
import io
from PIL import Image
import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        myDb = mysql.connector.connect(
            host='localhost',
            database='batch10_ai_project',
            user='root',
            password='12345'
        )
        return myDb
    except Error as e:
        st.error(f"Error connecting to MySQL database: {e}")
        return None

def insert_image(img_name, image_path, myDb):
    try:
        with open(image_path, 'rb') as file:
            image_data = file.read()

        insert_query = "INSERT INTO images (img_name, img) VALUES (%s, %s)"
        with myDb.cursor() as cursor:
            cursor.execute(insert_query, (img_name, image_data))
            myDb.commit()

        st.success("Image inserted successfully!")
    except Error as e:
        st.error(f"Failed to insert image into MySQL table: {e}")

def retrieve_image(myDb):
    try:
        select_query = "SELECT img_name, img FROM images ORDER BY id DESC LIMIT 1"
        with myDb.cursor() as cursor:
            cursor.execute(select_query)
            result = cursor.fetchone()

            if result is not None:
                img_name, image_data = result
                image_file = io.BytesIO(image_data)
                image = Image.open(image_file)
                st.image(image, caption="Retrieved Image")
                st.write("Image Name:", img_name)
            else:
                st.warning("No image found in the database.")
    except Error as e:
        st.error(f"Failed to retrieve image from MySQL table: {e}")

def main():
    st.title("Photo Uploader")

    # Connect to the database
    connection = create_connection()

    # Upload photo
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Save uploaded photo to a temporary file
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
         # Get the image name from the uploaded file
        img_name = uploaded_file.name

        # Insert uploaded photo into the database
        if connection:
            if st.button("Upload Photo"):
                insert_image(img_name, "temp_image.jpg", connection)

    # Retrieve photo from the database
    # Show Photo button
    if st.button("Show Photo"):
        if connection:
            retrieve_image(connection)

    # Close database connection
    if connection:
        connection.close()

if __name__ == '__main__':
    main()