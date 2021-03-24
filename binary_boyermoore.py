# first start off making the rightmost to the left of each position table
# Get the z_algorithm from part one, along with reverse string functions.

def z_algorithm(input_str):
    # first initialise z list and l and r list
    str_size = len(input_str)
    if str_size > 1: # if its bigger than one then we will do all the z_stuff
        z_list = [None for k in range(str_size)]
        # with the l_list and r_list we will concatenate values to them as we do comparisons.
        # this is easier since we can easily get the most recent l box and r box values
        l_list = [str_size]
        r_list = [str_size]
        # set first index (0th index) to be the length of the string.
        z_list[0] = str_size  # set z[0] to be length of string. This is z1.
        # now we find z2 (which in this case is z_list[1])
        match_counter = 0  # assign a variable to count the number of matches
        # now make while loop to count the number of matches.
        # Ensure that we do not go to end of string and end up getting an index error with the first condition.
        while 1 + match_counter < str_size and input_str[0 + match_counter] == input_str[1 + match_counter]:
            match_counter += 1
        z_list[1] = match_counter  # assign first index to the number of matches. (This is z2 in the lecture slides)
        if match_counter > 0:  # if number of matches > 0
            # set r to to be the number of matches.
            # This is shown as z2 + 1 in lectures cause the lectures 1 index everything.
            r_list += [match_counter]
            # set l to 1
            # (in lectures this is shown to be 2 but I am 0 indexing everything, thought it would be easier that way)
            l_list += [1]
        else:
            # i.e if number of matches is 0 then.
            # set r to 0
            r_list += [0]
            # set l to 0
            l_list += [0]
        # now we will do the comparisons in the rest of the string.
        # make a for loop to go through the rest of the string.

        for k in range(2, str_size):
            if k > r_list[-1]:  # Case 1 k > r
                # all we do now is explicitly compare from the start of the string.
                q_counter = 0  # set a variable to count our number of matches.
                # I used q cause q was in the lectures.
                while k + q_counter < str_size and input_str[k + q_counter] == input_str[q_counter]:
                    # loop through and find matches
                    q_counter += 1
                z_list[k] = q_counter
                if q_counter > 0:  # if zk > 0
                    # set r to be where last match occurred. In my case this is at k + q_counter - 1 (same as lecture)
                    r_list += [k + q_counter - 1]
                    # set l to k value
                    l_list += [k]
                else:  # if there were no matches.
                    # l and r retain there current values
                    r_list += [r_list[-1]]
                    l_list += [r_list[-1]]

            else:  # Case 2 where k <= r
                l = l_list[-1]
                r = r_list[-1]
                if z_list[k - l] < r - k + 1:  # case 2a where Z k  - l < r - k
                    # no need for the +1's as shown in lectures. All lines up fine
                    # set zk to Z k-l
                    z_list[k] = z_list[k - l]
                    # r and l remain unchanged
                    r_list += [r_list[-1]]
                    l_list += [l_list[-1]]


                elif z_list[k - l] > r - k + 1:  # Case 2b from tute. Zk - l > r - k.
                    # this case is like when a previous z_box is already bigger your current z_box
                    # then you will already know that the number of matches is r - k.
                    z_list[k] = r - k + 1
                    # nothing happens with l and r so they remain unchanged.
                    r_list += [r_list[-1]]
                    l_list += [l_list[-1]]

                else:
                    # Case 2c where Z k - l = r - k.
                    # this is where our two most recent z_boxes are the same length
                    # Thus we will have to do some explicit comparisons yee yee.
                    q_counter = 1  # set a variable to be our number of matches
                    while r + q_counter < str_size and input_str[r + q_counter] == input_str[r - k + 1]:
                        q_counter += 1
                    # Set Zk to be  number of matches + the current z_box size.
                    z_list[k] = (r - l + 1) + q_counter
                    # with r we update r to be current r value + the number that matches
                    r_list += [r + q_counter - 1]
                    # Set l to be k since this is the start of a new z_box that goes outside of our current one.
                    l_list += [k]

    else:  # if its length 1 then assign all the lists to be the string length.
        z_list = [1]
        l_list = [1]
        r_list = [1]

    return z_list

def reverse_string(string):
    result = ''
    n = len(string)
    for k in range(n - 1, -1 , -1):
        result += string[k]
    return result



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



def biggest_smaller(a_list, a_value):
    left = 0
    right = len(a_list) - 1
    if right == left:  # this means our list only has one element
        # for this we will just output the list element
        return a_list[0]

    while left <= right:  # while two dividing areas are not the same
        middle = (left + right) // 2

        if right == left + 1:  # this means we did not find the element
            # now check if the right or left elements are smaller than a_value
            if a_list[right] < a_value:
                return a_list[right]

            elif a_list[left] < a_value:
                return a_list[left]

            else:
                # this case is where a_value is in the list but we got to a point where right == left + 1
                return a_value

        elif a_value > a_list[middle]:  # if middle element is smaller than the one we are looking for
            left = middle  # set left to be the middle

        elif a_value < a_list[middle]:  # if the middle element is bigger than the one we are looking for
            right = middle  # set right to be the middle

        else:
            # this is the final case where we find the element
            # output the value and index
            return middle, a_value


def list_reverse(a_list):
    final_list = []
    n = len(a_list)
    for k in range(n -1, -1, -1):
        final_list.append(a_list[k])
    return final_list

def except_last(a_list):
    final_list = []
    n = len(a_list)
    for k in range(n - 1):
        final_list.append(a_list[k])
    return final_list


def z_suffix(a_string):
    # This function returns the z_suffix values for a string
    # all we got to do is compute the z_values for the string reversed.
    return except_last(list_reverse(z_algorithm(reverse_string(a_string))))


def good_suffix(a_string):
    good_suff = []
    z_suff = z_suffix(a_string)
    # use function given in lectures
    m = len(a_string)
    for j in range(m + 1):
        good_suff.append(0)

    for p in range(m - 1):
        j = m - z_suff[p]
        good_suff[j] = p + 1
    return good_suff


def matched_prefix(a_string):
    str_size = len(a_string)
    matched_prefix_list = []
    for k in range(str_size + 1):
        matched_prefix_list.append(0)
    start = 0
    end = str_size - 1
    while end != 0:
        counter = 0
        matches = 0
        while end + counter < str_size and a_string[end + counter] == a_string[start + counter]:
            matches += 1
            counter += 1
        matched_prefix_list[end] = matches   # set index to be the number of matches
        if matched_prefix_list[end] < matched_prefix_list[end + 1]:
            # if the number of matches is less than previous iteration
            # set number of matches to the bigger one
            matched_prefix_list[end] = matched_prefix_list[end + 1]
        end -= 1
    # set first index to be the length of the string
    matched_prefix_list[0] = str_size
    return matched_prefix_list



def good_suffix_shift(pat, k):
    good_suff = good_suffix(pat)
    matched_pre = matched_prefix(pat)
    shift = 0
    pat_length = len(pat)
    if good_suff[k + 1] > 0:
        shift = pat_length - good_suff[k + 1]
    else:
        shift = pat_length - matched_pre[k + 1]
    return shift




def boyer_moore(txt, pat):
    result = []
    # okay so we will first do the part for the bad character rule in the code.
    comp_counter = 0  # assign variable that will help to compare to all of txt. Stands for comparison counter
    total_counter = 0 # variable for total number of comparisons made by algorithm
    total_comparisons = 0  # assign a variable to count the total number of comparisons
    # assign two values to be the lengths of the txt and the pattern
    txt_length = len(txt)
    pat_length = len(pat)
    # now use the array that has the rightmost positions of the string
    # assign this to two variables
    bad_char_array = bad_char_processing(pat)[0]  # the rightmost positions
    already_there = bad_char_processing(pat)[1]  # this contains the ascii values of the letters in pattern
    # we can use already_there to see if a txt letter we are matching is even in the string
    # Now also preprocess the string for the good suffix stuff
    matched_pre = matched_prefix(pat)
    while pat_length + comp_counter <= txt_length:  # start outer loop and begin comparisons
        loop_counter = 1 # this checks if the for loop runs in its entirety.
        for k in range(pat_length - 1, -1, -1):  # check from left to right for matching characters
            total_counter += 1  # increment the total count since a comparison is about to be made.
            if pat[k] != txt[k + comp_counter]:  # in this case the characters do not match
                # good suffix:
                good_shift = good_suffix_shift(pat, k)
                # now we have to find the rightmost occurrence of the mismatched character in text, within pattern
                # if we cannot find it then default the shift to 1
                # first find ascii value of the mismatched character
                mismatch_asc = ord(txt[k])
                if already_there[mismatch_asc] is not None:  # here the mismatched character is in text
                    # now find the rightmost occurrence of this character
                    index_and_value = already_there[mismatch_asc]  # assign variable to hold the index and value
                    # of the mismatched character
                    index_in_pat = index_and_value[0]  # assign variable to index of mismatched character in pat
                    # the bad character list has the occurrences of this letter.
                    # to find them:
                    right_most = biggest_smaller(bad_char_array[index_in_pat], k)
                    # so now we got the right most occurrence of the mismatched character yee yee.
                    # Now we will assign a variable to the amount we got to shift by
                    shift_maybe = k - right_most
                    # the actual shift will be the maximum of this value and good_shift. Thus:
                    actual_shift = max(good_shift, shift_maybe)
                    comp_counter += actual_shift  # shift the pattern forward.
                    break  # now break out of the for loop no more comparison needed.

                else:  # here the mismatched character ain't even in text man.
                    actual_shift = max(good_shift, shift_maybe)  # so we just shift by max of the two.
                    comp_counter += actual_shift

            else:  # in this case the characters actually match so all good
                if loop_counter == pat_length:  # if the whole pattern matched
                    # then we can shift the pattern forward by matched_prefix[1]
                    result += [k + comp_counter]  # put the index where full match ends into the result list
                    # shift the pattern forward by pat_length - matched_prefix[1]
                    comp_counter += pat_length - matched_pre[1]
                else:  # otherwise keep checking

                    loop_counter += 1
    return result, total_counter


def get_text(a_file):
    with open(a_file, 'r') as file:
        content = file.readlines()
    return content[0]

print(boyer_moore('01010101010', '01'))
