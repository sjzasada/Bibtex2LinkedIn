import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from titlecase import titlecase
import json

with open('citations.bib') as bibtex_file:
    parser = BibTexParser()
    parser.customization = convert_to_unicode

    bib_database = bibtexparser.load(bibtex_file, parser=parser)

    for i, entry in enumerate(bib_database.entries):
        print(i);

        entry = bibtexparser.customization.author(entry)

        title = titlecase(entry['title'])

        journal = ""
        if 'journal' in entry:
            journal = entry['journal']
        elif 'booktitle' in entry:
            journal = entry['booktitle']
        elif 'school' in entry:
            journal = entry['school']

        journal = titlecase(journal)
        year = entry['year']

        pub = {}
        pub['date'] = {'year': year}

        pub['name'] = {'localized': {'en_US': title}, 'preferredLocale': {'country': 'US', 'language': 'en'}}
        pub['publisher'] = {'localized': {'en_US': journal}, 'preferredLocale': {'country': 'US', 'language': 'en'}}

        if 'url' in entry:
            pub['url'] = entry['url']

        names = bibtexparser.customization.getnames(entry['author'])

        for j, name in enumerate(names):
            nom = bibtexparser.customization.splitname(name, strict_mode=False)

            print(nom)

        json_data = json.dumps(pub)
        print(json_data)
