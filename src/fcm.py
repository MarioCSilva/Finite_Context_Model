from collections import defaultdict
import math

FILENAME = "./../example/example.txt"

class FCM:
    def __init__(self, k, alpha, filename=FILENAME) -> None:
        assert alpha > 0, "Values of alpha must be greater than zero"

        self.k = k
        self.alpha = alpha
        self.filename = filename
        self.symbol_dict = defaultdict(int)
        self.prob_table = []
        self.is_hash_table = False
        self.total_occurrences = 0


    def read_file(self):
        file_text = open(self.filename,"r")

        # get alphet and store indexes
        ind_counter = 0
        for line in file_text:
            for char in line:
                # non-aplhabetical count
                # Lower upper case
                if not self.symbol_dict[char]:
                    self.symbol_dict[char] = ind_counter
                    ind_counter += 1

        # store size of alphabet
        self.alphabet_size = ind_counter


        # memory formula
        if self.has_memory_limit():
            self.prob_table = [[0] * self.alphabet_size for _ in range(self.alphabet_size** self.k)]
        else:
            self.prob_table = defaultdict(lambda: defaultdict(int))
            self.is_hash_table = True

        context = ""

        file_text = open(self.filename,"r")
        for line in file_text:
            for char in line:
                # We should only use sequences of size k
                context += char

                if len(context) % (self.k+1) != 0:
                    continue

                # add to occurrences table one more occurency of this char sequence
                self.add_occur_to_table(context)
                self.total_occurrences += 1

                # clear first char of context
                context = context[1:]

        print(self.prob_table.keys())


    def has_memory_limit(self) -> bool:
        # verifies situations in which Memory Usage will be higher than 8GB
        mem = (self.alphabet_size ** self.k ) * self.alphabet_size * 16 /8/1024/1024
        return mem >= 8388608

    def calc_probabilities(self) -> None:
        if self.is_hash_table:
            pass
        else:
            pass 


    def add_occur_to_table(self, context):
        prefix = context[:-1]
        next_char = context[-1]
        
        if self.is_hash_table:
            self.prob_table[prefix][next_char] += 1
            print( self.prob_table)
            return

        context_index = 0
        
        for i in range(self.k, 0, -1):
            context_index += self.symbol_dict[context[self.k-i]] * self.alphabet_size**(i-1)
         
        self.prob_table[context_index][self.symbol_dict[next_char]] += 1

    def calc_entropy(self):
        #Calculates the events probabilities in the FCM, the entropies for each context/row and the final entropy of the model.
        
        self.probs = self.dic_model # new dictionary with the same keys that dic_model, at the end this data structure will save the events probabilities

        total = 0  
        total_rows = {}
        # for each context we calculate its total of occurences and we increment this to the total 
        for context in self.dic_model.keys(): 
            total_rows[context] = sum(self.dic_model[context].values()) 
            total += total_rows[context]

        for context in self.dic_model:
            context_entropy = 0 
            row_total = total_rows[context]

            # calculate the events probabilities and context entropy
            for char in self.dic_model[context]:
                p_char = (self.dic_model[context][char] + self.alpha) / (row_total + self.alpha * self.cardinality)
                self.probs[context][char] = p_char 
                context_entropy += p_char * math.log2(p_char)
            
            # deal with zeros at lines, if alpha equals 0, zeros don't matter
            if self.alpha > 0:
                dif = self.cardinality - len(self.dic_model[context].values())
                if dif != 0: # if dif differs to 0 this line have zeros
                    p_char = self.alpha / (row_total + self.alpha * self.cardinality) # calculate the probability 
                    context_entropy += dif * (p_char * math.log2(p_char)) # add the previoust value to context entropy n (dif) times

            context_probability = row_total/total  # calculate context probability 
            self.entropy += context_probability * context_entropy   # increase the final entropy

        self.entropy = -self.entropy


fcm = FCM(k=2,alpha=0.001)
fcm.read_file()