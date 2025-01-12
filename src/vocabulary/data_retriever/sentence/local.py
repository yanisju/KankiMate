from os import path
from csv import reader

from . import SentenceRetriever

class SentenceLocalRetriever(SentenceRetriever):
    def __init__(self) -> None:
        pass

    def get_sentences(self, word):
        addon_base_dir = path.realpath(__file__)
        for i in range(5):
            addon_base_dir = path.dirname(addon_base_dir)

        sentences_file_path = path.join(addon_base_dir, "data", "sentences_data")
        
        filename_path = path.join(sentences_file_path, "eng_to_jpn")
        transcriptions_filename_path = path.join(sentences_file_path, "transcriptions")

        data = read_csv(filename_path)
        transcriptions = read_transcriptions(transcriptions_filename_path)

        return find_phrases_containing_word(data, transcriptions, word)


def read_csv(filename):
    data = []
    with open(filename + '.tsv', newline='', encoding='utf-8') as file:
        csv_reader = reader(file, delimiter='\t')
        for row in csv_reader:
            if len(row) >= 4:
                data.append({
                    "ID": row[0],
                    "Sentence": row[1],
                    "Translation": row[3]
                })
    return data

def read_transcriptions(filename):
    transcriptions = []
    with open(filename + '.csv', newline='', encoding='utf-8') as file:
        csv_reader = reader(file, delimiter='\t')
        for row in csv_reader:
            if len(row) >= 5:
                transcriptions.append({
                    "ID": row[0],
                    "Transcription": row[4]
                })
    return transcriptions

def find_phrases_containing_word(data, transcriptions, search_word):
    filtered_data = [row for row in data if search_word in row["Sentence"]]
    unique_rows = {row["Sentence"]: row for row in filtered_data}.values()

    transcription_map = {row["ID"]: row["Transcription"] for row in transcriptions}

    results_with_transcriptions = [
        [
            row["Sentence"],
            row["Translation"],
            transcription_map.get(row["ID"], None)
        ]
        for row in unique_rows
    ]
    return results_with_transcriptions
