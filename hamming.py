# This is miniman working example of Hamming error correction.
# It can fix one bit flip error and it can alert two bit flips.
import numpy as np
power = 6                           # Determines block size
num_bits = 2**power                 # 2^6=64 bits transmitted
message_len = num_bits - power - 1  # 57 bits for message

def main():
    # Create a random binary message, e.g. [1,0,0,1,1,1,0...]
    message = np.random.randint(2, size=message_len)
    # Wrap it with error correction adding few extra bits
    wrapped = add_degenerancy(message)
    # Uh oh, bit flip occured at index 25
    wrapped[25] = 1 - wrapped[25]
    # Construction of original message
    message_received = error_correct(wrapped)
    assert(np.all(message == message_received))

def xor_sum_of_indices(bits):  # The magic of this algorithm
    acc = 0
    for i, bit in enumerate(bits):
        if bit == 1:
            acc = acc ^ i
    return acc  # Return number costructed with xor-ing

def map_idx(i):  # From 'wrapped' index to 'message' index
    if i == 0 or np.isclose(np.log2(i)%1.0, 0.0):
        return None  # power of two indices are reserved
    else:
        return i - int(np.log2(i)) - 2

def add_degenerancy(message):
    wrapped = np.zeros(num_bits, dtype=np.int_)
    for i in range(num_bits):
        idx = map_idx(i)  # skip every 2**i:th index
        if idx is not None:
            wrapped[i] = message[idx]
    xor_sum = xor_sum_of_indices(wrapped)  # e.g. 6
    xor_bits = np.binary_repr(xor_sum)     # e.g. "110"
    for p, bit in enumerate(reversed(xor_bits)):
        wrapped[2**p] = int(bit)
    wrapped[0] = wrapped.sum() % 2  # Additional parity check
    return wrapped

def error_correct(wrapped):
    idx = xor_sum_of_indices(wrapped)
    correct_parity = (wrapped.sum() % 2 == 0)
    wrapped_fixed = wrapped.copy()
    if (idx != 0) and correct_parity:
        raise Exception("Assert, two bit flips encountered!")
    elif not correct_parity:
        print("Detected and fixed bit flip at idx = ", idx)
        wrapped_fixed[idx] = 1 - wrapped[idx]  # fix it
    message = np.zeros(message_len, dtype=np.int_)
    for i, bit in enumerate(wrapped_fixed):
        idx = map_idx(i)
        if idx is not None:
            message[idx] = bit
    return message

main()
