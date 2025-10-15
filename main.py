import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

# Local modules
from email_reader import get_unread_emails
from llama_model import chat_with_llama
from memory import init_db, save_message, get_user_history


# --- Lifespan event (startup/shutdown) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")

    # Load environment variables
    load_dotenv()

    # Initialize database
    init_db()

    # Load Gmail credentials into app state
    app.state.gmail_user = os.getenv("gmail_user")
    app.state.gmail_pass = os.getenv("gmail_pass")

    if not app.state.gmail_user or not app.state.gmail_pass:
        print("Gmail credentials are missing in your .env file")
    else:
        print("Gmail credentials loaded successfully")

    print("Startup complete: .env and DB ready")

    yield

    print("Shutting down...")


# --- FastAPI App ---
app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# --- Models ---
class ChatRequest(BaseModel):
    user_id: str
    message: str


# --- Routes ---
@app.get("/", response_class=HTMLResponse)
def serve_chat_ui(request: Request):
    """Serve the chat UI."""
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/")
async def chat(request: Request, payload: ChatRequest):
    """Handle chat messages and email summaries."""
    user_input = payload.message
    user_id = "0000"
    save_message(user_id, "user", user_input)

    # --- Email summarization mode ---
    if "summarize my emails" in user_input.lower():
        gmail_user = request.app.state.gmail_user
        gmail_pass = request.app.state.gmail_pass

        if not gmail_user or not gmail_pass:
            return {
                "response": "Missing Gmail credentials! Please check your .env file (gmail_user, gmail_pass)."
            }

        try:
            emails_text = get_unread_emails(gmail_user, gmail_pass)
            if emails_text and emails_text.strip() != "[]":
                print("📬 Unread emails successfully fetched.")
            else:
                print("📭 No unread emails found.")

        except Exception as e:
            print(f"❌ Error in get_unread_emails(): {e}")
            return {"response": f"Uh oh! 😵 Something went wrong reading your emails: {e}"}

        if not emails_text or emails_text.strip() == "[]":
            return {"response": "Bello! 🥸 No new banana-grams (emails) to summarize! Ba-ba-ba-ba-banana!"}

        prompt = (
            "You are a silly and funny Minion from Despicable Me. 🟡👓 "
            "You are still smart and helpful, but you speak in a playful tone and like to say things like 'Banana!', "
            "'Bello!', and laugh (e.g., 'hehehe'). "
            "Summarize the following unread emails in bullet points. For each email, include:\n"
            "- 📅 Date\n"
            "- 👤 Sender\n"
            "- ✉️ Subject (or say 'No Subject' if missing)\n"
            "- 📝 A short silly summary of the content (still accurate!)\n\n"
            "Use Minion-style expressions occasionally. Keep it fun but informative. Here are the emails:\n\n"
            "dont mention things like, Note: I tried to condense the information while still keeping it fun and Minion-like!"
            f"{emails_text}"
        )

        history = get_user_history(user_id)
        response = chat_with_llama(prompt, history)
        save_message(user_id, "assistant", response)
        return {"response": response}

    # --- Normal chat mode ---
    minion_prompt = (
        "You are a silly but helpful Minion from Despicable Me. 🟡👓 "
        "You speak in a goofy, excited tone. Use fun words like 'banana!', 'bello!', and silly laughter like 'hehehe'. "
        "Even though you're funny, still try to answer accurately and helpfully.\n"
        f"User said: {user_input}"
    )

    history = get_user_history(user_id)
    response = chat_with_llama(minion_prompt, history)
    save_message(user_id, "assistant", response)
    return {"response": response}

