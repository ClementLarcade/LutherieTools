import threading as th

def even():#creating second function
    for i in range(0,20,2):
        print(i)

def odd():
    for i in range(1,20,2):
        print(i)

# creating a thread for each function
trd1 = th.Thread(target=even)
trd2 = th.Thread(target=odd)

trd1.start() # starting the thread 1 
trd2.start() # starting the thread 2

trd1.join()
trd2.join()

print('End')