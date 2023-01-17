# import re
# import datetime
# dat = datetime.date(2022,12,5)
# dat.timetuple()
# print(dat.timetuple())
#
# print()
# mass = [None]*7
# for i in range(1,32):
#     try:
#         dat = datetime.date(2023, 2, i)
#     except:
#         print(mass[0],mass[1],mass[2],mass[3],mass[4],mass[5],mass[6])
#         break
#     inf = dat.timetuple()
#     mass[inf.tm_wday] = i
#     if inf.tm_wday == 6:
#         print(mass[0], mass[1], mass[2], mass[3], mass[4], mass[5], mass[6])
#         mass = [None] * 7
# else:
#     print(mass[0], mass[1], mass[2], mass[3], mass[4], mass[5], mass[6])
#
#
# # for i in range(1,32):
#
# # for i in range(1,32):
# #     try:
# #
# #     except ValueError:
# #         pass
# # print(dat.timetuple())
# # print(dat + datetime.timedelta(days = 1))
# # print("yes" if a else "No")
# # if re.(r"\d\d\.\d\d\.\d\d",s) == []:
# #     print("")

#
# import json
#
# with open("mgou.json","r") as f:
#     val = json.load(f)
#     print(val)

# def f(st):
#     for i in range(st,(lambda x: x+3 if (st+3)<13 else 13)):
#         print(i)
# for i in range(0,11,3):
#     f(i)

from progress.bar import IncrementalBar
from time import sleep
a = [1,2,3,4,5,6,7,8]
bar = IncrementalBar('Countdown', max=len(a))
print(bar)
for i in a:
    bar.next()
    sleep(1)
bar.finish()


