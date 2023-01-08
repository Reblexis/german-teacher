import random
import eel

from dictionary import DictionaryController, Noun
from Statistics import statistics


class PracticeController:
    NUM_POSSIBLE_ANSWERS = 4  # How many possible answers should be displayed to the user

    def __init__(self):
        print("Initializing practice controller...")
        self.types = ["article", "meaning", "english_names"]
        self.correct_answer = None
        self.dictionary_controller = DictionaryController()
        self.statistics_controller = statistics.get_controller()
        self.question_type = None
        self.questioned_noun = None
        print("Practice controller initialized.")

    def create_question(self):
        if len(self.types) == 0:
            self.question_type = None
            return "no_categories"

        self.question_type = random.choice(self.types)
        random_nouns = self.dictionary_controller.get_random_nouns(self.question_type, self.NUM_POSSIBLE_ANSWERS)
        correct_option = random.randint(0, self.NUM_POSSIBLE_ANSWERS - 1)
        self.questioned_noun: Noun = random_nouns[correct_option]
        self.correct_answer = self.questioned_noun.to_dict()[self.question_type]
        self.correct_option = correct_option
        possible_answers = [noun.to_dict()[self.question_type] for noun in random_nouns]

        for i in range(len(possible_answers)):
            if isinstance(possible_answers[i], list):
                possible_answers[i] = ", ".join(possible_answers[i])

        question = {"type": self.question_type, "questioned_content": self.questioned_noun.name,
                    "possible_answers": possible_answers}
        return question

    def receive_answer(self, new_answer_data: dict):
        answer_data = {"answer_text": None, "answer_option": None}
        answer_data.update(new_answer_data)
        received_answer = answer_data["answer_text"] if answer_data["answer_option"] is None \
            else answer_data["answer_option"]
        is_correct = (received_answer == self.correct_answer or received_answer == self.correct_option)

        self.statistics_controller.add_guess(self.question_type, self.questioned_noun.name, received_answer,
                                             self.correct_answer, is_correct)
        return is_correct

    def push_new_question(self):
        eel.set_new_question(self.create_question())

    def set_category(self, category: str, state: bool):
        if category in self.types:
            self.types.remove(category)
        if state:
            self.types.append(category)
        if (category == self.question_type and not state) or self.question_type is None:
            self.push_new_question()


practice_controller = PracticeController()


@eel.expose
def create_question():
    return practice_controller.create_question()


@eel.expose
def answer(answer_content: dict):
    return practice_controller.receive_answer(answer_content)


@eel.expose
def set_category(category: str, state: bool):
    practice_controller.set_category(category, state)
