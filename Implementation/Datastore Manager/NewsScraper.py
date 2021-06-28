import requests
import re
from bs4 import BeautifulSoup
import os
import PyPDF2 
from newsapi import NewsApiClient
from datetime import date,timedelta


DOMAINS = ['www.gov.sg','www.straitstimes.com','www.channelnewsasia.com']
KEYWORDS = ['Covid','Singapore']


# returns a list of google page urls 
    # domains: LIST  
    # keywords: LIST
    # e.g https://www.google.com/search?q=Covid+Singapore+site:www.gov.sg&tbm=nws&start=0
def get_google_page_urls(domains, keywords, numPages = 10):
    q = ''.join([f"{k_}+" for k_ in keywords])
    google_page_urls = []
    for d_ in domains:
        for start in range(0,numPages*10+1,10):
            google_page_urls.append(f'https://www.google.com/search?q={q}site:{d_}&tbm=nws&start={start}')
    return google_page_urls


# returns article urls 
    # domains: LIST 
    # googlePageUrl: str 
def get_article_urls_from_google_page(domains, googlePageUrl):
    r = requests.get(googlePageUrl,headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '      # headers = ... - ensure successful request
                                            'AppleWebKit/537.11 (KHTML, like Gecko) '
                                            'Chrome/23.0.1271.64 Safari/537.11',
                                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                                            'Accept-Encoding': 'none',
                                            'Accept-Language': 'en-US,en;q=0.8',
                                            'Connection': 'keep-alive'})                                     # request page
    soup = BeautifulSoup(r.content, 'html5lib')               # turn to soup object
    links = []
    for L_ in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        link = re.split(":(?=http)",L_["href"].replace("/url?q=",""))[0].split("&")[0]
        if link not in links:
            for d_ in [f'https://{d_}' for d_ in domains]:
                if d_ in link:
                    links.append(link)
    return links

# scrapes articles from the following domains 'www.gov.sg','www.straitstimes.com','www.channelnewsasia.com'
def scrape(url, clean_function, include_title = True):
    
    r = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '      # headers = ... - ensure successful request
                                    'AppleWebKit/537.11 (KHTML, like Gecko) '
                                    'Chrome/23.0.1271.64 Safari/537.11',
                                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                                    'Accept-Encoding': 'none',
                                    'Accept-Language': 'en-US,en;q=0.8',
                                    'Connection': 'keep-alive'})                                     
    soup = BeautifulSoup(r.content, 'html5lib')               
    text = ""
    
    content_locations = {"www.gov.sg": soup.findAll('div', attrs = {'class':'content'}),
                         "www.channelnewsasia.com" :soup.findAll('p'),
                         "www.straitstimes.com":soup.findAll('p')}
    
    for domain in content_locations.keys():
        if domain in url:
            for tag in content_locations[domain]:
                text = f"{text} {tag.text}"
            break
    
    if include_title:                                          # whether to include title on the front of the text
        text = f"{url.split('/')[-1].replace('-',' ')} {text}"
        
    return clean_function(text)





##### OLDER VERSIONS BELOW #####











# # purpose: scrapes an article from gov.sg 
# # input:str (urls from gov.sg) , func (cleans the text)
# # output:str 
# def url2Text(url, cleaningfunc, include_title = True):
#     r = requests.get(url)                                     # request page
#     soup = BeautifulSoup(r.content, 'html5lib')               # turn to soup object
#     text = ""
#     for content in soup.findAll('div', attrs = {'class':'content'}): # all relevant content found in  <div class="component content">
#         text += cleaningfunc(content.text)
#     if include_title:
#         return url.split('/')[-1].replace('-',' ')+text
#     return text


# # converts pdf file into text
# # input: str,func
# # output: list[str]
# def pdf2Text(pdfname, cleaningfunc, include_title = True, min_length = 30):
    
#     # read pdf
#     pdfFileObj = open(pdfname,'rb')                              
#     pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#     text = cleaningfunc(' '.join([pdfReader.getPage(i).extractText() for i in range(pdfReader.numPages)]))
#     if len(text)<min_length:
#         print(f'Error in {pdfname}')
        
#     # include title as first element or not
#     if include_title:
#         return [pdfname[:-4]]+[text]
#     return  [text]

# # function: gets urls of recent news in the past n weeks
# # input: url
# # output: list[str]
# def getRecentNewsUrl(q = ['covid','singapore'],
#                      domains = ['channelnewsasia.com'],
#                      weeks_ago = 1,
#                      sort_by = 'relevancy',
#                      api_key='98835000ddca452896545df99ca3a98e'):
    
#     newsapi = NewsApiClient(api_key=api_key)
#     q = ' AND '.join(q)
#     domains = ','.join(domains)
#     top_headlines = []
#     from_param = date.today()
#     for i in range(weeks_ago):   
#         to, from_param = from_param, from_param-timedelta(weeks = 1)
#         top_headlines.extend(newsapi.get_everything(q=q,
#                                                    domains = domains,
#                                                    language='en',
#                                                    sort_by=sort_by,
#                                                    from_param = from_param,
#                                                    to = to)['articles'])
#     return [article['url'] for article in top_headlines]

# # function: scrapes CNN articles
# # input: url+cleaning function
# # output: str
# def scrapeCNN(url,
#               cleaningfunc,
#               exclude = ['subscribe to our Telegram channel','meREWARDS','All rights reserved','email address you entered is not valid']):
#     def is_irrelevant(text):
#         for invalid_word in exclude:
#             if invalid_word in text:
#                 return True
#         return False
#     r = requests.get(url,headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
#                                     'AppleWebKit/537.11 (KHTML, like Gecko) '
#                                     'Chrome/23.0.1271.64 Safari/537.11',
#                                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#                                     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#                                     'Accept-Encoding': 'none',
#                                     'Accept-Language': 'en-US,en;q=0.8',
#                                     'Connection': 'keep-alive'})   
#     soup = BeautifulSoup(r.content, 'html5lib')  
#     try:
#         datetime = soup.find('time').text 
#     except:
#         datetime = ''
#     try:
#         title = soup.find('title').text
#     except:
#         title = ''
#     text = ' '.join([cleaningfunc(p.text) for p in soup.findAll('p') if not is_irrelevant(p.text)])
#     return f'{datetime} {title} {text}'
