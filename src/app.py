import gradio as gr
from llm import generate_answer


def answer_question(question):

    if not question or not question.strip():
        return "Please enter a financial question."

    return generate_answer(question.strip())


with gr.Blocks(
    title="FinTrace AI - Financial Research Assistant"
) as demo:

    gr.Markdown(
        """
        # FinTrace AI
        ### Financial Research Assistant

        Ask questions about Microsoft, NVIDIA, TCS and Jio Platforms.
        """
    )

    question_input = gr.Textbox(
        label="Enter Your Financial Question",
        placeholder="Example: What was NVIDIA's revenue growth in Q2 FY2027?",
        lines=3
    )

    analyze_button = gr.Button(
        "Analyze",
        variant="primary"
    )

    gr.Markdown("### Financial Analysis")

    answer_output = gr.Markdown(
        value="Your answer will appear here..."
    )

    analyze_button.click(
        fn=answer_question,
        inputs=question_input,
        outputs=answer_output
    )

    gr.Markdown(
        """
        ---
        **Technology:** Python | RAG | ChromaDB |
        Sentence Transformers | OpenRouter | NVIDIA Nemotron | Gradio

        *Answers are generated using the available financial knowledge base.*
        """
    )


if __name__ == "__main__":

    demo.launch(
        server_name="127.0.0.1",
        server_port=7863,
        show_error=True,
        theme=gr.themes.Soft()
    )