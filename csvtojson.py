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
            data.append(
                {"name": name.strip(),
                 "institution": inst.strip(),
                 "bolsa-cnpq": cnpq.strip(),
                 "num-csindexbr-papers": int(numA)+int(numB)+int(numC),
                 "num-csindexbr-confs": "todo",
                 "num-csindexbr-journals": "todo",
                 "num-top-papers": int(numA),
                 "csindexbr-score": float(score),
                 "csrankings-score": "todo",
                 "papers": []
                }
                )    

    json_data = json.dumps({"data": data}, indent=4, separators=(',', ': '))

    print(json_data)


if __name__ == "__main__":
    main()
