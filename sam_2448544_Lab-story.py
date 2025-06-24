import streamlit as st
import ollama
import re


MODEL_NAME = "deepseek-r1:1.5b"


raw_prompts = [
    "   the lost treasure in the forest   ",
    "A ROBOT WHO learned to DREAM!!",
    "when   the moon    disappeared    for a day.",
    "The cat who saved a city from fire!!!",
    "  ",
    "Sam's Struggle during LLM exam"
]


st.set_page_config(page_title="StoryBot", page_icon="📖", layout="centered")
st.title("📚 StoryBot - AI Story Generator")
st.markdown("Generate short, creative stories using a powerful language model.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


def preprocess_prompt(prompt):
    if not prompt.strip():
        return None
    prompt = prompt.strip()
    prompt = re.sub(r'\s+', ' ', prompt)
    prompt = re.sub(r'[^\w\s]', '', prompt)
    prompt = prompt.lower().capitalize()
    return prompt


def clean_output(text):
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


def generate_story(prompt, genre="Surprise Me"):
    processed_prompt = preprocess_prompt(prompt)
    if not processed_prompt:
        return "⚠️ Skipped: empty or invalid prompt."
    
    genre_instruction = f"Write a short, {genre.lower()} story" if genre != "Surprise Me" else "Write a short, imaginative story"
    system_prompt = f"{genre_instruction} based on this idea:\n{processed_prompt}\n\nStory:"
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": system_prompt}]
        )
        raw_output = response['message']['content'].strip()
        return clean_output(raw_output)
    except Exception as e:
        return f"❌ Error: {str(e)}"

genre = st.selectbox(
    "🎭 Choose a Genre for Your Story:",
    ["Fantasy", "Sci-Fi", "Mystery", "Adventure", "Comedy", "Horror", "Drama", "Romance", "Surprise Me"]
)


user_input = st.chat_input("Type a story prompt...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    with st.spinner("Generating story..."):
        story = generate_story(user_input, genre)
        st.session_state.chat_history.append(("assistant", story))


for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)


with st.expander("📦 Batch Generate from Sample Prompts"):
    batch_genre = st.selectbox(
        "🎨 Choose Genre for Batch Generation:",
        ["Fantasy", "Sci-Fi", "Mystery", "Adventure", "Comedy", "Horror", "Drama", "Romance", "Surprise Me"],
        key="batch"
    )

    if st.button("Generate All Stories"):
        for i, prompt in enumerate(raw_prompts):
            story = generate_story(prompt, batch_genre)
            st.markdown(f"**Prompt {i+1}:** `{prompt}`")
            st.markdown(f"**Generated Story:**\n{story}")
            st.divider()
