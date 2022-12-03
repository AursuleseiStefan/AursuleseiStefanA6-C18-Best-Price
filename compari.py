import requests as req
from bs4 import BeautifulSoup
import sys


def functiecuargumente():
    if len(sys.argv)<2:
        return "prea putine argumente"
    return True


def functieptcrawl():
    if functiecuargumente():
        vectordeargumente=[]
        for i in range(1,len(sys.argv)):
            vectordeargumente.append(sys.argv[i])
        vectcupretur=[]
        for url in vectordeargumente:
            vectcupretur=[]
            dictionarcutoate={}
            vectorfararon=[]
        #print (vectordeargumente)
        #url="https://www.compari.ro/telefoane-mobile-c3277/samsung/galaxy-z-fold4-5g-256gb-12gb-ram-dual-f936-p841779084/"
            resp = req.get(url)
            bsup=BeautifulSoup(resp.text,"lxml")
            a=bsup.find('div' ,{'id':'offer-block-paying'})
            b=bsup.find('div' ,{'id':'offer-block-promoted'})
            c=bsup.find('h1' ,{'class':'hidden-xs'})
            #d=bsup.find('div' ,{'class':'row-price'})
            d=bsup.find('div' ,{'id':'offer-block-free'})
            #NUMELE PRODUSULUI
            for link in c.findAll('span',{'itemprop':'name'}):
                numecomplet=numecomplet+" "+link.text
            # b=bsup.find('span' ,{'data-akjl':'Price||Price||1'})
            #OFERTELE NOASTRE...
            for link in a.findAll('span' ,{'data-akjl':'Price||Price||1'}):
                vectcupretur.append(link.text)
            
            #OFERTE EVIDENTIATE
            for link in b.findAll('span' ,{'data-akjl':'Price||Price||1'}):
                vectcupretur.append(link.text)
            
            for link in d.findAll('span' ,{'data-akjl':'Price||Price||1'}):
                vectcupretur.append(link.text)
            
            # #OFERTELE NOASTRE POT FI ACHIZITIONATE DE PE COMPARI.RO##se afla in OFERTELE NOASTRE
            # for link in d.findAll('span' ,{'data-akjl':'Price||Price||1'}):
            #     vectcupretur.append(link.text)
            #     print(link.text)
            sorted(vectcupretur)
            print(bsup.title.string)     
        print (vectcupretur)
        #print (vectordeargumente)


if __name__=='__main__':
    #print(functiecuargumente())
    functieptcrawl()

# for link in bsup.find('div' ,{'id':'offer-block-paying'}):
#     if 'href' in link.attrs:
#         print(link.attrs['href'])
# print(b.text)
#print("Titlu paginii este " + bsup.title.string)
#continutulcunume=bsup.find("div",{"class" : "mv-parser-output"})
    # #for link in soup.findall('a',{'class': 'Table_personName__UO41W'}):
    # for link in continutulcunume.find_all('a'):
    #     print("link")