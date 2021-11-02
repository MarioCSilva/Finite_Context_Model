import matplotlib.pyplot as plt
from collections import defaultdict
from fcm import FCM
from copy import deepcopy

class Data_Plotter:
    def __init__(self):
        self.k_values = [1, 2, 3, 4, 5, 6]
        self.a_values = [0.0001, 0.001, 0.01, 0.1, 1, 2]

        self.results = defaultdict(lambda: defaultdict(float))
        
        # self.results = {
        #     1:{0.0001:3.319, 0.001:3.319, 0.01:3.319, 0.1:3.319, 1:3.324, 2:3.324}, \
        #     2:{0.0001:2.548, 0.001:2.548, 0.01:2.549, 0.1:2.559, 1:2.619, 2:2.669}, \
        #     3:{0.0001:1.997, 0.001:1.999, 0.01:2.009, 0.1:2.074, 1:2.376, 2:2.571}, \
        #     4:{0.0001:1.663, 0.001:1.670, 0.01:1.717, 0.1:1.941, 1:2.652, 2:3.002}, \
        #     5:{0.0001:1.444, 0.001:1.465, 0.01:1.598, 0.1:2.093, 1:3.173, 2:3.591}, \
        #     6:{0.0001:1.263, 0.001:1.309, 0.01:1.584, 0.1:2.408, 1:3.720, 2:4.136}
        # }
        
        self.calc_entropies()

        self.plot_results()


    def get_entropy(self, fcm_for_k, k, a):
        fcm = FCM(k, a)

        fcm.prob_table = deepcopy(fcm_for_k.prob_table)
        fcm.total_occurrences = fcm_for_k.total_occurrences
        fcm.alphabet = deepcopy(fcm_for_k.alphabet)
        fcm.alphabet_size = fcm_for_k.alphabet_size
        fcm.is_hash_table = fcm_for_k.is_hash_table

        fcm.calc_probabilities()

        fcm.calc_entropy()

        return fcm.entropy


    def calc_entropies(self):
        for k in self.k_values:
            fcm_for_k = FCM(k, 1)
            fcm_for_k.read_file()
            fcm_for_k.setup_table()
            fcm_for_k.set_occurrences()

            for a in self.a_values:
                result = self.get_entropy(fcm_for_k, k, a)

                self.results[k][a] = result

                print(f"k = {k:<5} a = {a:<10} entropy = {result}")


    def plot_results(self):
        plt.rcParams['figure.constrained_layout.use'] = True
        fig, ax = plt.subplots(len(self.a_values)//2, 2,figsize=(len(self.a_values)+10,10))

        num_plots = 0
        for a in self.a_values:
            x_pos = num_plots % (len(self.a_values) // 2) 
            y_pos = 1 if num_plots % 2 == 0 else 0
            num_plots += 1

            k_entropy_results = []
            for k in self.k_values:
                ax[x_pos, y_pos].annotate(f"{self.results[k][a]:0.3f}", xy=(k, self.results[k][a]+self.results[k][a]*0.03), fontsize=8)
                k_entropy_results.append(self.results[k][a])
            
            ax[x_pos, y_pos].plot(self.k_values, k_entropy_results,\
                color='blue', linestyle='dashed', linewidth=1,\
                marker='o', markerfacecolor='red', markersize=5)
            min_y = min(k_entropy_results)
            max_y = max(k_entropy_results)
            ax[x_pos, y_pos].set_ylim(min_y - min_y*0.05, max_y + max_y*0.05)
            ax[x_pos, y_pos].set_xlabel('k')
            ax[x_pos, y_pos].set_ylabel('Entropy')
            ax[x_pos, y_pos].set_title(f"Entropy with alpha = {a}")
        plt.show()

        fig, ax = plt.subplots(len(self.a_values)//2, 2,figsize=(len(self.a_values)+10,10))

        num_plots = 0
        for k in self.k_values:
            x_pos = num_plots % (len(self.a_values) // 2) 
            y_pos = 1 if num_plots % 2 == 0 else 0
            num_plots += 1

            a_entropy_results = []
            for a in self.a_values:
                ax[x_pos, y_pos].annotate(f"{self.results[k][a]:0.3f}", xy=(a, self.results[k][a]+self.results[k][a]*0.03), fontsize=8)
                a_entropy_results.append(self.results[k][a])

            ax[x_pos, y_pos].plot(self.a_values, a_entropy_results,\
                color='green', linestyle='dashed', linewidth=1,\
                marker='o', markerfacecolor='red', markersize=5)
            min_y = min(a_entropy_results)
            max_y = max(a_entropy_results)
            ax[x_pos, y_pos].set_ylim(min_y - min_y*0.05, max_y + max_y*0.05)
            ax[x_pos, y_pos].set_xlabel('alpha')
            ax[x_pos, y_pos].set_ylabel('Entropy')
            ax[x_pos, y_pos].set_title(f"Entropy with k = {k}")
        plt.show()

if __name__ == "__main__":
    Data_Plotter()