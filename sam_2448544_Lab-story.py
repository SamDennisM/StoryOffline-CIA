import ollama
import re

# Step 1: Define the transformer-based model from Ollama
MODEL_NAME = "deepseek-r1:1.5b"

# Step 2: Small synthetic dataset (story prompts)
raw_prompts = [
    "   the lost treasure in the forest   ",
    "A ROBOT WHO learned to DREAM!!",
    "when   the moon    disappeared    for a day.",
    "The cat who saved a city from fire!!!",
    "  ",
    "Sam's Struggle during LLM exam"
]

# Step 3: Preprocessing function
def preprocess_prompt(prompt):
    if not prompt.strip():
        return None  # skip empty prompts
    prompt = prompt.strip()
    prompt = re.sub(r'\s+', ' ', prompt)  # normalize multiple spaces
    prompt = re.sub(r'[^\w\s]', '', prompt)  # remove punctuation
    prompt = prompt.lower().capitalize()  # normalize casing
    return prompt

# Step 4: Model interaction
def generate_story(prompt):
    processed_prompt = preprocess_prompt(prompt)
    if not processed_prompt:
        return "Skipped: empty or invalid prompt."
    
    system_prompt = f"Write a short, imaginative story based on this idea:\n{processed_prompt}\n\nStory:"
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": system_prompt}]
    )
    return response['message']['content'].strip()

# Step 5: Output generation loop
for i, raw_prompt in enumerate(raw_prompts):
    story = generate_story(raw_prompt)
    print(f"\n--- Story {i+1} ---")
    print(f"Raw Prompt: {repr(raw_prompt)}")
    print("Generated Story:\n", story)
