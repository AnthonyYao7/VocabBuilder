import requests
import pprint
import numpy as np
import genanki


api_key = "use your own api key, get it from merriam webster"
url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/{}?key={}"

my_model = genanki.Model(
    1607392319,
    'Simple Model',
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
    ],
    templates=[
    {
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
])


def fmt_url(word, apikey=api_key):
    return url.format(word, apikey)


def read_wordlist(file):
    with open(file) as f:
        words = f.read()
        return words.split('\n')


def get_word_defs(word, n=2):
    w_url = fmt_url(word)

    r = requests.get(w_url).json()

    definitions = []
    
    for definition in r:
        definitions += (definition['shortdef'])


    len_list = [len(x) for x in definitions]
    indices = np.argpartition(len_list, -min(n, len(len_list)))[-min(n, len(len_list)):]

    final_defs = [definitions[indices[x]] for x in range(min(len(indices), n))]

    return final_defs
    

def create_anki_note(word, defs):
    notes = []
    
    for definition in defs:
        notes.append(genanki.Note(
            model=my_model,
            fields=[word, definition]
        ))
        notes.append(genanki.Note(
            model=my_model,
            fields=[definition, word]
        ))
    return notes


def main():
    words = read_wordlist("words.txt")

    my_deck = genanki.Deck(
        2059400110,
        'VocabWords'
    )
    
    for word in words:
        
        defs = get_word_defs(word)
        
        
        notes = create_anki_note(word, defs)
        for note in notes:
            my_deck.add_note(note)

    genanki.Package(my_deck).write_to_file("output.apkg")


if __name__ == "__main__":
    main()
