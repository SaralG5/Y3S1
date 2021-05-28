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


def decode_elias(a_rep):
    # decode the elias integer encoding of something
    if a_rep[0] == '1':
        return 1, 1  # 0 , 1
    start = 0
    str_length = len(a_rep)
    end = 0  # 1
    prev = 0
    bin_rep = ''
    while a_rep[start] != '1':  # if we go in that means we are still looking at length components
        if end == 0:  # first iteration
            bin_rep = '1'
            start = 1
            end = 3

        else:  # not the first iteration
            prev = int(bin_rep, 2) + 1
            current_comp = a_rep[start: end]
            # change first bit to a 0
            list_rep = list(current_comp)
            list_rep[0] = '1'
            bin_rep = ''.join(list_rep)
            move_forward = int(bin_rep, 2) + 1
            start += prev
            end += move_forward
    answer = a_rep[start: end]
    # return  start end
    return int(answer, 2), end


def test_elias_decode(an_integer):
    # bin_rep = bin(an_integer)[2:]
    encoding = elias(an_integer)
    value = decode_elias(encoding)[0]
    return value == an_integer


# print(test_elias_decode(1))
# print(decode_elias('011110000111110001001000110001101001'))

def portion_header(a_string):
    times_check = 7
    letter_bits = a_string[0: 7]
    actual_letter = chr(int(letter_bits, 2))
    elias_part = a_string[7:]
    huffman_code_info = decode_elias(elias_part)
    end_elias = huffman_code_info[1]
    huffman_code_length = huffman_code_info[0]
    times_check += end_elias
    # now we are at the start of the actual huffman code and the rest of the string is the huffman code.
    # which we now have the length and the starting position for
    huffman_code = a_string[times_check: ]
    times_check += huffman_code_length  # now we know how long everything was
    all_info = [actual_letter, huffman_code]
    return all_info, times_check


print(portion_header('110000111'))
print(portion_header('110001001000'))
print(portion_header('110001101001'))


def decode_header(a_string):
    initial = decode_elias(a_string)
    amount_unique = initial[0]
    huff_start = initial[1]
    # now we decode the actual information in the header.
    # first thing is the ascii value which is seven bits, so we know to read 7 bits from this point

    return amount_unique, huff_start


#print(decode_header('011110000111110001001000110001101001'))
