import numpy as np
import os
from tqdm import tqdm
import math
from os import listdir
from os.path import isfile, join
import sys
import argparse
import random

MAX = 5500000

parser = argparse.ArgumentParser(description='Runs sample data')


parser.add_argument('-n', dest="n", type=int,
                    required=True,
                    help='N samples to extract\n'
                         '(type: int)\n'
                         '(REQUIRED)')

parser.add_argument('-src', dest="src", type=str,
                    required=True,
                    help='Path to source file\n'
                         '(type: str)\n'
                         '(REQUIRED)')

parser.add_argument('-tgt', dest="tgt", type=str,
                    required=True,
                    help='Path to target file\n'
                         '(type: str)\n'
                         '(REQUIRED)')

args = parser.parse_args()

N = args.n

src = args.src
tgt = args.tgt


sample_dir = "sample"
try:
  os.mkdir(sample_dir)
except:
  print(sample_dir+" dir already exist")


data = []
with open(src, "r") as s_file, open(tgt, "r") as t_file:
  for s, t in tqdm(zip(s_file, t_file)):
    data.append([s.rstrip(), t.rstrip()])
    #tgt_data.append(t.rstrip())

res = random.sample(data, N)

print(len(res))

name_s = src.split("/")[-1]
name_t = tgt.split("/")[-1]
with open(sample_dir+"/"+name_s.split(".")[0]+"_"+str(N)+"."+name_s.split(".")[1], "w") as s_file, open(sample_dir+"/"+name_t.split(".")[0]+"_"+str(N)+"."+name_t.split(".")[1], "w") as t_file:
  for s, t in res:
    s_file.write(s+'\n')
    t_file.write(t+'\n')
