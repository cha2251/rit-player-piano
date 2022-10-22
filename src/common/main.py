from src.mixing.mixing import Mixing


class Main:
    mixing = None

    def main(self):
        print("Creating Mixing Subsystem")
        self.createMixing()
        print("Sanity Check Pass: "+str(self.mixing.is_even(2)))
        input("Press Enter")

    def createMixing(self):
        self.mixing = Mixing()


if __name__ == "__main__":
    main = Main()
    main.main()