# PEACOCK ENGINE WebUI - Feature Specification
> **For Design Team** - Version 1.0
> **Goal**: Complete feature inventory so every function has a designed place

---

## 1. CORE CHAT INTERFACE

### 1.1 Primary Chat View
- **Message input area** (multi-line, resizable)
- **Send button** (with keyboard shortcut: Enter/Ctrl+Enter)
- **Message history display** (user messages on right, AI on left)
- **Streaming text animation** (words appearing character-by-character)
- **Stop generation button** (visible while streaming)
- **New conversation button** (clears history)

### 1.2 Model Selection
- **Model dropdown/picker** showing all active models
- **Model cards/info** on selection (show: gateway, RPM, tier, price)
- **Favorite/star models** for quick access
- **Recently used models** section
- **Filter by gateway** (Google, Groq, DeepSeek, Mistral)
- **Warning indicator** for frozen/disabled models

### 1.3 Message Features
- **Copy message** button (hover on message)
- **Delete message** (remove from conversation)
- **Edit message** (resend with modifications)
- **Regenerate response** (retry with same prompt)
- **Message timestamps**
- **Token count per message** (input + output)
- **Cost per message** (calculated from token usage)

---

## 2. FILE & CONTEXT MANAGEMENT

### 2.1 File Upload
- **Drag & drop zone** for files
- **File picker button** (browse local files)
- **Multiple file upload** support
- **File type indicators** (.py, .js, .txt, .md, .pdf, images)
- **File size warning** (if too large)
- **Remove file** button (X on each file chip)

### 2.2 Context Display
- **Attached files list** (above chat input)
- **File preview panel** (collapsible sidebar showing file contents)
- **Syntax highlighting** for code files
- **Search within files**
- **File tokens count** (shows how many tokens each file uses)

### 2.3 Conversation History
- **Sidebar with past conversations**
- **Search conversations**
- **Delete/archive conversations**
- **Rename conversations**
- **Export conversation** (JSON, Markdown, PDF)
- **Conversation folders/tags**

---

## 3. TOOL CALLING INTERFACE

### 3.1 Tool Configuration Panel
- **Enable/disable tools** toggle per conversation
- **Tool list** with descriptions:
  - Google Search (web search)
  - Google Maps (location data)
  - Code Execution (Python runner)
  - URL Context (web page reading)
  - File Search (RAG from uploaded docs)
  - Computer Use (browser automation)
- **Tool parameters** configuration (if needed)

### 3.2 Tool Execution Display
- **Tool call notification** ("Model is searching...")
- **Tool result panel** (shows search results, code output, etc.)
- **Expand/collapse tool results**
- **Tool execution time**
- **Retry tool** button (if failed)

### 3.3 Custom Tools
- **Add custom tool** form (name, description, endpoint)
- **Custom tool list** management
- **Test custom tool** button

---

## 4. TOKEN & COST TRACKING

### 4.1 Real-time Display
- **Current conversation tokens** (running total)
- **Current conversation cost** (running total in $)
- **Model price info** (input/output per 1M tokens)
- **Token breakdown** (prompt vs completion)

### 4.2 Cost Dashboard
- **Daily spend** display
- **Weekly/monthly charts**
- **Cost by gateway** breakdown
- **Cost by model** breakdown
- **Budget settings** (alerts when approaching limit)

### 4.3 Token Counter Tool
- **Standalone token counter** page/popup
- **Paste text** to count tokens
- **Upload file** to count tokens
- **Select model** for accurate counting
- **Multimodal token counting** (images, video, audio)

---

## 5. MODEL MANAGEMENT

### 5.1 Model Registry View
- **Grid/table of all models**
- **Model status indicators**:
  - ✅ Active (ready to use)
  - ❄️ Frozen (temporarily disabled)
  - 🚫 Deprecated (permanently disabled)
- **Model details panel**:
  - Context window size
  - RPM/TPM limits
  - Pricing
  - Capabilities (tools, streaming, multimodal)
  - Gateway

### 5.2 Model Actions
- **Freeze model** button (with reason input)
- **Unfreeze model** button
- **Test model** button (quick validation)
- **Set as default** model

### 5.3 Model Performance
- **Success rate** per model (% of requests that succeed)
- **Average latency** per model
- **Error rate** tracking
- **Usage charts** (requests over time)

---

## 6. API KEY MANAGEMENT

### 6.1 Key Overview
- **List of all API keys** (by gateway)
- **Key health status**:
  - 🟢 Healthy (working normally)
  - 🟡 Warning (high usage or recent errors)
  - 🔴 Exhausted/Cooldown (temporarily disabled)
  - ⚫ Dead (invalid key)
- **Masked key display** (show only first/last 4 chars)
- **Key labels/names** (editable)

### 6.2 Key Details
- **Usage statistics** per key:
  - Requests today
  - Tokens used today
  - Success/failure rate
  - Average latency
- **Rate limit status** (RPM/TPM remaining)
- **Cooldown timer** (if on cooldown)
- **Last used** timestamp

### 6.3 Key Actions
- **Add new key** button (input field for key + label)
- **Delete key** button (with confirmation)
- **Test key** button (validation)
- **Edit label** button
- **Toggle key** (enable/disable without deleting)

---

## 7. TESTING & VALIDATION

### 7.1 Quick Test Panel
- **Test all models** button
- **Test all keys** button
- **Test specific model** dropdown + button
- **Test specific key** dropdown + button

### 7.2 Validation Results Display
- **Test results table** showing:
  - Model/Key name
  - Status (✅ Pass / ❌ Fail)
  - Latency
  - Error message (if failed)
  - Action taken (frozen, etc.)
- **Auto-freeze toggle** (enable/disable automatic freezing)
- **Export results** button (JSON/CSV)

### 7.3 System Health Dashboard
- **Gateway health** indicators:
  - Google: 🟢/🟡/🔴
  - Groq: 🟢/🟡/🔴
  - DeepSeek: 🟢/🟡/🔴
  - Mistral: 🟢/🟡/🔴
- **Overall system status** (ONLINE/DEGRADED/OFFLINE)
- **Recent errors** log (last 10)
- **Active alerts** panel

---

## 8. SETTINGS & CONFIGURATION

### 8.1 General Settings
- **Default model** selector
- **Default temperature** slider (0.0 - 2.0)
- **Default output format** (text/JSON/Pydantic)
- **Theme** (dark/light/system)
- **Language** selector

### 8.2 Performance Settings
- **Performance mode** selector:
  - Black Key (Stealth) - Conservative
  - Blue Key (Balanced) - Normal
  - Red Key (Apex) - Aggressive
- **Request timeout** setting
- **Streaming** toggle (on/off)
- **Auto-retry** toggle (on/off)

### 8.3 Notification Settings
- **Enable notifications** toggle
- **Alert thresholds**:
  - Cost threshold ($)
  - Rate limit threshold (%)
  - Error rate threshold (%)
- **Webhook URL** (for external alerts)

### 8.4 Security Settings
- **API key for WebUI** (authentication)
- **IP allowlist** (restrict access)
- **Session timeout** setting
- **Audit log** viewer

---

## 9. ADVANCED FEATURES

### 9.1 Structured Output
- **JSON mode** toggle (force JSON output)
- **Schema editor** (for Pydantic structured output)
  - Add fields
  - Set field types
  - Mark required/optional
- **Schema templates** (common patterns)

### 9.2 Batch Operations
- **Batch request** interface:
  - Upload CSV/JSON of prompts
  - Select model
  - Process all
  - Download results
- **Progress indicator** for batch jobs

### 9.3 Prompt Templates
- **Template library** (save/load prompts)
- **Template variables** ({{variable}} syntax)
- **Template categories/tags**
- **Share templates** (export/import)

---

## 10. MOBILE-SPECIFIC FEATURES

### 10.1 Mobile Navigation
- **Bottom tab bar** (Chat, Models, Keys, Settings)
- **Swipe gestures**:
  - Swipe right: Open sidebar
  - Swipe left: Close/open model panel
  - Swipe up: Expand chat input
- **Pull to refresh** (for lists)

### 10.2 Mobile Optimizations
- **Voice input** button (mic icon)
- **Fullscreen chat** mode (hide all sidebars)
- **Touch-friendly buttons** (min 44px)
- **Bottom sheet** for model selection
- **Floating action button** (new chat)

---

## 11. USER ONBOARDING

### 11.1 First-time Setup
- **Welcome modal** (brand intro)
- **API key setup** wizard:
  - Add Google key
  - Add Groq key
  - Test keys
- **Model selection** guide
- **Quick tutorial** (tooltips on first use)

### 11.2 Help & Documentation
- **In-app help** panel
- **Keyboard shortcuts** reference
- **API documentation** link
- **Video tutorials** section
- **FAQ** accordion

---

## 12. ADMIN/DEBUG PANEL (Advanced Users)

### 12.1 Request Inspector
- **Raw request/response** viewer
- **Headers display**
- **Timing breakdown** (DNS, connect, TTFB, etc.)
- **Copy as cURL** button

### 12.2 Logs Viewer
- **System logs** (filterable by level)
- **Request logs** (recent API calls)
- **Error logs** (failed requests)
- **Export logs** button

### 12.3 Cache Management
- **Clear conversation cache**
- **Clear model list cache**
- **Force reload** button

---

## INTERFACE LAYOUT STRUCTURE

```
┌─────────────────────────────────────────────────────────────────┐
│  HEADER: Logo | Model Selector | Status | Settings | User Menu │
├──────────────────┬──────────────────────────────┬───────────────┤
│                  │                              │               │
│  CONVERSATION    │        CHAT AREA             │   CONTEXT     │
│  SIDEBAR         │        (Main)                │   PANEL       │
│                  │                              │   (Collapsible)│
│  - Search        │   ┌──────────────────────┐   │               │
│  - New Chat      │   │  AI Message          │   │   - Files     │
│  - History List  │   └──────────────────────┘   │   - Tools     │
│                  │   ┌──────────────────────┐   │   - Token     │
│  [Folder Tree]   │   │  User Message        │   │     Count     │
│                  │   └──────────────────────┘   │               │
│                  │                              │               │
│                  │   [Input Area + Send]        │               │
│                  │   [Attached Files Row]       │               │
│                  │                              │               │
├──────────────────┴──────────────────────────────┴───────────────┤
│  FOOTER: Token Count | Cost | Gateway Status | Version          │
└─────────────────────────────────────────────────────────────────┘
```

---

## MOBILE LAYOUT STRUCTURE

```
┌─────────────────────────────────┐
│  HEADER: Menu | Model | Settings│
├─────────────────────────────────┤
│                                 │
│         CHAT AREA               │
│         (Full Screen)           │
│                                 │
├─────────────────────────────────┤
│  [Input] [Mic] [Send]           │
├─────────────────────────────────┤
│  [Chat] [Models] [Keys] [More]  │  ← Bottom Tab Bar
└─────────────────────────────────┘
```

---

## DESIGN NOTES FOR DESIGNER

1. **Color Scheme**: Dark mode primary (cyberpunk/professional feel)
   - Primary: Peacock Blue (#0066CC)
   - Accent: Gold (#FFD700) for highlights
   - Success: Green (#00C851)
   - Warning: Orange (#FF8800)
   - Error: Red (#CC0000)
   - Frozen: Ice Blue (#00BFFF)

2. **Typography**: Monospace for code, sans-serif for UI

3. **Animations**:
   - Smooth transitions between views
   - Typing indicator for streaming
   - Loading spinners for async operations
   - Toast notifications for actions

4. **Accessibility**:
   - High contrast mode option
   - Screen reader support
   - Keyboard navigation
   - Focus indicators

5. **Responsive Breakpoints**:
   - Mobile: < 768px (single column, bottom nav)
   - Tablet: 768px - 1024px (collapsible sidebars)
   - Desktop: > 1024px (full 3-panel layout)

---

## PRIORITY TIERS

**P0 (Must Have for MVP)**
- Core chat interface (1.1, 1.2)
- File upload (2.1)
- Model selection (1.2)
- Token/cost display (4.1)
- Mobile responsive (10.x)

**P1 (Should Have)**
- Tool calling (3.x)
- Conversation history (2.3)
- Model registry view (5.1)
- Key management (6.x)
- Settings panel (8.x)

**P2 (Nice to Have)**
- Batch operations (9.2)
- Advanced admin panel (12.x)
- Prompt templates (9.3)
- Detailed cost dashboard (4.2)

---

**END OF SPECIFICATION**

Once you have the design mockups, bring them to me and I'll wire up all the functionality!
