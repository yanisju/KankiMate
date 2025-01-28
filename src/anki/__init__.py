from aqt import mw
from aqt.utils import showInfo

class AnkiManager:
    def __init__(self):
        self.field_names = ["Sentence", "Translation", "Vocabulary1", "Vocabulary1_translation", "Vocabulary2", "Vocabulary2_translation"]

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
            note.fields[1] = sentence.translation  
            note.fields[2] = sentence.word1_data.word 
            note.fields[3] = sentence.word1_data.meaning  
            if sentence.word2_data:
                note.fields[4] = sentence.word2_data.word  
                note.fields[5] = sentence.word2_data.meaning

            col.addNote(note)

        col.save()

        showInfo("Toutes les notes ont été ajoutées avec succès.")