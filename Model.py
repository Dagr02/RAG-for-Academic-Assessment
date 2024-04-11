import nltk

nltk.download('punkt')
from gpt4all import GPT4All
from nltk.tokenize import word_tokenize
import logging

logging.basicConfig(level=logging.INFO)

# Models available
models = ["mistral-7b-instruct-v0.1.Q4_0.gguf",
          "mistral-7b-openorca.gguf2.Q4_0.gguf",
          "Nous-Hermes-2-Mistral-7B-DPO.Q4_0.gguf",
          "nous-hermes-llama2-13b.Q4_0.gguf",
          "orca-2-13b.Q4_0.gguf",
          "wizardlm-13b-v1.2.Q4_0.gguf",
          "orca-2-7b.Q4_0.gguf"
          ]

model = GPT4All('orca-mini-3b-gguf2-q4_0.gguf')


def query_model(legislative_text, academic_abstract):

    prompt = f""" 
        Given the academic abstract and the legislative text on dual-use items, you MUST first provide 
        a rating on a scale of 1-10. A rating of 1 means the legislative text does not at all have any direct 
        implications with the academic text, and a rating of 10 means it has a lot of direct implications. Following the 
        rating, provide a brief explanation (within 50-100 words) on how specifically the legislation relates to the 
        academic abstract, noting that 'does not relate' is a valid answer. Start your response with the scale rating 
        followed by your explanation. Academic Abstract: {academic_abstract}

        Legislative Text on dual-use items: {legislative_text}
        """

    print(f"User prompt tokens: {len(word_tokenize(prompt))}")
    with model.chat_session():
        response = model.generate(prompt, max_tokens=2048)

    return response
