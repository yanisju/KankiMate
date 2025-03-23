from aqt import mw
from aqt.utils import showInfo, showCritical
import os
import shutil

from anki import errors

class AnkiManager:
    field_names = ["SentKanji", 
                   "SentFurigana", 
                   "SentEng", 
                   "VocabKanji", 
                   "VocabFurigana", 
                   "VocabPitchPattern", 
                   "VocabPitchNum", 
                   "VocabDef", 
                   "VocabAudio", 
                   "Vocab2Kanji", 
                   "Vocab2Furigana", 
                   "Vocab2Def", 
                   "Image", 
                   "Notes", 
                   "MakeProductionCard"]

    @staticmethod
    def is_model_existing(model_name):
        models = mw.col.models
        existing_model = models.by_name(model_name)
        if existing_model:
            return existing_model
        else:
            return False
        
    @classmethod
    def is_model_existing_valid(cls, model):
        model_field_names = model.field_names
        if model_field_names == cls.field_names:
            return True
        else:
            return False
    
    @staticmethod
    def modify_model_parameters(model_name: str, model_front: str, model_back: str, model_style: str) -> bool:
        models = mw.col.models
        existing_model = mw.col.models.by_name(model_name)
        existing_model["css"] = model_style

        for template in existing_model["tmpls"]:
            template["qfmt"] = model_front
            template["afmt"] = model_back

        try:
            models.save(existing_model)
        except(errors.CardTypeError) as err:
            showCritical(err._message)
            return False
        
        return True


    @classmethod
    def create_new_model(cls, model_name: str, model_front: str, model_back: str, model_style: str) -> bool:
        models = mw.col.models
        new_model = mw.col.models.new(model_name)
        new_model["css"] = model_style

        for field in cls.field_names:
            models.addField(new_model, models.new_field(field))

        template = models.new_template("Normal")
        template["qfmt"] = model_front
        template["afmt"] = model_back

        models.addTemplate(new_model, template)
        models.add(new_model)

        return True

    @classmethod
    def add_to_deck(cls, sentence_manager):
        col = mw.col

        config = mw.addonManager.getConfig(__name__)

        model_name = config["model_name"]

        model = col.models.by_name(model_name)
        if not model:
            showInfo(f"Model {model_name} doesn't exist.")
            return

        deck_name = config["deck_name"]
        deck = col.decks.by_name(deck_name)
        if not deck:
            showInfo(f"Deck {deck_name} doesn't exist.")
            return

        col.models.set_current(model)


        for sentence in sentence_manager:
            note = col.newNote()

            note.model()['id'] = model['id']  
            note.model()['did'] = deck['id']  

            note.fields[0] = sentence.get_sentence_bold()  
            note.fields[1] = sentence.get_sentence_furigana_bold()  
            note.fields[2] = sentence.translation  
            note.fields[3] = cls.move_audio_file_to_collection(sentence.sentence, sentence.has_audio)
            note.fields[4] = sentence.word1_data.word 
            note.fields[5] = f"{sentence.word1_data.word}[{sentence.word1_data.reading}]"
            note.fields[6] = "" # Pitch pattern
            note.fields[7] = str(sentence.vocabulary.meaning.pitch_accent.value) # Pitch accent
            note.fields[8] = str(sentence.word1_data.meaning) # VocabDef
            note.fields[9] = cls.move_audio_file_to_collection(sentence.word1_data.word, sentence.vocabulary.meaning.has_audio) # VocabAudio

            if sentence.word2_data:
                note.fields[10] = sentence.word2_data.word  
                note.fields[11] = f"{sentence.word2_data.word}[{sentence.word2_data.reading}]"
                note.fields[12] = sentence.word2_data.meaning

            col.addNote(note)

        col.save()

        showInfo("All notes have been added with success.")

    @staticmethod
    def move_audio_file_to_collection(name, has_audio) -> str:
        if not has_audio:
            return ""

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Remonte 2 niveaux
        audio_file_name = f"{name}_audio.mp4"
        audio_file_path = os.path.join(base_dir, "data", "temp", "audio", audio_file_name)


        if not os.path.exists(audio_file_path):
            showInfo(f"Error : audio file related to vocabulary doesn't exist -> {audio_file_path}")
            return ""
        
        media_folder = mw.col.media.dir()
        destination_path = os.path.join(media_folder, audio_file_name)

        try:
            # Déplacer le fichier
            shutil.move(audio_file_path, destination_path)
            return f"[sound:{audio_file_name}]"
        except Exception as e:
            showInfo(f"Error when moving audio file : {e}")
            return ""