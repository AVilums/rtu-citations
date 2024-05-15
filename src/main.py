import requests
import pyperclip
import keyboard
import sys


# docker build -t citations .
# docker run -it --rm citations
def get_citation_journal(doi):
    """
    Builds journal citation information from Crossref API based on DOI and copies it to clipboard.

    Args:
        doi (str): The DOI (Digital Object Identifier) of the publication.

    Returns:
        None
    """
    # Make the API call
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:

        data = response.json()

        # check if citation applies
        if data['message']['type'] == ' journal-article':
            return print("Error: The provided DOI does not correspond to a journal article: ",
                         data['message']['type'])

        print("Full response:")
        print(data)
        print()

        # Extract required information for citation
        authors = ", ".join([f"{author['family']}, {author['given'][0]}." for author in data['message']['author']])
        title = " ".join(data['message']['title'])
        journal = data['message']['container-title'][0]
        volume = data['message']['volume']
        issue = data['message'].get('issue', None)  # Using get() to handle missing 'issue'
        pages = data['message']['page']
        year = data['message']['published-print']['date-parts'][0][0]
        issn_list = data['message']['ISSN']
        issn_print = issn_list[0]
        issn_electronic = issn_list[1] if len(issn_list) > 1 else None  # Use None if only one ISSN is available
        doi_link = data['message']['URL']

        # according to: 7. PUBLIKĀCIJA ZINĀTNISKAJĀ ŽURNĀLĀ:
        # https://ebooks.rtu.lv/wp-content/uploads/sites/32/2023/03/9789934226960-DITF_metodiskie_norad-2021-LV.pdf
        citation_parts = [authors, title, ".", journal, ".", f"{year}, vol. {volume},"]
        if issue:
            citation_parts.append(f"no. {issue},")
        citation_parts.extend([f"pp. {pages}.", f"ISSN {issn_print}."])
        if issn_electronic:
            citation_parts.append(f"e-ISSN {issn_electronic}.")
        citation_parts.append(f"Available from: {doi_link}.")

        citation = " ".join(citation_parts)

        # Copy the citation to clipboard
        pyperclip.copy(citation)

        print("Citation:")
        print(citation)
    else:
        print(f"Error: {response.status_code}")


def main():
    """
    Main function to interact with the user and call get_citation function.
    """
    while True:
        try:
            doi = input("\nEnter DOI: ")
            get_citation_journal(doi)
        except Exception as e:
            print("Error:", e)

        stop = input("Continue? y/n  ").upper()
        if stop == "N":
            break

    sys.exit(1)


if __name__ == "__main__":
    main()
