from collections import defaultdict

FILENAME = "./../example/example.txt"

class FCM:
    def __init__(self, k, alpha, filename=FILENAME) -> None:
        self.k = k
        self.alpha = alpha
        self.filename = filename
        self.symbol_dict = defaultdict(int)
        self.prob_table = []

    def read_file(self):
        file_text = open(self.filename,"r")

        # get alphet and store indexes
        ind_counter = 0
        for line in file_text:
            for char in line:
                # non-aplhabetical count
                # Lower upper case
                if not self.symbol_dict.get(char):
                    self.symbol_dict[char] = ind_counter
                    ind_counter += 1

        # store size of alphabet
        self.alphabet_size = ind_counter


        # memory formula
        if self.has_memory_limit():
            self.prob_table = [0 for _ in range(self.alphabet_size**(self.k+1))]

        context = ""

        file_text = open(self.filename,"r")
        for line in file_text:
            for char in line:
                # We should only use sequences of size k
                context += char

                if len(context) % (self.k+1) != 0:
                    continue

                # add to occurencies table one more occurency of this char sequence
                self.add_occur_to_table(context)

                # clear first char of context
                context = context[1:]


    def has_memory_limit(self) -> bool:
        # verifies situations in which Memory Usage will be higher than 8GB
        mem = (self.alphabet_size ** self.k ) * self.alphabet_size * 16 /8/1024/1024
        return mem >= 8,388,608

    def char_probability(n_occorrences) -> None:
        pass

    def add_occur_to_table(self, context):
        # pos_char_in_alphabet*len_alph**3 + pos_char_in_alphabet*len_alph**2 + pos_char_in_alphabet*len_alph**1
        for i in range(self.k, -1, -1):
            index = self.symbol_dict[context[i]] * self.alphabet_size**i
            self.prob_table[index] += 1

fcm = FCM(k=1,alpha=0)
fcm.read_file()