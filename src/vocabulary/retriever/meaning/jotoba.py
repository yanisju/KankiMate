import urllib.request
import urllib.parse
import json
from os import path

from . import MeaningRetriever
from ...meaning import VocabularyMeaning
from ....constants import VocabularyJLPTLevel, VocabularyPitchAccent


class JotobaMeaningRetriever(MeaningRetriever):
    """Implementation of MeaningRetriever using Jotoba API."""

    API_URL = "https://jotoba.de/api/search/words"

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
            data["pitch_accent"],
            data["pitch_pattern"],
            data["has_audio"]
        )

    def _fetch_from_api(self, word: str) -> dict:
        """Fetch JSON data from Jotoba API and check response validity."""
        request_data = {
            "query": word,
            "language": "English",
            "no_english": False
        }
        headers = {"Content-Type": "application/json"}
        request_body = json.dumps(request_data).encode("utf-8")

        req = urllib.request.Request(self.API_URL, data=request_body, headers=headers)
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                raise ValueError(f"Error fetching data: HTTP {response.status}")
            
            return json.loads(response.read().decode("utf-8"))

    def _format_data(self, word: str, data: dict) -> dict:
        """Format raw JSON data into structured information."""
        if "words" not in data or not data["words"]:
            return {
                "meanings": ["No meanings found"],
                "kana_reading": "No reading found",
                "parts_of_speech": ["Unknown"],
                "is_common": False,
                "jlpt_level": "Unknown",
                "pitch_accent": VocabularyPitchAccent.UNKNOWN,
                "pitch_pattern": []
            }
        kanji_entry = data["kanji"][0]
        word_entry = data["words"][0]
        kana_reading = word_entry["reading"]["kana"]
        meanings = [", ".join(sense["glosses"]) for sense in word_entry.get("senses", [])]
        parts_of_speech = [", ".join(pos.keys()) for sense in word_entry.get("senses", []) for pos in sense.get("pos", [])]

        pitch_accent, pitch_pattern = self._get_pitch_accent_and_pattern(word_entry)

        has_audio = self._get_audio(word_entry, word)

        return {
            "kana_reading": kana_reading,
            "meanings": meanings,
            "parts_of_speech": parts_of_speech,
            "is_common": word_entry.get("common", False),
            "jlpt_level": self._get_jlpt_level(kanji_entry),
            "pitch_accent": pitch_accent,
            "pitch_pattern": pitch_pattern,
            "has_audio": has_audio
        }

    def _get_jlpt_level(self, word_entry: dict) -> VocabularyJLPTLevel:
        """Get VocabularyJLPTLevel Enum depending on the word entry."""
        jlpt_level = word_entry.get("jlpt", 5)
        if jlpt_level == 1:
            return VocabularyJLPTLevel.JLPT_N1
        elif jlpt_level == 2:
            return VocabularyJLPTLevel.JLPT_N2
        elif jlpt_level == 3:
            return VocabularyJLPTLevel.JLPT_N3
        elif jlpt_level == 4:
            return VocabularyJLPTLevel.JLPT_N4
        elif jlpt_level == 5:
            return VocabularyJLPTLevel.JLPT_N5
        else:
            return VocabularyJLPTLevel.UNKNOWN

    def _get_pitch_accent_and_pattern(self, word_entry: dict):
        """Extract pitch accent and pitch pattern from the API response."""
        pitch_accent = VocabularyPitchAccent.UNKNOWN
        pitch_pattern = [False] * len(word_entry["reading"]["kana"])

        if "pitch" in word_entry:
            pitch_data = word_entry["pitch"]
            if pitch_data:
                pitch_pattern = []
                for part in pitch_data:
                    pitch_pattern.extend([part["high"]] * len(part["part"]))

            if pitch_pattern[0]:
                pitch_accent = VocabularyPitchAccent.ATAMADAKA
            else:
                if not pitch_pattern[-1]:
                    pitch_accent = VocabularyPitchAccent.NAKADAKA
                else:
                    if True: # TODO: Can't differentitate Odaka and Heiban for now
                        pitch_accent = VocabularyPitchAccent.ODAKA
                    else:
                        pitch_accent = VocabularyPitchAccent.HEIBAN
        

        return pitch_accent, pitch_pattern        

    def _get_audio(self, word_entry: dict, word: str) -> bool:
        audio_path = word_entry.get("audio")
        if audio_path:
            audio_url =  f"https://jotoba.de{audio_path}"
        
            file_name = word + "_audio.mp4"

            addon_base_dir = path.realpath(__file__)
            for i in range(5):
                addon_base_dir = path.dirname(addon_base_dir)

            file_path = path.join(addon_base_dir, "data", "temp", "audio", file_name)
            
            try:
                urllib.request.urlretrieve(audio_url, file_path)
                return True
            except Exception as e:
                pass
        return False

        