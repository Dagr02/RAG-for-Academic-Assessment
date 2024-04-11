from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import MatrixSimilarity
from Model import query_model  # using local models
from OpenAIModel import query_model_openai  # using openai model
from Util import get_file_paths
import json
import os


#not needed
def preprocess(text):  # removing stopwords
    return [word for word in simple_preprocess(text, deacc=True) if word not in STOPWORDS]


documents = []

# get our processed chunks <500 tokens
texts = get_file_paths('./ProcessedData')

for text in texts:
    with open(text, 'r', encoding='utf-8') as f:
        content = f.read()
        documents.append(content)

# load our abstracts
path = './Abstracts/abstracts.json'
with open(path, 'r', encoding='utf-8') as file:
    data = json.load(file)

if len(documents) == 0:
    print("No documents")
    exit()

# gensim preprocess => removes whitespace etc.
processed_docs = [preprocess(doc) for doc in documents]
dictionary = Dictionary(processed_docs)

# initialize indexing models
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
tfidf = TfidfModel(bow_corpus)
corpus_tfidf = tfidf[bow_corpus]

similarity_index = MatrixSimilarity(corpus_tfidf, num_features=len(dictionary))

# data is academic abstracts loaded in json file format
for obj in data:
    try:
        # query doc for sim search
        query_document = obj['text']

        query_bow = dictionary.doc2bow(preprocess(query_document))
        query_tfidf = tfidf[query_bow]

        # search
        sims = similarity_index[query_tfidf]

        # sort by best and get top 5
        sorted_sims = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
        top_sims = sorted_sims[:5]

        for index, legislative_text in enumerate(top_sims):
            document_number, score = legislative_text
            response = query_model_openai(documents[document_number], query_document)

            #sim in %
            percentage_score = round(score * 100, 2)

            print(f"Document: {documents[document_number]}\nScore: {percentage_score:.2f}%\n")
            print(f"Response: {response}")

            if not os.path.isdir('Results'):
                os.makedirs('Results')

            filepath = "./Results"
            filename = f"{filepath}/{obj['title']}_{index}.txt"

            # formatting to file
            text = "\n\n".join(
                [obj['title'], obj['ref'], obj['text'], documents[document_number], str(percentage_score), response])

            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text.strip())

    except TypeError as e:
        print(f'Error has occurred: {e}')
        print(f"{obj['text']}")
