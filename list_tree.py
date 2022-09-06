class LogLister:
    """ """

    def __init__(self, path):
        self.path = path

    def generate_data(self):
        log_file = open(self.path, "r")
        line_list = log_file.readlines()

        self.genesis = Node("File", 0)
        self.genesis.get_children(line_list)

        self.data_list = self.genesis.compile_tree()[0]

        return self._data_to_tuple(self.data_list)

    def find_node_toggle_collapse(self, index):
        self.genesis.find_node(index)
        new_data = self.genesis.compile_tree()[0]
        return self._data_to_tuple(new_data)

    def print_data(self, data):
        for line in data:
            print(line[0])

    def _data_to_tuple(self, data):
        tuple_list = []
        for index, item in enumerate(data):
            tuple_list.append((item, index))
        return tuple_list


class Node:
    def __init__(self, value, line, children=[], opened=True, output=None):
        self.value = value
        self.line = line
        self.children = children[:]
        self.opened = opened
        self.output = output
        self.print_range = []

    def get_children(self, line_list, line_no=0):

        while True:

            if line_list[line_no].startswith("->"):
                child = Node(line_list[line_no][2:].strip(), line_no + 1)
                line_no += 1

                if line_list[line_no].startswith("->"):
                    # Reset to beginning of while if end of node
                    self.children.append(child)
                    continue

                if not line_list[line_no].startswith("--"):
                    # If not a control - must be output
                    child.set_output(line_list[line_no].strip())
                    line_no += 1
                    self.children.append(child)
                    if line_list[line_no].startswith("--Return--"):
                        # Check if output is list in children
                        line_no += 1
                        break

                else:
                    if line_list[line_no].startswith("--Call--"):
                        line_no += 1
                        line_no = child.get_children(
                            line_list, line_no=line_no)
                        self.children.append(child)

                    elif line_list[line_no].startswith("--Return--"):
                        line_no += 1
                        self.children.append(child)
                        break

                    else:
                        print("ERROR")
                        pass

        return line_no

    def compile_tree(self, print_no=0, prefix=""):
        # If the node is not opened then dont give any children
        print_list = []
        self.print_range = [print_no]
        if self.opened:
            print_list.append(f"{print_no} {prefix}▼ {self.value}")
            print_no += 1
            prefix += "  "
            if self.output:
                print_list.append(f"{print_no} {prefix}  {self.output}")
                print_no += 1
            if self.opened:
                for child in self.children:
                    return_list, print_no = child.compile_tree(
                        print_no, prefix)
                    print_list += return_list
        else:
            print_list.append(f"{print_no} {prefix}▶ {self.value}")
            print_no += 1
        self.print_range.append(print_no)
        return print_list, print_no

    def find_node(self, index):
        if self.print_range[0] == index:
            self.toggle_opened()
            return
        else:
            for child in self.children:
                child.find_node(index)

    def get_value(self):
        return self.value

    def set_print_range(self, print_range):
        self.print_range = print_range

    def set_output(self, output):
        self.output = output

    def set_value(self, value):
        self.value = value

    def toggle_opened(self):
        if self.opened:
            self.opened = False
        else:
            self.opened = True
