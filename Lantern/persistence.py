import os
import json
import logging
import streamlit as st
import uuid
import tempfile

# --- Configuration ---
SESSIONS_DIR = os.path.join(os.getcwd(), "sessions")
if not os.path.exists(SESSIONS_DIR):
    os.makedirs(SESSIONS_DIR)

logger = logging.getLogger(__name__)

def get_session_id():
    """
    Retrieves a STABLE session ID stored in session_state.
    We avoid query_params for ID generation to prevent instability across Cloud reruns.
    """
    # STABLE SESSION PATTERN:
    # 1. Initialize once in session_state default.
    # 2. Never trust query params to Dictate identity, only to Hint it.
    
    if "stable_session_id" not in st.session_state:
        # Generate a truly new session ID for this runtime instance
        # Use short UUID for readability like 'a1b2c3d4'
        new_id = str(uuid.uuid4())[:8]
        st.session_state.stable_session_id = new_id
        logger.info(f"✨ NEW SESSION INIT: {new_id}")
    
    return st.session_state.stable_session_id

def save_session_state(tree, current_node_id):
    """Saves the current tree and pointer to disk (atomic write)."""
    sid = get_session_id()
    filename = f"tree_{sid}.json"
    filepath = os.path.join(SESSIONS_DIR, filename)

    data = {
        "tree": tree,
        "current_node_id": current_node_id,
        "timestamp": str(uuid.uuid4()) # rudimentary versioning
    }

    try:
        # Atomic write pattern
        with tempfile.NamedTemporaryFile("w", delete=False, dir=SESSIONS_DIR, encoding="utf-8") as tmp:
            json.dump(data, tmp, indent=2)
            temp_name = tmp.name
        
        # Rename atomic replace
        if os.path.exists(filepath):
            os.remove(filepath)
        os.rename(temp_name, filepath)
        # logger.info(f"💾 Saved session {sid} to {filename}")
    except Exception as e:
        logger.error(f"❌ Failed to save session {sid}: {e}")

def load_session_state():
    """Loads tree from disk if exists for this session ID."""
    sid = get_session_id()
    filename = f"tree_{sid}.json"
    filepath = os.path.join(SESSIONS_DIR, filename)

    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(f"📂 Loaded session {sid}")
            return data["tree"], data.get("current_node_id")
        except Exception as e:
            logger.error(f"❌ Corrupt session file {filename}: {e}")
            return None, None
    return None, None
