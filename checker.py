import requests
from bs4 import BeautifulSoup
import re
import time

"""
To handle routing to insecure page i.e navigatiing to 'http' requests which donot 
have SSL certificates and are consideres to be insecure.
The below lines are added to suppress the below error:
------------------------------------------------------
InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised.

reference:
https://medium.com/@akhilsai831/coding-a-python-script-to-find-dead-links-in-a-wikipedia-page-ff7dc35dcb3e
https://github.com/saiyerniakhil/python-75-hackathon/tree/master/wikipedia-deadlink-finder
"""
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

""" 
    Filtering URLs from the mixed collection of href's contaings routes, images and URLs based on a Regular Expression.
"""





def url_validation(link):
    urlregex = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return re.match(urlregex, str(link)) is not None

urls = ["https://www.sportsbusinessjournal.com/Daily.aspx",
         "https://www.sportsbusinessjournal.com/Daily/Morning-Buzz.aspx",
        "https://www.sportsbusinessjournal.com/Daily/Morning-Buzz.aspx", 
        "https://www.sportsbusinessjournal.com/Daily/Closing-Bell.aspx", 
        "https://www.sportsbusinessjournal.com/Daily/Global.aspx", 
        "https://www.sportsbusinessjournal.com/Esports.aspx",
        "https://www.sportsbusinessjournal.com/Journal/Print-Online.aspx",
        "https://www.sportsbusinessjournal.com/Archive/Sections/Marketing-and-Sponsorship.aspx",
        "https://www.sportsbusinessjournal.com/Archive/Sections/Media.aspx",
        "https://www.sportsbusinessjournal.com/Archive/Sections/Leagues-and-Governing-Bodies.aspx",
        "https://www.sportsbusinessjournal.com/Archive/Sections/Franchises.aspx",
        "https://www.sportsbusinessjournal.com/Archive/Sections/Betting.aspx",
        "https://www.sportsbusinessjournal.com/Archive/Sections/Colleges.aspx",
        "https://www.sportsbusinessjournal.com/Archive/Sections/Events-and-Attractions.aspx",
        "https://www.sportsbusinessjournal.com/Archive/Sections/Facilities.aspx",
        "https://www.sportsbusinessjournal.com/Archive/Sections/Labor-and-Agents.aspx",
        "https://www.sportsbusinessjournal.com/Podcasts.aspx",
        "https://www.sportsbusinessjournal.com/Podcasts/SBJ-Morning-Buzzcast.aspx",
        "https://www.sportsbusinessjournal.com/Podcasts/SBJ-Spotlight.aspx",
        "https://www.sportsbusinessjournal.com/College-University/About-the-Program.aspx",
        "https://advertise.sportsbusinessjournal.com/",
        "https://www.sportsbusinessjournal.com/Subscribe/Subscription-Landing.aspx",
        "https://www.sportsbusinessjournal.com/Native.aspx"]

tested_urls = []

sbj = 'https://www.sportsbusinessjournal.com'

prot = ['http', 'https']
    
oklinks = ["https://www.linkedin.com/company/sports-business-journal/", "https://www.instagram.com/sbj_sbd/", "https://www.instagram.com/esportsobserver/",
           "https://www.linkedin.com/company/the-esports-observer/"]


def deadLinkFinder(url):

    linkset = []
    first_column = []
    valid_urls = []
    dead_links = []
    conn_refused = []
    forbidden_urls = []
    link_urls = []   

    link_count = 0
    
    print("Testing: ", url)
    page = requests.get(url)  # The URL is of our choice
    
    soup = BeautifulSoup(page.content, 'html.parser')
    linkset = soup.find_all('a')

    # To get the href from the collected Hyperlinks
    for i in linkset:
        link_urls.append(i.get('href'))

    # Applying URL validation and Holding together all the valid URLs in a list.
    for i in link_urls:
      if i and i[0] == '/':
        i = sbj + i
      if i not in tested_urls:
        if url_validation(i):
            valid_urls.append(i)
    """
    Making request to all the valid URLs.
    If the URL gives us a status-code, 200. Then it's a Dead Link. 
    If the URL gives us a status-code, 403. Then its a Forbidden Link.
    """
    print("Dead Links: ")
    for i in valid_urls:
      tested_urls.append(i)
      link_addr = i.split(":")
      if link_addr[0] in prot:
        try:
            temp_page = requests.get(i, verify=False)
        except:
            conn_refused.append(i)
        if (temp_page.status_code == 403):
            forbidden_urls.append(i)
        elif not (temp_page.status_code == 200):
          if i not in oklinks:
            print("* ", i)
            dead_links.append(i)
      link_count += 1

    # Finally printing out all the Dead Links,Forbidden Links and the URLs that are taking too long to respond.

    if len(dead_links) == 0:
        print("No Dead links found.")
    print(link_count)

for link in urls:
  link_addr = link.split(":")
  if link_addr[0] in prot:
    deadLinkFinder(link)
