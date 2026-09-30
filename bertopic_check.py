import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from markdown import markdown
from bertopic import BERTopic
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer



def sanitize_and_chunk(filepath, tool_name):
    """Strips diagrams and flattens tables/lists into raw semantic text."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Eradicate Diagram & Code Noise
    # Fenced blocks containing Mermaid/PlantUML flows or JSON schemas are 
    # removed to prevent syntax tokens from skewing the K-Means clusters.
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    
    chunks = []
    # 2. Split by Markdown headers to isolate contextual sections
    for section in re.split(r'\n#{1,4}\s+', content):
        if len(section.strip()) < 50:
            continue
            
        # 3. Flatten Tables and Lists into Plain Text
        # Converting Markdown to HTML and extracting text strips structural 
        # characters (like table pipes or list numbers) while preserving the words.
        html = markdown(section, extensions=['tables'])
        clean_text = BeautifulSoup(html, "html.parser").get_text(separator=' ')
        
        # 4. Remove residual ASCII punctuation (arrows, ASCII tree lines)
        clean_text = re.sub(r'[-=*>|]+', ' ', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        if clean_text:
            chunks.append({"text": clean_text, "tool": tool_name})
            
    return chunks

# 1. Walk the directory tree to ingest all 29+ markdown files
root_dir = "./BerTopicCheck/files/"
data = []

# Iterates through bmadmethod, kiro, openspec, speckit, tessl
for tool_folder in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, tool_folder)
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".md"):
                file_path = os.path.join(folder_path, filename)
                data.extend(sanitize_and_chunk(file_path, tool_folder))

df = pd.DataFrame(data)
docs = df["text"].tolist()
classes = df["tool"].tolist()

# 2. Force K-Means Clustering (Bypassing HDBSCAN density requirements)
kmeans_model = KMeans(n_clusters=20, random_state=42)

study_case_stopwords = [
    # Core Calculator & Math Domain
    "calculator", "math", "arithmetic", "expression", "expressions", 
    "evaluate", "evaluation", "calculate", "calculation", "calculations", 
    "pemdas", "parentheses", "exponents", "multiplication", "division", 
    "addition", "subtraction", "decimal", "precision", "floating", "float", 
    "point", "operator", "operators", "operand", "zero", "result", "chained",
    
    # UI, UX & Accessibility
    "ui", "ux", "interface", "experience", "responsive", "layout", 
    "desktop", "mobile", "tablet", "screen", "sizes", "button", "buttons", 
    "keyboard", "keys", "enter", "backspace", "clear", "delete", 
    "escape", "reset", "accessibility", "a11y", "visual", "colors", 
    "contrast", "aria", "role", "typography", "reader", "label", "labeling",
    "focus", "clipped", "overflow", "horizontal",
    
    # Specific Tech Stack & Frameworks
    "python", "fastapi", "react", "typescript", "vite", "next", "nextjs", 
    "pytest", "ast", "json",
    
    # General Web App, Architecture, & Seed Document Terms
    "backend", "frontend", "api", "endpoint", "rest", "client", 
    "server", "service", "state", "components", "component", "props", 
    "hooks", "payload", "payloads", "response", "responses", "tests", 
    "unit", "markup", "seed", "executive", "intent", "truth"
]

    # Add this to your vectorizer configuration:
    # custom_stop_words = base_stop_words + sdd_domain_words + study_case_stopwords

# 3. Strip universal SDD terminology to force differentiation
custom_stop_words = list(CountVectorizer(stop_words="english").get_stop_words()) + study_case_stopwords
vectorizer_model = CountVectorizer(stop_words=custom_stop_words, ngram_range=(1, 3))

# 4. Fit the Topic Model
topic_model = BERTopic(
    hdbscan_model=kmeans_model,
    vectorizer_model=vectorizer_model,
    language="english"
)

topics, probs = topic_model.fit_transform(docs)

# 5. Extract and Visualize the Tool Priorities
topics_per_class = topic_model.topics_per_class(docs, classes=classes)
#6 Add percentage of documents per class to the topics_per_class DataFrame
topics_per_class['percentage'] = topics_per_class['Frequency'] / topics_per_class.groupby('Class')['Frequency'].transform('sum') * 100
print(topics_per_class)

fig = topic_model.visualize_topics_per_class(topics_per_class, top_n_topics=10, normalize_frequency=True)
fig.show()