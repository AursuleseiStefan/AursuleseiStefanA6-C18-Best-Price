import requests as req
from bs4 import BeautifulSoup
import sys
import json
import re
import lxml


def functiecuargumente():
    # Verificam daca dam de la tastatura mai putin de 2 argumente
    if len(sys.argv) < 2:
        return "prea putine argumente"
    return True


def functieptcrawl():
    listadedictionare = []
    if functiecuargumente():
        vectordeargumente = []
        numecomplet = ""
        # am pus in vectorul "vectordeargumente" fiecare argument dat in linia de comanda incepand cu a 2 a pozitie
        for i in range(1, len(sys.argv)):
            vectordeargumente.append(sys.argv[i])
        vectcupretur = []
        # Am creat o variabila url care primeste pe rand argumentele,in cazul nostru url urile
        for url in vectordeargumente:
            vector_de_verificare=[]
            vectcupretur = []
            dictionarcutoate = {}
            vectorfararon = []
            # Trimite un requeste catre url 200-ok  404-not found
            rasp = req.get(url)
            # Atribuim variabilei bsup raspunsul requestului url ului si folosim lxml ca default parser
            bsup = BeautifulSoup(rasp.text, "lxml")
            # Atribuim variabilei c un find in care o sa cautam numele produsului
            c = bsup.find('div', {'class': 'row product-page-top'})
            # Atribuim unei variabile cate un find catre un bloc de continut din site ul compari.ro
            # in care o sa cautam preturile produselor (structura site-ului)
            a = bsup.find('div', {'id': 'offer-block-paying'})
            b = bsup.find('div', {'id': 'offer-block-promoted'})
            d = bsup.find('div', {'id': 'offer-block-free'})
            tip_de_produs=functie_pentru_tipul_produsului(url)
    #---o varianta mai rapida decat sa ma joc cu link ul
            tip_de_produs2 = bsup.find('div', {'class': 'breadcrumb-cat hidden-xs'})
            nume_categorie = tip_de_produs2.findAll('a', {})[2].text
    #------
            #pentru numarul de oferte de pe site
            pentru_oferte = bsup.find('div', {'class': 'row product-page-top'})
            pret_ascuns = bsup.find(('div', {'class': 'optoffer-more-wrap device-desktop'}))
            # Cautam in site din toate headerele cu propietatile mentionate numele produsului
            # atribuind unei variabile "numecomplet" toate spanurile cu itemprop name
            # structura site-ului avand numele telefonului cu modelul separate
            # am pus spatiu intre ele deoarece nume complet ar fi fost : "NumeprodusModelul"
            for link in c.findAll('span', {'itemprop': 'name'}):
                numecomplet = numecomplet + " " + link.text
            # Am luat toate span-urile din div urile de mai sus atribuit variabilelor "a","b" si respectiv "c"
            # si am adaugat in vector toate preturile din bloc-urile:
            # "Ofertele noastre","Alege oferte pentru produsul"si respectiv"Mai multe oferte"

            # Ofertele noastre
            #nume=era numele magazinului,am facut mai mult pentru debug
            for link,nume in zip(a.findAll('span', {'data-akjl': 'Price||Price||1'}),a.findAll('div', {'data-akjl': 'Store name||StoreName'})):
                vectcupretur.append(link.text)
                # vector_de_verificare.append(link.text)
                # vector_de_verificare.append(nume.text)

            # Oferte evidentiate
            try:
                for link,nume in zip(b.findAll('span', {'data-akjl': 'Price||Price||1'}),b.findAll('div', {'data-akjl': 'Store name||StoreName'})):
                    vectcupretur.append(link.text)
                    # vector_de_verificare.append(link.text)
                    # vector_de_verificare.append(nume.text)
            except:
                pass
            # Mai multe oferte
            try:
                for link,nume in zip(d.findAll('span', {'data-akjl': 'Price||Price||1'}),d.findAll('div', {'data-akjl': 'Store name||StoreName'})):
                    vectcupretur.append(link.text)
                    # vector_de_verificare.append(link.text)
                    # vector_de_verificare.append(nume.text)
            except:
                #print(e)
                pass
            #pt numarul de oferte
            for nr_oferta in pentru_oferte.findAll('span',{'class': 'offer-count'}):
                oferte=nr_oferta.text


            # for link,nume in zip(pret_ascuns.findAll('span', {'data-akjl': 'Price||Price'}),pret_ascuns.findAll('div', {'data-akjl': 'Store name||StoreName'})):
            #     vector_de_verificare.append(link.text)
            #     vector_de_verificare.append(nume.text)
            # Acest for are scopul de a transforma textul din "vectcupretur" intr-un float
            # astfel incat sa putem sorta corect preturile pentru a le putea folosi ulterior
            for i in range(0, len(vectcupretur)):
                # Am vrut sa creez un vector in care sa avem numai cifre
                # Structura site-ului returneaza un pret de forma "1 000,00 RON"
                # Am adaugat in vectorfararon un regex in care scoate currency ul produsului
                vectorfararon.append((re.split(r"[\s]+[A-Z]+", vectcupretur[i])[0]))
                # Am inlocuit in "vectorfararon" virgula cu punct
                # pregatind string ul de conversia in float
                # Exemplu: 1 000,00 -> 1 000.00
                vectorfararon[i] = vectorfararon[i].replace(",", ".")
                # Am redus spatiul dintr-e cifre
                # Exemplu: 1 000.00 -> 1000.00
                vectorfararon[i] = vectorfararon[i].replace(" ", "")
                # Am convertit string-ul in float pentru a putea sorta vectorul de preturi
                vectorfararon[i] = float(vectorfararon[i])
            # Am sortat vectorul cu preturi
            vectorfararon.sort()

            # Am creat un dictionar gol la linia de cod 33 in care
            # Atribuim unui "nume" numele produsului luat din for ul de la linia de cod 50
    #--VARIANTA MAI RAPIDA
            dictionarcutoate["nume"] = nume_categorie+" ->"+numecomplet
    #------
            #dictionarcutoate["nume"] = tip_de_produs + " ->" + numecomplet
            # Atribum cheilor "cel mai mic pret" si "cel mai mare pret"
            # prima si ultima valoare din vectorul sortat adaugand si currency ul respectiv
            # L-am transformat in string ca sa pot lipi de currency
            dictionarcutoate["cel mai mic pret"] = str(vectorfararon[0]) + " Ron"
            dictionarcutoate["cel mai mare pret"] = str(vectorfararon[-1]) + " Ron"
            # Am adaugat in oferte lungimea vectorului "vectorfararon"
            # deoarece dorim sa vedem cate oferte avem
            dictionarcutoate["oferte"] = oferte #len(vectorfararon)
            # Am golit variabila "numecomplet" deoarece dorim pentru fiecare url
            # sa sa nu se lipeasca numele de cel anterior
            numecomplet = ""

            # In "listadicionare" creeat la linia de cod 22
            # am creat o lista in care sa punem toate produsele
            # pentru a putea sa exportam toate datele la un loc
            # intr-un fisier json
            listadedictionare.append(dictionarcutoate)
        #print(vectorfararon)

        # for i in range (0,len(vector_de_verificare),2):
        #     print(vector_de_verificare[i+1])
        # print(len(vector_de_verificare) / 2)
        # Am apelat functia "functiepentrujson" creeata la linia de cod 109
        functiedepusinjson(listadedictionare)


def functie_pentru_tipul_produsului(nume_link_produs):
    ceva=nume_link_produs.split("/")
    #print(ceva[3])
    if ceva[2] == 'www.compari.ro':
        #https://www.compari.ro/masini-de-spalat-vase-c3171/bosch/smv46kx04e-p484330443/---->
        tip_produs = ceva[3]
        #masini-de-spalat-vase-c3171
        split_la_produs = tip_produs.split("-")
        #['masini', 'de', 'spalat', 'vase', 'c3171']
        split_la_produs.pop(-1)
        #['masini', 'de', 'spalat', 'vase']
        final=''
        for cuvant in split_la_produs:
            final += ' '+cuvant
        #" masini de spalat vase"
        string_fara_spatiu=final[1:]
        #print(final)
        #fara primul spatiu
        return string_fara_spatiu.title()
    else:
        # https://periuta-de-dinti-electrica.compari.ro/oral-b/io-series-4-p826222398/
        tip_produs=ceva[2]
        #periuta-de-dinti-electrica.compari.ro
        #split_la_produs=tip_produs.split('-')
        split_la_produs=tip_produs.split('.')
        #['periuta-de-dinti-electrica', 'compari', 'ro'
        split_la_produs.pop(-1)
        split_la_produs.pop(-1)
        split2=split_la_produs[0]
        #['periuta-de-dinti-electrica']
        cuvant_final=split2.replace('-',' ')
        #tip_produs.replace('-',' ')
        #periuta de dinti electrica
        return cuvant_final.title()

    #print(split_la_produs)
    #.title() face prima litera mare

    #return split_la_produs

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


if __name__ == '__main__':
    functieptcrawl()
