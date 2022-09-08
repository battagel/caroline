class LogLister:
    """ """

    def __init__(self, path):
        self.path = path
        self.create_tree()

    def create_tree(self):
        """
        Creates a genesis Node in which the tree is stored
        Parameters:
            None
        Exception:
            None
        Returns:
            None
        """
        log_file = open(self.path, "r")
        line_list = log_file.readlines()
        self.genesis = Node("File", 0)
        self.genesis.get_children(line_list)

    def generate_data(self):
        """
        Formats the tree into strings with line numbers
        Parameters:
            None
        Exception:
            None
        Returns:
            List of tuples
        """
        data_list = self.genesis.compile_tree()[0]
        prefixed_data_list = self._fill_list(data_list)
        tuple_list = self._data_to_tuple(prefixed_data_list)
        return tuple_list

    def find_node_toggle_collapse(self, index):
        """
        Find the node with the given index and toggle collapse
        Parameters:
            Index of node to be collapsed
        Exception:
            None
        Returns:
            New list of tuples with collapsed node
        """
        self.genesis.find_node(index)
        return self.generate_data()

    def print_data(self, data):
        """
        Debug method for printing a list
        """
        for line in data:
            print(line[0])

    def _fill_list(self, printed_list):
        """
        Find the highest index in the list and adds prefixes whitespace.
        Parameters:
            printed_list: The list of printed nodes
        Exception:
            None
        Returns:
            printed_list: The list of printed nodes with the whitespace prefixed
        """
        highest_index = len(printed_list) - 1
        whitespace = " "
        for line in printed_list:
            index = printed_list.index(line)
            diff = len(str(highest_index)) - len(str(index))
            prefix = whitespace * diff
            printed_list[index] = prefix + printed_list[index]
        return printed_list

    def _data_to_tuple(self, data):
        """
        Parameters:
            data: List of formatted strings which displays the tree
        Exception:
            None
        Returns:
            tuple_list: A list of tuples with the string and index
        """
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
        """
        Find the children of a parent node by traversing the output log
        Parameters:
                line_list: A list of lines from the output log
            optional:
                line_no: The position of the cursor in the line list
        Exception:
            None
        Returns:
            line_no: The position of the cursor in the line list
        """

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
        """
        Recursively compile a list of formatted strings which are the printed tree
        Parameters:
            Optional
                print_no: the line number of the print
                prefix: used in the formatting of each string
        Exception:
            None
        Returns:
            print_list: A list of printed strings
            print_no: used in the recursion
        """
        # If the node is not opened then dont give any children
        print_list = []
        self.print_range = [print_no]
        if self.opened:
            print_list.append(
                f"{print_no} {prefix}▼ {self.value}")
            print_no += 1
            prefix += "  "
            if self.output:
                print_list.append(
                    f"{print_no} {prefix}  {self.output}")
                print_no += 1
            if self.opened:
                for child in self.children:
                    return_list, print_no = child.compile_tree(
                        print_no, prefix)
                    print_list += return_list
        else:
            print_list.append(
                f"{print_no} {prefix}▶ {self.value}")
            print_no += 1
        self.print_range.append(print_no)
        return print_list, print_no

    def find_node(self, index):
        """
        Recursively find the node with the matching print index then toggle opened
        Parameters:
            index: The index in which to find the node
        Exception:
            None
        Returns:
            None
        """
        if self.print_range[0] == index:
            self.toggle_opened()
        else:
            for child in self.children:
                child.find_node(index)

    def toggle_opened(self):
        """
        Toggles the boolean value of the opened attribute
        Parameters:
            None
        Exception:
            None
        Returns:
            None
        """
        if self.opened:
            self.opened = False
        else:
            self.opened = True

    def set_output(self, value):
        self.output = value
