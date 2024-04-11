import os
import shutil

from Util import return_files_above_token_count, get_file_paths, get_file_tokens, split_file, \
    return_files_below_token_count

# Should move to util.py

text_files_paths = get_file_paths('./extracted_texts')
files_and_tokens = get_file_tokens(text_files_paths)
files_above_token_max = return_files_above_token_count(files_and_tokens, 500)
files_below_token_max = return_files_below_token_count(files_and_tokens, 500)

if not os.path.isdir('ProcessedData'):
    os.makedirs('ProcessedData')

for file in files_below_token_max:  # copy pre-existing < 500 token files to output dir
    shutil.copy(file[0], './ProcessedData')

for fileIndex, file in enumerate(files_above_token_max):
    chunks = split_file(file[0], 500)

    for i, chunk in enumerate(chunks):
        filename = f'ProcessedData/file_{fileIndex}_chunk_{i}.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(chunk)
