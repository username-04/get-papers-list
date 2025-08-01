# papers_fetcher/heuristics.py
from typing import Tuple

# Keywords that strongly suggest a corporate or commercial entity.
COMPANY_KEYWORDS = [
    "inc", "ltd", "llc", "corp", "pharmaceuticals", "pharma",
    "biotech", "therapeutics", "diagnostics", "labs", "group",
    "solutions", "ag", "gmbh"
]

# Keywords that suggest an academic or non-profit research institution.
ACADEMIC_KEYWORDS = [
    "university", "college", "institute", "hospital", "school of medicine",
    "research center", "foundation", "nhs", "nih", "medical center"
]

def is_company_affiliation(affiliation: str) -> bool:
    """
    Applies heuristics to determine if an affiliation is from a company.

    Args:
        affiliation: The affiliation string of an author.

    Returns:
        True if the affiliation is likely a company, False otherwise.
    """
    if not affiliation:
        return False

    lower_affiliation = affiliation.lower()

    # Rule 1: If any academic keyword is present, it's likely not a company.
    if any(keyword in lower_affiliation for keyword in ACADEMIC_KEYWORDS):
        return False

    # Rule 2: If any company keyword is present, it's likely a company.
    if any(keyword in lower_affiliation for keyword in COMPANY_KEYWORDS):
        return True

    # Rule 3: Check email domains if available.
    if "@" in lower_affiliation:
        domain = lower_affiliation.split('@')[-1]
        if ".edu" in domain or ".gov" in domain or ".ac." in domain:
            return False
        # Assume other domains might be corporate
        return True

    return False