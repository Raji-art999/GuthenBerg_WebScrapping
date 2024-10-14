# import os
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
#
# # Load the CSV file containing book information
# csv_file_path = "gutenberg_filtered_metadata copy.csv"  # Update with the correct file path
# df = pd.read_csv(csv_file_path)
#
# # Create a folder to save the books if it doesn't exist
# folder_name = "/Users/sundaramrajashree/PycharmProjects/Webscraping/Gutenberg books"
# os.makedirs(folder_name, exist_ok=True)
#
# # Iterate through the rows of the DataFrame
# for index, row in df.iterrows():
#     book_url = row["URL"]
#     title = row["Title"]
#     author = row["Authors"]
#
#     # Send a request to the book URL
#     response = requests.get(book_url)
#
#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         # Parse the HTML content of the page
#         soup = BeautifulSoup(response.content, "html.parser")
#
#         # Extract all text elements from the page
#         text_elements = soup.find_all(text=True)
#
#         # Combine text elements into the book text
#         book_text = "\n".join(text_elements)
#
#         # Create a file name for the book
#         file_name = f"{title} - {author}.txt"
#         file_path = os.path.join(folder_name, file_name)
#
#         # Save the book text to a text file
#         with open(file_path, "w", encoding="utf-8") as file:
#             file.write(book_text)
#
#         print(f"Book '{title}' by '{author}' saved as '{file_name}' in '{folder_name}' folder.")
#     else:
#         print(f"Failed to retrieve the book from the URL: {book_url}")



import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load the CSV file containing book information
csv_file_path = "gutenberg_filtered_metadata copy.csv"  # Update with the correct file path
df = pd.read_csv(csv_file_path)

# Create a folder to save the books if it doesn't exist
folder_name = "/Users/sundaramrajashree/PycharmProjects/Webscraping/Gutenberg books"
os.makedirs(folder_name, exist_ok=True)

# Iterate through the rows of the DataFrame
for index, row in df.iterrows():
    book_url = row["URL"]
    title = row["Title"]
    author = row["Authors"]

    # Send a request to the book URL
    response = requests.get(book_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract all text elements from the page
        text_elements = soup.find_all(text=True)

        # Combine text elements into the book text
        book_text = "\n".join(text_elements)

        # Create a file name for the book
        file_name = f"{title} - {author}.txt"
        file_path = os.path.join(folder_name, file_name)

        try:
            # Save the book text to a text file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(book_text)

            print(f"Book '{title}' by '{author}' saved as '{file_name}' in '{folder_name}' folder.")
        except FileNotFoundError as e:
            print(f"Failed to save '{file_name}': {str(e)}")
    else:
        print(f"Failed to retrieve the book from the URL: {book_url}")
