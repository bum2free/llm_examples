from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

template = ChatPromptTemplate.from_messages([
    ("system", "You are an English to French translator."),
    ("user", "Translate this to French: {text}")
])

chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
formatted_messages = template.format_messages(text="Hello, how are you?")
result = chat.invoke(formatted_messages)
print(result.content)