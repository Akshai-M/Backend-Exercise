import requests
import re
import csv
import argparse
import xml.etree.ElementTree as ET

# Base URL for PubMed API
PUBMED_API_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

# Keywords for detecting company affiliations
COMPANY_KEYWORDS = ["Inc.", "Ltd.", "Pharma", "Biotech", "Corp.", "Therapeutics", "Laboratories"]
ACADEMIC_KEYWORDS = ["University", "Institute", "College", "Hospital", "School", "Academy"]

def fetch_papers_from_pubmed(query, max_results=5):
    """Fetches research papers from PubMed and extracts relevant author details."""
    
    # Step 1: Search for papers using ESearch
    search_url = f"{PUBMED_API_BASE}esearch.fcgi"
    search_params = {"db": "pubmed", "term": query, "retmax": max_results, "retmode": "json"}
    
    response = requests.get(search_url, params=search_params)
    response.raise_for_status()
    search_data = response.json()
    
    paper_ids = search_data.get("esearchresult", {}).get("idlist", [])
    if not paper_ids:
        print("No papers found for the query.")
        return []

    # Step 2: Fetch details using EFetch to get authors & affiliations
    fetch_url = f"{PUBMED_API_BASE}efetch.fcgi"
    fetch_params = {"db": "pubmed", "id": ",".join(paper_ids), "retmode": "xml"}
    
    response = requests.get(fetch_url, params=fetch_params)
    response.raise_for_status()
    xml_data = response.text

    # Step 3: Extract relevant details
    papers = []
    root = ET.fromstring(xml_data)

    for article in root.findall(".//PubmedArticle"):
        paper_id = article.find(".//PMID").text
        title_elem = article.find(".//ArticleTitle")
        title = title_elem.text if title_elem is not None else "N/A"
        
        authors, company_affiliations, corresponding_email = extract_authors_and_affiliations(article)

        papers.append({
            "PubmedID": paper_id,
            "Title": title,
            "Non-academic Authors": ", ".join(authors) if authors else "N/A",
            "Company Affiliations": ", ".join(company_affiliations) if company_affiliations else "N/A",
            "Corresponding Author Email": corresponding_email or "N/A"
        })

    return papers

def extract_authors_and_affiliations(article):
    """
    Extracts author names, non-academic affiliations, and corresponding author email from XML.
    """
    authors = []
    company_affiliations = []
    corresponding_email = None

    for author in article.findall(".//Author"):
        last_name = author.find("LastName")
        fore_name = author.find("ForeName")
        name = f"{fore_name.text} {last_name.text}" if last_name is not None and fore_name is not None else "Unknown"

        affiliation_elem = author.find(".//Affiliation")
        if affiliation_elem is not None:
            affiliation = affiliation_elem.text
            if any(keyword in affiliation for keyword in COMPANY_KEYWORDS):
                company_affiliations.append(affiliation)
                authors.append(name)

    # Extract corresponding author email (if available)
    email_match = re.search(r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", ET.tostring(article, encoding="unicode"))
    if email_match:
        corresponding_email = email_match.group(1)

    return authors, company_affiliations, corresponding_email

def save_to_csv(data, filename):
    """
    Saves the fetched paper details into a CSV file.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["PubmedID", "Title", "Non-academic Authors", "Company Affiliations", "Corresponding Author Email"])
        writer.writeheader()
        writer.writerows(data)
    print(f"Results saved to {filename}")

def print_results(data):
    """
    Prints the fetched paper details to the console.
    """
    for paper in data:
        print("\n---------------------------------")
        for key, value in paper.items():
            print(f"{key}: {value}")
    print("\n---------------------------------")


def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed and save results to a CSV file.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Filename to save results (if not provided, prints to console)")
    
    args = parser.parse_args()
    papers = fetch_papers_from_pubmed(args.query)

    if papers:
        if args.file:
            save_to_csv(papers, args.file)
        else:
            print_results(papers)
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
