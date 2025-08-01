# papers_fetcher/parser.py
import xml.etree.ElementTree as ET
from typing import List, Optional

from .models import Paper, Author
from .heuristics import is_company_affiliation

def _get_text(element: ET.Element, path: str) -> Optional[str]:
    """Safely get text content from an XML element."""
    node = element.find(path)
    return node.text if node is not None and node.text else None

def _get_corr_email(article_element: ET.Element) -> Optional[str]:
    """Attempt to find the corresponding author's email."""
    # Emails are often in the affiliation of authors marked as corresponding.
    for author in article_element.findall(".//Author[@ValidYN='Y']"):
        affiliation_info = author.find(".//AffiliationInfo/Affiliation")
        if affiliation_info is not None and affiliation_info.text and "@" in affiliation_info.text:
            # Simple extraction, could be improved with regex
            words = affiliation_info.text.split()
            for word in reversed(words):
                if "@" in word:
                    return word.strip('.,;()[]')
    return None

def parse_pubmed_xml(xml_data: str) -> List[Paper]:
    """
    Parses a string of XML data from PubMed into a list of Paper objects.

    Args:
        xml_data: The XML string returned by the PubMed efetch API.

    Returns:
        A list of Paper objects.
    """
    papers: List[Paper] = []
    if not xml_data:
        return papers

    root = ET.fromstring(xml_data)
    for article_element in root.findall(".//PubmedArticle"):
        pubmed_id = _get_text(article_element, ".//PMID")
        title = _get_text(article_element, ".//ArticleTitle")

        # Handle various date formats
        pub_date_node = article_element.find(".//PubDate")
        if pub_date_node is not None:
            year = _get_text(pub_date_node, "Year")
            month = _get_text(pub_date_node, "Month")
            day = _get_text(pub_date_node, "Day")
            publication_date = f"{year}-{month}-{day}"
        else:
            publication_date = "N/A"

        authors: List[Author] = []
        for author_node in article_element.findall(".//Author"):
            last_name = _get_text(author_node, "LastName")
            fore_name = _get_text(author_node, "ForeName")
            initials = _get_text(author_node, "Initials")
            affiliation = _get_text(author_node, ".//AffiliationInfo/Affiliation")
            authors.append(Author(last_name, fore_name, initials, affiliation))

        email = _get_corr_email(article_element)

        if pubmed_id and title:
            papers.append(Paper(
                pubmed_id=pubmed_id,
                title=title,
                publication_date=publication_date,
                authors=authors,
                corresponding_author_email=email
            ))

    return papers