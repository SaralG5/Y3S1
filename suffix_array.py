def is_prefix(a_string, first_tup, second_tup):
    """
    This function checks if the string represented by first_tup is a prefix of the string represented by second_tup
    or if second_tup is a prefix of first_tup
    :param a_string: a string
    :param first_tup: a tuple/list representing the starting an ending indexes of a sub string of a_string
    :param second_tup: another tuple/list representing the starting and ending indexes of a sub string of a_string
    :return: (Bool, index of match or mismatch)
    @complexity_time: O(n) where n is the length of a_string
    """

    size_first_tup = abs(first_tup[0] - first_tup[1]) + 1  # create variable representing size of string for first_tup
    # size_second_tup = second_tup[0] + second_tup[1] + 1  # create variable for size of string representing second_tup.
    start_first = first_tup[0]  # get the starting index of the first tuple.
    start_second = second_tup[0]  # get the starting index of the second tuple.
    counter = 0
    # if first_tup <= second_tup:
    while counter < size_first_tup:
        if a_string[start_first + counter] != a_string[start_second + counter]:
            return False, start_first + counter, start_second + counter
        counter += 1
    return True, start_first + counter, start_second + counter


class SuffixTree:
    def __init__(self, a_string):
        self.input_string = a_string  # the input string
        self.root_list = []  # this list will act as the root node for the suffix tree
        for k in range(122):  # 122 because the assignment specs say that 122 is the highest ascii value
            self.root_list.append([])  # append an empty list
            # each empty list will act as a branch from the root node

    def ukkonen(self):
        global_end = 0  # initialise global end.
        last_j = 0  # initialise last_j which is the last place that you did a rule 2/1.
        phase = 0  # initialise phase.
        extension = 0  # initialise extension.
        size_string = len(self.input_string)  # the length of the input string.
        while phase < size_string:  # while the phases are less than the string length.
            extension = 0
            while extension <= phase:  # while the extensions are less then the phases.
                # the string we have to compare to root node branches is: str[extension: phase].
                # this can be represented as two integers [extension,phase].
                # So firstly we have to check if the root node list even has stuff in it.
                current_string = [extension, phase]  # get the current string for that extension and phase.
                # now find the ascii value of the first character in current string.
                asc_value = ord(self.input_string[extension])
                # Now check if the root list has anything at this ascii value
                if not self.root_list[asc_value]:  # if there is nothing there
                    self.root_list[asc_value].append(extension)  # append the index of the current letter
                    extension += 1
                else:  # Otherwise if we have an edge.
                    # (i.e there is an integer in the list there at the index of the ascii value)
                    # Then we have to see if we have a rule 1, 2 or 3 situation
                    extension = last_j + 1  # In general the comparisons will start from last_j onwards
                    current_string = [extension, phase]  # get current string of extension and phase
                    edge_string = [self.root_list[asc_value][0], global_end]  # get string on edge
                    # check if current string is a prefix of whats on the edge
                    is_a_prefix = is_prefix(self.input_string, current_string, edge_string)
                    # if it is a prefix then we have a rule 3 situation
                    if is_a_prefix[0]:  # if it is a prefix
                        # then we can stop this phase
                        break
                    else:  # if not then it will be a rule 2 situation
                        # in rule 2's we have to deal with suffix links and all that jazz
                        for i in range(extension, global_end + 1):
                            # go to each index of the starting letter
                            index_letter = ord(self.input_string[i])
                            # add to the root list
                            self.root_list[index_letter].append(i)
                        last_j = global_end  # reset last_j value
                        break  # can go straight to the next phase after this
            global_end += 1
            phase += 1
        return global_end - 1, self.root_list


def mismatch_finder(a_string, pair_one, pair_two):
    # get the smaller of the two
    one_size = abs(pair_one[1] - pair_one[0]) + 1
    two_size = abs(pair_two[1] - pair_two[0]) + 1
    one_start = pair_one[0]
    two_start = pair_two[0]
    counter = 0
    if one_size < two_size:
        while counter < one_size:
            if a_string[one_start + counter] != a_string[two_start + counter]:
                return False, one_start + counter, two_start + counter
            counter += 1
        return True, 0, 1

    elif one_size == two_size:
        while counter < one_size:
            if a_string[one_start + counter] != a_string[two_start + counter]:
                return False, one_start + counter, two_start + counter
            counter += 1
        return True, 0, 0  # this case will never happened, just put a return there for safekeeping.

    else:
        while counter < two_size:
            if a_string[one_start + counter] != a_string[two_start + counter]:
                return False, one_start + counter, two_start + counter
            counter += 1
        return True, 1, 0


class BinaryNode:
    def __init__(self, suffix_id):
        self.left = None
        self.right = None
        self.suffix_id = suffix_id


class BinaryTree:
    def __init__(self, a_string, end):
        self.root = None
        self.input_string = a_string
        self.end = end

    def insert(self, suffix_id):
        if self.root is None:
            self.root = BinaryNode(suffix_id)
        else:
            self._insert(suffix_id, self.root)

    def _insert(self, suffix_id, a_node):
        mismatch = mismatch_finder(self.input_string, [a_node.suffix_id, self.end], [suffix_id, self.end])
        node_letter = ord(self.input_string[mismatch[1]])
        insert_letter = ord(self.input_string[mismatch[2]])
        if mismatch[0]:
            node_letter = mismatch[1]
            insert_letter = mismatch[2]
        if insert_letter < node_letter:
            if a_node.left is not None:
                self._insert(suffix_id, a_node.left)
            else:
                a_node.left = BinaryNode(suffix_id)
        else:
            if a_node.right is not None:
                self._insert(suffix_id, a_node.right)
            else:
                a_node.right = BinaryNode(suffix_id)

    def insert_many(self, suffix_id_list):
        for k in suffix_id_list:
            self.insert(k)

    def retrieve(self):
        if self.root is not None:
            return self._retrieve(self.root)

    def _retrieve(self, a_node):
        if a_node is None:
            return []
        else:
            return self._retrieve(a_node.left) + [a_node.suffix_id] + self._retrieve(a_node.right)


def ukkonen_full(a_string):
    initial = SuffixTree(a_string)
    suffix_tree = initial.ukkonen()
    end = suffix_tree[0]
    edges = suffix_tree[1]
    suffix_array = []
    for i in edges:
        if i:
            binary = BinaryTree(a_string, end)
            binary.insert_many(i)
            suffix_array += binary.retrieve()
    return [end + 1] + suffix_array

print(ukkonen_full('abcdabcbdab'))
#a = SuffixTree('mississippi')
#print(a.ukkonen())
# b = BinaryTree('mississippi', 10)
# b.insert(1)
# b.insert(4)
# b.insert(7)
# b.insert(10)
# print(b.retrieve())

#
# def ukkonen_other(self):
#     global_end = 0  # initialise global end.
#     last_j = 0  # initialise last_j which is the last place that you did a rule 2/1.
#     phase = 0  # initialise phase.
#     extension = 0  # initialise extension.
#     size_string = len(self.input_string)  # the length of the input string.
#     while phase < size_string:  # while the phases are less than the string length.
#         extension = 0
#         while extension <= phase:  # while the extensions are less then the phases.
#             # the string we have to compare to root node branches is: str[extension: phase].
#             # this can be represented as two integers [extension,phase].
#             # So firstly we have to check if the root node list even has stuff in it.
#             current_string = [extension, phase]  # get the current string for that extension and phase.
#             # now find the ascii value of the first character in current string.
#             asc_value = ord(self.input_string[extension])
#             # Now check if the root list has anything at this ascii value
#             if not self.root_list[asc_value]:  # if there is nothing there
#                 self.root_list[asc_value].append(extension)  # append the index of the current letter
#                 extension += 1
#             else:  # Otherwise if we have an edge.
#                 # (i.e there is an integer in the list there at the index of the ascii value)
#                 # Then we have to see if we have a rule 1, 2 or 3 situation
#                 extension = last_j + 1  # In general the comparisons will start from last_j onwards
#                 asc_value = ord(self.input_string[extension])
#                 if not self.root_list[asc_value]:  # if there is nothing there
#                     print('here')
#                     self.root_list[asc_value].append(extension)  # append the index of the current letter
#                     # increment global_end, extension and last_j
#                     extension += 1
#                     last_j += 1
#                 else:  # if there is an edge
#                     current_string = [extension, phase]  # get current string of extension and phase
#                     edge_string = [self.root_list[asc_value][0], global_end]  # get string on edge
#                     # check if current string is a prefix of whats on the edge
#                     is_a_prefix = is_prefix(self.input_string, current_string, edge_string)
#                     # if it is a prefix then we have a rule 3 situation
#                     if is_a_prefix[0]:  # if it is a prefix
#                         # then we can stop this phase
#                         break
#                     else:  # if not then it will be a rule 2 situation
#                         # in rule 2's we have to deal with suffix links and all that jazz
#                         for i in range(extension, global_end + 1):
#                             # go to each index of the starting letter
#                             index_letter = ord(self.input_string[i])
#                             # add to the root list
#                             self.root_list[index_letter].append(i)
#                         last_j = global_end  # reset last_j value
#                         break  # can go straight to the next phase after this
#         global_end += 1
#         phase += 1
#     # So at this point we have all the information about the suffixes in the root list
#     # To construct the suffix array we need an array indexed by id that contains the rank of each suffix
#     # so we will construct this and then pass this into the suffix array function.
#     return global_end - 1, self.root_list
