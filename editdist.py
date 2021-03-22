# first code z algorithm

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
                if z_list[k - l] < r - k:  # case 2a where Z k  - l < r - k
                    # no need for the +1's as shown in lectures. All lines up fine
                    # set zk to Z k-l
                    z_list[k] = z_list[k - l]
                    # r and l remain unchanged
                    r_list += [r_list[-1]]
                    l_list += [l_list[-1]]

                elif z_list[k - l] > r - k:  # Case 2b from tute. Zk - l > r - k.
                    # this case is like when a previous z_box is already bigger your current z_box
                    # then you will already know that the number of matches is r - k.
                    z_list[k] = r - k
                    # nothing happens with l and r so they remain unchanged.
                    r_list += [r_list[-1]]
                    l_list += [l_list[-1]]

                else:  # Case 2c where Z k - l = r - k.
                    # this is where our two most recent z_boxes are the same length
                    # Thus we will have to do some explicit comparisons yee yee.
                    q_counter = 0  # set a variable to be our number of matches
                    while r + 1 + q_counter < str_size and input_str[r + 1 + q_counter] == input_str[r - k + 1]:
                        q_counter += 1
                    # Set Zk to be r - k + q_counter. This is the number of matches + the current z_box size.
                    z_list[k] = r - k + q_counter
                    # with r we update r to be current r value + the number that matches
                    r_list += [r + q_counter]
                    # Set l to be k since this is the start of a new z_box that goes outside of our current one.
                    l_list += [k]

    else:  # if its length 1 then assign all the lists to be the string length.
        z_list = [1]
        l_list = [1]
        r_list = [1]
    return z_list


def dist_finder(txt, pat):
    pos_in_text = []
    # First lets deal with insertion
    norm_concat = pat + txt  # concatenate the two together
    str_length = len(norm_concat)
    txt_length = len(txt)
    pat_length = len(pat)

    reverse_concat = reverse_string(pat) + reverse_string(txt)    #

    # now run z_algorithm on both the norm_concat and reverse_concat
    norm_z = z_algorithm(norm_concat)
    reverse_z = z_algorithm(reverse_concat)

    for i in range(pat_length, str_length):
        if norm_z[i] >= 1:
            if reverse_z[txt_length - 1 + pat_length - norm_z[i] ] + norm_z[i] == pat_length:
                pos_in_text.append([i-pat_length, 0])
            # check reverse_z list for any z_value at corresponding letter
            elif reverse_z[txt_length - 1 + pat_length - norm_z[i] ] + norm_z[i] == pat_length - 1:
                pos_in_text.append([i - pat_length, 1])

    return pos_in_text



def reverse_string(string):
    result = ''
    n = len(string)
    for k in range(n - 1, -1 , -1):
        result += string[k]
    return result


print(reverse_string('abcd'))
#print(dist_finder('zxycade', 'cab'))
print(dist_finder('abdyabxdcyabcdz', 'abcd'))
print(dist_finder('zxycade','cab'))
#print(z_algorithm('aaba'))


# one below is real one
def z_algorithm_two(input_str):
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
                    z_list[k] = r - k
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
                    # Set Zk to be r - k + q_counter. This is the number of matches + the current z_box size.
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

print(z_algorithm_two('abacababaca'))

