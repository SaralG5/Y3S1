def initial_mod(base, exponent, n):
    binary_rep = bin(exponent)[2:]
    result = 1
    for i in binary_rep:
        if i == '1':
            result = (result * base) % n
        else:
            result = (result * result) % n
    return result


def two_power_form(even_number):
    """
    This function takes an even number and essentially writes it in the form 2^s x k where k is an odd integer
    :param even_number: an even integer
    :return: this function will output s and k
    """
    # Pseudocode
    # Step 1: Initialise s = 0
    # Step 2: Get the even number and divide by 2
    # Step 3: if it divides then increment s by 1
    #           otherwise go to step 5
    # Step 4: If  the result is divisible 2, then repeat Step 3.
    # Step 5: Output s and k = result.
    # ACTUAL CODE NOW
    s = 0  # Initialise list as empty Step 1
    while True:
        if even_number % 2 == 0:
            even_number = even_number / 2
            s += 1
        else:
            return s, int(even_number)


def repeated_square(base, exponent, n):
    # first write the exponent in the form 2^s x k where k is an odd integer.
    # Now the first step here is to compute base ^ k mod n, and this could be huge
    # So we will calculate this in the function initial_mod
    s, k = two_power_form(exponent)
    current = initial_mod(base, k, n)
    for i in range(s):
        prev = current
        current = (current * current) % n
        if current == 1:
            if prev != 1 or prev != n - 1:
                return False
    if current != 1:
        return False
    # otherwise
    return True


print(repeated_square(2, 14, 15))
