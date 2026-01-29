# Lantern - Changelog / Recent Updates

## [2026-01-29] - UI Overhaul & Quota Stabilization

### ✨ New Features
- **Smart Payload Architecture**: Lantern now intelligently filters its knowledge base and academic principles per request. Context is only sent when strictly necessary (e.g., Expanding ideas), resulting in **up to 90% reduction in token usage** for typical edits.
- **AI Context & Structure Tabbed UI**: Consolidated Focus Range, Segmentation, and Focus Preview into a single, clean tabbed interface.
- **Dedicated Help Tooltips**: Added granular guidance for each tool to help users manage their AI focus range effectively.

### 🛠️ Bug Fixes & Reliability
- **Dramatically Improved 429 Mitigation**: Upgraded the LLM client with randomized exponential backoff (Jitter) and a stricter cooldown between calls.
- **Paragraph Selection Persistence**: Resolved the race condition that caused the paragraph list to disappear during AI thinking states.
- **Stable Structural Sync**: Centralized the document segmentation logic to provide a consistent substrate for all AI actions.
- **Diagnostic Usage Logging**: Internal logs now track prompt length to help optimize and prevent TPM/RPM limit violations.

### 🧠 Performance & UX
- **Modern Tabbed Layout**: Reduced vertical scrolling for better usable workspace.
- **Differentiated Reset Logic**: Clearer distinction between resetting the thought tree (preserving draft) vs. a full workspace wipe.

---

## [2026-01-28] - Stability & Performance Update

### ✨ New Features
- **Focus Mode Improvements**: Added direct shortcuts and improved tooltips for document focus range selection.
- **Manual AI Map Refresh**: Enhanced logical structure scanning.
- **Robust LLM Client**: Re-engineered the Gemini API connector with basic retries.
