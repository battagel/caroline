from list_tree import LogLister

if __name__ == "__main__":
    test = LogLister("output.txt")
    data = test.generate_data()
    print(data)
