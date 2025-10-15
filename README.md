# Minion Agent

A web-based intelligent agent that can **chat** or **read and summarize emails** using a Large Language Model (LLM) backend.

## Project Overview

This project allows users to interact with a client interface built with **HTML + PHP**. The backend is powered by **FastAPI**, which handles requests in two modes:

1. **Chat Mode**: Normal conversation with the LLM agent.
2. **Email Mode**: Reads emails via **Google IMAP**, processes their content, and generates concise summaries using the LLM agent.

The architecture is as follows:

<img width="504" height="360" alt="image" src="https://github.com/user-attachments/assets/17204c3e-ae82-4687-a24b-d070ea9fbf46" />
