from bs4 import BeautifulSoup
from urllib.request import (urlopen, urlparse, urlunparse, urlretrieve)
import csv
from difflib import SequenceMatcher
import heapq
import unidecode

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

## directories
DATA_DIR="../data"

## list of researchers
profs="{0}/profs/all-authors.csv".format(DATA_DIR)

# URL to download list from CNPq
URL="http://plsql1.cnpq.br/divulg/RESULTADO_PQ_102003.prc_comp_cmt_links?V_COD_DEMANDA=200310&V_TPO_RESULT=CURSO&V_COD_AREA_CONHEC=10300007&V_COD_CMT_ASSESSOR=CC"

# cnpq uses complete names whereas csindex does not
cnpq_to_csindex_name_map = {}

def main():

    ## look for correspondence
    dict={}
    ## load name of researchers as per csindex
    csindexnames = [line.rstrip('\n') for line in open(profs)]
    ## load cnpq data
    soup = BeautifulSoup(urlopen(URL), 'lxml') # Parse the HTML as a string
    table = soup.find_all('table')[3].find_all('table')[1] # Grab the first table
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns)<2: continue
        ## cnpq data includes accents; csindex does not. this is a big problem for comparison.
        ## remove accents!
        authorName=unidecode.unidecode(columns[0].get_text())
        if authorName == "Nome" or authorName == "Início": continue
        level=columns[1].get_text()

        firstnameCNPQ = authorName.split(" ")[0]

        ##TODO: check if first + last name is an exact match!
        
        if not authorName in csindexnames:                
            # look for the most similar name whose first name match
            prioQueue = []
            for x in csindexnames:
                firstnameCSINDEX = x.split(" ")[0]
                if (not firstnameCNPQ == firstnameCSINDEX): continue
                sim = similar(authorName, x)
                heapq.heappush(prioQueue, (sim, x))

            ## call attention to fix this thing!
            authorName = "{0} => {1}".format(authorName, heapq.nlargest(5, prioQueue))

        dict.update({authorName: level})
    
    for (key, value) in dict.items():
        print("{0}, {1}".format(key, value))


if __name__ == "__main__":
    # a='Adenilso da Silva Simao'
    # b='Adenilso Simao'
    # seq=SequenceMatcher(None, a,b)
    # d=seq.ratio()*100
    # print(d)
    # d=similar(a, b)
    # print(d)
    # print('{0:.2f} , {1}'.format(d, 'hello'))
    main()