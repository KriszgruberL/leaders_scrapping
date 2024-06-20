# Wikipedia Leaders Extractor

This project contains a Python script designed to fetch and process information about country leaders from a specified API. The main functionalities include retrieving leader data, extracting the first paragraph from their Wikipedia pages, and saving this information to a JSON file.

## Features

- Fetches leaders' data for various countries using the API : "https://country-leaders.onrender.com"
- Extracts the first paragraph from the leaders' Wikipedia pages, cleaning up unwanted text.
- Saves the processed data to a JSON file.
- Reads and prints the saved data from the JSON file.
- Includes timing for the main data fetching function.

## Requirements

- Python 3.12
- Requests library
- BeautifulSoup4 library

## Installation

1. Clone the repository or download the script file.
2. Ensure you have Python 3.12 installed on your machine.
3. Install the required libraries using pip:
    ```bash
    pip install requests beautifulsoup4
    ```

## Usage

### Running the Script

To run the script, execute the following command in your terminal:
```bash
python leaders_scrapper.py
```
This will fetch the leaders' data, extract the first paragraph from their Wikipedia pages, save the data to `leaders.json`, and print the contents of the file.

### Functions

#### print_timing

A decorator function that prints the execution time of the decorated function.

```python
def print_timing(func)
```
___
#### get_first_paragraph

Extracts and cleans the first paragraph from a given Wikipedia page.

```python
def get_first_paragraph(wikipedia_url: str, session: Session) -> str
```

- **Args:**
    - `wikipedia_url (str)`: The URL of the Wikipedia page.
    - `session (Session)`: The requests session to use for making the HTTP request.
- **Returns:** The cleaned first paragraph text.
______
#### get_leaders

Fetches leaders' data including their first Wikipedia paragraph for each country. This function is decorated with `@print_timing`.

```python
@print_timing
def get_leaders() -> dict
```

- **Returns:** A dictionary with country codes as keys and a list of leaders as values.
___
#### save

Saves the leaders' data to a JSON file.

```python
def save(leaders_per_country)
```

- **Args:**
    - `leaders_per_country (dict)`: The dictionary containing leaders' data.
____
#### read

Reads and prints the leaders' data from the JSON file.

```python
def read()
```

## Example Output

```json

{
  "us": [
    {
      "id": "Q23",
      "first_name": "George",
      "last_name": "Washington",
      "birth_date": "1732-02-22",
      "death_date": "1799-12-14",
      "place_of_birth": "Westmoreland County",
      "wikipedia_url": "https://en.wikipedia.org/wiki/George_Washington",
      "start_mandate": "1789-04-30",
      "end_mandate": "1797-03-04",
      "first_paragraph": "George Washington (February 22, 1732– December 14, 1799) was an American Founding Father..."
    }
  ],
  "fr": [
    {
      "id": "Q315656",
      "first_name": "Jean",
      "last_name": "Casimir-Perier",
      "birth_date": "1847-11-08",
      "death_date": "1907-03-11",
      "place_of_birth": "Paris",
      "wikipedia_url": "https://fr.wikipedia.org/wiki/Jean_Casimir-Perier",
      "start_mandate": "1894-06-27",
      "end_mandate": "1895-01-16",
      "first_paragraph": "Jean Casimir-Perier, né le 8 novembre 1847 à Paris..."
    }
  ]
}

```

## Notes

- The script uses regex patterns to clean the extracted Wikipedia text. Adjust the patterns if necessary to improve text cleaning based on specific Wikipedia page structures or languages.
- The timing decorator `@print_timing` is used to measure the execution time of the `get_leaders` function.
