n, q = chr(10), chr(34)  # newline, quote
l1 = "n, q = chr(10), chr(34)  # newline, quote"
l4 = "print(l1, 'l1 = ' + q + l1, 'l4 = ', q + l4, l4, sep=q+n)"
print(l1, 'l1 = ' + q + l1, 'l4 = '+ q + l4, l4, sep=q+n)
