from queue import Queue


q = Queue(maxsize=3)

max = 10

for i in range(10):
    if not q.full():
        q.put(i)
    else:
        q.get()
        q.put(i)

for i in range(q.maxsize):
    if not q.empty():
        print(q.get())