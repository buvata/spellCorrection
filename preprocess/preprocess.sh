#!/bin/sh
#python3 preprocess.py --train_src data/train_data/data_train_src.txt --train_tgt data/train_data/data_train_des_piece.txt --src_vocab data/demo/vocab_tts_tai_src.pt  --tgt_vocab data/demo/vocab_tts_tai_tgt.pt --save_data data/demo/tts

python3 preprocess.py --train_src data/train_data/test.txt --train_tgt data/train_data/test.txt --save_data data/new_data_train/new_spell -shard_size 2