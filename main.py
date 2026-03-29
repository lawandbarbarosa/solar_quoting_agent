import os

from dotenv import load_dotenv

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

from typing import TypedDict, Optional


class AgentState(TypedDict):
     """Shared state that flows through all nodes in the graph."""

     Location: str
     monthly_bill: int
     roof_type: list[str]
     shading: str
     battery_intrest: str
     Primary_goal: str

     research_notes: Optional[str]
     draft_quoting: Optional[str]

     final_quote: Optional[str]
    
print("Agent state defined")

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model = "gpt-5.2",
    temperature=0,
)

print(f"LLM initialized {llm}")

from langchain_core.messages import HumanMessage, SystemMessage

def research_node(state: AgentState) -> AgentState:
    """Analyze the product and extract research insights."""

    print("Research node is running...")

    roof_type = "\n".join(f"  - {f}" for f in state['roof_type'])

    messages = [
        SystemMessage(content=(
           """
You are SolarBot, a solar energy advisor for SimkoSolar.
Your task is to prepare the technical foundation for a solar quote.

CALCULATION RULE: 
1. Calculate the 25-year total cost of electricity: (Monthly Bill * 12 * 25).
2. Create a 'Estimated 25-Year Savings Range' which is 60% to 70% of that total.
3. Format these as currency with $ (e.g., $15,000).

Output a clean summary including these calculated savings.

"""
        )),

        HumanMessage(content=(
f"""
Prepare research for:
Location: {state['Location']}
Monthly Bill: ${state['monthly_bill']}
Roof: {state['roof_type']}
Shading: {state['shading']}
Goal: {state['Primary_goal']}

Provide the 25-year savings estimate range based on the rules above.
"""
        ))
    ]

    response = llm.invoke(messages)
    print("✅ Research complete.")
    return {**state, "research_notes": response.content}

print("✅ research note identified")

def draft_node(state: AgentState) -> AgentState:
    """Write a first draft of the product description using research notes."""
    print("Draft node is running....")
    
    roof_value = state["roof_type"] if isinstance(state["roof_type"], str) else ", ".join(state["roof_type"])


    messages = [
        SystemMessage(
            content=(
                """
             You are an expert solar copywriter. Write a warm, professional message.
             CRITICAL: Every time you mention a dollar amount, you MUST put the '$' BEFORE the number.
               """
            )
        ),
        HumanMessage(
            content=f"""
Write a solar quote message (150-200 words).

Details:
- Location: {state['Location']}
- Bill: ${state['monthly_bill']}
- Savings: Use the range from the research notes.

Rules:
1. Start with the savings and the location in the first 2 sentences.
2. Use '$' for all numbers (e.g., $20,000).
3. Do NOT use markdown or emojis.
4. Keep it concise and conversational.
"""
        )
    ]
    response = llm.invoke(messages)
    print(f"Draft completed {response}")

    return {**state, "draft_quoting": response.content}

print("✅ draft_node defined")

def refine_node(state: AgentState) -> AgentState:
    """Polish and optimize the solar quote draft."""

    print("Refine node is running....")

    roof_value = state["roof_type"] if isinstance(state["roof_type"], str) else ", ".join(state["roof_type"])

    messages = [
        SystemMessage(
            content=(
                "You are a senior solar quoting editor for SimkoSolar Energy. "
                "Your job is to refine draft solar estimate messages so they are clear, persuasive, trustworthy, and easy to read. "
                "Keep the strongest value-driving information early, especially anything related to savings and lowering electricity bills. "
                "Do not make the message longer than necessary. "
                "Do not invent facts, savings numbers, percentages, or technical details. "
                "Only improve clarity, flow, readability, and sales impact while staying faithful to the original draft and provided information."
            )
        ),
        HumanMessage(
            content=f"""
Refine this draft. 

Requirements:
- Ensure all numbers have the '$' prefix (e.g., $15,000).
- Keep the tone professional and warm.
- No markdown, no bullets.

Output EXACTLY in this format:

location: {state['Location']}
monthly_bill: ${state['monthly_bill']}
roof type: {roof_value}
goal: {state['Primary_goal']}
shading: {state['shading']}
battery_interest: {state['battery_intrest']}
primary goal: {state['Primary_goal']}

estimates 25 years saving: [Insert the range here, e.g., $18,000 - $22,000]

[Insert the polished conversational message here]

Original Draft:
{state["draft_quoting"]}
"""
        )
    ]

    response = llm.invoke(messages)

    print("Refinement complete")
    return {**state, "final_quote": response.content}

print("✅ refine_node defined")

from langgraph.graph import START, END, StateGraph


builder = StateGraph(AgentState)

builder.add_node("research", research_node)
builder.add_node("draft", draft_node)
builder.add_node("refine", refine_node)


builder.add_edge(START,    "research")
builder.add_edge("research", "draft")
builder.add_edge("draft", "refine")
builder.add_edge("refine", END)

agent = builder.compile()

print("✅ LangGraph compiled successfully!")
print("\nGraph flow: START → research → draft → refine → END")

# Visualize the graph structure (requires graphviz)
try:
    from IPython.display import Image, display
    display(Image(agent.get_graph().draw_mermaid_png()))
except Exception:
    # Fallback: print Mermaid diagram code
    print(agent.get_graph().draw_mermaid())

product_input: AgentState = {
    "Location": "10001 (New york)",
    "monthly_bill": 180,
    "roof_type": ["flat"],
    "shading": "no shading",
    "battery_intrest": "no",
    "Primary_goal": "Lower the Electricity bills",


    "research_notes": None,
    "draft_quoting": None,
    "final_quote": None
}

print("✅ Product input ready. Running agent...\n")
print("=" * 60)


result = agent.invoke(product_input)
print("=" * 60)
print("\n🎉 Agent complete!")

from IPython.display import Markdown, display

# ── Research Notes ──
print("=" * 60)
print("🔍 RESEARCH NOTES")
print("=" * 60)
display(Markdown(result["research_notes"]))


# ── Research Notes ──
print("=" * 60)
print("🔍 Draft")
print("=" * 60)
display(Markdown(result["draft_quoting"]))


# ── Research Notes ──
print("=" * 60)
print("🔍 Draft")
print("=" * 60)
display(Markdown(result["final_quote"]))