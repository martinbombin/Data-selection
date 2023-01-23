import os
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
import sys
import time
import argparse
import itertools

parser = argparse.ArgumentParser(description='Runs Get Embeddigs')

parser.add_argument('-p', dest="path", type=str,
                    required=True,
                    help='Path to the data\n'
                         '(type: string)\n'
                         '(REQUIRED)')

parser.add_argument('-l', dest="max_length", type=int,
                    default=5000,
                    help='Max chars of sentences\n'
                         '(type: int)\n'
                         '(default: 5000)')

parser.add_argument('-t', dest="tgt_leng", type=str,
                    default=None,
                    help='Target lenguage code\n'
                         '(type: str)\n'
                         '(default: None)')

parser.add_argument('-p2', dest="path2", type=str,
                    required=True,
                    help='Path to the other data\n'
                         '(type: string)\n'
                         '(REQUIRED)')


args = parser.parse_args()

path = args.path
path2 = args.path2
max_length = args.max_length
tgt_code = args.tgt_leng

# Guardamos el nombre del fichero
flavor = path.split(".")[-2]
src_code = path.split(".")[-1]
if "/" in path:
  #print(flavor.split("/"))
  flavor = flavor.split("/")[-1]


flavor2 = path2.split(".")[-2]
src_code2 = path2.split(".")[-1]
if "/" in path2:
  #print(flavor.split("/"))
  flavor2 = flavor2.split("/")[-1]


reduced_dir = "checked_data"

try:
  os.mkdir(reduced_dir)
except:
  print(reduced_dir+" dir already exist")


# Leemos el fichero y lo guardamos en una lista
src_data = []
lon = 0
print(path)
print(flavor)
print(src_code)
with open(path, "r") as file, open(reduced_dir+"/"+flavor+"_"+str(max_length)+"."+src_code,"w") as red:

  if (tgt_code):
    with open(path.replace("."+src_code,"."+tgt_code), "r") as t_file, open(reduced_dir+"/"+flavor+"_"+str(max_length)+"."+tgt_code,"w") as t_red:
      for l, l2 in tqdm(zip(file, t_file)):
        if len(l) < max_length:
          #if l.rstrip()+l2.rstrip() not in src_data:
          src_data.append(l.rstrip()+"\n"+l2.rstrip())
          red.write(l)
          t_red.write(l2)

         # else:
          #  repeated = repeated + 1

        else:
          lon = lon +1

l_data = len(src_data)
data = set(src_data)
print("Frases finales: "+str(l_data))
print("Frases demasiado largas: "+str(lon))
print("Frases sin repetidas: "+str(len(data)))


src_data2 = []
lon = 0
print(path2)
print(flavor2)
print(src_code2)
with open(path2, "r") as file, open(path2.replace("."+src_code2,"."+tgt_code), "r") as t_file:

  if (tgt_code):
    for l, l2 in tqdm(zip(file, t_file)):
      if len(l) < max_length:
          #if l.rstrip()+l2.rstrip() not in src_data:
        src_data2.append(l.rstrip()+"\n"+l2.rstrip())
          #red.write(l)
          #t_red.write(l2)

          #else:
          #  repeated = repeated + 1

      else:
        lon = lon +1


"""
  else:
    for l in tqdm(file):
      if len(l) < max_length:
        src_data.append(l.rstrip())
        red.write(l)
"""

l_data = len(src_data2)
data2 = set(src_data2)
print("Frases finales: "+str(l_data))
print("Frases demasiado largas: "+str(lon))
print("Frases sin repetidas: "+str(len(data2)))


output_list = list(set(itertools.chain(list(data), list(data2))))
print(len(output_list))
l3 = [x for x in output_list if x not in data]
print(len(l3))

if (tgt_code):
  with open(reduced_dir+"/"+flavor2+"_"+str(max_length)+"."+src_code2,"w") as red, open(reduced_dir+"/"+flavor2+"_"+str(max_length)+"."+tgt_code,"w") as t_red:
    for l in tqdm(l3):
      red.write(l.split("\n")[0]+"\n")
      t_red.write(l.split("\n")[1]+"\n")
