import string
import random
import datetime
from datetime import timedelta

# res = session.query(Object).filter(Object.created_date+timedelta(days=1))>datetime.now()
# print(res)
# def randomcode(size=6, char=string.digits):
#     print(''.join(random.choice(char) for _ in range(0,size)))

# randomcode()

# print(datetime.datetime.now()+datetime.timedelta(days=5))
x=[datetime.datetime.now(),datetime.datetime.now()+datetime.timedelta(days=5), datetime.datetime.now()+datetime.timedelta(days=8)]
for i in x:
    print("KAKA", i.strftime('%d'))
    if  i.strftime('%d')=="14":
        print("mantap")
        print(i.strftime('%Y'))
        print(i.strftime('%m'))
        print(i.strftime('%d'))
    else:
        pass
    
