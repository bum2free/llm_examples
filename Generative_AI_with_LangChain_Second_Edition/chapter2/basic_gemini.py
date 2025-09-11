from langchain_google_genai import GoogleGenerativeAI

# initialize Gemini
gemini_pro = GoogleGenerativeAI(model="gemini-2.0-flash")

response = gemini_pro.invoke("Tell me a joke about light bulbs!")
print(response)
