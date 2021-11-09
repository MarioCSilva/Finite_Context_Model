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
          #   1:{0.0001:3.3187162107763704, 0.001:3.3187245621479615, 0.01:3.318795663670953, 0.1:3.319386180714881, 1:3.3241526890842827, 2:3.328847440105709}, \
          #   2:{0.0001:2.547609907491271, 0.001:2.547839813044308, 0.01:2.5498026924739454, 0.1:2.566278031100472, 1:2.7009360975871726, 2:2.830442696512285}, \
          #   3:{0.0001:1.997769638996046, 0.001:2.0053342901888933, 0.01:2.0764399903171022, 0.1:2.6487982855067544, 1:4.55481920691499, 2:5.054943141977196}, \
          #   4:{0.0001:1.7050735634194736, 0.001:2.0568855677456015, 0.01:3.778528350290523, 0.1:5.413973903828152, 1:5.721792087475998, 2:5.739294587210711}, \
          #   5:{0.0001:3.008058662157925, 0.001:5.112995354653897, 0.01:5.68193488811552, 0.1:5.747956884582386, 1:5.7543158975980875, 2:5.754628676702176}, \
          #   6:{0.0001:5.613416371178265, 0.001:5.740412628607464, 0.01:5.753480429045851, 0.1:5.754762052929056, 1:5.754878099470984, 2:5.754883394196358}
        # }

        self.calc_entropies()

        self.plot_results()


    def get_entropy(self, fcm_for_k, occur_table, a):
        fcm_for_k.prob_table = deepcopy(occur_table)
        fcm_for_k.entropy = 0
        fcm_for_k.alpha = a

        fcm_for_k.calc_probabilities()
        fcm_for_k.calc_entropy()

        return fcm_for_k.entropy


    def calc_entropies(self):
        for k in self.k_values:
            fcm_for_k = FCM(k, 1)
            fcm_for_k.read_file()
            fcm_for_k.setup_table()
            fcm_for_k.set_occurrences()
            occur_table = deepcopy(fcm_for_k.prob_table)

            for a in self.a_values:
                result = self.get_entropy(fcm_for_k, occur_table, a)

                self.results[k][a] = result

                print(f"k = {k:<5} a = {a:<10} entropy = {result}")


    def plot_results(self):
        color_arr = ['b', 'g', 'c', 'm', 'y', 'brown'] 
        plt.rcParams['figure.constrained_layout.use'] = True
        plt.rcParams.update({'font.size': 16})

        fig, ax = plt.subplots(len(self.a_values)//2, 2,figsize=(len(self.a_values)+10,10))
        fig2, ax2 = plt.subplots(figsize=(8,8))

        num_plots = 0
        for a in self.a_values:
            x_pos = num_plots % (len(self.a_values) // 2)
            y_pos = 1 if num_plots % 2 == 0 else 0

            k_entropy_results = []
            for k in self.k_values:
                ax2.annotate(f"{self.results[k][a]:0.3f}", xy=(k, self.results[k][a]+self.results[k][a]*0.01), fontsize=13)
                ax[x_pos, y_pos].annotate(f"{self.results[k][a]:0.3f}", xy=(k, self.results[k][a]+self.results[k][a]*0.01), fontsize=8)
                k_entropy_results.append(self.results[k][a])
            
            ax[x_pos, y_pos].plot(self.k_values, k_entropy_results,\
                color='blue', linestyle='dashed', linewidth=1,\
                marker='o', markerfacecolor='red', markersize=5)
            min_y = min(k_entropy_results)
            max_y = max(k_entropy_results)
            ax2.plot(self.k_values, k_entropy_results,\
                color=color_arr[num_plots], linestyle='solid', linewidth=1,\
                marker='o', markerfacecolor='red', markersize=5, label=f"alpha={a}")
            ax[x_pos, y_pos].set_ylim(min_y - min_y*0.05, max_y + max_y*0.05)
            ax[x_pos, y_pos].set_xlabel('k')
            ax[x_pos, y_pos].set_ylabel('Entropy')
            ax[x_pos, y_pos].set_title(f"Entropy with alpha = {a}")
            num_plots += 1
        lst_entropies = [self.results[x][y] for x in self.results for y in self.results[x]]
        min_entropy = min(lst_entropies)
        max_entropy = max(lst_entropies)
        ax2.set_ylim(min_entropy - min_entropy*0.1, max_entropy + max_entropy*0.1)
        ax2.set_xlabel('k')
        ax2.set_ylabel('Entropy')
        ax2.set_title(f"Entropy for different values for k and alpha")
        plt.legend(loc='best')
        plt.show()

        fig, ax = plt.subplots(len(self.a_values)//2, 2,figsize=(len(self.a_values)+10,10))
        fig2, ax2 = plt.subplots(figsize=(8, 8))

        num_plots = 0
        for k in self.k_values:
            x_pos = num_plots % (len(self.a_values) // 2) 
            y_pos = 1 if num_plots % 2 == 0 else 0

            a_entropy_results = []
            for a in self.a_values:
                ax2.annotate(f"{self.results[k][a]:0.3f}", xy=(a, self.results[k][a]+self.results[k][a]*0.01), fontsize=13)
                ax[x_pos, y_pos].annotate(f"{self.results[k][a]:0.3f}", xy=(a, self.results[k][a]+self.results[k][a]*0.03), fontsize=8)
                a_entropy_results.append(self.results[k][a])

            ax[x_pos, y_pos].plot(self.a_values, a_entropy_results,\
                color='green', linestyle='dashed', linewidth=1,\
                marker='o', markerfacecolor='red', markersize=5)
            ax2.plot(self.a_values, a_entropy_results,\
                color=color_arr[num_plots], linestyle='solid', linewidth=1,\
                marker='o', markerfacecolor='red', markersize=5, label=f"k={k}")
            min_y = min(a_entropy_results)
            max_y = max(a_entropy_results)
            ax[x_pos, y_pos].set_ylim(min_y - min_y*0.1, max_y + max_y*0.1)
            ax[x_pos, y_pos].set_xlabel('alpha')
            ax[x_pos, y_pos].set_ylabel('Entropy')
            ax[x_pos, y_pos].set_title(f"Entropy with k = {k}")
            num_plots += 1
        ax2.set_ylim(min_entropy - min_entropy*0.05, max_entropy + max_entropy*0.05)
        ax2.set_xlabel('a')
        ax2.set_ylabel('Entropy')
        ax2.set_title(f"Entropy for different values for alpha and k")
        plt.legend(loc='best')
        plt.show()

if __name__ == "__main__":
    Data_Plotter()
