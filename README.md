# curriculoom

Weave your CV! Generate PDF CVs from YAML data.

## Prerequisites

```bash
# macOS - install system dependencies (one-time)
brew install pango uv
```

> **Why pango?** WeasyPrint (the PDF engine) requires the Pango text rendering library.

## Usage

```bash
# Generate CV
uv run cv-generate data/cv.yaml output/cv.pdf
```

That's it. On first run, uv will:
1. Install the correct Python version
2. Create a virtual environment
3. Install pinned dependencies from `uv.lock`

## Customization

Edit `data/cv.yaml` to change:

- **Content**: name, experience, education, projects, etc.
- **Styling**: colors, fonts, spacing

```yaml
style:
  colors:
    primary: "#1e3a5f"      # Accent color
    sidebar_bg: "#1e3a5f"   # Sidebar background
    sidebar_text: "#ffffff" # Sidebar text
  fonts:
    main: "Helvetica Neue, Helvetica, Arial, sans-serif"
  spacing:
    sidebar_width: "35%"
    page_padding: "12mm"
```

## Project Structure

```
├── data/cv.yaml              # Your CV content + styling
├── cv_generator/
│   ├── generator.py          # PDF generation logic
│   └── templates/
│       ├── cv.html           # Jinja2 template
│       └── style.css         # Styling
├── output/                   # Generated PDFs (gitignored)
├── pyproject.toml            # Project metadata
└── uv.lock                   # Pinned dependencies
```
