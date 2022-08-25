import collections as coll


class LogLister:
    """ """

    def __init__(self, path):
        self.path = path

    def generate_data(self):
        log_file = open(self.path, "r")
        line_list = log_file.readlines()
        line_no = 0

        self.genesis = Node("File", -1)
        self.genesis.get_children(line_list, line_no)

        self.data_list = self.genesis.print_tree()
        print(self.data_list)

        self._data_to_tuple()

        return self.tuple_list

    def _data_to_tuple(self):
        self.tuple_list = []
        for index, item in enumerate(self.data_list):
            self.tuple_list.append((item, index))


class Node:
    def __init__(self, value, line, children=[], opened=False, output=None):
        self.value = value
        self.line = line
        self.children = children[:]
        self.opened = opened
        self.output = output

    def get_children(self, line_list, line_no):
        print("getting children")

        while True:

            print(line_no)
            if line_list[line_no].startswith("->"):
                # Must be the start of a node
                print("Code")
                child = Node(line_list[line_no][2:].strip(), line_no)
                line_no += 1

                if not line_list[line_no].startswith("->"):
                    # Must have some data
                    if line_list[line_no].startswith("--Call--"):
                        print("Called")
                        line_no += 1
                        line_no = child.get_children(line_list, line_no)
                        self.children.append(child)

                    elif not line_list[line_no].startswith("--"):
                        print("Output")
                        child.set_output(line_list[line_no].strip())
                        line_no += 1

                    if line_list[line_no].startswith("--Return--"):
                        # We have found the return for this nodes children
                        # Break out of this function
                        print("Returned")
                        line_no += 1
                        self.children.append(child)
                        break

                else:
                    # New node so just continue
                    print("End of data")
                self.children.append(child)
        return line_no

    def print_tree(self, markerStr="+- ", levelMarkers=[]):
        print_list = []
        emptyStr = " " * len(markerStr)
        connectionStr = "|" + emptyStr[:-1]

        level = len(levelMarkers)
        mapper = lambda draw: connectionStr if draw else emptyStr
        markers = "".join(map(mapper, levelMarkers[:-1]))
        markers += markerStr if level > 0 else ""
        print_list.append(f"{markers}{self.value}")
        if self.output:
            spacer = "|" + "  "
            print_list.append(f"{spacer}{markers}{self.output}")
        for i, child in enumerate(self.children):
            isLast = i == len(self.children) - 1
            print_list += child.print_tree(markerStr, [*levelMarkers, not isLast])
        return print_list

    # def print_tree(self, print_list, markerStr="+- ", levelMarkers=[]):
    #     emptyStr = " " * len(markerStr)
    #     connectionStr = "|" + emptyStr[:-1]
    #     level = len(levelMarkers)
    #     mapper = lambda draw: connectionStr if draw else emptyStr
    #     markers = "".join(map(mapper, levelMarkers[:-1]))
    #     markers += markerStr if level > 0 else ""
    #     print(f"{markers}{self.value}")
    #     if self.output:
    #         spacer = "|" + "  "
    #         print(f"{spacer}{markers}{self.output}")
    #     for i, child in enumerate(self.children):
    #         isLast = i == len(self.children) - 1
    #         child.print_tree(print_list, markerStr, [*levelMarkers, not isLast])

    def get_value(self):
        return self.value

    def print_children(self, prefix):
        # If the node is not opened then dont give any children
        prefix += "- "
        for child in self.children:
            print(prefix + child.value)
            if child.output:
                print(prefix + "- = " + child.output)

            child.print_children(prefix)

    def debug(self):
        for child in self.children:
            print(child.value)
            print(child.line)

    def add_child(self, child):
        self.children.append(child)

    def set_output(self, output):
        self.output = output

    def set_value(self, value):
        self.value = value

    def toggle_opened(self):
        self.opened ^= True
