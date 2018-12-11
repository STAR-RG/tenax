import json
import csv

CSVFILE="/tmp/ranking.csv"

def main():

        # load venues abbreviation data
    data=[]
    with open(CSVFILE) as csv_file:                                                                        
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            score = row[0]
            cnpq = row[1]
            name = row[2]
            numA = row[3]
            numB = row[4]
            numC = row[5]
            inst = row[6]
            numConferencePapers = row[7]
            numJournalPapers = row[8]
            data.append(
                {"name": name.strip(),
                 "institution": inst.strip(),
                 "bolsa-cnpq": cnpq.strip(),
                 "num-csindexbr-papers": int(numA)+int(numB)+int(numC),
                 "num-csindexbr-confs": numConferencePapers,
                 "num-csindexbr-journals": numJournalPapers,
                 "num-tier-one": int(numA),
                 "num-tier-two": int(numB),
                 "num-tier-three": int(numC),
                 "csindexbr-score": float(score),
                 "papers": []
                }
                )    

    json_data = json.dumps({"data": data}, indent=4, separators=(',', ': '))

    print(json_data)


if __name__ == "__main__":
    main()
