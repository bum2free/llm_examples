
# from: https://github.com/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/output_parsers.ipynb

from langchain_google_genai import GoogleGenerativeAI
from enum import Enum
from langchain.output_parsers import EnumOutputParser
from langchain_core.messages import HumanMessage

llm = GoogleGenerativeAI(model="gemini-2.0-flash")

# load job_description from file "example_jd.txt" in the same directory
# get the path of the current file
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
# construct the path to the example_jd.txt file
with open(os.path.join(current_dir, "example_jd.txt"), "r") as f:
    job_description = f.read()

# a dummy test
'''
prompt_template  = (
    "Given a job description, decide whether it suites a junior Java developer."
    "\nJOB DESCRIPTION:\n{job_description}\n"
)
result = llm.invoke(prompt_template.format(job_description=job_description))
print(result)
'''

class IsSuitableJobEnum(Enum):
    YES = "YES"
    NO = "NO"

parser = EnumOutputParser(enum=IsSuitableJobEnum)

# parser dummy tests
'''
assert parser.invoke("NO") == IsSuitableJobEnum.NO
assert parser.invoke("YES\n") == IsSuitableJobEnum.YES
assert parser.invoke(" YES \n") == IsSuitableJobEnum.YES
assert parser.invoke(HumanMessage(content=" YES \n")) == IsSuitableJobEnum.YES
'''
prompt_template_enum = (
    "Given a job description, decide whether it suites a junior Java developer."
    "\nJOB DESCRIPTION:\n{job_description}\n\nAnswer only YES or NO."
)

# llm and parser test
'''
chain = llm | parser
result = chain.invoke(prompt_template_enum.format(job_description=job_description))
print(result) # this print: IsSuitableJobEnum.NO
'''


from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class JobApplicationState(TypedDict):
    job_description: str
    is_suitable: IsSuitableJobEnum
    application: str

analyze_chain = llm | parser


def analyze_job_description(state):
    job_description = state["job_description"]
    prompt = prompt_template_enum.format(job_description=job_description)
    result = analyze_chain.invoke(prompt)
    return {"is_suitable": result}


def is_suitable_condition(state: JobApplicationState):
    return state["is_suitable"] == IsSuitableJobEnum.YES


def generate_application(state):
    print("...generating application...")
    return {"application": "some_fake_application", "actions": ["action2"]}


builder = StateGraph(JobApplicationState)
builder.add_node("analyze_job_description", analyze_job_description)
builder.add_node("generate_application", generate_application)
builder.add_edge(START, "analyze_job_description")
builder.add_conditional_edges(
    "analyze_job_description", is_suitable_condition,
     {True: "generate_application", False: END})
builder.add_edge("generate_application", END)

graph = builder.compile()

res = graph.invoke({"job_description": job_description})
print(res)

# got the following result:
'''
{'job_description': 'SPS-Software Engineer......', 'is_suitable': <IsSuitableJobEnum.NO: 'NO'>}
'''