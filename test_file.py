breakpoint()


class Stuff:
    def __init__(self):
        print("Init")

    def do_stuff(self):

        print("hello")
        for n in range(0, 3):
            print(n)


if __name__ == "__main__":
    stuff = Stuff()
    stuff.do_stuff()
