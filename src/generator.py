from fcm import FCM
from random import randint, choices, choice
FILENAME = "./../example/example.txt"

class Generator:
    def __init__(self, text_size=1000, fcm=None) -> None:
        self.fcm = fcm

        self.text_size = text_size

        self.generated_text = ''


    def generate(self) -> str:
        alphabet = list(self.fcm.alphabet.keys())
        initial_context = ""
        for i in range(self.fcm.k):
            initial_context += choice(alphabet)

        self.generated_text = initial_context
        context = initial_context

        for _ in range(self.text_size):
            predicted_symbol = choices(alphabet, \
                weights = self.fcm.get_context_probabilities(context=context), k=1)[0]
            
            context = context[1:] + predicted_symbol

            self.generated_text += predicted_symbol

        with open('generated_text.txt', 'w') as f:
            f.write(self.generated_text)


    def get_entropy(self):
        new_fcm = FCM(self.fcm.k, self.fcm.alpha, 'generated_text.txt')
        new_fcm.run()
        return new_fcm.entropy
