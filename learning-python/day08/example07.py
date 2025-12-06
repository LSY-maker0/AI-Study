import random
import string

allchars=string.digits+string.ascii_letters
print(allchars)

select_chars=random.choices(allchars,k=8)
print(select_chars)

