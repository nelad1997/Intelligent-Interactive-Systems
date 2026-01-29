# Lantern - Changelog / Recent Updates

## [2026-01-29] - UI Overhaul & Quota Stabilization

### ✨ New Features
- **Smart Payload Architecture**: Lantern now intelligently filters its knowledge base and academic principles per request. Context is only sent when strictly necessary (e.g., Expanding ideas), resulting in **up to 90% reduction in token usage** for typical edits.
- **AI Context & Structure Tabbed UI**: Consolidated Focus Range, Segmentation, and Focus Preview into a single, clean tabbed interface.
- **Dedicated Help Tooltips**: Added granular guidance for each tool to help users manage their AI focus range effectively.

### 🛠️ Bug Fixes & Reliability
- **Navigation Data Persistence**: Fixed a major bug where switching nodes in the Thought Tree would occasionally clear the editor. The draft is now robustly preserved or inherited during all navigation actions.
- **Pro-Level Quota Mitigation**: Standardized Gemini 2.5 Pro with a 30s RPM safety buffer and modular system instructions.
- **Paragraph Selection Persistence**: Resolved the race condition that caused the paragraph list to disappear.
- **Diagnostic Usage Logging**: Internal tracking of prompt length for better quota management.

### 🧠 Performance & UX
- **Modern Tabbed Layout**: Reduced vertical scrolling for better usable workspace.
- **Differentiated Reset Logic**: Clearer distinction between resetting the thought tree (preserving draft) vs. a full workspace wipe.

---

## [2026-01-28] - Stability & Performance Update

### ✨ New Features
- **Focus Mode Improvements**: Added direct shortcuts and improved tooltips for document focus range selection.
- **Manual AI Map Refresh**: Enhanced logical structure scanning.
- **Robust LLM Client**: Re-engineered the Gemini API connector with basic retries.
