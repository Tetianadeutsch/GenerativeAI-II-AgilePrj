import gradio as gr
from graph_config import rag_agent, rag_graph
from typing import Tuple, List

def chat_with_graph(user_input: str, language: str) -> Tuple[List[Tuple[str, str]], str]:
    # Update agent language
    rag_agent.language = language
    
    # Process query
    result = rag_graph.invoke({
        "question": user_input,
        "chat_history": rag_agent.memory.load_memory_variables({})["chat_history"]
    })
    
    # Format chat history for display
    chat_history = []
    for i in range(0, len(rag_agent.memory.chat_memory.messages), 2):
        user_msg = rag_agent.memory.chat_memory.messages[i]
        ai_msg = rag_agent.memory.chat_memory.messages[i+1]
        chat_history.append((
            user_msg.content if hasattr(user_msg, 'content') else str(user_msg),
            ai_msg.content if hasattr(ai_msg, 'content') else str(ai_msg)
        ))
    
    return chat_history, ""

with gr.Blocks(title="Financial RAG Analyst") as app:
    with gr.Row():
        language = gr.Dropdown(
            choices=["English", "Deutsch"],
            value="English",
            label="Language/Sprache"
        )
    
    chatbot = gr.Chatbot(height=500)
    msg = gr.Textbox(label="Your Question/Ihre Frage")
    clear = gr.Button("Clear/Clear")

    def respond(message, chat_history, lang):
        lang_code = "en" if lang == "English" else "de"
        rag_agent.language = lang_code
        result = rag_graph.invoke({
            "question": message,
            "chat_history": rag_agent.memory.load_memory_variables({})["chat_history"]
        })
        chat_history.append((message, result["answer"]))
        return chat_history, ""

    msg.submit(respond, [msg, chatbot, language], [chatbot, msg])
    clear.click(lambda: [], None, chatbot, queue=False)

if __name__ == "__main__":
    app.launch()