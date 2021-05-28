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
    if a_rep == '1':
        return 1     # 0 , 1
    start = 0
    str_length = len(a_rep)
    end = 0
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
    return int(answer, 2)

def test_elias_decode(an_integer):
    # bin_rep = bin(an_integer)[2:]
    encoding = elias(an_integer)
    value = decode_elias(encoding)
    return value == an_integer

print(decode_elias('011110000111110001001000110001101001'))