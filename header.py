import random
import timeit
import csv
import string


# Radix Sort used in huffman making
def count_sort(num_list, b):
    """
    This function gives a list that contains the position of each element in the output list, when later used for radix sort.
    @param: num_list    a list containing positive integers in the range [1, 2**64 - -1]
    @param: b           an integer in the range [2, infinity] that will be the base used for sorting
    @return             a sorted list
    @complexity         O(M) where  M is the largest integer in num_list when represented in base 10.
    """
    count = []
    position = []
    output = []
    biggest = find_max(num_list)
    zero_count = 0
    for i in range(biggest + 1):  # initialise count and position with the right amount on zeroes
        count.append(0)
        position.append(0)
    for z in range(len(num_list)):
        output.append(0)
    for integer in num_list:  # incrementing count where appropriate
        if integer == 0:
            zero_count += 1
        count[integer] += 1
    for j in range(1, biggest + 1):  # put values into position
        if j == 1:
            position[j] = 1
        else:
            position[j] = position[j - 1] + count[j - 1]

    for u in range(1, len(position)):  # dealing with zeroes
        position[u] = position[u] + zero_count
    position[0] = 1

    return position  # had output as return previously


def find_max(list_num):
    """
    This function finds the biggest number in a list
    :param list_num     list containing positive integers
    :return:            the maximum element of num_list
    @complexity         O(N) where N is the length of num_list
    """
    current_max = list_num[0]
    for i in range(len(list_num)):
        if list_num[i] > current_max:
            current_max = list_num[i]
    return current_max


def number_of_digits(a_number, b):
    """
    This function counts the number of digits in a number represented in base b
    :param  a_number: any integer
    :param b:       the base for representation
    :return:        the number of digits in the number
    @complexity:    O(n) where n is the number of digits in the number
    """
    count = 0
    while a_number != 0:
        a_number = a_number // b
        count += 1
    return count


def radix_sort(num_list, b):
    """
    This function sorts a list in ascending order
    @param: num_list    a list containing positive integers in the range [1, 2**64 - 1]
    @param: b           an integer in the range [2, infinity] that will be the base used for sorting
    @return             a sorted list
    @complexity          O((N + b) * M) N is the length of num_list, b is the base used for sorting
                        and M is the number of digits of the largest integer in numlist when represented in base b
    """
    if not num_list:
        return []
    output = []
    place = 0
    biggest = find_max(num_list)
    amount = number_of_digits(biggest, b)  # amount of digits in largest integer of num_list

    for z in range(len(num_list)):  # initialise output
        output.append(0)
        # sorted_list.append(0)

    while place < amount:
        digits = []
        sorted_list = []
        for i in range(len(num_list)):  # get last number and put in a list
            if place == 0:
                last_number = (num_list[i] // b ** place) % b  # here was a 10
                digits.append(last_number)
            else:
                last_number = (output[i] // b ** place) % b  # here was a 10
                # output list should be somewhere here
                digits.append(last_number)

        position_list = count_sort(digits, b)
        # print(position_list)

        for f in range(len(num_list)):
            sorted_list.append(0)

        if place == 0:  # first iteration
            for k in num_list:  # set output to corresponding values in position list based of last digit (base 10)
                moded = (k // b ** place) % b
                index_insert = position_list[moded] - 1
                output[index_insert] = k
                position_list[moded] += 1

        else:  # after last digit
            for k in output:  # set output to corresponding values in position list based of last digit (base 10)
                moded = (k // b ** place) % b
                index_insert = position_list[moded] - 1
                sorted_list[index_insert] = k  # another list so that output can be continuously reset
                position_list[moded] += 1
            output = sorted_list
        place += 1

    return output


def radix_sort_list(double_list, b):
    """
    This function sorts a list of lists in ascending order based of the 1st indices of each of the lists.
    @param: double_list    a list containing lists that have two integers elements. For example [[1,2], [2,4]]
    @param: b           an integer in the range [2, infinity] that will be the base used for sorting
    @return             a sorted list
    @complexity          O((N + b) * M) N is the length of num_list, b is the base used for sorting
                        and M is the number of digits of the largest integer in double_list when represented in base b
    """
    if not double_list:
        return []
    num_list = []
    for i in double_list:
        num_list.append(i[1])
    output = []
    place = 0
    biggest = find_max(num_list)
    amount = number_of_digits(biggest, b)  # amount of digits in largest integer of num_list

    for z in range(len(num_list)):  # initialise output
        output.append(0)
        # sorted_list.append(0)

    while place < amount:
        digits = []
        sorted_list = []
        for i in range(len(num_list)):  # get last number and put in a list
            if place == 0:
                last_number = (double_list[i][1] // b ** place) % b  # here was a 10
                digits.append(last_number)
            else:
                last_number = (output[i][1] // b ** place) % b  # here was a 10
                # output list should be somewhere here
                digits.append(last_number)

        position_list = count_sort(digits, b)
        # print(position_list)

        for f in range(len(num_list)):
            sorted_list.append(0)

        if place == 0:  # first iteration
            for k in double_list:  # set output to corresponding values in position list based of last digit (base 10)
                moded = (k[1] // b ** place) % b
                index_insert = position_list[moded] - 1
                output[index_insert] = k
                position_list[moded] += 1

        else:  # after last digit
            for k in output:  # set output to corresponding values in position list based of last digit (base 10)
                moded = (k[1] // b ** place) % b
                index_insert = position_list[moded] - 1
                sorted_list[index_insert] = k  # another list so that output can be continuously reset
                position_list[moded] += 1
            output = sorted_list
        place += 1

    return output


class HuffmanNode:
    def __init__(self, a_string):
        self.left = None
        self.left_bit = None
        self.right = None
        self.right_bit = None
        self.full_string = a_string


class HuffmanTree:
    def __init__(self, a_string, left_node, right_node):
        self.root = HuffmanNode(a_string)
        self.root.left_bit = '0'
        self.root.right_bit = '1'
        self.root.left = left_node
        self.root.right = right_node

    def insert_node(self, a_node):
        # a_node has the smaller frequency value
        new_node = HuffmanNode(a_node.full_string + self.root.full_string)
        new_node.left = a_node
        new_node.left_bit = '0'
        new_node.right = self.root
        new_node.right_bit = '1'
        self.root = new_node

    def insert_tree(self, a_tree):
        # a_tree is the smaller frequency tree
        # the root actually has all the information we need
        new_node = HuffmanNode(a_tree.root.full_string + self.root.full_string)
        new_node.left = a_tree.root
        new_node.left_bit = '0'
        new_node.right = self.root
        new_node.right_bit = '1'
        self.root = new_node

    def retrieval_aux(self, a_node, current_string):
        if a_node.left is None:  # this means there is only a single letter here
            return [[a_node.full_string, current_string]]
        else:
            return (self.retrieval_aux(a_node.left, current_string + a_node.left_bit) +
                    self.retrieval_aux(a_node.right, current_string + a_node.right_bit))

    def retrieval(self):
        return self.retrieval_aux(self.root, '')


# tree = HuffmanTree('ab', HuffmanNode('a'), HuffmanNode('b'))
# tree.insert_node(HuffmanNode('c'))
# other_tree = HuffmanTree('ef', HuffmanNode('e'), HuffmanNode('f'))
# tree.insert_tree(other_tree)
# print(tree.retrieval())
#

def get_frequencies(a_string):
    # first count the frequencies of each unique character in the string.
    character = [0 for k in range(128)]
    output = []
    for letter in a_string:
        if character[ord(letter)] == 0:
            character[ord(letter)] = [letter, 1]
        else:
            character[ord(letter)][1] += 1
    for j in character:
        if type(j) == list:
            output.append(j)
    for i in output:
        i.append(HuffmanNode(i[0]))
    return radix_sort_list(output, 10)


def huffman_code_maker(a_string):
    frequencies = get_frequencies(a_string)
    if len(frequencies) == 1:
        return '1'
    # Theres at least two different things in the input string
    # OPTIMISATION POINT: can put all these assignments in a function
    first_letter = frequencies[0][0]
    first_letter_frequency = frequencies[0][1]
    second_letter = frequencies[1][0]
    second_letter_frequency = frequencies[1][1]
    first_left_node = HuffmanNode(first_letter)  # A node of the lower frequency letter
    first_right_node = HuffmanNode(second_letter)  # A node of the higher frequency letter
    first_two_letters = first_letter + second_letter
    first_two_frequency = first_letter_frequency + second_letter_frequency
    main_tree = HuffmanTree(first_two_letters, first_left_node, first_right_node)  # start the tree off
    new_frequencies = [[first_two_letters, first_two_frequency, main_tree]] + frequencies[2:]  # make a new frequencies list
    new_frequencies = radix_sort_list(new_frequencies, 10)  # sort the new frequencies
    # OPTIMISATION POINT: List slicing, maybe use a queue or something
    new_freq_length = len(new_frequencies)
    if new_freq_length == 1:
        # Then we would be done, this would imply a_string has only two unique characters
        # and we would then retrieve everything from main tree
        return main_tree.retrieval()
    while new_freq_length != 1:
        first_element = new_frequencies[0]
        second_element = new_frequencies[1]
        first_node = first_element[2]
        second_node = second_element[2]
        if type(first_element[2]) == HuffmanNode and type(second_element[2]) == HuffmanNode:
            concat = first_element[0] + second_element[0]
            total_freq = first_element[1] + second_element[1]
            new_frequencies = [[concat, total_freq, HuffmanTree(concat, first_node, second_node)]] + new_frequencies[2:]
            new_frequencies = radix_sort_list(new_frequencies, 10)
            new_freq_length = len(new_frequencies)

        elif type(first_element[2]) == HuffmanNode and type(second_element[2]) == HuffmanTree:
            concat = first_element[0] + second_element[0]
            total_freq = first_element[1] + second_element[1]
            the_tree = second_element[2]
            the_tree.insert_node(first_node)
            new_frequencies = [[concat, total_freq, the_tree]] + new_frequencies[2:]
            new_frequencies = radix_sort_list(new_frequencies, 10)
            new_freq_length = len(new_frequencies)

        elif type(first_element[2]) == HuffmanTree and type(second_element[2]) == HuffmanNode:
            concat = first_element[0] + second_element[0]
            total_freq = first_element[1] + second_element[1]
            the_tree = first_element[2]
            the_node = second_element[2]
            new_tree = HuffmanTree(concat, the_tree.root, the_node)
            new_frequencies = [[concat, total_freq, new_tree]] + new_frequencies[2:]
            new_frequencies = radix_sort_list(new_frequencies, 10)
            new_freq_length = len(new_frequencies)

        else: # both are trees
            concat = first_element[0] + second_element[0]
            total_freq = first_element[1] + second_element[1]
            smaller_tree = first_element[2]
            bigger_tree = second_element[2]
            bigger_tree.insert_tree(smaller_tree)
            new_frequencies = [[concat, total_freq, bigger_tree ]] + new_frequencies[2:]
            new_frequencies = radix_sort_list(new_frequencies, 10)
            new_freq_length = len(new_frequencies)

    return new_frequencies[0][2].retrieval()

#print(huffman_code_maker('A_DEAD_DAD_CEDED_A_BAD_BABE_A_BEADED_ABACA_BED'))

def reverser(a_list):
    new = []
    while a_list != []:
        new.append(a_list.pop())
    return new

def elias(an_integer):
    integer_binary = bin(an_integer)[2:]
    length_comp_size = len(integer_binary)
    components = []
    while length_comp_size > 1:
        comp_string = bin(length_comp_size - 1)[2:]
        length_comp_size = len(comp_string)
        # OPTIMISATION POINT: the way the zero is assigned
        comp_string = '0' + comp_string[1:]
        components.append(comp_string)
    in_order_comp = reverser(components)
    in_order_comp.append(integer_binary)
    output = ''.join(in_order_comp)
    return output

print(elias(561))





        # OPTIMISATION POINT: probably can change the way a zero is assigned











