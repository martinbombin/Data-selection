import numpy as np
import os
from tqdm import tqdm
import math
from os import listdir
from os.path import isfile, join
import time
import faiss
import sys
import argparse

parser = argparse.ArgumentParser(description='Runs Faiss find on CPUs')

parser.add_argument('-n', dest="n_sims", type=int,
                    default=50,
                    help='N higher cosine similarity values for each entry\n'
                         '(type: int)\n'
                         '(default: 50)')

args = parser.parse_args()

n = args.n_sims

start_time = time.time()


embeddings_dir = "embeddings_client/"
path = [f for f in listdir(embeddings_dir) if isfile(join(embeddings_dir, f))][0]

monol_data = np.load(embeddings_dir+path)

print("\n--- %s seconds en cargar los datos ---" % (time.time() - start_time))

try:
  os.mkdir("findings")
except:
  print("findings dir already exist")


onlyfiles = [f for f in listdir("indexes/") if isfile(join("indexes/", f))]

for f in onlyfiles:

  start_time = time.time()

  index = faiss.read_index("indexes/"+f)

  distances, neighbours = index.search(monol_data, k = n)

  print("\n--- %s seconds en calcular las distancias ---" % (time.time() - start_time))

  print(neighbours.shape)
  print(neighbours)

  print("\n")

  print(distances.shape)
  print(distances)

  np.save("findings/"+f+"_neig", neighbours)
  np.save("findings/"+f+"_dist", distances)
