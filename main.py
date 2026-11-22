
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# ==================================
# STEP 1: DEFINE STATE
# ==================================

class SupportState(TypedDict):
    question: str
    category: str
    response: str


# ==================================
# STEP 2: CREATE NODES
# ==================================

# Node 1: Classify user question

def classify_question(state: SupportState):

    question = state["question"].lower()

    if "order" in question:
        category = "order"

    elif "refund" in question:
        category = "refund"

    elif "payment" in question:
        category = "payment"

    elif "return" in question:
        category = "return"

    else:
        category = "general"

    print(f"\n[Agent] Question category: {category}")

    return {"category": category}


# Node 2: Order support

def order_support(state: SupportState):

    print("[Agent] Processing order query...")

    return {
        "response": "Please provide your order ID to check the order status."
    }


# Node 3: Refund support

def refund_support(state: SupportState):

    print("[Agent] Processing refund query...")

    return {
        "response": "I can help you with your refund. Please provide your order ID."
    }


# Node 4: Payment support

def payment_support(state: SupportState):

    print("[Agent] Processing payment query...")

    return {
        "response": "Please share your payment transaction ID so I can help."
    }


# Node 5: Return support

def return_support(state: SupportState):

    print("[Agent] Processing return query...")

    return {
        "response": "Please provide your order ID to start the return process."
    }


# Node 6: General support

def general_support(state: SupportState):

    print("[Agent] Processing general query...")

    return {
        "response": "Hello! Welcome to Customer Support. How can I help you?"
    }


# ==================================
# STEP 3: CONDITIONAL ROUTING
# ==================================

def route_question(state: SupportState):

    category = state["category"]

    if category == "order":
        return "order"

    elif category == "refund":
        return "refund"

    elif category == "payment":
        return "payment"

    elif category == "return":
        return "return"

    else:
        return "general"


# ==================================
# STEP 4: CREATE GRAPH
# ==================================

graph = StateGraph(SupportState)


# ==================================
# STEP 5: ADD NODES
# ==================================

graph.add_node("classify", classify_question)

graph.add_node("order", order_support)

graph.add_node("refund", refund_support)

graph.add_node("payment", payment_support)

graph.add_node("return", return_support)

graph.add_node("general", general_support)


# ==================================
# STEP 6: CONNECT NODES
# ==================================

graph.add_edge(START, "classify")


# Conditional edges

graph.add_conditional_edges(
    "classify",
    route_question,
    {
        "order": "order",
        "refund": "refund",
        "payment": "payment",
        "return": "return",
        "general": "general"
    }
)


# Connect all support nodes to END

graph.add_edge("order", END)

graph.add_edge("refund", END)

graph.add_edge("payment", END)

graph.add_edge("return", END)

graph.add_edge("general", END)


# ==================================
# STEP 7: COMPILE GRAPH
# ==================================

app = graph.compile()


# ==================================
# STEP 8: RUN CUSTOMER SUPPORT AGENT
# ==================================

def run_agent():

    print("=" * 45)
    print("   LANGGRAPH CUSTOMER SUPPORT AGENT")
    print("=" * 45)

    print("\nType 'exit' to stop the application.")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("\nAgent: Thank you! Have a nice day.")
            break

        if not question:
            print("Agent: Please enter a question.")
            continue

        # Execute LangGraph
        result = app.invoke({
            "question": question
        })

        # Display result
        print("\nCategory:", result["category"])

        print("Agent:", result["response"])


# ==================================
# MAIN FUNCTION
# ==================================

if __name__ == "__main__":
    run_agent()
