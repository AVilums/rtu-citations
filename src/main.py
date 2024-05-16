import sys
import requests
import pyperclip


def format_datu_kopa():
    authors = input("Enter authors (Surname, N.): ")
    title = input("Enter title: ")
    publisher = input("Enter publisher: ")
    publication_date = input("Enter publication date (e.g., 'July 29, 2021'): ")
    url = input("Enter URL: ")

    reference = f"{authors}. {title} [datu kopa]. {publisher}, {publication_date}. Pieejams: {url}"

    # Copy the citation to clipboard
    pyperclip.copy(reference)

    print("Formatted reference:")
    print(reference)


def format_zinatniskais_zurnals(doi):
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
        volume = data['message'].get('volume', None)  # get handles missing
        # volume = data['message']['volume']
        issue = data['message'].get('issue', None)
        pages = data['message'].get('page', None)
        year = data['message']['created']['date-parts'][0][0]
        issn_list = data['message']['ISSN']
        issn_print = issn_list[0]
        issn_electronic = issn_list[1] if len(issn_list) > 1 else None  # Use None if only one ISSN is available
        doi_link = data['message']['URL']

        # according to: 7. PUBLIKĀCIJA ZINĀTNISKAJĀ ŽURNĀLĀ:
        # https://ebooks.rtu.lv/wp-content/uploads/sites/32/2023/03/9789934226960-DITF_metodiskie_norad-2021-LV.pdf
        reference_parts = [authors, title, ".", journal, ".", f"{year}, vol. {volume},"]

        if issue:
            reference_parts.append(f"no. {issue},")
        reference_parts.extend([f"pp. {pages}.", f"ISSN {issn_print}."])
        if issn_electronic:
            reference_parts.append(f"e-ISSN {issn_electronic}.")
        reference_parts.append(f"Available from: {doi_link}.")

        reference = " ".join(reference_parts)

        # Copy the citation to clipboard
        pyperclip.copy(reference)

        print("Formatted reference:")
        print(reference)
    else:
        print(f"Error: {response.status_code}")


def main():
    style_options = ['7', '14']
    print("Available formatting styles: ")
    for option in style_options:
        print(option)

    while True:
        style = input("\n Choose a formatting style: ").upper()

        match style:
            case "7":
                try:
                    doi = input("\n Enter DOI: ")
                    format_zinatniskais_zurnals(doi)
                except Exception as e:
                    print("Error: ", e)
            case "14":
                try:
                    format_datu_kopa()
                except SyntaxError as s:
                    print("Error: ", s)
            case default:
                print("\n Error: Invalid")

        stop = input("Continue? y/n  ").upper()
        if stop == "N":
            break

    sys.exit(1)


if __name__ == "__main__":
    main()
