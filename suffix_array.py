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
            return False, start_first + counter
        counter += 1
    return True, start_second + counter

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
                    asc_value = ord(self.input_string[extension])
                    if not self.root_list[asc_value]:  # if there is nothing there
                        self.root_list[asc_value].append(extension)  # append the index of the current letter
                        # increment global_end, extension and last_j
                        extension += 1
                        last_j += 1
                    else:  # if there is an edge
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
        # now iterate and make everything output friendly, Still O(n) yee yee
        output_list = []
        ranks = []
        different_lets = 0
        for k in self.root_list:
            if k:
                for i in k:
                    ranks.append(different_lets)
                    output_list.append(i)
                different_lets += 1
        return output_list, ranks

    def suffix_array(self, id_list, rank_list):
        k = 1
        id_and_rank = []
        size_lists = len(id_list)
        for i in range(size_lists):
            id_and_rank.append([id_list[i], rank_list[i]])  # list for both ranks and id's
        indexed = [0 for k in range(size_lists)]
        for j in id_and_rank:
            indexed[j[0]] = j
        temp = [0 for i in range(size_lists)]
        while k < size_lists:
            new_indexed = [0 for i in range(size_lists)]
            print(indexed, new_indexed)
            counter = 0
            # now iterate through the rank_list
            while counter < size_lists - 1:
                first_suf = indexed[counter]
                second_suf = indexed[counter + 1]
                if first_suf[1] < second_suf[1]:
                    new_indexed[second_suf[0]] = [second_suf[0], first_suf[1] + 1]
                    counter += 1 # do nothing in this case
                else:
                    rank_one = indexed[first_suf[0] + k][1]
                    rank_two = indexed[second_suf[0] + k][1]
                    if rank_one < rank_two:
                        new_indexed[second_suf[0]] = [second_suf[0], first_suf[1] + 1]
                    else:
                        new_indexed[first_suf[0]] = [first_suf[0], second_suf[1] + 1]
                    counter += 1
            indexed = new_indexed
            k *= 2
        return indexed







a = SuffixTree('mississippi$')
c = a.ukkonen()
print(a.suffix_array(c[0], c[1]))

# extension  = 0
