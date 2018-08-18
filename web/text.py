import collections
import json
import os
import re
from typing import Tuple

import docx2txt
import nltk
from vocabulary.vocabulary import Vocabulary


class UnsupportedFileError(Exception):
    pass


def extract_text(file):
    ext = os.path.splitext(file.name)[1]
    if ext == '.docx':
        text = docx2txt.process(file)
    elif ext == '.txt':
        text = file.read().decode('utf')
    else:
        raise UnsupportedFileError(f'File {ext} is not supported')
    return text


def get_stopwords(download=True):
    try:
        return set(nltk.corpus.stopwords.words('english'))
    except LookupError:
        if download:
            nltk.download('stopwords')
            return get_stopwords(download=False)
        raise  # something wrong with downloading


def modify(text: str) -> Tuple[str, str]:
    stopwords = get_stopwords()
    re_word = re.compile(r'^\w+$')
    word_counter = collections.Counter(
        w for w in text.lower().split() if w not in stopwords and re_word.match(w)
    )
    freq_words = word_counter.most_common(5)

    modified_text = text
    for word, _ in freq_words:
        try:
            syns = json.loads(Vocabulary.synonym(word))
        except TypeError as e:
            print(f'Cannot find synonym for "{word}" ({e})')
            continue
        repl = syns[0]['text']
        modified_text = re.sub(word, repl, modified_text,
                               flags=re.I | re.M | re.S)
    return modified_text
