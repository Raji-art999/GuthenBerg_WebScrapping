# import aiohttp
# import asyncio
# from bs4 import BeautifulSoup
#
# # Define the URL to fetch
# url = "https://www.gutenberg.org/browse/scores/top#authors-last30"
#
# # Set up a set to store unique URLs
# unique_links = set()
#
#
# # Function to fetch and parse the HTML content
# async def fetch_and_parse_url(url):
#     async with aiohttp.ClientSession() as session:
#         retry_count = 0
#         while retry_count < 3:  # Retry up to 3 times in case of errors
#             try:
#                 async with session.get(url) as response:
#                     html_content = await response.text()
#                     return html_content
#             except aiohttp.ClientConnectorError as e:
#                 print(f"Error connecting to {url}: {e}")
#                 retry_count += 1
#                 await asyncio.sleep(1)  # Wait before retrying
#         raise Exception(f"Failed to fetch {url} after 3 retries.")
#
#
# # Function to extract links from the HTML content
# def extract_links(html_content):
#     soup = BeautifulSoup(html_content, 'html.parser')
#     links = [a['href'] for a in soup.find_all('a', href=True)]
#     return links
#
#
# # Main function to fetch and process the URL
# async def main(url):
#     html_content = await fetch_and_parse_url(url)
#     links = extract_links(html_content)
#
#     # Filter out the duplicates and add them to the unique_links set
#     unique_links.update(links)
#
#     # Check if we have collected 100 unique links, if so, stop
#     if len(unique_links) >= 100:
#         return
#
#     # Look for the "Next 100" link and follow it
#     next_page_link = None
#     for link in links:
#         if "Next 100" in link:
#             next_page_link = link
#             break
#
#     if next_page_link:
#         next_page_url = f"https://www.gutenberg.org{next_page_link}"
#         await main(next_page_url)
#
#
# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main(url))
#
#     # Save unique links to a text file
#     filename = "unique_links.txt"
#     save_links_to_file(filename, unique_links)
#
#     print(f"Unique links saved to {filename}")
#
# import os
# import requests
# import xml.etree.ElementTree as ET
# import csv
#
# # Define the URL for the Project Gutenberg RDF metadata file
# metadata_url = "https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2"
#
# # Function to download and extract the metadata file
# def download_metadata():
#     response = requests.get(metadata_url)
#     if response.status_code == 200:
#         with open("metadata.tar.bz2", "wb") as file:
#             file.write(response.content)
#         os.system("tar -xvjf metadata.tar.bz2")
#
# # Function to extract and save URLs to a CSV file
# def extract_and_save_urls_to_csv():
#     # Create a list to store URLs
#     urls = []
#
#     # Define the RDF namespace used in the metadata
#     rdf_namespace = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
#                      'pgterms': 'http://www.gutenberg.org/2009/pgterms/'}
#
#     # Parse RDF metadata files and extract URLs
#     for root, _, files in os.walk("cache/epub"):
#         for file in files:
#             if file.endswith(".rdf"):
#                 filepath = os.path.join(root, file)
#                 tree = ET.parse(filepath)
#                 root = tree.getroot()
#                 # Find the 'rdf:about' attribute within the 'pgterms:file' element
#                 file_element = root.find(".//pgterms:file", namespaces=rdf_namespace)
#                 if file_element is not None:
#                     url = file_element.attrib.get('{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', '')
#                     urls.append(url)
#
#     # Save the URLs to a CSV file
#     with open("gutenberg_urls.csv", "w", newline='') as csvfile:
#         fieldnames = ['URL']
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for url in urls:
#             writer.writerow({'URL': url})
#
# if __name__ == "__main__":
#     download_metadata()
#     extract_and_save_urls_to_csv()
#
#


import os
import sqlite3
import requests
import xml.etree.ElementTree as ET
import csv

# Define the URL for the Project Gutenberg RDF metadata file
metadata_url = "https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2"


# Function to download and extract the metadata file
def download_metadata():
    response = requests.get(metadata_url)
    if response.status_code == 200:
        with open("metadata.tar.bz2", "wb") as file:
            file.write(response.content)
        os.system("tar -xvjf metadata.tar.bz2")


# Function to extract and save metadata to a CSV file
def extract_and_save_metadata_to_csv():
    # Create a list to store metadata
    metadata_list = []

    # Define the RDF namespace used in the metadata
    rdf_namespace = {'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
                     'dcterms': 'http://purl.org/dc/terms/',
                     'pgterms': 'http://www.gutenberg.org/2009/pgterms/'}

    # Parse RDF metadata files and extract metadata
    for root, _, files in os.walk("cache/epub"):
        for file in files:
            if file.endswith(".rdf"):
                filepath = os.path.join(root, file)
                tree = ET.parse(filepath)
                root = tree.getroot()

                # Extract metadata fields with checks for existence
                title = root.find(".//dcterms:title", namespaces=rdf_namespace).text if root.find(".//dcterms:title",
                                                                                                  namespaces=rdf_namespace) is not None else ''
                book_type = root.find(".//dcterms:type", namespaces=rdf_namespace).text if root.find(".//dcterms:type",
                                                                                                     namespaces=rdf_namespace) is not None else ''
                language = root.find(".//dcterms:language", namespaces=rdf_namespace).find(".//rdf:value",
                                                                                           namespaces=rdf_namespace).text if root.find(
                    ".//dcterms:language", namespaces=rdf_namespace) is not None else ''
                authors = [author.text for author in
                           root.findall(".//dcterms:creator/pgterms:name", namespaces=rdf_namespace)]
                subject = root.find(".//dcterms:subject", namespaces=rdf_namespace).find(".//rdf:value",
                                                                                         namespaces=rdf_namespace).text if root.find(
                    ".//dcterms:subject", namespaces=rdf_namespace) is not None else ''
                loc = root.find(".//dcterms:subject", namespaces=rdf_namespace).find(".//rdf:value",
                                                                                     namespaces=rdf_namespace).text if root.find(
                    ".//dcterms:subject", namespaces=rdf_namespace) is not None else ''
                bookshelves = [shelf.text for shelf in
                               root.findall(".//dcterms:hasFormat/pgterms:file/pgterms:bookshelf",
                                            namespaces=rdf_namespace)]
                url = root.find(".//pgterms:file", namespaces=rdf_namespace).attrib.get(
                    '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about', '')

                # Append metadata to the list
                metadata_list.append(
                    [title, book_type, language, ', '.join(authors), subject, loc, ', '.join(bookshelves), url])

    # Save the metadata to a CSV file
    with open("gutenberg_metadata_1.csv", "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Type', 'Language', 'Authors', 'Subject', 'LoC', 'Bookshelves', 'URL']
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)
        writer.writerows(metadata_list)


if __name__ == "__main__":
    download_metadata()
    extract_and_save_metadata_to_csv()
