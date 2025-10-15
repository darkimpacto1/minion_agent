# Minion Agent

A web-based intelligent agent that can **chat** or **read and summarize emails** using a Large Language Model (LLM) backend.

## Project Overview

This project allows users to interact with a client interface built with **HTML + PHP**. The backend is powered by **FastAPI**, which handles requests in two modes:

1. **Chat Mode**: Normal conversation with the LLM agent.
2. **Email Mode**: Reads emails via **Google IMAP**, processes their content, and generates concise summaries using the LLM agent.

The architecture is as follows:

<img width="504" height="360" alt="image" src="https://github.com/user-attachments/assets/17204c3e-ae82-4687-a24b-d070ea9fbf46" />

## Features

- **Two Modes**: Chat or Email processing.
- **Email Reading**: Connects securely to Gmail via IMAP.
- **Automatic Summaries**: LLM generates concise email summaries.
- **Web Client**: Simple HTML/PHP interface for user interaction.

---

## Installation

1. **Clone the repository**:

```bash
git clone https://github.com/darkimpacto1/minion_agent.git
cd minion_agent
```
2. Create .env file
   add email address and imap passkey

```
```
2. Run the FastAPI backend:

```
uvicorn main:app --reload
