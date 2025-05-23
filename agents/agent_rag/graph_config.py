from langgraph.graph import StateGraph
from langgraph.graph.graph import END
from financial_rag_agent import FinancialRAGAgent
from typing import TypedDict, List, Dict, Any
from langchain.memory import ConversationBufferMemory

class AgentState(TypedDict):
    input_question: str
    retrieved_context: str
    conversation_history: List[Dict[str, Any]]
    generated_answer: str

def create_rag_graph(agent: FinancialRAGAgent):
    def retrieve_node(state: AgentState):
        docs = agent.get_relevant_documents(state["input_question"])
        return {
            "retrieved_context": agent._format_docs(docs),
            "input_question": state["input_question"],
            "conversation_history": state.get("conversation_history", [])
        }

    def answer_node(state: AgentState):
        answer = agent.query(state["input_question"])
        return {
            "generated_answer": answer,
            "input_question": state["input_question"],
            "conversation_history": state["conversation_history"]
        }

    workflow = StateGraph(AgentState)
    workflow.add_node("retriever", retrieve_node)
    workflow.add_node("generator", answer_node)
    workflow.set_entry_point("retriever")
    workflow.add_edge("retriever", "generator")
    workflow.add_edge("generator", END)
    
    return workflow.compile()

rag_agent = FinancialRAGAgent(language="en")
rag_graph = create_rag_graph(rag_agent)