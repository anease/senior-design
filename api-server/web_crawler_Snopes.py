
import requests
from  bs4 import BeautifulSoup
from selenium import webdriver

# Object to store website's text content and URLs
class Snopes_Site:
    def __init__(self, statement, title, descrip, author, pub_date, url, claim, rating, rating_whatsTrue, rating_whatsFalse, origin):
        self.statement = statement
        self.title = title
        self.descrip = descrip
        self.author = author
        self.pub_date = pub_date
        self.claim = claim
        self.origin = origin
        self.url = url
        self.root_url = 'https://www.snopes.com'
        self.rating = rating
        self.rating_whatsTrue = rating_whatsTrue
        self.rating_whatsFalse = rating_whatsFalse
        self.searchURL = 'https://www.snopes.com/?s='

    # Print website content
    def print(self):
        print('Statement Searched for: {}'.format(self.statement))
        print('URL: {}'.format(self.url))
        print('TITLE: {}'.format(self.title))
        print('DESCRIPTION: {}'.format(self.descrip))
        print('AUTHOR: {}'.format(self.author))
        print('DATE PUBLISHED: {}\n'.format(self.pub_date))
        print('RATING:\n{}\n'.format(self.rating))
        print('WHAT\'S TRUE:\n{}\n'.format(self.rating_whatsTrue))
        print('WHAT\'S FALSE:\n{}\n'.format(self.rating_whatsFalse))
        print('ORIGIN: {}\n\n'.format(self.origin))

"""
#Object to store the Snopes search results
class Snopes_Search_Results:
    def __init__(self, statement, titles, links):
        self.statement = statement
        self.titles = titles
        self.links = links
    # Print website content
    def print(self):
        print('Searched Statement: {}'.format(self.statement))
        print('RESULT TITLES: {}'.format(self.titles))
        print('RESULT LINKS: {}'.format(self.links))
"""

class Search_n_Scraper:

    ####### RETRIEVES DYNAMIC HTML CONTENT #######
    def getPage(self, url):
        #Lando's code
        #browser = webdriver.Chrome()

        #Changed to work on Andrew's machine
        browser = webdriver.Chrome(executable_path='./chromedriver')

        try:
            browser.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(browser.page_source, 'html.parser')

        
    ####### RETRIEVES HTML CONTENT #######
    def getPage2(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')


    ####### SEARCHES SNOPES AND RETURNS TOP 10 RESULTS #######
    def snopes_search(self, statement):
        bs = self.getPage('https://www.snopes.com/?s=' + statement)
        search_results = []

        grabbed_content = self.scrape_searchResults(bs, statement)
        
        for g in grabbed_content:
            search_results.append(self.scrape_snopes(g, statement))

        return search_results


    ####### SCRAPE SEARCH RESULTS FOR LINKS #######
    def scrape_searchResults(self, bs_site, statement):
        retrieved_links = []
        
        links = bs_site.find_all('a', {'class': "search-entry link"})
        
        for i in links:
            retrieved_links.append(str(i).split("\"")[3])

        return retrieved_links


    ####### SCRAPE SNOPES ARTICLE FOR RELEVANT INFO ########
    def scrape_snopes(self, site_url, statement):
        
        bs_site = self.getPage2(site_url)

        title = bs_site.find('h1', {'class': "title"})
        if title is None:
            title = bs_site.find('h1', {'class': "card-body h2 pb-1"})
        if title is not None:
            title = str(title).split('\t')
            title = title[1].split('<')[0]

        descrip = bs_site.find('h2', {'class': "subtitle"})
        if descrip is None:
            descrip = bs_site.find('h2', {'class': "card-body h5 font-weight-normal py-0"})
        if descrip is not None:
            descrip = str(descrip).split('\t')[2]

        author = bs_site.find('ul', {'class': "list-unstyled authors list-unstyled d-flex flex-wrap comma-separated"})
        if author is None:
            author = bs_site.find('ul', {'class': "list-unstyled card-body d-flex authors comma-separated pb-0 mb-0"})
        if author is not None:
            author = str(author).split('\t')
            author = [author[6], author[0].split('\"')[5]]

        pub_date = bs_site.find('ul', {'class': "list-unstyled dates list-unstyled d-flex flex-wrap comma-separated-md"})
        if pub_date is None:
            pub_date = bs_site.find('ul', {'class': "list-unstyled card-body d-flex comma-separated pt-0"})
        if pub_date is not None:
            pub_date = str(pub_date).split('\t')
            if len(pub_date) > 10:
                pub_date = ["Published " + pub_date[4], "Updated "+pub_date[11]]
            else: 
                pub_date = ["Published " + pub_date[4]]

        claim = bs_site.find('div', {'class': "claim-text card-body"})
        if claim is not None:
            claim = str(claim).split('\t')[3]
            claim = claim.rstrip('\n')

        rating = bs_site.find('div', {'class': "media-body d-flex flex-column align-self-center"})
        if rating is not None:
            rating = str(rating).split('\n')[1]
            rating = rating.split('>')[1]
            rating = rating.split('<')[0]

        rating_whatsTrue = bs_site.find('div', {'class': "media whats-true"})
        if rating_whatsTrue is not None:
            rating_whatsTrue = str(rating_whatsTrue).split('>')[5]
            rating_whatsTrue = rating_whatsTrue.split('<')[0]

        rating_whatsFalse = bs_site.find('div', {'class': "media whats-false"})
        if rating_whatsFalse is not None:
            rating_whatsFalse = str(rating_whatsFalse).split('>')[5]
            rating_whatsFalse = rating_whatsFalse.split('<')[0]

        origin = bs_site.find('div', {'class': "single-body card card-body rich-text"})
        if origin is not None:
            origin = origin.get_text()

        return Snopes_Site(statement, title, descrip, author, pub_date, site_url, claim, rating, rating_whatsTrue, rating_whatsFalse, origin)
        

# grab_Snopes = Search_n_Scraper()
# sites = grab_Snopes.snopes_search("Diet Coke Button")

# sites[0].print()

# # for i in sites:
# #     i.print()
