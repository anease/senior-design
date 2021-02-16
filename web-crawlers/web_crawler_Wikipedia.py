
import requests
from  bs4 import BeautifulSoup

# Object to store website's text content and URLs
class Wiki_Site:
    def __init__(self, statement, url, body, links, tag):
        self.statement = statement
        self.title = "Wikipedia - " + statement
        self.body = body
        self.url = url
        self.root_url = 'https://wikipedia.org'
        self.links = links
        self.searchURL = 'https://en.wikipedia.org/w/index.php?search='
        self.page_type_tag = tag      # True => search results    False => wiki page
    # Print website content
    def print(self):
        print('Found Statement: {}'.format(self.statement))
        print('URL: {}'.format(self.url))
        print('TITLE: {}'.format(self.title))
        print('BODY:\n{}'.format(self.body))
        print('LINKS:\n{}'.format(self.links))

# This crawler will extract links and text information from a passed in Wikipedia page
class Crawler:
    res = []
    visited = []
    tb_visited = []
    url = 'https://wikipedia.org'

    filter_memb_str_wiki = ["href=\"/wiki/", "class=mw-redirect"]
    filter_nonmemb_str_wiki = ["class=", "accesskey=", "/wiki/Template:", "/Special:BookSources/", "/wiki/Wikipedia:", "/wiki/Category:", "/wiki/Help:", "/wiki/Portal:", "/wiki/Template_talk:"]
    
    
    def getPage(self, url):
        try:
            req = requests.get(url)
        except requests.exceptions.RequestException:
            return None
        return BeautifulSoup(req.text, 'html.parser')
        
    ### Filter functions that cross reference strings with a list of 
    #       preselected strings
    def apply_nonmemb_filter(self, strn, filter_str):
        bl = True
        for i in filter_str:
            if strn.find(i) != -1:
                bl = False
        return bl
    def apply_memb_filter(self, strn, filter_str):
        bl = True
        for i in filter_str:
            if strn.find(i) == -1:
                bl = False
        return bl

    # This function is designed to search Wikipedia and may not work 
    #   the same for other websites
    def wiki_search(self, statement):
        bs = self.getPage('https://en.wikipedia.org/w/index.php?search=' + statement)

        # Determines if the url queried returns as a wiki page or a search results
        if str(bs.html.head.title).find('Search results') != -1:

            grabbed_content = self.scrape_searchResults(bs, statement)
            return Wiki_Site(grabbed_content[0], grabbed_content[1], grabbed_content[2], grabbed_content[3], True)

        elif str(bs.html.head.title).find('Search results') == -1:
            
            grabbed_content = self.scrape_wiki(bs, statement)
            return Wiki_Site(grabbed_content[0], grabbed_content[1], grabbed_content[2], grabbed_content[3], False)
        #print(str(bs.html).split('\n')[0])


    # This function is designed to scrape the text and links from a Wikipedida page
    def scrape_wiki(self, bs_site, statement):
        filtered_content = []
        filtered_links = []

        # Finds all the <p> elements on the html and filters them for 
        # preffered elements (created based on Wikipedia's structure)
        content = bs_site.find_all('p')
        for i in content:
            if str(i).find("<p>") != -1:
                filtered_content.append(i.get_text())

        # Finds all the <a> elements on the html and further filters them for 
        # preferred links based on their href content (created based on Wikipedia's structure)
        links = bs_site.find_all('a')

        # Filtering happens here
        for i in links:
            if str(i).find(self.filter_memb_str_wiki[0]) != -1:
                if self.apply_memb_filter(str(i), self.filter_memb_str_wiki):
                    filtered_links.append(self.url + str(i).split("\"")[1])
                elif self.apply_nonmemb_filter(str(i), self.filter_nonmemb_str_wiki):
                    filtered_links.append(self.url + str(i).split("\"")[1])     

        url = filtered_links[-1]
        return [statement, url, filtered_content, filtered_links]

    # This function is designed to scrape the links from a Wikipedia search results page
    def scrape_searchResults(self, bs_site, statement):
        retrieved_links = []

        links = bs_site.find_all('a')

        # Filtering happens here
        for i in links:
            if str(i).find("data-serp-pos=\"") != -1:
                #print(self.url + str(i).split("\"")[3])
                retrieved_links.append(self.url + str(i).split("\"")[3])
                
        return [statement, None, None, retrieved_links]

    # This takes an inception wiki web page and crawls+scrapes every filtered link 
    #   found on that page. If the page is search results, each linked result
    #   is crawled+scraped through
    def crawl(self, incept_site):
        # Determines whether the inception point is search results or wiki page
        if incept_site.page_type_tag is True:
            self.visited.append(incept_site.links[0])
            bs = self.getPage(incept_site.links[0])
        elif incept_site.page_type_tag is False:
            self.visited.append(incept_site.url)
            bs = self.getPage(incept_site.url)

        # Scrapes the inception page first
        self.res.append(self.scrape_wiki(bs, incept_site.statement))
        
        # Scrapes all associated links next
        for j in incept_site.links:
            bs = self.getPage(j)
            self.res.append(self.scrape_wiki(bs, incept_site.statement))
            self.visited.append(j)
        """
        for k in self.res:
            print(k)
            print("-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-\n")
        """
        return self.res


crawler = Crawler()
site = crawler.wiki_search('Algebra')
crawler.crawl(site)

