import anthropic
from langgraph.graph import StateGraph

client = anthropic.Anthropic()

def node_user(state):
    return state

def node_claude(state):
    resp = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[{"role": "user", "content": state["prompt"]}],
    )
    # Claude returns a list of content blocks
    state["answer"] = resp.content[0].text
    return state

lg = StateGraph()
lg.add_node("user", node_user)
lg.add_node("claude", node_claude)
lg.add_edge("user", "claude")
lg.set_entrypoint("user")
lg.set_exit("claude")

pipeline = lg.compile()

if __name__ == "__main__":
    out = pipeline({"prompt": "Explain LangGraph in one paragraph."})
    print(out["answer"])