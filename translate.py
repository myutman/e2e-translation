import http.client
import argparse
import json
import os
import sys
import time

IAM_TOKEN = os.environ['IAM_TOKEN']
BUCKET_ID = os.environ['BUCKET_ID']
print(IAM_TOKEN)

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_dir',
        required=True,
        type=str
    )
    parser.add_argument(
        '--output_dir',
        required=True,
        type=str
    )
    return vars(parser.parse_args(sys.argv[1:]))


def split_line(line):
    return [line[0], ' '.join(line[1:])]


def make_request(payload):
    api = http.client.HTTPSConnection("translate.api.cloud.yandex.net")
    headers = {
        'content-type': "application/json",
        'authorization': f"Bearer {IAM_TOKEN}"
    }
    api.request("POST", "/translate/v2/translate", payload, headers)
    res = api.getresponse()
    data = res.read()
    data = data.decode('utf-8')
    data_json = json.loads(data)
    return data_json


def translate(input_filename, output_filename):
    with open(input_filename) as f:
        labels, texts = zip(*[(split_line(line.split(' '))) for line in f.readlines()])
        labels = list(labels)
        texts = list(texts)

    i = 0

    lines = []
    while i < len(texts):
        j = i
        sum_len = 0
        while j < len(texts) and sum_len + len(texts[j]) <= 10000:
            sum_len += len(texts[j])
            j += 1

        payload = json.dumps({"folder_id": BUCKET_ID, "targetLanguageCode": "ru", "texts": texts[i:j]})
        i = j

        data_json = make_request(payload)
        while 'translations' not in data_json.keys():
            print(data_json['message'])
            if data_json['message'] == 'limit on units was exceeded. Limit: 1000000, Interval: 1h0m0s':
                time.sleep(3600)
            data_json = make_request(payload)


        translations = data_json['translations']
        sub_lines = [x['text'] for x in translations]
        lines += sub_lines

    with open(output_filename, 'w') as ouf:
        for label, line in zip(labels, lines):
            ouf.write(f'{label} {line}')


def run(input_dir, output_dir):

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for p, d, f in os.walk(input_dir):
        output_dirpath = os.path.join(output_dir, os.path.relpath(p, input_dir))
        print(output_dirpath)
        if not os.path.exists(output_dirpath):
            os.mkdir(output_dirpath)
        for filename in f:
            if os.path.splitext(filename)[1] == '.txt':
                input_filename = os.path.join(p, filename)
                output_filename = os.path.join(output_dirpath, filename)
                if not os.path.exists(output_filename):
                    translate(input_filename, output_filename)


if __name__ == '__main__':
    run(**parse())
