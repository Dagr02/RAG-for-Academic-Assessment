from openai import OpenAI

openai_key = ""


def query_model_openai(legislative_text, academic_abstract):
    client = OpenAI(api_key=openai_key)
    system_prompt = f""""""
    user_prompt = f""" Given the academic abstract and the legislative text on dual-use items, you MUST first provide 
    a rating on a scale of 1-10. A rating of 1 means the legislative text does not at all have any direct 
    implications with the academic text, and a rating of 10 means it has a lot of direct implications. Following the 
    rating, provide a brief explanation (within 50-100 words) on how specifically the legislation relates to the 
    academic abstract, noting that 'does not relate' is a valid answer. Start your response with the scale rating 
    followed by your explanation. Academic Abstract: {academic_abstract}

    Legislative Text on dual-use items: {legislative_text}
    """
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": user_prompt}

        ]
    )

    return completion.choices[0].message.content

