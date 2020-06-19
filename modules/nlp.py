import itertools
import nltk
import gensim
import string

from bs4 import BeautifulSoup
from bs4.element import Comment
from modules.dbConnection import next_pending_content
from nltk.stem import WordNetLemmatizer
from polyglot.detect import Detector
from gensim import corpora

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

ADDITIONAL_STOPWORDS = [
    'html', 'login', 'register', 'online', 'user', 'faq', 'comment', 'post',
    'link', 'registration', 'username'
]

languages = {
    'en': "english",
    'es': "spanish",
    'ru': "russian"
}

ID = 0
CONTENT = 1
URI = 2


def get_language(text):
    lang = Detector(
        str(text).encode('ascii', 'replace').decode(),
        quiet=True).language.code
    if lang in languages.keys():
        lang = languages[lang]
    else:
        lang = "english"
    return lang


def clean_text(text, lang):
    stopwords = set(nltk.corpus.stopwords.words(lang))
    for sw in ADDITIONAL_STOPWORDS:
        stopwords.add(sw)
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    stop_word_removal = " ".join(
        [i for i in text.lower().split() if i not in stopwords])
    punctuation_removal = ''.join(
        ch for ch in stop_word_removal if ch not in exclude)
    normalized = " ".join(
        lemma.lemmatize(word) for word in punctuation_removal.split())
    return normalized


def analysis():
    content = next_pending_content()
    print("Analyzing..."+content[URI])
    text_found = text_from_html(content[CONTENT])
    lang = get_language(text_found)
    text_cleaning = [
        clean_text(document, lang).split() for document in [text_found]]

    if not text_cleaning or (len(text_cleaning) == 1 and not text_cleaning[0]):
        return {
        'id': content[ID],
        'topic': [],
        'lang': lang
    }

    dictionary = corpora.Dictionary(text_cleaning)
    dt_matrix = [dictionary.doc2bow(doc) for doc in text_cleaning]
    lda_object = gensim.models.ldamodel.LdaModel
    lda_model = lda_object(dt_matrix, num_topics=1, id2word=dictionary)

    print(lda_model.print_topics(num_topics=1, num_words=10))
    terms = []
    for tw in lda_model.show_topic(topicid=0, topn=10):
        terms.append(tw[0])

    return {
        'id': content[ID],
        'topic': terms,
        'lang': lang
    }


def tag_visible(element):
    valid_tags = ['style', 'script', 'head', 'title', 'meta', '[document]']
    if element.parent.name in valid_tags:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)

    meta = soup.find_all('meta')
    clave_tags = ['description', 'keywords']
    key_texts = []
    for tag in meta:
        if ('name' in tag.attrs.keys()
                and tag.attrs['name'].strip().lower() in clave_tags
                and tag.attrs.get('content')):
            key_texts.append(tag.attrs['content'])

    return u" ".join(
        t.strip() for t in itertools.chain(visible_texts, key_texts))
