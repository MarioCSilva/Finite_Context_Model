import argparse
from fcm import FCM
from generator import Generator
import sys
FILENAME = "./../example/example.txt"

class Main:
    def __init__(self) -> None:
        self.fcm = FCM(*self.check_arguments())

        self.fcm.run()

        if self.text_size:
            self.generator = Generator(self.text_size, self.fcm)
            self.generator.generate()

        self.get_results()


    def get_results(self) -> None:
        if self.text_size:
            print(self.generator.generated_text)
            print(f"\nEntropy of generated text: {self.generator.get_entropy()}, text size: {self.text_size}")
        print(f"FCM with k={self.fcm.k}, alpha: {self.fcm.alpha}, text size: {self.fcm.total_occurrences}")
        print(f"Entropy of data set: {self.fcm.entropy}")


    def usage(self):
        print("Usage: python3 main.py \n\t-f <file name for data set:str> \n\t-k <context size:int>" +\
            "\n\t-a <alpha:int> \n\t-g <generate text> \n\t-t <number of characters to generate:int>\n")


    def check_arguments(self):
        arg_parser = argparse.ArgumentParser(
            prog="Finite Context Model",
            usage=self.usage
        )

        arg_parser.add_argument('-f', nargs=1, default=[FILENAME])
        arg_parser.add_argument('-k', nargs=1, type=int, default=[3])
        arg_parser.add_argument('-a', nargs=1, type=float, default=[0.1])
        arg_parser.add_argument('-g', action="store_true", default=False)
        arg_parser.add_argument('-t', nargs=1, type=int, default=[10000])
        args = None
        try:
            args = arg_parser.parse_args()
        except:
            self.usage()
            sys.exit(0)
        file_name = args.f[0]
        k = args.k[0]
        alpha = args.a[0]
        self.text_size = args.t[0] if args.g else None

        return k, alpha, file_name


if __name__ =="__main__":
    main = Main()
