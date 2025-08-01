# papers_fetcher/api.py
import requests
from typing import List, Optional

# Base URL for the NCBI Entrez Programming Utilities (E-utilities)
EUTILS_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def search_pubmed(query: str, max_results: int = 20) -> Optional[List[str]]:
    """
    Searches PubMed for a given query and returns a list of PubMed IDs (PMIDs).

    Args:
        query: The search term, using PubMed's advanced query syntax.
        max_results: The maximum number of PMIDs to return.

    Returns:
        A list of PubMed IDs as strings, or None if the API call fails.
    """
    search_url = f"{EUTILS_BASE_URL}esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "usehistory": "y"
    }
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except requests.RequestException as e:
        print(f"Error during PubMed search: {e}")
        return None

def fetch_paper_details(pmids: List[str]) -> Optional[str]:
    """
    Fetches the full details for a list of PubMed IDs in XML format.

    Args:
        pmids: A list of PubMed IDs.

    Returns:
        A string containing the XML data for the papers, or None on failure.
    """
    if not pmids:
        return None

    fetch_url = f"{EUTILS_BASE_URL}efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }
    try:
        response = requests.get(fetch_url, params=params)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching paper details: {e}")
        return None