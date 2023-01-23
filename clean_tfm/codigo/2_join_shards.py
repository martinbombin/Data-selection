import numpy as np
import os
from tqdm import tqdm
import math
from os import listdir
from os.path import isfile, join
import sys
import argparse

parser = argparse.ArgumentParser(description='Runs Join shards')


parser.add_argument('-client', dest="client", type=bool,
                    default=False,
                    help='If it is client data or data to search in\n'
                         '(default: True)\n'
                         '(type: Boolean)'
                    )

args = parser.parse_args()

client = args.client


dir = "embeddings_database"
dir_shards = "shards_database"
if client:
  dir = "embeddings_client"
  dir_shards = "shards_client"

try:
  os.mkdir(dir)
except:
  print(dir+" dir already exist")


paths = [x[0] for x in os.walk(dir_shards+"/")][1:]

for path in paths:
  path = path + "/"
  print(path)
  onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

  print(np.load(path+"shard_1.npy").shape)
  print(np.load(path+"shard_2.npy").shape)
  print(np.load(path+"shard_"+str(len(onlyfiles))+".npy").shape)

  array = list()
  for f in tqdm(range(1, len(onlyfiles)+1)):
    aux = np.load(path+"shard_"+str(f)+".npy")
    for l in range(0, aux.shape[0]):
      array.append(aux[l])

  array = np.array(array)
  print(array.shape)

  np.save(dir+"/"+path.split("/")[-2], array)
