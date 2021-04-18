# first do naive implementation of Ukkonen

def is_prefix(a_string, another_string):
    # checks if a_string is a prefix of another_string
    another_string_length = len(another_string)
    a_string_length = len(a_string)
    a_string_counter = 0
    another_string_counter = 0
    if a_string_length > another_string_length:
       return False, -1
    elif a_string_length < another_string_length:
        for k in range(a_string_length):
            if a_string[k] == another_string[k]:
                pass
            else:
                return False, k
        return True, -1
    else:
        for k in range(a_string_length):
            if a_string[k] == another_string[k]:
                pass
            else:
                return False, k
        return True, -1


    #
    # if a_string_length > another_string_length:  # you cant hope to be a prefix mate in this case.
    #     return False, -1
    # elif another_string_length == a_string_length:
    #     for k in range(another_string_length):
    #         if a_string[k] == another_string[k]:
    #             pass
    #         else:
    #             return False, k
    #     return True, -1
    # else:
    #     for k in range(a_string_length):
    #         if a_string[k] == another_string[k]:
    #             pass
    #         else:
    #             return False, k
    #     return True, -1


class TreeNode:
    def __init__(self):
        self.has_edges = False
        self.edges = []  # The strings along the edges.
        self.has_links = False
        self.links = []  # links to other nodes


def part_string(start, end, a_string):
    output_str = ''
    for k in range(start, end + 1):
        output_str += a_string[k]
    return output_str


class SuffixTree:
    def __init__(self, a_string):
        self.input_string = a_string
        self.root = TreeNode()

    def insert(self, a_node, a_string):
        a_node.edges.append(a_string)
        return

    def ukkonen(self):
        # first find length of the string
        size_string = len(self.input_string)
        for k in range(size_string):
            for j in range(k + 1):
                current_suffix = part_string(j, k, self.input_string)  # get the string for the current extension.
                if not self.root.has_edges:  # check if there are edges from root
                    self.root.edges.append([current_suffix, False])
                    # if not then put current string in root edges list
                    # the false means that there is no node in that edge.
                    self.root.has_edges = True  # Now the root has edges.

                else:  # if the root node does have edges
                    no_edges = len(self.root.edges)
                    # then check if the current string is a prefix of any suffixes in the root edge list
                    for i in range(no_edges):
                        edge_string = self.root.edges[i][0]
                        rule_one_check = is_prefix(edge_string, current_suffix)
                        rule_three_check = is_prefix(current_suffix, edge_string)
                        if rule_one_check[0]:
                            # since we are building the tree we check if
                            # the current edges are prefixes of the string at a given suffix extension for rule 1
                            # if this case is true we apply rule 1 and extend the edge by the last character
                            # Since we are at a 'leaf'
                            edge_string += current_suffix[-1]
                            self.root.edges[i][0] = edge_string  # add the last character of string to edge.
                        elif rule_three_check[0]:  # Rule 3
                            pass  # do nothing
                        else:  # Rule 2 Extension
                            print(current_suffix, edge_string)
                            # we can either have a node at the point of mismatch or not
                            mismatch_index = rule_two_check[1]
                            mismatched_char = current_suffix[mismatch_index]
                            if mismatch_index == 0:  # alternative case for root, means first letter not match
                                self.root.edges.append([current_suffix, False])
                            else:
                                if type(self.root.edges[i][1]) == TreeNode:  # alternative case not root Rule 2
                                    already_node = self.root.edges[i][1]
                                    # check if this node has any edges
                                    if not already_node.has_edges:  # if there are no edges
                                        # then add the mismatched character
                                        already_node.edges.append([mismatched_char, False])
                                        already_node.has_edges = True
                                        self.root.edges[i][1] = already_node
                                    else:  # if there are edges
                                        # then we have to check which one to add to
                                        amount_char = len(already_node.edges)
                                        added = False
                                        for j in range(amount_char):
                                            if is_prefix(mismatched_char, already_node.edges[j][0]):
                                                already_node.edges[j][0] += mismatched_char
                                                added = True
                                                self.root.edges[i][1] = already_node
                                        if not added:  # means mismatched char is not in nodes edges
                                            already_node.edges.append([mismatched_char, False])
                                            self.root.edges[i][1] = already_node

                                else:  # rule 2 have to add node and a leaf
                                    # add a node
                                    new_node = TreeNode()
                                    new_node.edges.append([mismatched_char, False])
                                    self.root.edges[i][1] = new_node


















a = SuffixTree('abac')
a.ukkonen()
print(a.root.edges)