from openai import OpenAI
 
# pip install openai 
# if you saved the key under a different environment variable name, you can do something like:
client = OpenAI(
  api_key="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",
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)