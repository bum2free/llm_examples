from langgraph.graph import StateGraph, START, END, Graph
from typing_extensions import TypedDict
from typing import Literal

class JobApplicationState(TypedDict):
    job_description: str
    is_suitable: bool
    application: str

def analyze_job_description(state):
    print("...Analyzing a provided job description ...")
    return {"is_suitable": len(state["job_description"]) > 1}

def generate_application(state):
    print("...generating application...")
    return {"application": "some_fake_application"}

builder = StateGraph(JobApplicationState)
builder.add_node("analyze_job_description", analyze_job_description)
builder.add_node("generate_application", generate_application)

# The type checking for Literal types (and Python type hints in general) is done by static type checkers, not by Python itself at runtime
# 
def is_suitable_condition(state: JobApplicationState) -> Literal["generate_application", END]:
    if state.get("is_suitable"):
        return "generate_application"
    return END

builder.add_edge(START, "analyze_job_description")
builder.add_conditional_edges("analyze_job_description", is_suitable_condition)
builder.add_edge("generate_application", END)

graph = builder.compile()

#png_bytes = graph.get_graph().draw_mermaid_png()
#out_path = "langgraph_2_condition.png"
#with open(out_path, "wb") as f:
#    f.write(png_bytes)

res = graph.invoke({"job_description":"fake_jd"})
print(res)