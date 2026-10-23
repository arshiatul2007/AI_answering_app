# AI Question & Answering System

## Project overview

This project is a Streamlit-based question answering application that sends user questions to a Gemini model and displays the generated answer in a ChatGPT-style chat interface. It keeps conversation history within the session and supports follow-up prompts while preserving a clean separation between UI logic, configuration, prompt text, and service code.

## Features

- Chat-style question and answer interface with Streamlit
- Gemini model integration using the Google Generative AI SDK
- Session-based conversation history for follow-up questions
- Configurable model and temperature via environment variables
- Input validation to prevent empty submissions
- Graceful handling of API errors without exposing sensitive details
- Structured project layout with separate modules for config, prompts, services, and logging

## Architecture

The application follows a modular structure:

- `app/config/settings.py` loads environment variables and validates required configuration
- `app/services/openai_service.py` encapsulates Gemini API communication
- `app/prompts/qa_prompt.py` contains the system prompt that guides the model
- `app/main.py` contains the Streamlit interface
- `app/utils/logging_config.py` configures application logging
- `tests/` contains pytest-based validation tests

## Project structure

```text
question_answering_app/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── openai_service.py
│   ├── prompts/
│   │   ├── __init__.py
│   │   └── qa_prompt.py
│   └── utils/
│       ├── __init__.py
│       └── logging_config.py
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   └── test_openai_service.py
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── run.sh
└── .env
```

## Prerequisites

- Python 3.10 or newer
- A Google Gemini API key
- Access to the Google AI API

## Python version requirement

This project is designed for Python 3.10+.

## Gemini API key setup

1. Create a Google AI Studio account or use a valid Gemini API project.
2. Generate an API key from Google AI Studio.
3. Store it in a local `.env` file in the project root.

Do not commit the `.env` file or share the key in source control.

## Virtual environment setup

### macOS/Linux

```bash
cd question_answering_app
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
cd question_answering_app
python -m venv .venv
.venv\Scripts\activate
```

## Dependency installation

```bash
pip install -r requirements.txt
```

## .env configuration

Copy the example file and update it with your values:

### macOS/Linux

```bash
cp .env.example .env
```

### Windows

```powershell
copy .env.example .env
```

Then edit `.env` to include your values:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.8-flash
TEMPERATURE=0.2
```

## How to run the Streamlit application

From the project root:

```bash
streamlit run app/main.py
```

Or use the helper script:

```bash
bash run.sh
```

## How to run tests

```bash
pytest
```

## Example questions

- What is the difference between Python lists and tuples?
- Explain the benefits of using a virtual environment.
- Summarize the purpose of a REST API.
- Why might a developer use caching in an application?

## Troubleshooting

### Missing API key

If the app shows a configuration error:

- Ensure `.env` exists in the project root.
- Confirm the `GEMINI_API_KEY` value is populated correctly.
- Restart the Streamlit app after saving the file.

### Dependency issues

Run:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Streamlit does not start

Check that you are running the command from the project root and that the package dependencies are installed.

## Security considerations

- Never hard-code the Gemini API key in source files.
- Do not print API keys in logs or the UI.
- Keep `.env` out of version control.
- Only log generic application events and avoid storing sensitive conversation data by default.

## How to deactivate the virtual environment

```bash
deactivate
```

## How to stop the Streamlit application

Press `Ctrl+C` in the terminal running the app.

## Future enhancements

- Add document upload and retrieval for grounded Q&A
- Support model selection in the UI
- Add conversation export and download
- Include prompt templates for specific domain expertise
- Add authentication and role-based access for multi-user deployments
