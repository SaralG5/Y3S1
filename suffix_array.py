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


def id_rank(str_size, root_list):
    # this function creates a list indexed by rank with the ID of each suffix.
    output_list = [0 for i in range(str_size)]
    sorted_on_rank = []
    different_lets = 0
    for k in root_list:  # iterate through the edges of the root node.
        if k:  # if there is an edge
            for i in k:  # for each suffix on that edge
                sorted_on_rank.append([different_lets, i])  # put the rank and id into a list that is sorted on rank.
                output_list[i] = [different_lets, i]  # put the rank and ID into the output list.
                # indexed by the ID.
            different_lets += 1
    return str_size, sorted_on_rank, output_list


def in_place(str_size, a_list):
    output_list = [[] for k in range(str_size)]
    final_output = []
    for i in a_list:
        output_list[i[0]].append(i)
    for k in output_list:
        for j in k:
            if j:
                final_output.append(j)
    return final_output


def suffix_array(str_size, rank_sorted, id_sorted):
    k = 1
    ranks = 0
    while k < str_size:
        new_id_sorted = [0 for i in range(str_size)]
        new_id_sorted[0] = id_sorted[0]
        for j in range(str_size - 1):
            current_suffix = rank_sorted[j]  # the current suffix
            next_suffix = rank_sorted[j + 1]  # the next suffix
            if current_suffix[0] < next_suffix[0]:  # if the first rank is less than the second one
                # the set the rank of the next suffix to be the current one + 1
                new_id_sorted[next_suffix[1]] = [current_suffix[0] + 1, next_suffix[1]]

            elif current_suffix[0] == next_suffix[0]:  # the rank of current suffix is same as next one
                new_id_sorted[next_suffix[1]] = next_suffix

            else:  # the rank of the first suffix is bigger than the second.
                new_id_sorted[next_suffix[1]] = next_suffix
                new_id_sorted[current_suffix[1]] = [next_suffix[0] + 1, current_suffix[1]]
        rank_sorted = in_place(str_size, new_id_sorted)
        id_sorted = new_id_sorted
        k *= 2
    return rank_sorted


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
        # So at this point we have all the information about the suffixes in the root list
        # To construct the suffix array we need an array indexed by id that contains the rank of each suffix
        # so we will construct this and then pass this into the suffix array function.
        return id_rank(size_string, self.root_list)

a = SuffixTree('mississippi$')
b = a.ukkonen()
print(suffix_array(b[0], b[1], b[2]))