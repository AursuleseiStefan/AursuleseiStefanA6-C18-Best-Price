""" URL utile pentru a rula rapid proiectul:
 https://www.compari.ro/telefoane-mobile-c3277/samsung/galaxy-z-fold4-5g-256gb-12gb-ram-dual-f936-p841779084/ 
 https://www.compari.ro/telefoane-mobile-c3277/samsung/galaxy-s22-5g-128gb-8gb-ram-dual-sm-s901b-p766823406/
 https://www.compari.ro/telefoane-mobile-c3277/samsung/galaxy-z-flip4-5g-128gb-8gb-ram-dual-f721-p841833855/
 https://www.compari.ro/frigidere-congelatoare-c3168/heinner/hc-v268f-p450754938/
"""
import requests as req
from bs4 import BeautifulSoup
import sys
import json
import re

def functiecuargumente():
    # Verificam daca dam de la tastatura mai putin de 2 argumente
    if len(sys.argv)<2:
        return "prea putine argumente"
    return True


def functieptcrawl():
    listadedictionare = []
    if functiecuargumente():
        vectordeargumente = []
        numecomplet = ""
        # am pus in vectorul "vectordeargumente" fiecare argument dat in linia de comanda incepand cu a 2 a pozitie
        for i in range(1,len(sys.argv)):
            vectordeargumente.append(sys.argv[i])
        vectcupretur = []
        # Am creat o variabila url care primeste pe rand argumentele,in cazul nostru url urile
        for url in vectordeargumente:
            vectcupretur = []
            dictionarcutoate = {}
            vectorfararon = []
            # Trimite un requeste catre url 200-ok  404-not found
            rasp = req.get(url)
            # Atribuim variabilei bsup raspunsul requestului url ului si folosim lxml ca default parser
            bsup=BeautifulSoup(rasp.text,"lxml")
            # Atribuim variabilei c un find in care o sa cautam numele produsului
            c=bsup.find('h1' ,{'class':'hidden-xs'})
            # Atribuim unei variabile cate un find catre un bloc de continut din site ul compari.ro
            # in care o sa cautam preturile produselor (structura site-ului)
            a=bsup.find('div' ,{'id':'offer-block-paying'})
            b=bsup.find('div' ,{'id':'offer-block-promoted'})
            d=bsup.find('div' ,{'id':'offer-block-free'})
            # Cautam in site din toate headerele cu propietatile mentionate numele produsului
            # atribuind unei variabile "numecomplet" toate spanurile cu itemprop name
            # structura site-ului avand numele telefonului cu modelul separate
            # am pus spatiu intre ele deoarece nume complet ar fi fost : "NumeprodusModelul"
            for link in c.findAll('span' ,{'itemprop':'name'}):
                numecomplet=numecomplet + " " + link.text
            # Am luat toate span-urile din div urile de mai sus atribuit variabilelor "a","b" si respectiv "c"
            # si am adaugat in vector toate preturile din bloc-urile:
            # "Ofertele noastre","Alege oferte pentru produsul"si respectiv"Mai multe oferte"
            
            # Ofertele noastre
            for link in a.findAll('span' ,{'data-akjl':'Price||Price||1'}):
                vectcupretur.append(link.text)
            
            # Oferte evidentiate
            for link in b.findAll('span' ,{'data-akjl':'Price||Price||1'}):
                vectcupretur.append(link.text)
            
            # Mai multe oferte
            for link in d.findAll('span' ,{'data-akjl':'Price||Price||1'}):
                vectcupretur.append(link.text)
            
            # Acest for are scopul de a transforma textul din "vectcupretur" intr-un float
            # astfel incat sa putem sorta corect preturile pentru a le putea folosi ulterior
            for i in range(0,len(vectcupretur)):
                # Am vrut sa creez un vector in care sa avem numai cifre
                # Structura site-ului returneaza un pret de forma "1 000,00 RON"
                # Am adaugat in vectorfararon un regex in care scoate currency ul produsului 
                vectorfararon.append((re.split(r"[\s]+[A-Z]+",vectcupretur[i])[0]))
                # Am inlocuit in "vectorfararon" virgula cu punct 
                # pregatind string ul de conversia in float
                # Exemplu: 1 000,00 -> 1 000.00
                vectorfararon[i] = vectorfararon[i].replace("," , ".")
                # Am redus spatiul dintr-e cifre 
                # Exemplu: 1 000.00 -> 1000.00
                vectorfararon[i] = vectorfararon[i].replace(" " , "")
                # Am convertit string-ul in float pentru a putea sorta vectorul de preturi
                vectorfararon[i] = float(vectorfararon[i])
            # Am sortat vectorul cu preturi
            vectorfararon.sort()
            
            # Am creat un dictionar gol la linia de cod 33 in care
            # Atribuim unui "nume" numele produsului luat din for ul de la linia de cod 50
            dictionarcutoate["nume"] = numecomplet
            # Atribum cheilor "cel mai mic pret" si "cel mai mare pret"
            # prima si ultima valoare din vectorul sortat adaugand si currency ul respectiv
            # L-am transformat in string ca sa pot lipi de currency
            dictionarcutoate["cel mai mic pret"] = str(vectorfararon[0]) + " Ron"
            dictionarcutoate["cel mai mare pret"] = str(vectorfararon[-1]) + " Ron"
            # Am adaugat in oferte lungimea vectorului "vectorfararon"
            # deoarece dorim sa vedem cate oferte avem
            dictionarcutoate["oferte"] = len(vectorfararon)
            # Am golit variabila "numecomplet" deoarece dorim pentru fiecare url
            # sa sa nu se lipeasca numele de cel anterior
            numecomplet = ""
            
            # In "listadicionare" creeat la linia de cod 22
            # am creat o lista in care sa punem toate produsele 
            # pentru a putea sa exportam toate datele la un loc
            # intr-un fisier json 
            listadedictionare.append(dictionarcutoate)
        # Am apelat functia "functiepentrujson" creeata la linia de cod 109
        functiedepusinjson(listadedictionare)
            
def functiedepusinjson(listadedicti):
    # Am creat un obiect json in care folosim functia dumps 
    # pentru a pune obiecte din python intr un string de tipul json
    # Folosim indent deoarece nu dorim 
    # sa ne puna toate datele intr-un singur rand
    # 2 = spatii folosite
    json_object = json.dumps(listadedicti, indent=2) 
    
    # Deschiden fisierul (daca nu exista,creeam unul)
    # Am introdus in open numele fisierului si
    # am pus "w" pentru write deoarece dorim sa scriem in fisier
    # Folosind with ne inchide automat fisierul dupa folosire
    with open("fisier1.json", "w") as outfile:
        # Am scris in fisier obiectul convertit din python
        outfile.write(json_object)
    
if __name__=='__main__':
    functieptcrawl()
