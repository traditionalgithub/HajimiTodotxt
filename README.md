# HajimiTodotxt

![HajimiTodotxt Banner](banner.png)

[English](README.md) | [繁體中文](README_zht.md) | [简体中文](README_zhs.md)

---

### Overview

HajimiTodotxt is a lightweight, local-first task management tool built as a single-page web application. It follows [the todo.txt format](https://github.com/todotxt/todo.txt) with extensions, providing a clean interface for managing your tasks, projects, and deadlines.  

About the project name: This project was originally created as a personal interest project to test Gemini 3.1 Pro performance, hence the name. However, the current banner image was not generated using Nano Banana.  

This project uses free AI computing power as much as possible for generation.  

### First, what is todo.txt?

[todo.txt](https://github.com/todotxt/todo.txt) is a **plain-text task management format** started by Gina Trapani — and the inspiration for this project. Its first and most important rule is simple:

> **A single line in your todo.txt text file represents a single task.**

There are no databases, no vendor-specific software, and no importing/exporting — tasks live in a plain text file called `todo.txt` that any text editor can read and edit directly. Because plain text isn't tied to any operating system or software, it is **searchable, portable, lightweight, and easy to manipulate**; even if some cloud service goes down, your task list stays intact.

Using special notation, todo.txt lets you slice your list along three key axes:

- **Priority**: `(A)`–`(Z)`, with `(A)` being most important, so you can see at a glance what to do next
- **Project**: `+Project`, e.g. `+GarageSale`, to list all tasks belonging to a project
- **Context**: `@context`, e.g. `@home`, `@office`, `@phone`, inspired by David Allen's *Getting Things Done*, categorizing tasks by place and situation

**Format rules:**

| Element | Format | Description |
|---------|--------|-------------|
| Priority | `(A)`–`(Z)` | If present, it **always** appears first |
| Creation date | `YYYY-MM-DD` | Optional, directly after the priority |
| Completion marker | `x` | Completed tasks start with a **lowercase** `x`, followed by the completion date |
| Project tag | `+Project` | Zero or more, appearing after the priority/date |
| Context tag | `@context` | Zero or more |
| Additional fields | `key:value` | For extensions, e.g. `due:2026-04-10` for a due date |

**Complete example:**

```
x 2011-03-02 2011-03-01 Review Tim's pull request +TodoTxtTouch @github
```

This task was created on 2011-03-01 and completed on 2011-03-02, belonging to the `+TodoTxtTouch` project and the `@github` context.

Because todo.txt is plain text, it is especially well suited to:

- **Portability**: readable and writable on any system with any editor; great for Git version control
- **Sync**: easy cross-device sync with tools like Syncthing and Rclone
- **Longevity**: plain text never goes out of date, with no vendor lock-in
- **Ecosystem**: dozens of compatible CLI, desktop, and mobile apps to choose from

HajimiTodotxt keeps that elegant "plain text, one task per line" spirit while adding extensions like hierarchical projects and recurring tasks — which is what the next section is about.

### What's different from the original todo.txt format?

HajimiTodotxt is compatible with the core todo.txt spec (`(A)` priority, creation date, `x` completion marker, `+project`, `@context`), but adds extensive extensions on top of it. The main differences are:

**Note: some features may not be implemented in other todo.txt tools.**

**1. Extended fields (metadata not in the original format)**

| Field | Description |
|-------|-------------|
| `t:YYYY-MM-DD` | Threshold (hidden) date: tasks are hidden by default until this date, shown with a dashed border and reduced opacity |
| `rec:...` | Recurrence rule: automatically generates the next task when a task is completed |
| `desc:"..."` | Multi-line detailed description: fill `"..."` with a multi-line description to record task hints (e.g. a relevant URL) or implementation steps directly on the task. Using `\n` for line breaks; input containing `\n` will automatically get `\` prepended for character escaping |
| `id:...` | ID field (from older versions, only written when `show_id=true`, planned for future deprecation) |

Note: the `desc` field **may not be supported by other todo.txt tools**. 

**2. Hierarchical projects**
- The original todo.txt only has flat `+Project`; HajimiTodotxt supports `+Project.SubProject.SubSubProject` at any depth, following the multi-level `+project.subproject` idea from [TaskWarrior](https://taskwarrior.org/)
- Project filters support wildcards: `+Project.*` (single level), `+**.SubProject` (any depth)
- Provides a tree view, a project overview, and click-to-filter on project segments

**3. Recurring tasks**
- The original todo.txt spec has no recurrence support at all; the common extension rule uses the `rec:` tag for this, and HajimiTodotxt is no exception:
  - `+1d` / `+1m` / `+1y`: repeat relative to today
  - `1d` (no prefix): repeat relative to the original due date
  - A bare number like `rec:5` is automatically treated as `rec:+5d`
  - `++1d` / `++1m` / `++1y`: **(may not be implemented in other todo.txt tools)** advance to the next occurrence greater than today (stepping from the original due date), implementing the `++` syntax from [org-mode](https://orgmode.org/)
- Completing a task with `rec:` automatically creates the next occurrence; if `t:` is also set, its relative distance to `due:` is preserved
- The `---REPEAT-ABOVE---` / `---REPEAT-COPY---` markers inside the description control which content is copied to the next recurring task with a `rec:` tag

**4. Today-task marker**
Similar to the "My Day" feature of [MS To Do](https://en.wikipedia.org/wiki/Microsoft_To_Do) and [Super Productivity](https://github.com/super-productivity/super-productivity)
- A special `@☀️.YYYYMMDD` context tag marks a task for today and is automatically hidden from display
- Visual indicators: ☀️ for today, 😱 for overdue, 🌙 for future

**5. Search / filter syntax**
- Date comparisons: `<today`, `<=tomorrow`, `>2026-08-10`, to quickly filter tasks before or after a given date
- Priority expressions: `pri=A`, `pri<C`, `pri=A-C` (range), `pri=A,B` (list), `pri=!` (no priority)
- Project wildcard filters and click-to-filter on context tags

**6. Other differences**
- Tasks are addressed by line number (array index), not by ID
- `todo.rc` config supports complex JSON structures (`sort_keys`, `saved_filters`, `opacity`, etc.)
- Server layer: random token authentication, atomic writes (temp file + rename), localhost-only CORS, CSRF protection

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