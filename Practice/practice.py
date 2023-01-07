import random
import eel

from dictionary import DictionaryController, Noun


class PracticeController:
    def __init__(self):
        self.types = ["article", "meaning", "english_names"]
        self.correct_answer = None
        self.dictionary_controller = DictionaryController()

    def create_question(self):
        question_type = random.choice(self.types)
        random_noun: Noun = self.dictionary_controller.get_random_noun(question_type)
        question = {"type": question_type, "word_data": random_noun.to_dict()}
        self.correct_answer = random_noun.to_dict()[question_type]
        return question

    def receive_answer(self, answer: dict):
        # TODO: manage statistics
        return answer["content"] == self.correct_answer


practice_controller = PracticeController()


@eel.expose
def create_question():
    return practice_controller.create_question()


@eel.expose
def receive_answer(answer: dict):
    return practice_controller.receive_answer(answer)
