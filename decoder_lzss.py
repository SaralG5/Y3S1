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
    huffman_code = a_string[times_check: times_check + huffman_code_length]
    times_check += huffman_code_length  # now we know how long everything was
    all_info = [actual_letter, huffman_code]
    return all_info, times_check


#
# print(portion_header('110000111'))
# print(portion_header('110001001000'))
# print(portion_header('110001101001'))

def header_dictionary(huff_codes):
    code_dict = {}
    for k in huff_codes:
        code_dict[k[1]] = k[0]
    return code_dict


def decode_header_part(a_string):
    initial = decode_elias(a_string)
    amount_unique = initial[0]
    huff_start = initial[1]
    main_portion = a_string[huff_start:]
    # now we decode the actual information in the header.
    # first thing is the ascii value which is seven bits, so we know to read 7 bits from this point
    full_codes = []
    for j in range(amount_unique):  # for each unique character go through and get information
        current_letter = portion_header(main_portion)
        full_codes.append(current_letter[0])
        main_portion = main_portion[current_letter[1]:]
    # return main portion as well
    return header_dictionary(full_codes), main_portion


# print(decode_header_part('011110000111110001001000110001101001'))


def decode_data_part(a_string, huff_dictionary):
    output_str = []
    # huff dictionary the key is the code and the value is the letter itself.
    # first find the total number of fields
    fields_start = decode_elias(a_string)
    total_fields = fields_start[0]
    data_start = fields_start[1]
    actual_data_part = a_string[data_start:]
    # now the data decoding begins using our dictionary.
    # number of fields means the number of times we should see a 1 or a 0 in the format fields encoding stuff.
    data_length = len(actual_data_part)
    count = 0
    while count < data_length:
        if actual_data_part[count] == '1':  # Format 1 string
            huff_count = 1
            start_code = count + 1
            # what comes after it has to be a huffman code so we will see it its in the dictionary
            chunk = actual_data_part[start_code: start_code + huff_count]
            while chunk not in huff_dictionary:
                huff_count += 1
                chunk = actual_data_part[start_code: start_code + huff_count]
            output_str.append(huff_dictionary[chunk])
            count += (huff_count + 1)  # increment count to the start of the next format field

        else:  # Format 0 field
            pass
    return ''.join(output_str)


def full_decoding(header_and_data):
    header_info = decode_header_part(header_and_data)
    code_dict = header_info[0]
    data_text = header_info[1]
    data_decoded = decode_data_part(data_text, code_dict)
    pass
    # return data_decoded


# print(decode_data_part('00011111111010011000100100001101111', {}))
# print(full_decoding('1110000110110'))
