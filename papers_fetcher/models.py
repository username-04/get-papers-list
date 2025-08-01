# papers_fetcher/models.py
from typing import List, Optional, NamedTuple

class Author(NamedTuple):
    """Represents a single author with their affiliation."""
    last_name: Optional[str]
    fore_name: Optional[str]
    initials: Optional[str]
    affiliation: Optional[str]

class Paper(NamedTuple):
    """Represents a single research paper."""
    pubmed_id: str
    title: str
    publication_date: str
    authors: List[Author]
    corresponding_author_email: Optional[str]

class FilteredPaper(NamedTuple):
    """Represents a paper that has passed the non-academic filter."""
    pubmed_id: str
    title: str
    publication_date: str
    non_academic_authors: str
    company_affiliations: str
    corresponding_author_email: Optional[str]