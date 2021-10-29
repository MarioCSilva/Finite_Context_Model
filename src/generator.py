from fcm import FCM
from random import randint, choices, choice
FILENAME = "./../example/example.txt"

class Generator:
    def __init__(self, k, alpha, filename=FILENAME, text_size=10000) -> None:
        self.fcm = FCM(k=k, alpha=alpha, filename=filename)
        self.text_size = text_size
        self.fcm.read_file()

    def generate(self) -> str:
        alphabet = list(self.fcm.alphabet.keys())

        initial_context = ""
        for i in range(self.fcm.k):
            initial_context += choice(alphabet)

        generated_text = initial_context
        context = initial_context

        for _ in range(self.text_size):
            predicted_symbol = choices(alphabet, \
                weights = self.fcm.get_context_probabilities(context=context), k=1)[0]
            
            context = context[1:] + predicted_symbol

            generated_text += predicted_symbol

        return generated_text


gen = Generator(k=3, alpha=0.00000000001)
text = gen.generate()
print(text)
