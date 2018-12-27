from os import listdir
from os.path import isfile, join
import csv
import glob
import unidecode

## public options
option_anonymize = False
option_crash_on_missing_venue = True

## debugging options
debug_author=True
debug_author_name="Wagner"
debug_venues=False

## directories
DATA_DIR="CSIndex/data"
PROF_DATA_DIR="{0}/profs/search".format(DATA_DIR)

## publication record of researchers
profs="{0}/profs/all-authors.csv".format(DATA_DIR)
## data for journals and conferences
journals_stats="{0}/*-out-stats-journals.csv".format(DATA_DIR)
confs_stats="{0}/*-out-stats.csv".format(DATA_DIR)
## affiliation of researches
#affiliation="{0}/all-researchers.csv".format(DATA_DIR)
## area of researchers
area="{0}/profs.csv".format(DATA_DIR)

## list of authors to deanonymize
publicNamesFileName="data/publicnames.txt"

## abreviated names for venues
venuesAbrev="data/abrevs.txt"

## cnpq-pq data
cnpqpq="data/bolsas_cnpq_names_revised.csv"

## index of column for the rank in files 
JOURNAL_FILE_RANK_NUMBER=4 # *-out-stats-journals.csv
CONFERENCE_FILE_RANK_NUMBER=6 # *-out-stats.csv

## workaround: author names are not uniformly used in csindexbr
author_synonyms = {
    "Alberto Schaeffer Filho":"Alberto Schaeffer-Filho",
    "Mauricio Ayala Rincon":"Mauricio Ayala-Rincon"
}

## venues by type
A_venues=[]
B_venues=[]
C_venues=[]

def main():

    # load venues abbreviation data
    replacements={}
    with open(venuesAbrev) as csv_file:                                                                        
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            shortName = row[0]
            longName = row[1]
            replacements.update({shortName: longName})    

    # load affiliation and area data
    affiliation_dict={}
    areas_dict={}
    with open(area) as csv_file:                                                                        
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            authorName = row[0]
            instName = row[1]
            areas = row[2]
            affiliation_dict.update({authorName: instName})
            areas_dict.update({authorName: areas})


    # load CNPQ-PQ levels
    cnpq_pq_dict={} # name: level
    with open(cnpqpq) as csv_file:                                                                        
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            cnpq_pq_dict.update({row[0]: row[1]})

    # load solicitations of de-anonymization
    publicNames = [line.rstrip('\n') for line in open(publicNamesFileName)]

    # add journals and conferences to buckets A_venues, B_venues, and C_venues
    journals = glob.glob(journals_stats)
    processVenues(journals, JOURNAL_FILE_RANK_NUMBER, True)

    conferences = glob.glob(confs_stats)
    processVenues(conferences, CONFERENCE_FILE_RANK_NUMBER, False)
    if debug_venues:
        print(A_venues)
        print(B_venues)
        print(C_venues)

    ## iterate through researcher's record
    lines = [line.rstrip('\n') for line in open(profs)]
    for profname in lines:
        profNameFile="{0}/{1}.csv".format(PROF_DATA_DIR, profname).replace(' ', '-')
        if not isfile(profNameFile):
            raise Exception('Could not find file for {0}'.format(profNameFile))
        score = 0
        numA = 0
        numB = 0
        numC = 0
        numConference = 0
        numJournal = 0
        if debug_author and debug_author_name == profname: print('DEBUG: ' + profname)
        with open(profNameFile) as csv_file:                                                                        
            csv_reader = csv.reader(csv_file, delimiter=',')

            for row in csv_reader:
                ## variables for important columns to facilitate access
                ## first columns: year, venue, title, authors, ...
                venue = row[1]
                journalOrConference = row[6].strip() # J for journal and C for conference

                if venue in replacements:
                    venue = replacements[venue]

                if venue in A_venues:
                    numA += 1
                    if debug_author and debug_author_name == profname: print('DEBUG: {0} {1}'.format('A', venue))
                elif venue in B_venues:
                    numB += 1
                    if debug_author and debug_author_name == profname: print('DEBUG: {0} {1}'.format('B', venue))
                elif venue in C_venues:
                    numC += 1
                    if debug_author and debug_author_name == profname: print('DEBUG: {0} {1}'.format('C', venue))
                else:
                    if option_crash_on_missing_venue:
                        raise Exception("Could not find venue! >{0}< Update replacements".format(venue))
                    else:
                        print("Could not find venue! Update replacements>{0}".format(venue))
                
                if journalOrConference == 'C':
                    numConference += 1
                elif journalOrConference == 'J':
                    numJournal += 1
                else:
                    raise Exception("Bad kind. Please check >{0}<".format(journalOrConference))


        score = numA + 0.4*numB + 0.33*numC

        if debug_author and debug_author_name == profname: print('DEBUG: {0} {1} {2} -> score = {3}'.format(numA, numB, numC, score))

        ## look up the author institution name
        instName = ""

        # unidecode.unidecode removes accents, just in case
        profname2 = unidecode.unidecode(profname)
        
        ## finding insitution name
        if profname in affiliation_dict:
            instName = affiliation_dict[profname]
        elif profname2 in affiliation_dict:
            instName = affiliation_dict[profname2]
        else: # different ways to name the author :(
            instName = affiliation_dict[author_synonyms[profname]]

        ## finding area name
        if profname in areas_dict:
            areas = areas_dict[profname]
        elif profname2 in areas_dict:
            areas = areas_dict[profname2]
        else: # different ways to name the author :(
            areas = areas_dict[author_synonyms[profname]]

        if option_anonymize:
            if not profname in publicNames:
                profname = "anonymous"

        pqlevel = "x"
        if profname in cnpq_pq_dict:
            pqlevel = cnpq_pq_dict[profname]

        print("{0:.2f}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}".format(float(score), pqlevel, profname, numA, numB, numC, instName, areas, numConference, numJournal))

def processVenues(venues, rankNum, isJournal):
    for venue in venues:
        with open(venue) as csv_file:                                                                        
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                name = str.strip(row[0]) # removing leading-trailing white spaces
                rank = row[rankNum]
                if rank == "top":
                    A_venues.append(name)
                elif rank == "" and isJournal: # only journals in this category
                    B_venues.append(name)
                else: #includes magazines, short, and other
                    C_venues.append(name)    

if __name__ == "__main__":
    main()
