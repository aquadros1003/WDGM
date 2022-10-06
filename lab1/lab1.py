import numpy as np

def line():
    print("\n ----------------------------------------------------- \n")

#1
arr1=np.ones(50)*5
print(arr1)
line()

#2
arr2 = np.arange(1,26).reshape(5, 5)
print(arr2)
line()

#3
arr3 = np.linspace(10, 50, 21)
print(arr3)
line()

#4
arr4 = np.eye(5) * 8
print(arr4)
line()

#5
arr5 =  np.linspace(1, 1.99, 100).reshape(10,10)
print(arr5)
line()

#6
arr6 = np.linspace(0, 1, 50)
print(arr6)
line()

#7
arr7 = arr2[2:5,1:] 
print(arr7)
line()

#8
arr8 = arr2[:3,4].reshape(3, 1)
print(arr8)
line()

#9
arr8 = arr2[-2:, :].sum()
print(arr8)
line()

#10
dim = np.random.randint(100)
size = np.random.randint(100)
arr10 = np.random.randint(0, 100, (dim, size))
print(arr10)
line()

