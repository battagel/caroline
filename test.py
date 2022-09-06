from list_tree import LogLister

if __name__ == "__main__":
    test = LogLister("output.txt")
    data = test.generate_data()
    test.print_data(data)
    print("------------------------")
    new_data = test.find_node_toggle_collapse(1)
    test.print_data(new_data)
