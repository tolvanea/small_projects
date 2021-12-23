c = """c = QQQ{}QQQ
s1 = c.replace(chr(81), chr(34))
s2 = s1.format(c)
print(s2)"""
s1 = c.replace(chr(81), chr(34))
s2 = s1.format(c)
print(s2)
