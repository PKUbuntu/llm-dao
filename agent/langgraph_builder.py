from typing import Annotated

from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from utils.trace import config

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)


# llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")
llm = init_chat_model("ollama:qwen3", base_url="http://127.0.0.1:11434")

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile().with_config(config=config)


from IPython.display import Image, display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass

def stream_graph_updates(u_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": u_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break

# ----------------- Memory -----------------

from langgraph.checkpoint.memory import InMemorySaver

memory = InMemorySaver()

# 构建
graph = graph_builder.compile(checkpointer=memory).with_config(config=config)

# session 配置
config = {"configurable": {"thread_id": 1}}

user_input = "Hi there! My name is Will."

# The config is the **second positional argument** to stream() or invoke()!
events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()

# ask related question
user_input = "Remember my name?"

# The config is the **second positional argument** to stream() or invoke()!
events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config,
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()

config_2 = {"configurable": {"thread_id": 2}}

events = graph.stream(
    {"messages": [{"role": "user", "content": user_input}]},
    config_2,
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()

# snapshot 这里作为history的存储存在
snapshot = graph.get_state(config)
print(snapshot)

"""
StateSnapshot(values={'messages': [HumanMessage(content='Hi there! My name is Will.', additional_kwargs={}, response_metadata={}, id='98600c60-c613-4d74-a9b4-fc5b9d2262f8'), AIMessage(content="<think>\nOkay, the user introduced themselves as Will. I should respond in a friendly and welcoming manner. Let me make sure to acknowledge their name and express enthusiasm to chat. Maybe add a question or two to keep the conversation going. Keep the tone casual and approachable. Let me check for any typos and ensure the response flows naturally.\n</think>\n\nHi Will! Nice to meet you! 😊 How are you doing today? What's on your mind? I'm here to chat and help out whenever you need!", additional_kwargs={}, response_metadata={'model': 'qwen3', 'created_at': '2025-08-22T08:50:34.4207758Z', 'done': True, 'done_reason': 'stop', 'total_duration': 11622790500, 'load_duration': 37557500, 'prompt_eval_count': 16, 'prompt_eval_duration': 384748100, 'eval_count': 106, 'eval_duration': 11199977800, 'model_name': 'qwen3'}, id='run--06a36e05-def0-4acd-820b-fe681412eb12-0', usage_metadata={'input_tokens': 16, 'output_tokens': 106, 'total_tokens': 122}), HumanMessage(content='Remember my name?', additional_kwargs={}, response_metadata={}, id='25d32143-e6d5-491a-b7e5-0c7a1760089c'), AIMessage(content='<think>\nOkay, the user asked, "Remember my name?" Let me check the conversation history. The user introduced themselves as Will earlier. I should confirm that I remember their name and maybe express enthusiasm about it. I should keep the tone friendly and open for further conversation. Let me make sure to use their name and invite them to share more if they\'re comfortable. Also, keep the response concise and warm.\n</think>\n\nOf course I remember your name, Will! 😊 It’s always great to see you again. How are you doing today? I’d love to hear what’s on your mind!', additional_kwargs={}, response_metadata={'model': 'qwen3', 'created_at': '2025-08-22T08:50:48.0996409Z', 'done': True, 'done_reason': 'stop', 'total_duration': 13673449600, 'load_duration': 32301100, 'prompt_eval_count': 64, 'prompt_eval_duration': 357496000, 'eval_count': 123, 'eval_duration': 13282626700, 'model_name': 'qwen3'}, id='run--2ace913a-ca7f-402f-aed4-978816274bbe-0', usage_metadata={'input_tokens': 64, 'output_tokens': 123, 'total_tokens': 187})]}, next=(), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f07f351-92f4-66d3-8004-120a0b1bc49b'}}, metadata={'source': 'loop', 'step': 4, 'parents': {}}, created_at='2025-08-22T08:50:48.100833+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f07f351-1085-6460-8003-1f15f268e85c'}}, tasks=(), interrupts=())
"""
