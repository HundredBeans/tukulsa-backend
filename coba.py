import string
import random
import datetime
from datetime import timedelta

res = session.query(Object).filter(Object.created_date+timedelta(days=1))>datetime.now()
print(res)
# def randomcode(size=6, char=string.digits):
#     print(''.join(random.choice(char) for _ in range(0,size)))

# randomcode()

# print(datetime.datetime.now()+datetime.timedelta(days=5))