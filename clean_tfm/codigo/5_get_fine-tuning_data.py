import numpy as np
import os
from tqdm import tqdm
import math
from os import listdir
from os.path import isfile, join
import sys
import argparse

MAX = 5500000

parser = argparse.ArgumentParser(description='Runs Get fine-tuning data')


parser.add_argument('-n', dest="n_sims", type=int,
                    default=10,
                    help='N higher cosine similarity values for each entry\n'
                         '(type: int)\n'
                         '(default: 10)')

parser.add_argument('-th', dest="threshold", type=float,
                    default=0.5,
                    help='Threshold of cosine similarity\n'
                         '(type: float)\n'
                         '(default: 0.5)')

parser.add_argument('-mc', dest="minimum_chars", type=int,
                    default=25,
                    help='Minimum number of chars for source sentences\n'
                         '(type: int)\n'
                         '(default: 25)')

parser.add_argument('-mxc', dest="maximum_chars", type=int,
                    default=5000,
                    help='Maximum number of chars for source sentences\n'
                         '(type: int)\n'
                         '(default: 5000)')

parser.add_argument('-src', dest="src_leng", type=str,
                    required=True,
                    help='Source lenguage code\n'
                         '(type: str)\n'
                         '(REQUIRED)')

parser.add_argument('-tgt', dest="tgt_leng", type=str,
                    required=True,
                    help='Target lenguage code\n'
                         '(type: str)\n'
                         '(REQUIRED)')

parser.add_argument('-test', dest="test", type=bool,
                    default=False,
                    help='For testing, printing results\n'
                         '(default: False)\n'
                         '(type: Boolean)'
                    )

args = parser.parse_args()

N = args.n_sims
TH = args.threshold
MIN = args.minimum_chars
MAX = args.maximum_chars

test = args.test
src_code = args.src_leng
tgt_code = args.tgt_leng


MAXTH = 0.97
MAXL = 5500000

ft_dir = "fine-tune"
try:
  os.mkdir(ft_dir)
except:
  print(ft_dir+" dir already exist")


src_data = []
tgt_data = []
reduced_dir = "reduced_database/"
src_f_data = [f for f in listdir(reduced_dir) if isfile(join(reduced_dir, f)) and "."+src_code in f][0]
tgt_f_data = [f for f in listdir(reduced_dir) if isfile(join(reduced_dir, f)) and "."+tgt_code in f][0]
with open(reduced_dir+src_f_data, "r") as s_file, open(reduced_dir+tgt_f_data, "r") as t_file:
  for s, t in tqdm(zip(s_file, t_file)):
    src_data.append(s.rstrip())
    tgt_data.append(t.rstrip())


client_data = []
client_dir = "reduced_client/"
client_f = [f for f in listdir(client_dir) if isfile(join(client_dir, f))][0]
with open(client_dir+client_f, "r") as c_file:
  for s in tqdm(c_file):
    client_data.append(s.rstrip())


findings_dir = "findings/"
onlyfiles = [f for f in listdir(findings_dir) if isfile(join(findings_dir, f))]

#used = list()
ft_data = []
start = 0
for i in range(1, int(len(onlyfiles)/2)+1):

  neig = [f for f in onlyfiles if str(i) in f and "neig" in f][0]
  dist = [f for f in onlyfiles if str(i) in f and "dist" in f][0]

  indx = np.load(findings_dir+neig)
  dist = np.load(findings_dir+dist)

  end = start + MAXL

  act_src_data = src_data[start:end]
  act_tgt_data = tgt_data[start:end]

#  j_used = []

  if test:
    for z in range(0, len(client_data)):
      bol = True
      for j in range(0, N):
        ind = indx[z][j]
#        if dist[z][j] >= TH and dist[z][j] <= MAXTH and ind not in j_used and len(act_src_data[ind])>= MIN and len(act_src_data[ind])<=MAX:
        if dist[z][j] >= TH and ind and len(act_src_data[ind])>= MIN and len(act_src_data[ind])<=MAX:
          #if (act_src_data[ind] + act_tgt_data[ind]) not in used:
          if bol:
            bol = False
            print("\nFrase del cliente:")
            print(client_data[z]+"\n")
            print("Frase(s) mas parecidas:")

          print("src: "+act_src_data[ind])
          print("tgt: "+act_tgt_data[ind])

#          used.append(act_src_data[ind] + act_tgt_data[ind])
#          j_used.append(ind)


  else:
    for j in range(0, N):
      for z in range(0, len(client_data)):
        ind = indx[z][j]
#        if dist[z][j] >= TH and dist[z][j] <= MAXTH and ind not in j_used and len(act_src_data[ind])>= MIN and len(act_src_data[ind])<=MAX:
        if dist[z][j] >= TH and ind and len(act_src_data[ind])>= MIN and len(act_src_data[ind])<=MAX:
#          if (act_src_data[ind] + act_tgt_data[ind]) not in used:
#            used.append(act_src_data[ind] + act_tgt_data[ind])
#            j_used.append(ind)
          ft_data.append(act_src_data[ind]+"#\n#"+act_tgt_data[ind])


  start = end


if not test:
  ft = set(ft_data)
  ft_src_path = 'fine-tune_'+str(N)+'_'+str(TH).replace(".",",")+'_'+str(MIN)+'_'+str(MAX)+'.'+src_code
  ft_tgt_path = 'fine-tune_'+str(N)+'_'+str(TH).replace(".",",")+'_'+str(MIN)+'_'+str(MAX)+'.'+tgt_code
  with open(ft_dir+"/"+ft_src_path, "w") as src_file, open(ft_dir+"/"+ft_tgt_path, "w") as tgt_file:
    for d in tqdm(ft):
      src_file.write(d.split("#\n#")[0]+'\n')
      tgt_file.write(d.split("#\n#")[1]+'\n')

