import numpy as np
import os
from tqdm import tqdm
import math
from os import listdir
from os.path import isfile, join
import time
import faiss
import sys

dir = "embeddings_database/"

try:
  os.mkdir("indexes")
except:
  print("indexes dir already exist")


onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]

#onlyfiles = [f for f in onlyfiles if flavor in f]

for f in onlyfiles:

  tm_path = dir+f

  start_time = time.time()

  tm = np.load(tm_path)
  print("\nloaded\n")

  print("\n--- %s seconds en cargar datos ---" % (time.time() - start_time))

  print(tm.shape)

  start_time = time.time()

  vector_dim = 512
  index = faiss.IndexFlatIP(vector_dim)
  faiss.normalize_L2(tm)
  index.add(tm)

  faiss.write_index(index, "indexes/"+f.split(".")[-2]+"_ind")

  print("\n--- %s seconds en crear los indices ---" % (time.time() - start_time))

  start_time = time.time()
