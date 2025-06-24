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

# ---- Chat History ----
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
        return response['message']['content'].strip()
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ---- User Input ----
user_input = st.chat_input("Type a story prompt...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Generating story..."):
        story = generate_story(user_input)
        st.session_state.chat_history.append(("assistant", story))

# ---- Display Chat History ----
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# ---- Optional: Batch Generate from Raw Prompts ----
with st.expander("📦 Batch Generate from Sample Prompts"):
    if st.button("Generate All Stories"):
        for i, prompt in enumerate(raw_prompts):
            story = generate_story(prompt)
            st.markdown(f"**Prompt {i+1}:** `{prompt}`")
            st.markdown(f"**Generated Story:**\n{story}")
            st.divider()

