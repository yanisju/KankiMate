import threading
import requests
import time
import random
from math import ceil

from . import SentenceRetriever

from .. import check_word_contains_kana

class SentenceHTTPRetriever(SentenceRetriever):
    def __init__(self, lang_from, lang_to):
        self.lang_from = lang_from
        self.lang_to = lang_to

    def get_sentences(self, word):
        return get_sentences_http(word, self.lang_from, self.lang_to)

def create_sentences_html_request(word, lang_from, lang_to, page=1):
    """ Create HTML request: fetch through Tatoeba website."""

    http_request = "https://tatoeba.org/en/api_v0/search?from=" + \
        lang_from + "&to=" + lang_to + "&query=" + word + "&page=" + str(page)
    params = "&orphans=no&sort=relevance&trans_filter=limit&trans_orphan=no&trans_unapproved=no&unapproved=no&word_count_min=1"
    print(http_request + params)  # TODO: Remove one day
    return http_request + params


def retrieve_sentences_json(word, lang_from, lang_to, page=1):
    url = create_sentences_html_request(word, lang_from, lang_to, page)
    response = requests.get(url)
    if response.status_code == 429:
        time.sleep(random.uniform(0, 2))
        return retrieve_sentences_json(word, lang_from, lang_to, page)
    elif response.status_code != 204:
        return response.json()


def deserialize_json_sentence(json_sentences, word):
    sentences_data = []
    one_sentence_data = []

    sentences_count = len(json_sentences['results'])

    for i in range(sentences_count):
        this_lang_from_sentence = json_sentences['results'][i]["text"]
        if check_word_contains_kana(
                word) or word in this_lang_from_sentence:  # Add sentence if word does appear in sentence
            one_sentence_data.append(this_lang_from_sentence)

            j = 0
            while (json_sentences['results'][i]["translations"][j] == [
            ]):  # Sometimes the first translation is empty
                j += 1

            k = 0
            while (json_sentences['results'][i]
                   ["translations"][j][k] == []):  # Same
                k += 1
            one_sentence_data.append(
                json_sentences['results'][i]["translations"][j][k]["text"])  # Translation

            one_sentence_data.append(
                json_sentences['results'][i]["transcriptions"][0]["text"])  # Transcription
        sentences_data.append(list(one_sentence_data))
        one_sentence_data.clear()
    return sentences_data


def get_sentences_data(json_data, word, data: list):
    page_sentences_data = deserialize_json_sentence(json_data, word)
    data += page_sentences_data


def retrieve_and_get_sentences_data(args):
    word, lang_from, lang_to, i, data = args
    json_data = retrieve_sentences_json(word, lang_from, lang_to, i)
    get_sentences_data(json_data, word, data)


def get_paging_data(json_data):
    sentences_data = json_data["paging"]["Sentences"]
    current_page = int(sentences_data["page"])  # Current page
    # Number of items displayed in the current page
    current_page_items_number = int(sentences_data["current"])
    count = int(sentences_data["count"])  # Total number of results
    perPage = int(sentences_data["perPage"])  # Number of results per page
    return (current_page, current_page_items_number, count, perPage)


def get_sentences_http(word, lang_from, lang_to):
    start = time.time()

    json_data = retrieve_sentences_json(word, lang_from, lang_to)
    (current_page, current_page_items_number,
     count, perPage) = get_paging_data(json_data)
    total_page_number = ceil(count / perPage)

    data = []
    get_sentences_data(json_data, word, data)

    threads = []

    for i in range(2, total_page_number):
        t = threading.Thread(
            target=retrieve_and_get_sentences_data, args=(
                (word, lang_from, lang_to, i, data),))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    end = time.time()
    print("Time elapsed: ", end - start)

    return data
