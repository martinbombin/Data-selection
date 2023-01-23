# data-seletcion

Example of use:

python /home/m.barroso/clean_tfm/codigo/1_get_embeddings.py -p /home/m.barroso/clean_tfm/data/clean/TAUS_clean.en -t es

python /home/m.barroso/clean_tfm/codigo/1_get_embeddings.py -p /home/m.barroso/clean_tfm/data/clean/EMEA_clean.en -client True

python /home/m.barroso/clean_tfm/codigo/2_join_shards.py

python /home/m.barroso/clean_tfm/codigo/2_join_shards.py -client True

python /home/m.barroso/clean_tfm/codigo/3_faiss_index_data.py

python /home/m.barroso/clean_tfm/codigo/4_faiss_find_ind.py -n 25

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 1 -th 0.9 -mc 0 -mxc 5000 -src en -tgt es -test True

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 1 -th 0.7 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 3 -th 0.7 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 10 -th 0.7 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 25 -th 0.7 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 1 -th 0.6 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 3 -th 0.6 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 10 -th 0.6 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 25 -th 0.6 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 1 -th 0.5 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 3 -th 0.5 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 10 -th 0.5 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 25 -th 0.5 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 1 -th 0.4 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 3 -th 0.4 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 10 -th 0.4 -mc 0 -mxc 5000 -src en -tgt es

python /home/m.barroso/clean_tfm/codigo/5_get_fine-tuning_data.py -n 25 -th 0.4 -mc 0 -mxc 5000 -src en -tgt es
