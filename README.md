# Bibtex2LinkedIn

A Python 3 script to convert a Bibtex database to the [LinkedIn journal publications](https://developer.linkedin.com/docs/ref/v2/profile/publication) format for import using v2 of the [LinkedIn REST API](https://developer.linkedin.com/docs/guide/v2/people/profile-edit-api/publications).

## Usage

`python3 convert.py -f <bibtexfile> [-n <surname>] [-i <linkedin id>] [-t] [-j]`

If `surname` is specified, occurrences of surname will be replaced by LinkedIn ID in the authors list.

`-t` converts article titles to titlecase

`-j` converts journal names to titlecase

Journals are added to the publisher field on LinkedIn.
