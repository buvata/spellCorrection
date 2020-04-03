from onmt.translate.translator import Translator, build_translator
from flask import Flask
from flask import request, jsonify
from flask_restful import Api
import os
from handle_text import *
from urllib.parse import unquote


class Namespace():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def create_tmp_file(text):
    with open("text_input.tmp", "w") as wf:
        wf.write(text)


opt = Namespace(alpha=0.0, attn_debug=False, avg_raw_probs=False, batch_size=1, beam_size=5, beta=-0.0,
                block_ngram_repeat=0, config=None, coverage_penalty='none', data_type='text', dump_beam='',
                dynamic_dict=False, fp32=False, gpu=-1, ignore_when_blocking=[], image_channel_size=3,
                length_penalty='none', log_file='', log_file_level='0', max_length=350, max_sent_length=350,
                min_length=0, models=['/home/taibv/Documents/Projects/spellCorection/train/save_model/model_step_10.pt'],
                n_best=1, output='pred.txt', phrase_table='', random_sampling_temp=1.0, random_sampling_topk=1, ratio=-0.0,
                replace_unk=True, report_bleu=False, report_rouge=False, report_time=False, sample_rate=16000,
                save_config=None, seed=829, shard_size=10000, share_vocab=False, src='/home/taibv/Documents/Projects/spellCorection/vocab/test_input.tmp',
                src_dir='', stepwise_penalty=False, tgt=None, verbose=True)

translator = build_translator(opt)


def read_data_from_file(path_file):
    list_sent = []
    with open(path_file, "r") as rf:
        for e_line in rf.readlines():
            e_line = format_input(e_line)
            list_sent.append(e_line)
    return list_sent


def normalize_spell_output(data):
    if not os.path.isfile(data):
        if isinstance(data, list):
            list_sent = data
        else:
            list_sent = [data]
    else:
        list_sent = read_data_from_file(data)
    # data = norm_other_data_format(data)

    list_sent_norm = []
    for e_sent in list_sent:
        create_tmp_file(e_sent)
        output_translator = translator.translate(src="text_input.tmp", batch_size=1)
        # print(output_translator)
        output_after_norm = format_output(output_translator[1][0][0])
        print(output_after_norm)
        list_sent_norm.append(output_after_norm)

    return '\n'.join(list_sent_norm)


app = Flask(__name__)
api = Api(app)


@app.route("/", methods=['GET','POST'])
def handle_normalize_output_request():

    content_request = request.get_json()
    print(content_request)
    link_file_data = content_request['sentence']

    print(link_file_data)

    output_norm = normalize_spell_output(link_file_data)
    return output_norm


if __name__ == '__main__':
    # s = 'hôm nay toif di rất vui, gặp 37 bạn mới nhiễm covid-19 cách ly.'
    # print(format_input(s))
    app.run(host="0.0.0.0", port="8000", debug=True)