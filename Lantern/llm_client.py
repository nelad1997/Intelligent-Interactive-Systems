import os
import logging
from dotenv import load_dotenv
from typing import Optional
import time

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# ייבוא הגדרות הפרויקט
from definitions import ActionType
from prompt_builder import build_prompt

# טעינת משתני סביבה
load_dotenv()

# הגדרת לוגר
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Rate Limiter ---
import threading

class RateLimiter:
    def __init__(self, cooldown_seconds=5.0):
        self.cooldown = cooldown_seconds
        self.last_call_time = 0
        self.lock = threading.Lock()

    def wait_if_needed(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_call_time
            if elapsed < self.cooldown:
                wait_time = self.cooldown - elapsed
                logger.warning(f"⏳ Rate Limit: Waiting {wait_time:.1f}s before next call...")
                time.sleep(wait_time)
            self.last_call_time = time.time()

# Relaxed cooldown for better cloud responsiveness
_limiter = RateLimiter(cooldown_seconds=1.0)



def call_llm(prompt: str, system_instruction: Optional[str] = None) -> str:
    """
    Robust call to Gemini API with retries, rate limiting, and error handling.
    Uses gemini-2.5-pro for superior reasoning and system_instruction for token efficiency.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("CRITICAL: GEMINI_API_KEY is missing from environment variables!")
        raise RuntimeError("מפתח ה-API (GEMINI_API_KEY) חסר. אנא הגדר אותו ב-Secrets של Streamlit Cloud.")

    # Safe logging to verify request metadata
    key_display = f"{api_key[:4]}...{api_key[-4:]}"
    logger.info(f"🚀 INITIATING LLM CALL | Key: {key_display} | Prompt: {len(prompt)} chars")
    if system_instruction:
        logger.info(f"ℹ️ System Instruction Length: {len(system_instruction)} chars")

    genai.configure(api_key=api_key)

    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    }

    # model: Gemini 2.5 Pro (State-of-the-art reasoning)
    if not system_instruction:
        system_instruction = None
        
    model = genai.GenerativeModel(
        model_name="gemini-2.5-pro",
        safety_settings=safety_settings,
        system_instruction=system_instruction
    )

    # Enforce Rate Limit (Stricter for Pro model)
    _limiter.wait_if_needed()

    max_retries = 4
    retry_delay = 10 # Pro models usually have lower RPM, so we wait longer
    import random

    for attempt in range(max_retries):
        try:
            logger.info(f"📡 Calling Gemini 2.5 Pro (Attempt {attempt + 1}/{max_retries})...")
            start_time = time.time()
            response = model.generate_content(prompt)
            duration = time.time() - start_time
            
            logger.info(f"✅ API Response received in {duration:.2f}s")

            if not response or not hasattr(response, 'text') or not response.text:
                # Check for blocked content
                if hasattr(response, 'candidates') and response.candidates:
                    finish_reason = response.candidates[0].finish_reason
                    logger.error(f"❌ Response Blocked. Reason: {finish_reason}")
                    if finish_reason == 3: # SAFETY
                         raise RuntimeError("The request was blocked by safety filters. Please try rephrasing.")
                
                logger.warning(f"⚠️ Gemini returned an empty or blocked response.")
                raise RuntimeError("Empty response from Gemini")

            logger.info(f"📝 Response content length: {len(response.text)} chars")
            return response.text.strip()

        except Exception as e:
            err_msg = str(e)
            # Handle Rate Limit (429) or Resource Exhausted
            if "429" in err_msg or "ResourceExhausted" in err_msg or "Quota" in err_msg:
                if attempt < max_retries - 1:
                    # Randomized exponential backoff - more aggressive for Pro
                    wait_time = retry_delay * (2.5 ** attempt) + random.uniform(0, 3)
                    logger.warning(f"⚠️ Rate limit hit (429). Waiting {wait_time:.1f}s before retry {attempt + 2}/{max_retries}...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error("❌ Rate limit exceeded consistently after multiple retries.")
                    raise RuntimeError("מכסת הפעולה הגיעה למקסימום. דגם ה-Pro דורש המתנה ארוכה יותר בין פעולות. אנא נסה שוב בעוד דקה.")
            
            if "400" in err_msg and "model" in err_msg.lower():
                 logger.error(f"❌ Invalid model name or configuration: {e}")
                 raise RuntimeError("שגיאת תצורה במודל הבינה המלאכותית (Invalid Model).")

            logger.error(f"❌ Error during Gemini API call: {e}")
            raise e

# Legacy compatibility
def generate_content(action: ActionType, focus: str, system_instructions: str = "") -> str:
    """Wrapper for call_llm using the old signature if needed."""
    from prompt_builder import build_prompt
    # Use provided instructions or load defaults modularly
    if not system_instructions:
        from controller import load_academic_principles
        system_instructions = load_academic_principles(action)
        
    prompt = build_prompt(action, focus, instructions="")
    return call_llm(prompt, system_instruction=system_instructions)
