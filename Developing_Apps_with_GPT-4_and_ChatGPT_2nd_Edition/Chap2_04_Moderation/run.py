#from dotenv import load_dotenv
#load_dotenv()
from openai import OpenAI

client = OpenAI()

# Call the openai Moderation endpoint, with the text-moderation-latest model
# The book originally use text-moderation-latest
response = client.moderations.create(model="omni-moderation-2024-09-26",
input="I want to kill my neighbor.")

# Extract the response
print(response)
