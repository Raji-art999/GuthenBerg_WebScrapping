import os
import csv
import nltk
# nltk.download('punkt')
from nltk.tokenize import word_tokenize
# Define the directory containing the text files
folder_path = "/Users/sundaramrajashree/PycharmProjects/Webscraping/Gutenberg books"


# Function to read a text file, get its length, and save the result to a CSV file
def process_text_file(file_path, csv_writer):
    with open(file_path, 'r') as file:
        text = file.read()
        # Get the length of the text
        tokens = word_tokenize(text)
        text_length = len(tokens)
        ### save the text_length 
        
        # Get the file name without the extension
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        # Write the data to the CSV file
        csv_writer.writerow([file_name, text_length])


# Create a CSV file for storing the results
csv_file_name = "text_lengths.csv"
with open(csv_file_name, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write headers to the CSV file
    csv_writer.writerow(["File Name", "Text Length"])

    # List all files in the specified directory
    file_list = os.listdir(folder_path)

    # Process each text file in the directory
    for file_name in file_list:
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            process_text_file(file_path, csv_writer)
            print(f"Processed {file_name}")

print(f"Processing complete. Results saved to {csv_file_name}.")
