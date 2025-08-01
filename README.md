# Get Papers List

A command-line tool to fetch research papers from PubMed based on a user-specified query. The program identifies and returns papers with at least one author affiliated with a pharmaceutical or biotech company.

## Code Organization

The project is structured into two main parts to promote modularity and reusability:

1.  **`papers_fetcher/`**: A reusable Python module that contains all the core logic for:
    *   `api.py`: Interacting with the PubMed API.
    *   `parser.py`: Parsing the XML responses from PubMed.
    *   `heuristics.py`: Applying rules to identify company affiliations.
    *   `models.py`: Defining data structures (`Paper`, `Author`) for type safety and clarity.

2.  **`cli.py`**: A command-line interface built with [Typer](https://typer.tiangolo.com/). It handles user input, orchestrates calls to the `papers_fetcher` module, and formats the output.

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/username-04/get-papers-list.git
    cd get-papers-list
    ```

2.  **Install Poetry:**
    Follow the instructions on the [official Poetry website](https://python-poetry.org/docs/#installation).

3.  **Install dependencies:**
    This command will create a virtual environment and install all required libraries.
    ```bash
    poetry install
    ```

## How to Use

Once installed, you can run the program using the `get-papers-list` command, which is made available through Poetry.

### Basic Usage

Provide a search query to fetch papers. The output will be printed to the console.

```bash
poetry run get-papers-list "ozempic clinical trial"
```

### Command-line Options

*   **`--file` / `-f`**: Save the output to a CSV file.
    ```bash
    poetry run get-papers-list "monoclonal antibody therapy" --file results.csv
    ```

*   **`--debug` / `-d`**: Enable debug mode to see verbose output during execution, including why a paper was matched.
    ```bash
    poetry run get-papers-list "crispr gene editing" -d
    ```

*   **`--help` / `-h`**: Display the help message with all available options.
    ```bash
    poetry run get-papers-list --help
    ```

## Tools and Libraries Used

*   **Python 3.8+**
*   **[Poetry](https://python-poetry.org/)**: For dependency management and packaging.
*   **[PubMed Entrez API](https://www.ncbi.nlm.nih.gov/books/NBK25501/)**: The source for fetching all publication data.
*   **[Requests](https://requests.readthedocs.io/en/latest/)**: For making HTTP requests to the PubMed API.
*   **[Typer](https://typer.tiangolo.com/)**: For creating a clean and modern command-line interface.
*   **[Rich](https://rich.readthedocs.io/en/latest/)**: Used by Typer to provide beautiful formatting in the terminal (colors, progress spinners, etc.).
*   **Development Assistance**: This program structure, code, and documentation were generated with the assistance of Google's Gemini.