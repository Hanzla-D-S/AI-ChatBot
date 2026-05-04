import streamlit as st
import requests
import os


# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Chat Bot",
    layout="centered"
)

# ── Styling ─────────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        /* Main background */
        .stApp { background-color: #f5f7fa; }

        /* Chat bubbles */
        .user-bubble {
            background-color: #0084ff;
            color: white;
            padding: 12px 16px;
            border-radius: 18px 18px 4px 18px;
            margin: 6px 0;
            max-width: 75%;
            margin-left: auto;
            word-wrap: break-word;
        }
        .bot-bubble {
            background-color: #ffffff;
            color: #1a1a1a;
            padding: 12px 16px;
            border-radius: 18px 18px 18px 4px;
            margin: 6px 0;
            max-width: 75%;
            border: 1px solid #e0e0e0;
            word-wrap: break-word;
        }
        .bubble-wrapper-user {
            display: flex;
            justify-content: flex-end;
            margin: 4px 0;
        }
        .bubble-wrapper-bot {
            display: flex;
            justify-content: flex-start;
            margin: 4px 0;
        }

        /* Header */
        .chat-header {
            background: linear-gradient(90deg, #0084ff, #00c6ff);
            padding: 16px 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            color: white;
        }

        /* Input box */
        .stTextInput > div > div > input {
            border-radius: 24px;
            border: 2px solid #0084ff;
            padding: 10px 18px;
            font-size: 15px;
        }

        /* Send button */
        .stButton > button {
            border-radius: 24px;
            background-color: #0084ff;
            color: white;
            border: none;
            padding: 10px 28px;
            font-size: 15px;
            font-weight: 600;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: #006edc;
        }

        /* Hide streamlit default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ── Constants ───────────────────────────────────────────────────────────────────
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/chat")

# ── Session state ───────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Header ──────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="chat-header">
        <h2 style="margin:0; font-size:22px;">Customer Support</h2>
    </div>
""", unsafe_allow_html=True)

# ── Suggested questions (shown only at start) ───────────────────────────────────
if len(st.session_state.messages) == 0:
    "<p style='color: black; font-weight: bold;'>Hi! How can I help you today? Try asking:</p>",
    unsafe_allow_html=True
    suggestions = [
        "How do I track my order?",
        "What is your return policy?",
        "Is Cash on Delivery available?",
        "How long does delivery take?",
    ]
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        if cols[i % 2].button(suggestion, key=f"sug_{i}"):
            st.session_state.messages.append({
                "role": "user",
                "content": suggestion
            })
            with st.spinner("Thinking..."):
                try:
                    res = requests.post(
                        BACKEND_URL,
                        json={"message": suggestion},
                        timeout=30
                    )
                    reply = res.json().get("reply", "Sorry, something went wrong.")
                except Exception:
                    reply = "Cannot connect to backend. Make sure it's running!"
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })
            st.rerun()

# ── Chat history display ─────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
            <div class="bubble-wrapper-user">
                <div class="user-bubble">{msg["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="bubble-wrapper-bot">
                <div class="bot-bubble">{msg["content"]}</div>
            </div>
        """, unsafe_allow_html=True)

# ── Input area ───────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])

# counter to reset input box
if "input_counter" not in st.session_state:
    st.session_state.input_counter = 0

with col1:
    user_input = st.text_input(
        label="message",
        placeholder="Type your question here...",
        label_visibility="collapsed",
        key=f"user_input_{st.session_state.input_counter}"
    )

with col2:
    send = st.button("Send")

# ── Handle send ──────────────────────────────────────────────────────────────────
if send and user_input.strip():
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input.strip()
    })

    # Call backend
    with st.spinner("Thinking..."):
        try:
            response = requests.post(
                BACKEND_URL,
                json={"message": user_input.strip()},
                timeout=30
            )
            reply = response.json().get("reply", "Sorry, something went wrong.")
        except requests.exceptions.ConnectionError:
            reply = "Cannot connect to backend. Make sure it is running with: uvicorn backend.main:app --reload"
        except Exception as e:
            reply = f"Error: {str(e)}"

    # Add bot reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })
    st.session_state.input_counter += 1
    st.rerun()

# ── Clear chat button ────────────────────────────────────────────────────────────
if len(st.session_state.messages) > 0:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Clear Chat", key="clear"):
        st.session_state.messages = []
        st.rerun()