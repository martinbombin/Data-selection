import numpy as np
import os
from tqdm import tqdm
import math
from os import listdir
from os.path import isfile, join
import sys
import time
import tensorflow_hub as hub
import tensorflow_text
import tensorflow as tf
import argparse

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

parser.add_argument('-client', dest="client", type=bool,
                    default=False,
                    help='If it is client data or data to search in\n'
                         '(default: True)\n'
                         '(type: Boolean)'
                    )

args = parser.parse_args()

path = args.path
max_length = args.max_length
tgt_code = args.tgt_leng
client = args.client

MAX = 5500000

# Guardamos el nombre del fichero
flavor = path.split(".")[-2]
src_code = path.split(".")[-1]
if "/" in path:
  #print(flavor.split("/"))
  flavor = flavor.split("/")[-1]

module_url = "https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3"

model = hub.load(module_url)
print ("module %s loaded" % module_url)

reduced_dir = "reduced_database"
if client:
  reduced_dir = "reduced_client"

try:
  os.mkdir(reduced_dir)
except:
  print(reduced_dir+" dir already exist")


# Leemos el fichero y lo guardamos en una lista
src_data = []
with open(path, "r") as file, open(reduced_dir+"/"+flavor+"_"+str(max_length)+"."+src_code,"w") as red:

  if (tgt_code):
    with open(path.replace("."+src_code, "."+tgt_code), "r") as t_file, open(reduced_dir+"/"+flavor+"_"+str(max_length)+"."+tgt_code,"w") as t_red:
      for l, l2 in tqdm(zip(file, t_file)):
        if len(l) < max_length:
          src_data.append(l.rstrip())
          red.write(l)
          t_red.write(l2)

  else:
    for l in tqdm(file):
      if len(l) < max_length:
        src_data.append(l.rstrip())
        red.write(l)


l_data = len(src_data)
print(l_data)

shards_dir = "shards_database"
if client:
  shards_dir = "shards_client"

try:
  os.mkdir(shards_dir)
except:
  print(shards_dir+" dir already exist")


# Dividimos la lista para no crear un numpy array excesivamente grande en el futuro
steps = 1

if l_data > MAX:
  steps = math.ceil(l_data/MAX)

for step in range(1, steps+1):
  start = (step-1) * MAX
  end = start+MAX

  if start + MAX > l_data:
    end = l_data


  # Leemos el fichero y lo guardamos en una lista
  i = 0
  src_data = []
  with open(reduced_dir+"/"+flavor+"_"+str(max_length)+"."+src_code, "r") as file:
    for l in tqdm(file):
      if i >= start and i<end:
        src_data.append(l.rstrip())
      i = i + 1


  batch_size = 64
  n_batches = math.ceil((end-start)/batch_size)

  batched_data = []
  for b in range(n_batches):
    batch = src_data[batch_size*b:batch_size*(b+1)]
    batched_data.append(batch)

  print(len(batched_data))

  path = shards_dir+"/"+flavor+"_"+src_code+"_"+str(step)+"/"

  try:
    os.mkdir(path)
  except:
    print(path+" dir already exist")

  sentence_embeddings = []

  bi = 0
  i = bi + 1
  for b in tqdm(range(bi, len(batched_data))):

    res = []
    #with tf.device('/device:GPU:0'):
    tf.debugging.set_log_device_placement(True)
    gpus = tf.config.list_logical_devices('GPU')
    strategy = tf.distribute.MirroredStrategy(gpus)

    with strategy.scope():
    # encode corpus to get corpus embeddings
      res = model(batched_data[b])
    #res = np.array(res.cpu())

    sentence_embeddings.append(res)
    #print(b)
    #print(len(sentence_embeddings))
    if ( len(sentence_embeddings) == 10 and len(sentence_embeddings[-1]) == batch_size ):
      aux = np.array(sentence_embeddings)
      #print(aux.shape)
      #print(aux[0][0])
      #print(aux[1][0])
      aux = np.reshape(aux,[aux.shape[0]*aux.shape[1],aux.shape[2]])
      #print(aux.shape, (b+1/10))
      #print(aux[0])
      #print(aux[512])
      np.save(path+"shard_"+str(i), aux)
      i = i + 1
      sentence_embeddings = []

  if sentence_embeddings:
   aux = np.array([])
   for e in sentence_embeddings:
     if aux.size == 0:
       aux = np.array(e)
     else:
       aux = np.concatenate((aux, np.array(e)))
   print(aux.shape, b)
   np.save(path+"shard_"+str(i), aux)
   sentence_embeddings = []
