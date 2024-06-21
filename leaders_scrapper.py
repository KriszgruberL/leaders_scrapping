import json
import re
import requests
from bs4 import BeautifulSoup
from requests import Session
import time

def print_timing(func):
    '''Create a timing decorator function use @print_timing just above the function you want to time.'''
    def wrapper(*arg):
        start = time.perf_counter()
        #Run the function decorated
        result = func(*arg)
        end = time.perf_counter()
        execution_time = round((end - start), 2)
        print(f'{func.__name__} took {execution_time} sec')
        return result
    return wrapper


def get_first_paragraph(wikipedia_url: str, session: Session) -> str:
    """
    Extracts the first paragraph from a given Wikipedia page.

    Args:
        wikipedia_url (str): The URL of the Wikipedia page.
        session (Session): The requests session to use for making the HTTP request.

    Returns:
        str: The cleaned first paragraph text.
    """
    print(wikipedia_url)  # Print the URL for debugging purposes
    r = session.get(wikipedia_url)
    soup = BeautifulSoup(r.content, "html.parser")

    # Find the first paragraph after the infobox table
    infobox = soup.find("table", attrs={"class": "infobox"})
    if infobox:
        first_paragraph = infobox.find_next_sibling("p")
    else:
        first_paragraph = ""
        return first_paragraph

    clean_text = first_paragraph.get_text(separator=" ", strip=True)

    # Define regex patterns to remove unwanted text
    clean_text = re.sub(r"\[.*?\]", "", clean_text)
    clean_text = re.sub(r"\([^)]*\)", "", clean_text)
    clean_text = re.sub(r"/.*?/", "", clean_text)
    clean_text = re.sub(r"Écouter", " ", clean_text)
    clean_text = re.sub(r"\s+", " ", clean_text)
    clean_text = clean_text.replace(" ,", ",").replace(" .", ".").strip()

    return clean_text


@print_timing
def get_leaders():
    """
    Fetches leaders' data including their first Wikipedia paragraph for each country.

    Returns:
        dict: A dictionary with country codes as keys and a list of leaders as values.
    """
    url = "https://country-leaders.onrender.com"
    leaders_url = "/leaders"
    cookies_url = "/cookie"
    countries_url = "/countries"

    cookies = requests.get(f"{url}{cookies_url}").cookies.get_dict()
    countries = requests.get(f"{url}{countries_url}", cookies=cookies).json()

    # Fetch leaders for each country
    leaders_per_country = {c: requests.get(f"{url}{leaders_url}", cookies=cookies, params={"country": c}).json() for c
                           in countries}

    session = Session()
    for country, leaders in leaders_per_country.items():
        for leader in leaders:
            try:
                # Try to get the first paragraph of the leader's Wikipedia page
                leader['first_paragraph'] = get_first_paragraph(leader['wikipedia_url'], session)
                time.sleep(0.1)
            except requests.RequestException as e:
                # Refresh cookies if a request fails
                cookies = requests.get(f"{url}{cookies_url}").cookies.get_dict()
    return leaders_per_country


def save(leaders_per_country):
    """
    Saves the leaders data to a JSON file.

    Args:
        leaders_per_country (dict): The dictionary containing leaders data.
    """
    with open("leaders.json", "w") as file:
        json.dump(leaders_per_country, file)


def read():
    """
    Reads and prints the leaders data from the JSON file.
    """
    with open("leaders.json", "r") as file:
        json_file = json.load(file)
    print(json_file)


if __name__ == '__main__':
    lead = get_leaders()
    save(lead)
    read()
