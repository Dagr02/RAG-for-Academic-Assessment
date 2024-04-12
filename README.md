# RAG For Academic Assessment

## Getting started
1) Open the source code in an IDE. 
2) Install required packages:

pip install BeautifulSoup4

pip install html2text (if wanting to use the regex + md data extraction)

pip install gensim

pip install --upgrade openai

pip install gpt4all

pip install nltk

### The intended workflow:
- Make sure the legislative document is present in the project root directory
- Run one of the extract scripts
- Run splitfiles script
- Run Doc2Vec.py, here you can specify if you wish to use a local LLM or OpenAI model(needs an api key) by changing this line in Doc2Vec:

response = query_model_openai(documents[document_number], query_document) ## OpenAI model
to
response = query_model(documents[document_number], query_document) ## local LLM

In each: Model.py or OpenAIModel.py you can configure which model to run.
	- For OpenAIModel.py: modify model="", their models can be found online in their documentation
	- For local LLM, models3.json is the entire corpus of models available from GPT-4-ALL. 
		- On selection of model, if it doesn't exist then it will be downloaded.


