import streamlit as st
import openai
import re
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set up Google Sheets credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)

# Open the specific Google Sheet by its URL
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1WrSrkaNyxlJ4gB_7tc0veIUQk7FikQ01YnEh3Xw9PbE/edit?usp=sharing'
sheet = client.open_by_url(spreadsheet_url).sheet1

# Function to extract and normalize LinkedIn URLs
def extract_linkedin_urls(text):
    # Debug: Print the text to see if it's being received correctly
    print("Input text:", text)

    # Regex pattern to match LinkedIn URLs
    pattern = r'https?://(?:www\.)?linkedin\.com(?:›|\b)/(?:in/|pub/|[\w\-]+)'

    # Find all LinkedIn URLs in the text
    urls = re.findall(pattern, text)

    # Debug: Print the extracted URLs to understand why they might not be captured
    print("Extracted URLs:", urls)

    # Normalize the URLs to the 'https://www.linkedin.com/in/username' format
    normalized_urls = []
    for url in urls:
        # Remove any unwanted characters and normalize the URL format
        url = re.sub(r'\\s\*›\\s\*', '', url)  # Remove '›' and surrounding spaces
        if not url.startswith('https://www.linkedin.com/in/'):
            url = re.sub(r'https?://(?:www\.)?linkedin\.com(?:›|\b)/', 'https://www.linkedin.com/in/', url)
        normalized_urls.append(url)

    print("Normalized URLs:", normalized_urls)

    return normalized_urls

# Function to append URLs to Google Sheet
def append_to_sheet(urls):
    for url in urls:
        sheet.append_row([url])

# Streamlit UI
st.title("KaamBack LinkedIn URL Extractor")
message = st.text_area("Enter your message:")

if st.button("Extract LinkedIn URLs"):
    with st.spinner("Processing..."):
        urls = extract_linkedin_urls(message)
        if urls:
            append_to_sheet(urls)
            st.success("LinkedIn URLs have been extracted and saved to Google Sheet!")
            st.write(urls)
        else:
            st.warning("No LinkedIn URLs found in the message.")
