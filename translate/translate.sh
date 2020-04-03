#!/bin/sh
#python3 translate.py --model ../train/save_model/model_step_1500.pt  --src ../preprocess/data/train_data/data_test_src.txt --output result/pred.txt  -replace_unk --verbose -batch_size 16
# perl multi-bleu.perl challenger/valid.zh < challenger/valid_pred.58.79

python3 translate.py --model ../train/save_model/model_step_2520.pt  --src ../preprocess/data/train_data/sent_src_test.txt --output result/pred.txt  -replace_unk --verbose -batch_size 16