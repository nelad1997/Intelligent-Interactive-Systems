# Lantern 🏮 - AI-Augmented Thinking & Writing

Lantern is a specialized writing assistant designed to help human authors explore "Thought Trees"—divergent reasoning paths, logical critiques, and contextual refinements—using the power of LLMs.

## 🚀 Quick Start (Local)

### 1. Prerequisites
- **Python 3.9+** (Tested on 3.10.12)
- **Graphviz**: The system requires Graphviz to render the thinking tree.
  - **Windows**: Install via [graphviz.org](https://graphviz.org/download/) or `choco install graphviz`.
  - **Linux/Mac**: `sudo apt-get install graphviz` or `brew install graphviz`.

### 2. Installation
1. Clone the repository.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration
Add your API Key to env.:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### 4. Run Lantern
```bash
streamlit run app.py
```

---
   
4. **Graphviz Support**: The included `packages.txt` ensures that Graphviz is automatically installed on the cloud environment.

---

## 🛠 Features Summary
- **Thought Tree Visualization**: Real-time Graphviz map of your brainstorming process in the sidebar.
- **Contextual Actions**:
  - 🌱 **Diverge**: Generates creative alternative paths from specific paragraphs.
  - 🛡️ **Critique**: Analyzes logical consistency and potential blind spots.
  - 🪄 **Refine**: Suggests grammatical and stylistic improvements.
- **Tree Persistence**: Aggressive state synchronization to prevent data loss even in unstable cloud environments.
- **Manual/Auto Pinning**: Keep track of the best ideas and merge them into your main draft.
- **Full System Reset**: A dedicated "Start Over" button (🗑) to wipe the workspace and start fresh.

## 📂 Project Structure
- `app.py`: Main Streamlit interface and application logic.
- `sidebar_map.py`: Logic for rendering the Thought Tree and sidebar navigation.
- `controller.py`: Event handling and state orchestration.
- `tree.py`: Data structure logic for the hierarchical thinking process.
- `llm_client.py`: Interface for Gemini API communication.
- `prompt_builder.py`: Constructs complex system prompts for different AI behaviors.

---
*Created for the Intelligent Interactive Systems course at Technion.*
