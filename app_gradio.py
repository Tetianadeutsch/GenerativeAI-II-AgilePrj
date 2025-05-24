import gradio as gr
from agents.coordinator_agent import coordinator_agent  # Loading the coordinating agent
import base64
from PIL import Image
from io import BytesIO

def process_agent_response(response):
    # Handle dictionary output with chart
    if isinstance(response, dict) and "summary" in response:
        text = response["summary"]
        chart = None

        if "chart_base64" in response:
            img_bytes = base64.b64decode(response["chart_base64"])
            chart = Image.open(BytesIO(img_bytes))

        return text, chart

    # Fallback for plain text
    return str(response), None

def run_multi_agent(user_input: str):
    try:
        result = coordinator_agent.invoke({"messages": [{"role": "user", "content": user_input}]})
        output = result["messages"][-1].content

        # Trying to get image if base64 is present
        if isinstance(output, dict) and "chart_base64" in output:
            img_data = base64.b64decode(output["chart_base64"])
            img = Image.open(BytesIO(img_data))
            return output.get("summary", ""), img

        return output, None
    except Exception as e:
        return f"❌ ERROR: {str(e)}", None

with gr.Blocks() as demo:
    gr.Markdown("### 🤖 Multimodal Market Analysis Agent")
    input_text = gr.Textbox(label="Enter your market-related query")
    output_text = gr.Textbox(label="Agent Response")
    output_image = gr.Image(label="Chart (if any)")
    btn = gr.Button("Run Agent")

    btn.click(fn=run_multi_agent, inputs=[input_text], outputs=[output_text, output_image])

if __name__ == "__main__":
    demo.launch()