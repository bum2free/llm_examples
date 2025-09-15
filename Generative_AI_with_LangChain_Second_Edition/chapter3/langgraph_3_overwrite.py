# from: https://github.com/benman1/generative_ai_with_langchain/blob/second_edition/chapter3/langgraph_intro.ipynb

from langgraph.graph import StateGraph, START, END, Graph
from typing_extensions import TypedDict
from typing import Literal

class JobApplicationState(TypedDict):
    job_description: str
    is_suitable: bool
    application: str
    actions: list[str]

def analyze_job_description(state):
    print("...Analyzing a provided job description ...")
    result = {
        "is_suitable": len(state["job_description"]) < 100,
        "actions": ["action1"]}
    return result

def generate_application(state):
    print("...generating application...")
    return {"application": "some_fake_application", "actions": ["action2"]}



builder = StateGraph(JobApplicationState)
builder.add_node("analyze_job_description", analyze_job_description)
builder.add_node("generate_application", generate_application)
builder.add_edge(START, "analyze_job_description")
builder.add_edge("analyze_job_description", "generate_application")
builder.add_edge("generate_application", END)

graph = builder.compile()

#png_bytes = graph.get_graph().draw_mermaid_png()
#out_path = "langgraph_3.png"
#with open(out_path, "wb") as f:
#    f.write(png_bytes)

#res = graph.invoke({"job_description":"fake_jd"})
#print(res)

import asyncio

async def main():
    # Streaming just the values of state as they change
    async for chunk in graph.astream(
        {"job_description": "fake_jd"},
        stream_mode="values"
    ):
        print("Stream chunk:", chunk)
        print()

if __name__ == "__main__":
    asyncio.run(main())