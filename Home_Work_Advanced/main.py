import re
from pprint import pprint
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
#pprint(contacts_list)

def red_telephone(tel):
    pattern = r'^(\+7|8)?\s?\(*(\d{3})\)*[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s+\(?(доб.)\s*(\d*))?'
    substitution = r'+7(\2)\3-\4-\5 \7\8'
    result = re.sub(pattern, substitution, tel)
    print(result)
    return result

new_contacts = list()

for person in contacts_list[1:]:
    fio = ' '.join(person[:3]).split(' ')[:3]
    person[:3] = fio
    if person[5]:
        person[5] = red_telephone(person[5])
    if person[0] in new_contacts:
        j = new_contacts.index(person[0]) + 1
        for k in range(1, len(person)):
            if person[k]:
                contacts_list[j][k] = person[k]
        contacts_list.pop(len(new_contacts)+1)
    else:
        new_contacts.append(fio[0])

pprint(contacts_list)

## 2. Сохраните получившиеся данные в другой файл.
## Код для записи файла в формате CSV:
with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')

    ## Вместо contacts_list подставьте свой список:
    datawriter.writerows(contacts_list)