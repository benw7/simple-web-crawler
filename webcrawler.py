# Simple Web Crawler for URL Discovery

import urllib.request
from html.parser import HTMLParser
import re

class Parser(HTMLParser):
    """
    A class to parse HTML and handle the 'href' attribute of tags. Extends HTMLParser from module html.
    """

    def __init__(self, *, convert_charrefs: bool = ...):
        """
        Initialises the class object by calling the HTMLParser __init__ function and initialising our url_list.
        """
        super().__init__(convert_charrefs=convert_charrefs)
        self.url_list = []

    def handle_starttag(self, tag, attrs):
        """
        Called when the parser encounteres a HTML start tag. Checks for the 'href' attribute and checks if its value is a valid URL that isn't already in the url list.
        """
        for attribute in attrs:
            attr_type, attr_content = attribute[0], attribute[1]
            if attr_type and attr_content:
                isURL = re.match(r"(https?:\/\/)([\w\-])+\.{1}([a-zA-Z]{2,63})([\/\w-]*)*\/?\??([^#\n\r]*)?#?([^\n\r]*)", attr_content)
                if attr_type == 'href' and isURL and attr_content not in self.url_list:
                    self.url_list.append(attr_content)

    def feed(self, data: str):
        """
        Called when the object is fed new HTML data. Resets the url list and returns the HTMLParser's feed function.
        """
        self.url_list = []
        return super().feed(data)

        
def urlSearch(to_search, searched=[]):
    """
    Recurvise web crawling function that discovers URLs from the 'href' attribute of tags.

    Parameters:
        to_search: a list of URLs to search
        searched: a list recording the URLs that have already been searched
    """

    # Base case: discovered 100 URLs
    if len(searched + to_search) >= 100:
        for i in range(100):
            print((searched + to_search)[i])
    
    # Base case 2: Ran out of URLs to search before 100 URLs discovered
    elif len(to_search) == 0:
        print("Ran out of URLs to search! Printing discovered URLs:")
        for url in searched:
            print(url)
    
    # Search all URLs in to_search
    else:
        new_to_search = []
        for url in to_search:
            try:
                fp = urllib.request.urlopen(url)
                mybytes = fp.read()
                mystr = mybytes.decode("utf8")
                fp.close()
            except Exception as e:
                print("Error accessing '"+url+"': "+str(e))
            else:
                parser.feed(mystr)
                new_to_search += parser.url_list
            finally:
                searched.append(url)
        
        new_to_search = [*set([x for x in new_to_search if x not in searched])] # No duplicates, no overlap with searched
        urlSearch(new_to_search, searched)

if __name__ == "__main__":
    base_url = input("Please enter a starting URL:\n-->") # Include http:// or https://
    parser = Parser()
    urlSearch([base_url])