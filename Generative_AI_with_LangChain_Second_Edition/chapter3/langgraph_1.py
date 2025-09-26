# from: https://github.com/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/langgraph_intro.ipynb
from langgraph.graph import StateGraph, START, END, Graph
from typing_extensions import TypedDict

# Note about the TypeDict:
# 1: TypedDict is a feature from Python's typing module (or typing_extensions for older Python versions) that
# allows you to define the expected keys and value types for a dictionary, enabling type checking for dict-like objects.
# 2: In Python, TypedDict is only used for static type checking (e.g., with tools like mypy or Pyright).
# It does not enforce type constraints at runtime. So for example. when modify return {"application": 123} in generate_application,
# the code will still run.
# 3: When removing the TypedDict, the code fails to run because:
# - A TypedDict allows you to create instances using dictionary-style initialization, like JobApplicationState(job_description="...", ...), or by passing a dict. 
# - After removing the inheritance from TypedDict, the class JobApplicationState is now a plain Python class, and langgraph would call the
# constructor with keyword arguments, which is not supported by default in plain classes without a custom __init__ method.
# It would get the error as "TypeError: JobApplicationState() takes no arguments"
class JobApplicationState(TypedDict):
    job_description: str
    is_suitable: bool
    application: str

def analyze_job_description(state):
    print("...Analyzing a provided job description ...")
    return {"is_suitable": len(state["job_description"]) > 100}

def generate_application(state):
    print("...generating application...")
    return {"application": "some_fake_application"}

builder = StateGraph(JobApplicationState)
builder.add_node("analyze_job_description", analyze_job_description)
builder.add_node("generate_application", generate_application)

builder.add_edge(START, "analyze_job_description")
builder.add_edge("analyze_job_description", "generate_application")
builder.add_edge("generate_application", END)

graph = builder.compile()

#png_bytes = graph.get_graph().draw_mermaid_png()
#out_path = "langgraph_1.png"
#with open(out_path, "wb") as f:
#    f.write(png_bytes)

res = graph.invoke({"job_description":"fake_jd"})
print(res) #output: {'job_description': 'fake_jd', 'is_suitable': False, 'application': 'some_fake_application'}