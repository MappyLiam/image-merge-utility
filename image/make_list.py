import os
import random
import glob
from os import getcwd

current_dir = getcwd()

file_train = open('target.txt', 'w')
file_train2 = open('target2.txt', 'w')
####Process
list = []
for f_path in glob.iglob(os.path.join(current_dir, "*.png")):
    title, ext = os.path.splitext(os.path.basename(f_path))
    list.append(title)

while list:
    name = random.choice(list)
    print(name)
    file_train.write("{0}/{1}.png\n".format(current_dir.replace('\\','/'), name))
    file_train2.write("{0}/{1}.txt\n".format(current_dir.replace('\\','/'), name))
    list.remove(name)

file_train.close()
file_train2.close()


