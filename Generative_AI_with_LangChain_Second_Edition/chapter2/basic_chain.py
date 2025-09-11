from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda  # optional, or use a plain lambda

llm = GoogleGenerativeAI(model="gemini-1.5-flash")

# First chain generates a story
story_prompt = PromptTemplate.from_template("Write a short story about {topic}")
story_chain = story_prompt | llm | StrOutputParser()

# Second chain analyzes the story
analysis_prompt = PromptTemplate.from_template(
    "Analyze the following story's mood:\n{story}"
)
analysis_chain = analysis_prompt | llm | StrOutputParser()

# Combine chains
story_with_analysis = story_chain | analysis_chain
# when a PromptTemplate has exactly one input variable, you can pass a plain (non-dict) value and it will be implicitly wrapped into a dict under that single variable name.
# it actually the following:
# story_with_analysis = story_chain | RunnableLambda(lambda story: {"story": story}) | analysis_chain

# Run the combined chain
story_analysis = story_with_analysis.invoke({"topic": "a rainy day"})
print("\nAnalysis:", story_analysis)