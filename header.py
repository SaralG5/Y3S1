import random
import timeit
import csv
import string
#TASK 1
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
    for i in range(biggest + 1):  #initialise count and position with the right amount on zeroes
        count.append(0)
        position.append(0)
    for z in range(len(num_list)):
        output.append(0)
    for integer in num_list:            # incrementing count where appropriate
        if integer == 0:
            zero_count += 1
        count[integer] += 1
    for j in range(1, biggest + 1):   # put values into position
        if j == 1:
            position[j] = 1
        else:
            position[j] = position[j-1] + count[j-1]

    for u in range(1, len(position)):             #dealing with zeroes
        position[u] =  position[u] + zero_count
    position[0] = 1

    return position    #had output as return previously


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
    amount = number_of_digits(biggest, b)                       #amount of digits in largest integer of num_list

    for z in range(len(num_list)):  #initialise output
        output.append(0)
        #sorted_list.append(0)

    while place < amount:
        digits = []
        sorted_list = []
        for i in range(len(num_list)):  #get last number and put in a list
            if place == 0:
                last_number = (num_list[i] // b**place) % b     #here was a 10
                digits.append(last_number)
            else:
                last_number = (output[i] // b ** place) % b     #here was a 10
                #output list should be somewhere here
                digits.append(last_number)

        position_list = count_sort(digits,b)
        #print(position_list)

        for f in range(len(num_list)):
            sorted_list.append(0)

        if place == 0:                          # first iteration
            for k in num_list:                  # set output to corresponding values in position list based of last digit (base 10)
                moded = (k // b **place) % b
                index_insert = position_list[moded] - 1
                output[index_insert] = k
                position_list[moded] += 1

        else:                                   # after last digit
            for k in output:                  # set output to corresponding values in position list based of last digit (base 10)
                moded = (k // b**place) % b
                index_insert = position_list[moded] - 1
                sorted_list[index_insert] = k   #another list so that output can be continuously reset
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
    amount = number_of_digits(biggest, b)                       #amount of digits in largest integer of num_list

    for z in range(len(num_list)):  #initialise output
        output.append(0)
        #sorted_list.append(0)

    while place < amount:
        digits = []
        sorted_list = []
        for i in range(len(num_list)):  #get last number and put in a list
            if place == 0:
                last_number = (double_list[i][1] // b**place) % b     #here was a 10
                digits.append(last_number)
            else:
                last_number = (output[i][1] // b ** place) % b     #here was a 10
                #output list should be somewhere here
                digits.append(last_number)

        position_list = count_sort(digits,b)
        #print(position_list)

        for f in range(len(num_list)):
            sorted_list.append(0)

        if place == 0:                          # first iteration
            for k in double_list:                  # set output to corresponding values in position list based of last digit (base 10)
                moded = (k[1] // b **place) % b
                index_insert = position_list[moded] - 1
                output[index_insert] = k
                position_list[moded] += 1

        else:                                   # after last digit
            for k in output:                  # set output to corresponding values in position list based of last digit (base 10)
                moded = (k[1] // b**place) % b
                index_insert = position_list[moded] - 1
                sorted_list[index_insert] = k   #another list so that output can be continuously reset
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
        self.root.left_bit = 0
        self.root.right_bit = 1
        self.root.left = left_node
        self.root.right = right_node

    def insert_node(self, a_node):
        # a_node has the smaller frequency value
        self.root = HuffmanTree(a_node.full_string + self.root.full_string, a_node, self.root)
        self.root.left_bit = 0
        self.root.right_bit = 1

    def insert_tree(self, a_tree):
        # a_tree is the smaller frequency tree
        # the root actually has all the information we need
        new_node = HuffmanNode(a_tree.root.full_string + self.root.full_string)
        new_node.left = a_tree.root
        new_node.left_bit = 0
        new_node.right_bit = 1
        new_node.right = self.root
        self.root = new_node

c = HuffmanNode('c')
b = HuffmanNode('b')
d = HuffmanTree('cb', c, b)







