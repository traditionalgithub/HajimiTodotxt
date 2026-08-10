# HajimiTodotxt

![HajimiTodotxt Banner](banner.png)

[English](README.md) | [繁體中文](README_zht.md) | [简体中文](README_zhs.md)

---

### Overview

HajimiTodotxt is a lightweight, local-first task management tool built as a single-page web application. It follows the todo.txt format with extensions, providing a clean interface for managing your tasks, projects, and deadlines.  

About the project name: This project was originally created as a personal interest project to test Gemini 3.1 Pro performance, hence the name. However, the current banner image was not generated using Nano Banana.  

This project uses free AI computing power as much as possible for generation.  

**Key Features:**
- Hierarchical project system (`+Project.SubProject`)
- Context tags (`@context`) for task categorization
- Due dates and threshold dates
- Recurring tasks
- Today tasks with visual indicators
- 23 built-in themes
- Multi-language support (Traditional Chinese / English)
- Atomic file writes for data safety
- Mobile-responsive design

### Installation

#### Prerequisites
- Python 3.10 or higher
- No external dependencies required

#### Steps

```bash
# 1. Clone the repository
git clone https://github.com/traditionalgithub/HajimiTodotxt.git
cd HajimiTodotxt

# 2. Start the server
python server.py
```

The server will display a URL with an authentication token:
```
★ HajimiTodotxt Backend Service Launched!
★ Secure authentication link (please copy and open in browser):
   http://127.0.0.1:6888/?token=abc123def456...
```

### Usage

1. **Access the application**: Copy the URL from the terminal and open it in your browser
2. **Add tasks**: Click the ➕ button in the header
3. **Complete tasks**: Click the checkbox next to a task
4. **Filter tasks**: Use the search bar or click on project/context tags
5. **Sort tasks**: Click the 🔃 button to configure sorting

### Task Format

Tasks follow the todo.txt format with extensions:

```
[x YYYY-MM-DD] (Priority) YYYY-MM-DD Task Title +Project @Context due:YYYY-MM-DD t:YYYY-MM-DD rec:rec:+1d desc:"Description"
```

**Example tasks:**
```
(A) 2026-04-06 Write report +Work.Project due:2026-04-10 desc:"Final report"
(B) 2026-04-06 Math homework +School.Math due:2026-04-15 @Library
x 2026-04-05 (C) 2026-04-01 Completed task +Personal
```

### Configuration

Edit `todo.rc` to customize settings:

```ini
theme=nord-light                    # Theme selection (23 options)
confirm_delete=true                 # Confirm before deleting tasks
default_priority=(C)                # Default priority for new tasks
expand_projects=false               # Expand projects by default
click_action=filter                 # Click action: "filter" or "clipboard"
```

**Available themes:** neutral, dark, solarized-light, nord-light, sakura, mint, lavender, peach, cream, sky, matcha, linen, honey, seafoam, cloud, coral, solarized-dark, nord-dark, dim, forest, twilight, cocoa

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `+` | Add new task |
| `/` | Focus search bar |
| `Esc` | Close modals |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve index.html |
| `/api/read?file={todo\|done\|config}` | GET | Read file content |
| `/api/write` | POST | Write file content |

---

### Development

```bash
# Start development server
python server.py

# Access in browser
# Copy the displayed URL from terminal
```

### Project Structure

```
HajimiTodotxt/
├── index.html           # Frontend SPA (HTML/CSS/JS all inline)
├── server.py            # Python HTTP server
├── todo.txt             # Unfinished tasks
├── done.txt             # Completed tasks
├── todo.rc              # User configuration
└── lang/
    ├── zh-TW.json       # Traditional Chinese
    └── en.json          # English
```

### Data Synchronization

Sync your data across devices using tools like:
- [Syncthing](https://syncthing.net/)
- [Rclone](https://rclone.org/)

Sync these files:
- `todo.txt`
- `done.txt`
- `todo.rc`

---

**License:** [Blue Oak Model License 1.0.0](https://blueoakcouncil.org/license/1.0.0)
**Last Updated:** 2026-08-10