import re
from nltk.tokenize import word_tokenize
from os import walk
from pathlib import Path

files = []


def get_files_names(path):
    directories = []
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend(filenames)
        directories.extend(dirnames)
        break

    if directories is not None:
        for dirname in directories:
            get_files_names(path + "\\" + dirname)

    return files


def count_tokens_files(path, fileNames):
    file_tokens = []
    for file in fileNames:
        if not 'article' in file:
            filepath = f'{path}/{file}'
            with open(filepath, 'r', encoding="utf-8") as f:
                text = f.read()
                file_tokens.append((file, len(word_tokenize(text))))

        else:
            filepath = f'{path}/outputArticles/{file}'
            with open(filepath, 'r', encoding="utf-8") as f:
                text = f.read()
                file_tokens.append((file, len(word_tokenize(text))))

    return file_tokens


def count_tokens_file(path, fileName):
    tokens = 0
    if 'category' in fileName:
        filepath = f'{path}/{fileName}'
        with open(filepath, 'r', encoding="utf-8") as f:
            text = f.read()
            tokens = len(word_tokenize(text))
    else:
        filepath = f'{path}/outputArticles/{fileName}'
        with open(filepath, 'r', encoding="utf-8") as f:
            text = f.read()
            tokens = len(word_tokenize(text))
    return tokens


def write_tokens_to_file(file_tokens, nameOfFile):
    with open(nameOfFile, 'w', encoding='utf-8') as file:
        for fileName, fileTokens in file_tokens:
            file.write(f'"{fileName}","{fileTokens}"\n')


# Accept tuple
def return_files_above_token_count(file_tokens, min_token_count):
    filtered_files = [file_token for file_token in file_tokens if file_token[1] > min_token_count]
    return filtered_files


def return_files_below_token_count(file_tokens, max_token_count):
    filtered_files = [file_token for file_token in file_tokens if max_token_count > file_token[1]]
    return filtered_files


def read_text_from_file(filePath):
    with open(filePath, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


# better way to return all .txt files in dir and sub dirs
def get_file_paths(path):
    path_obj = Path(path)
    txt_files = list(path_obj.rglob('*.txt'))

    return txt_files


# better way to return tuple of path and tokens
def get_file_tokens(file_paths):
    path_and_tokens = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            path_and_tokens.append((file_path, len(word_tokenize(text))))

    return path_and_tokens


def simple_word_tokenize(text):
    # Split based on whitespace and remove punctuation
    return re.findall(r'\b\w+\b', text.lower())


# Found from:
# https://www.reddit.com/r/ChatGPT/comments/11wtxyg/comment/jczuavr/?utm_source=reddit&utm_medium=web2x&context=3
def split_file(in_file_path, max_tokens):
    print(f"Processing {in_file_path}")
    with open(in_file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    sentence_boundary_pattern = re.compile(r'(?<=[.!?])\s+(?=[^\d])')
    sentence_boundaries = [(m.start(), m.end()) for m in re.finditer(sentence_boundary_pattern, text)]

    chunks = []
    current_chunk = []
    current_token_count = 0
    current_position = 0

    for boundary_start, boundary_end in sentence_boundaries:
        sentence = text[current_position:boundary_start + 1]
        current_position = boundary_end

        token_count = len(simple_word_tokenize(sentence))

        if current_token_count + token_count <= max_tokens:
            current_chunk.append(sentence)
            current_token_count += token_count
        else:
            chunks.append(''.join(current_chunk))
            current_chunk = [sentence]
            current_token_count = token_count

    print(f'Current token count: {current_token_count}')
    # Append the last sentence
    last_sentence = text[current_position:]
    current_chunk.append(last_sentence)
    chunks.append(''.join(current_chunk))
    print(f'Chunk length: {len(chunks) - 1}')
    return chunks
