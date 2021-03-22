# README

<br>

## Wikipedia Crawler and Scraper
This tool uses the Wikipedia search URL to query the Wikipedia knowledge base for a word or a statement. The tool returns a list of Wikipedia pages that are linked to from the resultant page searched or the search results page.

Python libraries used are:
- requests
    - Allows us to query a web URL and receive its HTML content if the page exists
- Beautiful Soup 4
    - Provides tools to index, search, split, and process HTML text efficiently 

Websites are stored as a class object, with attributes for URL, body, and hyperlinks found.
The crawler is also implemented as a class object. 
Once the search has been executed, the results are checked for being a Wikipedia article or a Wikipedia search results page. 
Each legitimate link found is queried and stored as our Website class object

<br>

## Snopes Scraper
This tool uses the Snopes.com search URL to query the Snopes webpage for a word or a statement. The tool returns a website class object that has the statement fact-checked in the article, the rating given, a description, the author, publishing date, and origin story.

Python libraries used are:
- requests
- Beautiful Soup 4
- Selenium
    - Used for loading webpages through an instance of Google Chrome
    - Allows dynamically generated content to be loaded before getting scraped
    - Requires an executable called chromedriver to be downloaded to the project folder

A search is executed and the search results are then queried and scraped for the information that can be stored in the website class object.

