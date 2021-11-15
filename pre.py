import csv
import re

fieldnames = ['party', 'rep', 'text']
csvin = open('raw.csv', 'r', newline='', encoding='utf-8')
csvout = open('preprocessed.csv', 'w', newline='', encoding='utf-8')
csvreader = csv.reader(csvin, lineterminator='\n')
csvwriter = csv.DictWriter(csvout, lineterminator='\n', fieldnames=fieldnames)
joined_paragraph = ''
joined_kepviselo = ''
joined_party = ''
comment_reg = re.compile(r"\(.*\)")
csvwriter.writeheader()
for row in csvreader:
    if row[2].strip().startswith('ELNÖK'):
        continue
    if row[2].strip().startswith(row[1].upper()):
        if len(joined_paragraph) > 0:
            joined_paragraph = comment_reg.sub('', joined_paragraph).strip()
            csvwriter.writerow(
                {'party': joined_party, 'rep': joined_kepviselo, 'text': joined_paragraph})
        joined_party = row[0]
        joined_kepviselo = row[1]
        joined_paragraph = row[2].strip()
        startreg = re.compile(
            '^' + row[1].upper() + r',?[\w\s]{0,10}(\(\w+\))?[\w\s]{0,30}(:|,)')
        joined_paragraph = startreg.sub('', joined_paragraph).strip()
    else:
        joined_paragraph += '\n' + row[2].strip()
joined_paragraph = comment_reg.sub(' ', joined_paragraph).strip()
csvwriter.writerow(
    {'party': joined_party, 'rep': joined_kepviselo, 'text': joined_paragraph})
