import sys


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


# implement union find data structure
class DisjointSet:
    def __init__(self, vertex_number):
        self.vertex_parent = []  # initialise an array to hold the id and parent values.
        for k in range(vertex_number):  # put the height and vertex id's into the array
            self.vertex_parent.append([k, -1])

    def find(self, vertex):
        if self.vertex_parent[vertex][1] < 0: # its its own parent
            return vertex
        else: # reset all the children to the root
            self.vertex_parent[vertex][1] = self.find(self.vertex_parent[vertex][1])
            return self.vertex_parent[vertex][1]

    def union(self, u, v):
        root_u = self.find(u)  # get the root of vertex u
        root_v = self.find(v)
        if root_u == root_v:   # u and v already in same tree se we don't need to worry.
            return
        height_u = -(self.vertex_parent[self.find(u)][1] )
        height_v = -( self.vertex_parent[self.find(v)][1])
        if height_u > height_v: # the height of the 'u' tree is bigger
            # here we set the parent of v to be u
            self.vertex_parent[v][1] = root_u
        elif height_v > height_u:  # the height of the 'v' tree is bigger
            # here we set the parent of u to be v.
            self.vertex_parent[u][1] = root_v
        else:  # here the height of the two trees are equal
            self.vertex_parent[self.find(u)][1] = root_v
            self.vertex_parent[v][1] = -(height_u + 1)

def kruskal_algorithm(graph):
    # graph is formatted like [[u,v,w]. [u,v,w] ...]
    # first sort the graph by the edge weights.
    edge_weights = []
    size_graph = len(graph)
    sorted_by_weight = []
    output = []
    # first get the edge weights from the graph representation
    for k in graph:
        # graph is a list of lists and each list is u, v and w
        edge_weights.append(k[2])
        sorted_by_weight.append(None)
    positions = count_sort(edge_weights, 10)
    for i in range(size_graph):
        sorted_by_weight[positions[edge_weights[i]] - 1] = graph[i]
        positions[edge_weights[i]] += 1
    # so now we have all the edges sorted by weight.
    # now run through all of them and see if it makes a cycle at any iteration
    union_find = DisjointSet(size_graph)  # initialize a disjoint set data structure
    for edge in sorted_by_weight:
        u = edge[0]
        v = edge[1]
        if union_find.find(u) != union_find.find(v):
            #print(u,v, union_find.vertex_parent, union_find.find(u), union_find.find(v))
            union_find.union(u,v)
            output.append(edge)
    span = 0
    for j in output:
        span += j[2]
    return span, output


def readFiles(textFileName):
    textFile = open(textFileName, 'r')
    txt = textFile.read()
    textFile.close()
    return txt


def writeOutput(occurrences):
    output = open('output_binary_boyermoore.txt', 'w')
    for i in occurrences:
        output.write(str(i) + '\n')
    output.close()



# if __name__ == "__main__":
#     #txtFileName = sys.argv[1]
#     patFileName = sys.argv[2]
#     pat = readFiles(patFileName)
    # kruskal_output =
    # occurrences, comparisons = boyer_output[0], boyer_output[1]
    # writeOutput(occurrences)
    # print(comparisons)

#print(count_sort([10,12,3,4], 10))
#test_graph = [[0,1,5],[1,2,4],[2,3,2],[3,4,10],[4,5,6],[5,0,1], [0,6,8],[1,6,2],[2,6,1],[3,6,3], [4,6,7], [5,6,4]]
#print(kruskal_algorithm(test_graph))
#a = DisjointSet(7)
#a.union(5,6)
#rint(a.find(6))
#print(a.vertex_parent)




