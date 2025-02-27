from aqt import mw
from aqt.utils import showInfo
import os
import shutil

class AnkiManager:
    def __init__(self):
        self.field_names = ["Sentence", "SentenceFurigana", "Translation", "Audio", "Vocabulary1", "Vocabulary1_translation", "Vocabulary2", "Vocabulary2_translation"]

    def is_model_existing(self, model_name):
        models = mw.col.models
        existing_model = models.by_name(model_name)
        if existing_model:
            return existing_model
        else:
            return False
        
    def is_model_existing_valid(self, model):
        model_field_names = model.field_names
        if model_field_names == self.field_names:
            return True
        else:
            return False
        
    def modify_model_parameters(self, model_name: str, model_front: str, model_back: str, model_style: str):
        models = mw.col.models
        existing_model = mw.col.models.by_name(model_name)
        existing_model["css"] = model_style

        for template in existing_model["tmpls"]:
            template["qfmt"] = model_front
            template["afmt"] = model_back

        models.save(existing_model)


    def create_new_model(self, model_name: str, model_front: str, model_back: str, model_style: str):
        models = mw.col.models
        new_model = mw.col.models.new(model_name)
        new_model["css"] = model_style

        for field in self.field_names:
            models.addField(new_model, models.new_field(field))

        template = models.new_template("Normal")
        template["qfmt"] = model_front
        template["afmt"] = model_back

        models.addTemplate(new_model, template)
        models.add(new_model)

        return new_model

    def add_to_deck(self, sentence_manager):
        col = mw.col

        config = mw.addonManager.getConfig(__name__)

        model_name = config["model_name"]

        model = col.models.by_name(model_name)
        if not model:
            showInfo("Le modèle 'anki_test_new_model' n'existe pas.")
            return

        deck_name = config["deck_name"]
        deck = col.decks.by_name("Test_kanjis")
        if not deck:
            showInfo("Le deck 'Test_kanjis' n'existe pas.")
            return

        col.models.set_current(model)


        for sentence in sentence_manager:
            note = col.newNote()

            note.model()['id'] = model['id']  
            note.model()['did'] = deck['id']  

            note.fields[0] = sentence.sentence  
            note.fields[1] = sentence.get_sentence_furigana()  
            note.fields[2] = sentence.translation  
            note.fields[3] = self.move_audio_file_to_collection(sentence.sentence, sentence.has_audio)
            note.fields[4] = sentence.word1_data.word 
            note.fields[5] = f"{sentence.word1_data.word}[{sentence.word1_data.reading}]"
            note.fields[6] = "" # Pitch pattern
            note.fields[7] = sentence.vocabulary.meaning.pitch_accent.value # Pitch accent
            note.fields[8] = sentence.word1_data.meaning # VocabDef
            note.fields[9] = self.move_audio_file_to_collection(sentence.word1_data.word, sentence.vocabulary.meaning.has_audio) # VocabAudio

            if sentence.word2_data:
                note.fields[10] = sentence.word2_data.word  
                note.fields[11] = f"{sentence.word2_data.word}[{sentence.word2_data.reading}]"
                note.fields[12] = ""
                note.fields[13] = ""
                note.fields[14] = sentence.word2_data.meaning

            col.addNote(note)

        col.save()

        showInfo(sentence.get_sentence_furigana())

        showInfo("Toutes les notes ont été ajoutées avec succès.")

    def move_audio_file_to_collection(self, name, has_audio) -> str:
        if not has_audio:
            return ""

        # Déterminer le chemin du dossier parent deux niveaux au-dessus
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Remonte 2 niveaux
        audio_file_name = f"{name}_audio.mp4"
        audio_file_path = os.path.join(base_dir, "data", "temp", "audio", audio_file_name)

        # Vérifier si le fichier existe avant de le déplacer
        if not os.path.exists(audio_file_path):
            showInfo(f"Erreur : le fichier audio n'existe pas -> {audio_file_path}")
            return ""

        # Récupérer le dossier media d'Anki
        media_folder = mw.col.media.dir()
        destination_path = os.path.join(media_folder, audio_file_name)

        showInfo(f"Déplacement du fichier :\n{audio_file_path}\n→ {destination_path}")  # Debug

        try:
            # Déplacer le fichier
            shutil.move(audio_file_path, destination_path)
            return destination_path
        except Exception as e:
            showInfo(f"Erreur lors du déplacement : {e}")
            return ""