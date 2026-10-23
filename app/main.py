from __future__ import annotations

import streamlit as st

from app.config.settings import get_settings
from app.prompts.qa_prompt import SYSTEM_PROMPT
from app.services.openai_service import GeminiService
from app.utils.logging_config import get_logger

logger = get_logger(__name__)


def _initialize_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []


def _render_sidebar() -> None:
    settings = get_settings()

    st.sidebar.title("Controls")
    st.sidebar.caption("Gemini model configuration")
    st.sidebar.markdown(f"- Model: **{settings.gemini_model}**")
    st.sidebar.markdown(f"- Temperature: **{settings.temperature}**")

    if st.sidebar.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


def _display_chat_history() -> None:
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.markdown(content)


def main() -> None:
    """Render the Streamlit question-answering interface."""

    st.set_page_config(page_title="AI Question & Answering System", page_icon="🤖")
    st.title("AI Question & Answering System")
    st.caption("A question answering app powered by a Gemini model.")

    try:
        settings = get_settings()
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    _initialize_session_state()
    _render_sidebar()
    _display_chat_history()

    user_question = st.chat_input("Ask a question...")

    if user_question is not None:
        question = user_question.strip()

        if not question:
            st.warning("Please enter a valid question before submitting.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(question)

        try:
            service = GeminiService(
                api_key=settings.gemini_api_key,
                model=settings.gemini_model,
                temperature=settings.temperature,
            )

            with st.spinner("Thinking..."):
                answer = service.generate_answer(
                    messages=st.session_state.messages,
                    system_prompt=SYSTEM_PROMPT,
                )
        except RuntimeError as exc:
            logger.warning("Gemini request error handled in UI.")
            st.error(str(exc))
            return

        st.session_state.messages.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.markdown(answer)


if __name__ == "__main__":
    main()
