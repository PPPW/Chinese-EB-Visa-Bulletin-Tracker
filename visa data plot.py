import matplotlib.pyplot as plt
import datetime as dt

def stringToDatetime(s):
    date = s.split(',')
    return dt.datetime(int(date[0]), int(date[1]), int(date[2]))

f = open("Visa Bulletin Data.csv")

date = []
eb1 = []
eb2= []

for lines in f:
    fields = lines.strip().split('\t')
    date.append(stringToDatetime(fields[0]))
    if fields[1] == 'U':
        eb1.append(dt.datetime(2000,1,1))
    else:
        eb1.append(stringToDatetime(fields[1]))
    if fields[2] == 'U':
        eb2.append(dt.datetime(2000,1,1))
    else:
        eb2.append(stringToDatetime(fields[2]))

plt.plot(date, eb1, linestyle='solid', marker='.')
plt.plot(date, eb2, linestyle='solid', marker='.')
plt.legend(['EB1', 'EB2'], loc=2)
plt.show()

