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
    def __init__(self, a_string, b_string):
        self.input_string = a_string + b_string # the input string
        self.b_length = len(b_string)
        self.total_length = len(self.input_string)
        self.root_list = []  # this list will act as the root node for the suffix tree
        self.prefix = []
        for k in range(123):  # 122 because the assignment specs say that 122 is the highest ascii value
            self.root_list.append([])  # append an empty list
            self.prefix.append([])
            # each empty list will act as a branch from the root node

    def ukkonen(self):
        global_end = 0  # initialise global end.
        last_j = 0  # initialise last_j which is the last place that you did a rule 2/1.
        phase = 0  # initialise phase.
        extension = 0  # initialise extension.
        size_string = self.total_length  # the length of the input string.
        while phase < size_string:  # while the phases are less than the string length.
            extension = 0
            while extension <= phase:  # while the extensions are less then the phases.
                # the string we have to compare to root node branches is: str[extension: phase].
                # this can be represented as two integers [extension,phase].
                # So firstly we have to check if the root node list even has stuff in it.
                # now find the ascii value of the first character in current string.
                # Now check if the root list has anything at this ascii value
                asc_value = ord(self.input_string[extension])
                if not self.root_list[asc_value]:  # if there is nothing there
                    self.root_list[asc_value].append(extension)  # append the index of the current letter
                    extension += 1
                else:  # Otherwise if we have an edge.
                    # (i.e there is an integer in the list there at the index of the ascii value)
                    # Then we have to see if we have a rule 1, 2 or 3 situation
                    extension = last_j + 1  # In general the comparisons will start from last_j onwards
                    current_string = [extension, phase]  # get current string of extension and phase
                    asc_value = ord(self.input_string[extension])
                    matched = False
                    for suffix_id in self.root_list[asc_value]:
                        edge_string = [suffix_id, global_end]  # get string on edge
                        # check if current string is a prefix of whats on the edge
                        is_a_prefix = is_prefix(self.input_string, current_string, edge_string)
                        # if it is a prefix then we have a rule 3
                        if is_a_prefix[0]:  # if it is a prefix
                            #print(suffix_id, extension
                            # then we can stop this phase
                            matched = True
                            break
                    if matched:
                        break
                    # if not then it will be a rule 2 situation
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

