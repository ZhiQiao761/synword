import json
import re
from typing import Tuple

import docx2txt
import nltk
from vocabulary.vocabulary import Vocabulary


def extract_text(file):
    text = docx2txt.process(file)
    return text


def get_stopwords(download=True):
    try:
        return set(nltk.corpus.stopwords.words('english'))
    except LookupError:
        nltk.download('stopwords')
        return get_stopwords(download=False)


def modify(text: str) -> Tuple[str, str]:
    stopwords = get_stopwords()
    word_counter = collections.Counter(
        w for w in text.lower().split() if w not in stopwords
    )
    freq_words = word_counter.most_common(5)

    modified_text = text
    for word, _ in freq_words:
        syns = json.loads(Vocabulary.synonym(word))
        repl = syns[0]['text']
        modified_text = re.sub(word, repl, modified_text,
                               flags=re.I | re.M | re.S)
    return modified_text
