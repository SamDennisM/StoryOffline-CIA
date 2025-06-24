import streamlit as st
import ollama
import re

# ---- Model Configuration ----
MODEL_NAME = "deepseek-r1:1.5b"

# ---- Synthetic dataset ----
raw_prompts = [
    "   the lost treasure in the forest   ",
    "A ROBOT WHO learned to DREAM!!",
    "when   the moon    disappeared    for a day.",
    "The cat who saved a city from fire!!!",
    "  ",
    "Sam's Struggle during LLM exam"
]

# ---- Streamlit App Config ----
st.set_page_config(page_title="StoryBot", page_icon="📖", layout="centered")
st.title("📚 StoryBot - AI Story Generator")
st.markdown("Generate short, creative stories using a powerful language model.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---- Preprocessing ----
def preprocess_prompt(prompt):
    if not prompt.strip():
        return None
    prompt = prompt.strip()
    prompt = re.sub(r'\s+', ' ', prompt)
    prompt = re.sub(r'[^\w\s]', '', prompt)
    prompt = prompt.lower().capitalize()
    return prompt

# ---- Clean output from assistant ----
def clean_output(text):
    """
    Cleans filler phrases and removes <think>...</think> blocks.
    """
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    patterns_to_remove = [
        r"^(Sure|Certainly|Of course|Let me explain|Here's|Here is|As an AI.*?)[:,\-]\s*",
        r"^I'm an AI.*?\.\s*",
        r"^Let's dive in.*?\.\s*",
        r"^Here’s (what|how|a|an).*?:\s*"
    ]
    for pattern in patterns_to_remove:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.MULTILINE)
    text = re.sub(r"\n\s*\n", "\n\n", text)
    return text.strip()

# ---- Generate story ----
def generate_story(prompt):
    processed_prompt = preprocess_prompt(prompt)
    if not processed_prompt:
        return "⚠️ Skipped: empty or invalid prompt."
    system_prompt = f"Write a short, imaginative story based on this idea:\n{processed_prompt}\n\nStory:"
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": system_prompt}]
        )
        raw_output = response['message']['content'].strip()
        return clean_output(raw_output)
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ---- User input ----
user_input = st.chat_input("Type a story prompt...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Generating story..."):
        story = generate_story(user_input)
        st.session_state.chat_history.append(("assistant", story))

# ---- Display chat history ----
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# ---- Batch generate from preset prompts ----
with st.expander("📦 Batch Generate from Sample Prompts"):
    if st.button("Generate All Stories"):
        for i, prompt in enumerate(raw_prompts):
            story = generate_story(prompt)
            st.markdown(f"**Prompt {i+1}:** `{prompt}`")
            st.markdown(f"**Generated Story:**\n{story}")
            st.divider()


