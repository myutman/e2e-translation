import json
import os
import urllib.request

from tqdm import tqdm


from remove_commas import remove_commas_line


def download_list(input_file: str, output_dir: str, max_size: int, domain: str):
    with open(input_file) as f:
        records = json.load(f)

    references_filename = os.path.join(output_dir, 'references' + os.extsep + 'txt')
    with open(references_filename, 'w') as f:
        pass

    for record in tqdm(records[:max_size]):
        text: str = record["orig_ru_norm_text"]
        record_id: str = record["record_id"]

        url = os.path.join(domain, record_id + os.extsep + 'wav')
        response = urllib.request.urlopen(url)
        data = response.read()

        output_path = os.path.join(output_dir, record_id + os.extsep + 'wav')
        with open(output_path, 'wb') as f:
            f.write(data)

        with open(references_filename, 'a') as f:
            f.write(f'{record_id} {remove_commas_line(text.upper())}\n')
