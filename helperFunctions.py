def getWebsiteUrl(website: str):
    """Returns the url for the provided domain name."""
    if website == "BookStore":
        return "http://books.toscrape.com/"
    else:
        return ""


def cleanupFormInput(input: str):
    """Extracts the useful data from the submitted form."""
    cleanInput = input.split("&")
    for i in range(len(cleanInput)):
        cleanInput[i] = cleanInput[i].partition("=")[-1]
    cleanInput[0] = cleanInput[0].strip().casefold()
    print(cleanInput)
    return cleanInput
