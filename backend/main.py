from openai import OpenAI
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

client = OpenAI()
STREAM = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Say this is a test"}],
    stream=True,
)
response = STREAM.response()
for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")