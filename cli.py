# cli.py
import csv
import sys
from typing import List, Optional

import typer
from rich.console import Console

from papers_fetcher.api import search_pubmed, fetch_paper_details
from papers_fetcher.heuristics import is_company_affiliation
from papers_fetcher.models import Paper, FilteredPaper
from papers_fetcher.parser import parse_pubmed_xml

app = typer.Typer(
    help="A CLI tool to fetch PubMed research papers from authors affiliated with pharma/biotech companies.",
    context_settings={"help_option_names": ["-h", "--help"]},
)
console = Console()

def filter_papers_by_affiliation(papers: List[Paper], debug: bool) -> List[FilteredPaper]:
    """Filters papers to find those with non-academic authors."""
    filtered_list: List[FilteredPaper] = []
    for paper in papers:
        non_academic_authors = []
        company_affiliations = set()

        for author in paper.authors:
            if author.affiliation and is_company_affiliation(author.affiliation):
                author_name = f"{author.fore_name or ''} {author.last_name or ''}".strip()
                non_academic_authors.append(author_name)
                company_affiliations.add(author.affiliation)
                if debug:
                    console.log(f"[green]Match Found:[/green] Author '{author_name}' from '{author.affiliation}'")

        if non_academic_authors:
            filtered_list.append(FilteredPaper(
                pubmed_id=paper.pubmed_id,
                title=paper.title,
                publication_date=paper.publication_date,
                non_academic_authors="; ".join(non_academic_authors),
                company_affiliations="; ".join(sorted(list(company_affiliations))),
                corresponding_author_email=paper.corresponding_author_email,
            ))
    return filtered_list

@app.command()
def fetch(
    query: str = typer.Argument(..., help="The search query for PubMed (e.g., 'cancer therapy')."),
    file: Optional[str] = typer.Option(None, "-f", "--file", help="Filename to save the results in CSV format."),
    debug: bool = typer.Option(False, "-d", "--debug", help="Print debug information during execution."),
):
    """
    Fetch and filter research papers from PubMed.
    """
    with console.status("[bold blue]Searching PubMed...", spinner="dots") as status:
        if debug:
            console.log(f"Executing search with query: '{query}'")
        pmids = search_pubmed(query)

        if not pmids:
            console.print("[red]No papers found or API error.[/red]")
            raise typer.Exit(code=1)

        if debug:
            console.log(f"Found {len(pmids)} paper IDs: {pmids}")

        status.update("[bold blue]Fetching paper details...")
        xml_data = fetch_paper_details(pmids)
        if not xml_data:
            console.print("[red]Failed to fetch paper details.[/red]")
            raise typer.Exit(code=1)

        if debug:
            console.log("Successfully fetched XML data.")

        status.update("[bold blue]Parsing and filtering papers...")
        all_papers = parse_pubmed_xml(xml_data)
        filtered_papers = filter_papers_by_affiliation(all_papers, debug)

    if not filtered_papers:
        console.print("[yellow]No papers with authors from pharma/biotech companies were found.[/yellow]")
        raise typer.Exit()

    console.print(f"[bold green]Successfully found {len(filtered_papers)} matching papers![/bold green]")

    if file:
        try:
            with open(file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Write header
                writer.writerow(FilteredPaper._fields)
                # Write data
                writer.writerows(filtered_papers)
            console.print(f"Results saved to [cyan]{file}[/cyan]")
        except IOError as e:
            console.print(f"[red]Error writing to file {file}: {e}[/red]")
            raise typer.Exit(code=1)
    else:
        # Print to console
        console.print(filtered_papers)


if __name__ == "__main__":
    app()