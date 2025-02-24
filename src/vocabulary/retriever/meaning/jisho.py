import urllib.request
import urllib.parse
import json
import re

from . import MeaningRetriever 

from ...meaning import VocabularyMeaning

from ....constants import VocabularyJLPTLevel, VocabularyPitchAccent

class JishoMeaningRetriever(MeaningRetriever):
    """Implementation of MeaningRetriever using Jisho API."""

    API_URL = "https://jisho.org/api/v1/search/words?keyword="

    def retrieve(self, word: str) -> VocabularyMeaning:
        """Retrieve word information including meanings and part of speech."""
        raw_data = self._fetch_from_api(word)
        data = self._format_data(word, raw_data)

        return VocabularyMeaning(
            word,
            data["kana_reading"],
            data["meanings"],
            data["parts_of_speech"],
            data["is_common"],
            data["jlpt_level"],
            VocabularyPitchAccent.UNKNOWN,
            [False] * len(word)
        )

    def _fetch_from_api(self, word: str) -> list:
        """Fetch JSON data from Jisho API and check response validity."""
        http_request = self.API_URL + urllib.parse.quote(word)
        with urllib.request.urlopen(http_request) as response:
            if response.status != 200:
                raise ValueError(f"Error fetching data: HTTP {response.status}")
            
            json_meaning = json.loads(response.read().decode("utf-8"))
            if "data" not in json_meaning or not isinstance(json_meaning["data"], list):
                raise ValueError("Invalid response format: Missing 'data' key or incorrect type.")

        return json_meaning.get("data", [])
    
    def _get_jlpt_level(self, word_entry) -> VocabularyJLPTLevel:
        """Get VocabularyJLPTLevel Enum depending on the word entry. """
        jlpt_level_str = word_entry.get("jlpt", ["Unknown"])[0]
        if jlpt_level_str == "jlpt-n1":
            return VocabularyJLPTLevel.JLPT_N1
        elif jlpt_level_str == "jlpt-n2":
            return VocabularyJLPTLevel.JLPT_N2
        elif jlpt_level_str == "jlpt-n3":
            return VocabularyJLPTLevel.JLPT_N3
        elif jlpt_level_str == "jlpt-n4":
            return VocabularyJLPTLevel.JLPT_N4
        elif jlpt_level_str == "jlpt-n5":
            return VocabularyJLPTLevel.JLPT_N5
        else:
            return VocabularyJLPTLevel.UNKNOWN


    def _format_data(self, word: str, data: list) -> dict:
        """Format raw JSON data into structured information."""
        if not data:
            return {
                "kana_reading": "No reading found",
                "meanings": ["No meanings found"],
                "parts_of_speech": ["Unknown"],
                "is_common": False,
                "jlpt_level": "Unknown"
            }

        word_entry = self._find_matching_entry(word, data)

        kana_reading = word_entry[0]["reading"]

        meanings = []
        parts_of_speech = []
        for sense in word_entry.get("senses", []):
            meanings.append(", ".join(sense.get("english_definitions", [])))
            parts_of_speech.append(", ".join(sense.get("parts_of_speech", [])))


        return {
            "kana_reading": kana_reading,
            "meanings": meanings,
            "parts_of_speech": parts_of_speech,
            "is_common": word_entry.get("is_common", False),
            "jlpt_level": self._get_jlpt_level(word_entry)
        }

    def _find_matching_entry(self, word: str, data: list) -> dict:
        """Find the most relevant entry in the JSON data."""
        for entry in data:
            slug_kanji = self._extract_kanjis(entry["slug"])
            if slug_kanji == word or entry["slug"] == word:
                return entry
        return data[0]  # Default to the first entry if no exact match is found

    def _extract_kanjis(self, word: str) -> str:
        """Extract kanji characters from a word."""
        return ''.join(re.findall(r'[\u4e00-\u9faf]', word))