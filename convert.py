import getopt, sys
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
from titlecase import titlecase
import json

def parseBibentry(entry, myName, myId, titcase, jorcase):
    entry = bibtexparser.customization.author(entry)

    title = entry['title']
    if titcase:
        title = titlecase(title)

    journal = ""
    if 'journal' in entry:
        journal = entry['journal']
    elif 'booktitle' in entry:
        journal = entry['booktitle']
    elif 'school' in entry:
        journal = entry['school']

    if jorcase:
        journal = titlecase(journal)

    year = entry['year']

    pub = {}
    pub['date'] = {'year': year}

    pub['name'] = {'localized': {'en_US': title}, 'preferredLocale': {'country': 'US', 'language': 'en'}}
    pub['publisher'] = {'localized': {'en_US': journal}, 'preferredLocale': {'country': 'US', 'language': 'en'}}

    if 'url' in entry:
        pub['url'] = entry['url']

    names = bibtexparser.customization.getnames(entry['author'])

    people = []
    for j, name in enumerate(names):
        nom = bibtexparser.customization.splitname(name, strict_mode=False)

        components = nom['first']
        components.extend(nom['von'])
        components.extend(nom['last'])
        components.extend(nom['jr'])

        fullname = " ".join(components)

        if myName and myName in nom['last']:
            people.append({'memberId': 'urn:li:person:'+myId})

        else:
            people.append({'name': fullname})

        #LinkedIn limit of 10 authors
        if j > 9:
            break

    pub['authors'] = people
    return pub;

def usage():
    print("usage: convert.py -f <bibtexfile> [-n <surname>] [-i <linkedin id>] [-t] [-j]\n")
    print("If surname is specified, occurrences of surname will be replaced by LinkedIn ID in the authors list.")
    print("-t converts article titles to titlecase, and -j converts journal names to titlecase\n")
    return;

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "tjn:i:f:", ["name=", "id=", "file="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    titcase=False
    jorcase=False
    name = ""
    id = ""

    for o, a in opts:
        if o == "-t":
            titcase = True
        elif o == "-j":
            jorcase = True
        elif o in ("-f", "--file"):
            filename = a
        elif o in ("-n", "--name"):
            name = a
        elif o in ("-i", "--id"):
            id = a
        else:
            assert False, "unhandled option"

    #check for sensible arguments
    if 'filename' not in locals():
        print('Filename not set')
        usage()
        sys.exit(3)

    if not id:
        if name:
            print("Name set but ID not specified")
            usage()
            sys.exit(4)

    with open(filename) as bibtex_file:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bibtex_file, parser=parser)

        pubs = []
        for i, entry in enumerate(bib_database.entries):
            print('Entry {}'.format(i));

            pubs.append(parseBibentry(entry, name, id, titcase, jorcase))

        print(json.dumps(pubs, indent=4, sort_keys=True))

    return;

if __name__ == '__main__':
    main()
