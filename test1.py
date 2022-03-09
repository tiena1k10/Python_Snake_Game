f = open('data.txt', 'w')
a = str(10)
f.write(a)
f.close()
f = open('data.txt', 'r')
a = int(f.read())
print(a+1)
f.close()

z = [[1,2],[2,2]]


x = z[0]
y = z[1]

