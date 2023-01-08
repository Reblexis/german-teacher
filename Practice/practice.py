import random
import eel

from dictionary import DictionaryController, Noun


class PracticeController:
    NUM_POSSIBLE_ANSWERS = 4  # How many possible answers should be displayed to the user

    def __init__(self):
        print("Initializing practice controller...")
        self.types = ["article", "meaning", "english_names"]
        self.correct_answer = None
        self.dictionary_controller = DictionaryController()
        print("Practice controller initialized.")

    def create_question(self):
        question_type = random.choice(self.types)
        random_nouns = self.dictionary_controller.get_random_nouns(question_type, self.NUM_POSSIBLE_ANSWERS)
        correct_option = random.randint(0, self.NUM_POSSIBLE_ANSWERS - 1)
        questioned_noun: Noun = random_nouns[correct_option]
        self.correct_answer = questioned_noun.to_dict()[question_type]
        self.correct_option = correct_option
        possible_answers = [noun.to_dict()[question_type] for noun in random_nouns]

        for i in range(len(possible_answers)):
            if isinstance(possible_answers[i], list):
                possible_answers[i] = ", ".join(possible_answers[i])

        question = {"type": question_type, "questioned_content": questioned_noun.name,
                    "possible_answers": possible_answers}
        return question

    def receive_answer(self, new_answer_data: dict):
        # TODO: manage statistics
        answer_data = {"answer_text": None, "answer_option": None}
        answer_data.update(new_answer_data)
        return answer_data["answer_text"] == self.correct_answer or answer_data["answer_option"] == self.correct_option


practice_controller = PracticeController()


@eel.expose
def create_question():
    return practice_controller.create_question()


@eel.expose
def answer(answer_content: dict):
    return practice_controller.receive_answer(answer_content)
