
# first start off making the rightmost to the left of each position table
def boyer_moore(txt, pat):
    # start off with only bad character
    txt_length = len(txt)
    pat_length = len(pat)
    bad_char_array = bad_char_processing(pat)[0]
    ascii_val = bad_char_processing(pat)[1]
    full_matches = []
    counter = 0
    while counter < txt_length:
        for_counter = 0
        # now compare right to left stuff
        for k in range(pat_length,  0 , -1):
            asc = ord(txt[k])
            # if a mismatch occurs we shift stuff
            if pat[k] != txt[k]:
                # find rightmost occurrence of letter from position k
                # Two cases: if the char is in the pat or not
                if ascii_val[asc] != None:  # this means the txt mismatched character is in the pattern
                    # check its rightmost occurence
                    bad_index = ascii_val[asc][0]
                    occurences = bad_char_array[bad_index]
                    right_most = biggest_smaller(occurences, k)
                    # so now we shift by k - right_most position
                    counter = k - right_most
                    # and now we start our comparisons from here.

                else:
                    # the char in this case is not even in the pat
                    # so we just shift by 1
                    counter += 1
            else:
                # the character matched
                for_counter += 1
                if for_counter == pat_length:   # this means we have a full match
                    full_matches += [pat_length]






def bad_char_processing(a_string):
    # In this function we just want to make the extended bad character array,
    bad_array = []
    str_size = len(a_string)
    ascii_values = [None for j in range(256)]
    for i in range(str_size):
        asc_value = ord(a_string[i])
        if i == 0:
            # here we start to build the bad array
            bad_array += [[0]]
            ascii_values[asc_value] = (i, a_string[i])

        elif ascii_values[asc_value] != None:
                    most_recent = ascii_values[asc_value]
                    # this means this string is already in bad_array
                    # now just add the new index to the list, since we now where the character is
                    bad_array[most_recent[0]] += [i]

        else:  # here the character has not been seen yet
            # so just make a new list for that character
            bad_array += [[i]]
            ascii_values[asc_value] = (i, a_string[i])

    return (bad_array, ascii_values)

print(bad_char_processing('tbapxab'))




def biggest_smaller(a_list, a_value):
    left = 0
    right = len(a_list) - 1
    if right == left: # this means our list only has one element
        # for this we will just output the list element
        return a_list[0]

    while left <= right:   # while two dividing areas are not the same
        middle = (left + right) // 2

        if right == left + 1:         # this means we did not find the element
            # now check if the right or left elements are smaller than a_value
            if a_list[right] < a_value:
                return a_list[right]

            elif a_list[left] < a_value:
                return a_list[left]

            else:
                # this case is where a_value is in the list but we got to a point where right == left + 1
                return a_value

        elif a_value > a_list[middle]:   # if middle element is smaller than the one we are looking for
            left = middle              # set left to be the middle

        elif a_value < a_list[middle]:  # if the middle element is bigger than the one we are looking for
            right = middle              # set right to be the middle

        else:
            # this is the final case where we find the element
            # output the value and index
            return middle, a_value
