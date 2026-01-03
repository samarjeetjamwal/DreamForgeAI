import streamlit as st
import ollama
import json
import os
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from PIL import Image
import requests  # For future image gen if we add a free API, but start with text-to-text

# Note: Ollama doesn't natively generate images locally yet (unless you pull vision models like llava).
# Workaround: Use LLM to generate detailed descriptions, then user imagines/downloads. For images, we'll add a prompt for Stable Diffusion local later (optional Step 6).
# For now, focus on text story + simple visualization.

llm = Ollama(model="llama3:8b")  # Change to your pulled model

# Shared "world" state – start with local JSON file (later GitHub sync)
WORLD_FILE = "dream_world.json"
if not os.path.exists(WORLD_FILE):
    with open(WORLD_FILE, "w") as f:
        json.dump({"nodes": [], "connections": []}, f)

def load_world():
    with open(WORLD_FILE, "r") as f:
        return json.load(f)

def save_world(world):
    with open(WORLD_FILE, "w") as f:
        json.dump(world, f)

def generate_dream_fragment(prompt):
    template = PromptTemplate.from_template(
        "Expand this dream fragment into a vivid 100-word story snippet and suggest 3 connection points to other dreams: {prompt}"
    )
    response = llm.invoke(template.format(prompt=prompt))
    return response

st.title("DreamForge: Build Infinite Shared Dreams")

user_prompt = st.text_input("Describe your dream fragment:")
if st.button("Forge It!"):
    if user_prompt:
        story = generate_dream_fragment(user_prompt)
        st.write(story)
        
        # Add to world (simple node)
        world = load_world()
        new_node = {"id": len(world["nodes"]), "prompt": user_prompt, "story": story}
        world["nodes"].append(new_node)
        save_world(world)
        
        # TODO: Auto-merge logic with existing nodes using LLM similarity

st.subheader("Explore the Dream Realm")
world = load_world()
for node in world["nodes"]:
    with st.expander(f"Dream #{node['id']}: {node['prompt'][:50]}..."):
        st.write(node["story"])

# GitHub sync button (manual for MVP)
if st.button("Sync to GitHub (Commit World)"):
    os.system("git add . && git commit -m 'Update dream world' && git push")
    st.success("Synced!")
    def find_merge(part1, part2):
    merge_prompt = f"Merge these two dream stories into one cohesive new fragment, keeping surreal elements: Story1: {part1} Story2: {part2}"
    return llm.invoke(merge_prompt)
