import math
import random
import sys


def initial_mod(base, exponent, n):
    binary_rep = bin(exponent)[2:]
    result = 1
    for i in binary_rep:
        result = (result * result) % n
        if i == '1':
            result = (result * base) % n
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
            if prev == 1 or prev == n - 1:
                continue
            else:
                return False
    if current == 1:
        return True
    # otherwise
    return False


# print(repeated_square(2, 14, 15))
def miller_rabin(a_number, times_checked):
    if a_number % 2 == 0:
        return False
    else:
        for i in range(times_checked):
            base = random.randint(2, a_number - 1)
            keep_going = repeated_square(base, a_number - 1, a_number)
            if not keep_going:
                return False
    return True


def full_test(m):
    lower_bound = 2 ** (m - 1)
    upper_bound = (2 ** m) - 1
    if m >= 4:
        k = math.ceil(math.log(m, 4))
    else:
        k = 2
    while True:
        n = random.randint(lower_bound, upper_bound)
        if miller_rabin(n, k):
            if n - 2 >= lower_bound:
                if miller_rabin(n - 2, k):
                    return n - 2, n
            elif n + 2 <= upper_bound:
                if miller_rabin(n + 2, k):
                    return n, n + 2


def writeOutput(occurrences):
    twins = open('output_twin_prime.txt', 'w')
    twins.write(str(occurrences[0]) + '\n' + str(occurrences[1]))
    twins.close()


if __name__ == "__main__":
    m_value = int(sys.argv[1])
    output = full_test(m_value)
    writeOutput(output)
