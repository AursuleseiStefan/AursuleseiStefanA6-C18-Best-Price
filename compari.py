from urllib.request import urlopen
from bs4 import BeautifulSoup
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from robobrowser import RoboBrowser
import re


url="https://www.compari.ro/telefoane-mobile-c3277/samsung/galaxy-z-fold4-5g-256gb-12gb-ram-dual-f936-p841779084/"
browser=RoboBrowser(parser="html5lib")
browser.open(url)
htmlpage=str(browser.parsed)
bsup=BeautifulSoup(htmlpage,"html5lib")
a=bsup.find('div' ,{'id':'offer-block-paying'})
# b=bsup.find('span' ,{'data-akjl':'Price||Price||1'})
for link in a.findAll('span' ,{'data-akjl':'Price||Price||1'}):
      print(link.text)
# for link in bsup.find('div' ,{'id':'offer-block-paying'}):
#     if 'href' in link.attrs:
#         print(link.attrs['href'])
# print(b.text)



#print("Titlu paginii este " + bsup.title.string)
#continutulcunume=bsup.find("div",{"class" : "mv-parser-output"})
    # #for link in soup.findall('a',{'class': 'Table_personName__UO41W'}):
    # for link in continutulcunume.find_all('a'):
    #     print("link")