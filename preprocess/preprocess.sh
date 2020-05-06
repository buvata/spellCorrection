#!/bin/sh
#python3 preprocess.py --train_src /home/taibv/Documents/Projects/spellCorrection/preprocess/data/train_data/test.txt --train_tgt /home/taibv/Documents/Projects/spellCorrection/preprocess/data/train_data/test.txt --src_vocab /home/taibv/Documents/Projects/spellCorrection/preprocess/data/new_data_train/new_spell_vocab_src.pt  --tgt_vocab /home/taibv/Documents/Projects/spellCorrection/preprocess/data/new_data_train/new_spell_vocab_src.pt --save_data data/demo/spell -shard_size 20

python3 preprocess.py --train_src data/train_data/test.txt --train_tgt data/train_data/test.txt --save_data data/new_data_train/new_spell -shard_size 20