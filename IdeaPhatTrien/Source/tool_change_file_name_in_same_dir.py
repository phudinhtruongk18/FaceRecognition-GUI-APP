from os import walk
import os

name = "YenNhu"
_, _, filenames = next(walk(os.curdir))
print(name.__len__())
for temp in filenames:
    indexBatDau = temp.find(name)
    if indexBatDau > 0:
        tenthaythe = temp.replace(name,"ARAM025")
        os.rename(temp,tenthaythe)
    print(temp)

print("Done")
