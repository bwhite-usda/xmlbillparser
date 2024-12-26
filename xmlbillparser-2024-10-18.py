import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Function to download the XML version of the bill
def download_bill_xml(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to download the bill from {url}")
        return ""

# Function to parse the XML and extract sections and text
def parse_bill_sections(xml_content):
    soup = BeautifulSoup(xml_content, "xml")
    sections = {}
    
    # Assuming sections are marked with <section> or similar tags
    for section in soup.find_all("section"):
        section_num = section.find("num").text if section.find("num") else "Unknown Section"
        section_text = section.get_text()
        sections[section_num] = section_text
    
    return sections

# Updated function to find US Code citations in the XML content
def find_us_code_citations(text):
    # Updated regular expression for US Code citations
    us_code_pattern = r"section\s\d+\sof\stitle\s\d+,\sUnited\sStates\sCode|\b\d+\s*U\.?S\.?C\.?\s*§*\s*\d+\b"
    return re.findall(us_code_pattern, text)

# Function to match citations to sections in the bill
def match_citations_to_sections(sections):
    data = []
    
    for section_num, section_text in sections.items():
        citations = find_us_code_citations(section_text)
        for citation in citations:
            data.append({
                "US Code Citation": citation,
                "Section Number": section_num,
                "Bill Text": section_text[:200]  # limiting the bill text for better readability
            })
    
    return pd.DataFrame(data)

# The updated URL to the XML version of the bill (HR 118-8467)
bill_xml_url = "https://www.govinfo.gov/content/pkg/BILLS-118hr8467ih/xml/BILLS-118hr8467ih.xml"

# Download the XML content of the bill
xml_content = download_bill_xml(bill_xml_url)

# Parse the bill to get sections and their text
sections = parse_bill_sections(xml_content)

# Print sections to verify if they are being parsed correctly
print("Parsed Sections:")
print(sections)

# Match citations to sections
citation_table = match_citations_to_sections(sections)

# Display the DataFrame in the console
print("Citation Table:")
print(citation_table)

# Optionally save the DataFrame to an Excel file
citation_table.to_excel("us_code_citations_by_section.xlsx", index=False)
print("Citation table saved to 'us_code_citations_by_section.xlsx'")
