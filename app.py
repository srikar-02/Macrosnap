import streamlit as st
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT, WELCOME_MESSAGE_TEMPLATE
import smtplib
from email.message import EmailMessage


MODEL_NAME = "gemini-3.5-flash-lite"


st.set_page_config(
    page_title="MacroSnap",
    page_icon="🥗"
)


# ---------------- SECRETS ----------------

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
EMAIL_ADDRESS = st.secrets["EMAIL_ADDRESS"]
EMAIL_APP_PASSWORD = st.secrets["EMAIL_APP_PASSWORD"]


# ---------------- GEMINI CLIENT ----------------

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)


gemini_client = get_gemini_client()


# ---------------- DISPLAY MESSAGE ----------------

def render_message(message):

    with st.chat_message(message["role"]):

        if message["kind"] == "text":
            st.write(message["content"])

        elif message["kind"] == "image":
            st.image(message["content"])


# ---------------- ADD MESSAGE ----------------

def add_message(role, kind, content):

    message = {
        "role": role,
        "kind": kind,
        "content": content
    }

    st.session_state.messages.append(message)

    render_message(message)


# ---------------- ASK GEMINI ----------------

def ask_gemini(parts):

    try:

        response = st.session_state.chat.send_message(parts)

        return response.text

    except Exception as error:

        return f"Sorry, something went wrong: {error}"


# ---------------- SEND EMAIL ----------------

def send_email(recipient_email, name, summary):

    try:

        message = EmailMessage()

        message["Subject"] = "🥗 MacroSnap - Your Meal Summary"
        message["From"] = EMAIL_ADDRESS
        message["To"] = recipient_email

        message.set_content(
            f"""Hi {name},

Here is your MacroSnap meal summary:

{summary}

Keep tracking your meals with MacroSnap! 🥗
"""
        )

        print("================================")
        print("EMAIL DEBUG")
        print("Sender:", EMAIL_ADDRESS)
        print("Recipient:", recipient_email)
        print("Connecting to Gmail SMTP...")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls()

            print("TLS connection successful")

            server.login(
                EMAIL_ADDRESS,
                EMAIL_APP_PASSWORD
            )

            print("SMTP login successful")

            server.send_message(message)

            print("Email accepted by SMTP server")

        print("Email sending completed")
        print("================================")

        return True

    except Exception as error:

        print("================================")
        print("EMAIL ERROR:", error)
        print("================================")

        st.error(
            f"Could not send email: {error}"
        )

        return False


# ==================================================
# ONBOARDING
# ==================================================

if "onboarded" not in st.session_state:

    st.title("🥗 MacroSnap")

    st.caption(
        "Snap it. Track it. Email yourself the results."
    )

    with st.form("onboarding_form"):

        name = st.text_input(
            "Your name"
        )

        email = st.text_input(
            "Your email address",
            placeholder="example@gmail.com"
        )

        submitted = st.form_submit_button(
            "Let's go 🚀"
        )

        if submitted:

            if not name.strip() or not email.strip():

                st.warning(
                    "Please fill in both your name and email address."
                )

            else:

                st.session_state.name = name.strip()

                st.session_state.email = email.strip()

                st.session_state.chat = gemini_client.chats.create(

                    model=MODEL_NAME,

                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT
                    )

                )

                st.session_state.messages = []

                st.session_state.onboarded = True

                st.rerun()

    st.stop()


# ==================================================
# CHAT SCREEN
# ==================================================

st.title("🥗 MacroSnap")

st.caption(
    f"Logged in as {st.session_state.name}"
)


# ---------------- WELCOME MESSAGE ----------------

if not st.session_state.messages:

    add_message(
        "assistant",
        "text",
        WELCOME_MESSAGE_TEMPLATE.format(
            name=st.session_state.name
        )
    )

else:

    for message in st.session_state.messages:

        render_message(message)


# ==================================================
# CHAT INPUT
# ==================================================

user_input = st.chat_input(
    "Ask a question, or attach a photo of your meal",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"]
)


if user_input:

    photo = (
        user_input.files[0]
        if user_input.files
        else None
    )

    text = user_input.text

    parts = []


    # ---------------- PHOTO ----------------

    if photo is not None:

        photo_bytes = photo.getvalue()

        add_message(
            "user",
            "image",
            photo_bytes
        )

        parts.append(
            types.Part.from_bytes(
                data=photo_bytes,
                mime_type=photo.type
            )
        )


    # ---------------- TEXT ----------------

    if text:

        add_message(
            "user",
            "text",
            text
        )

        parts.append(text)


    # ---------------- PHOTO ONLY ----------------

    elif photo is not None:

        parts.append(
            "What is this meal? Give me the calories and macros."
        )


    # ---------------- GEMINI RESPONSE ----------------

    with st.spinner(
        "Crunching the numbers..."
    ):

        answer = ask_gemini(parts)


    add_message(
        "assistant",
        "text",
        answer
    )


# ==================================================
# EMAIL SUMMARY
# ==================================================

st.divider()

st.subheader("📧 Email Your Summary")


if st.button(
    "Send Summary to My Email"
):

    summary = ""


    # Collect assistant messages

    for message in st.session_state.messages:

        if (
            message["role"] == "assistant"
            and message["kind"] == "text"
        ):

            summary += (
                message["content"]
                + "\n\n"
            )


    if summary.strip():

        with st.spinner(
            "Sending email..."
        ):

            success = send_email(

                st.session_state.email,

                st.session_state.name,

                summary
            )


        if success:

            st.success(
                f"Summary sent successfully to "
                f"{st.session_state.email}!"
            )

    else:

        st.warning(
            "There is no meal summary to send yet. "
            "Ask MacroSnap about a meal first."
        )