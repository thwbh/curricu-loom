"""CV Generator - Generate PDF CVs from YAML data."""

import argparse
import base64
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS


def load_cv_data(yaml_path: Path) -> dict:
    """Load CV data from a YAML file."""
    with open(yaml_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_avatar_base64(avatar_path: Path, base_path: Path) -> str | None:
    """Load avatar image and convert to base64."""
    if not avatar_path:
        return None

    # Handle relative paths
    if not avatar_path.is_absolute():
        avatar_path = base_path / avatar_path

    if not avatar_path.exists():
        print(f"Warning: Avatar file not found: {avatar_path}", file=sys.stderr)
        return None

    with open(avatar_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def render_html(data: dict, template_dir: Path, avatar_base64: str | None) -> str:
    """Render the CV data to HTML using Jinja2."""
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("cv.html")

    # Default style configuration
    default_style = {
        "colors": {
            "primary": "#1e3a5f",
            "sidebar_bg": "#1e3a5f",
            "sidebar_text": "#ffffff",
            "body_text": "#333333",
            "muted_text": "#666666",
        },
        "fonts": {
            "main": "Helvetica Neue, Helvetica, Arial, sans-serif",
        },
        "spacing": {
            "sidebar_width": "35%",
            "page_padding": "12mm",
        },
    }

    # Merge user style with defaults
    user_style = data.get("style", {})
    style = {
        "colors": {**default_style["colors"], **user_style.get("colors", {})},
        "fonts": {**default_style["fonts"], **user_style.get("fonts", {})},
        "spacing": {**default_style["spacing"], **user_style.get("spacing", {})},
    }

    return template.render(
        personal=data.get("personal", {}),
        experience=data.get("experience", []),
        education=data.get("education", []),
        certificates=data.get("certificates", []),
        projects=data.get("projects", []),
        skills=data.get("skills", {}),
        languages=data.get("languages", []),
        interests=data.get("interests", []),
        avatar_base64=avatar_base64,
        style=style,
    )


def generate_pdf(html_content: str, css_path: Path, output_path: Path) -> None:
    """Generate PDF from HTML content."""
    css = CSS(filename=str(css_path))
    html = HTML(string=html_content)
    html.write_pdf(output_path, stylesheets=[css])


def generate_cv(
    yaml_path: Path,
    output_path: Path,
    template_dir: Path | None = None,
) -> None:
    """Generate a CV PDF from YAML data.

    Args:
        yaml_path: Path to the YAML file containing CV data
        output_path: Path where the PDF will be saved
        template_dir: Optional custom template directory
    """
    # Use default template directory if not specified
    if template_dir is None:
        template_dir = Path(__file__).parent / "templates"

    css_path = template_dir / "style.css"

    # Load data
    data = load_cv_data(yaml_path)

    # Load avatar if specified
    avatar_base64 = None
    if personal := data.get("personal"):
        if avatar_path := personal.get("avatar"):
            avatar_base64 = load_avatar_base64(
                Path(avatar_path),
                yaml_path.parent,
            )

    # Render HTML
    html_content = render_html(data, template_dir, avatar_base64)

    # Generate PDF
    generate_pdf(html_content, css_path, output_path)

    print(f"CV generated: {output_path}")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate PDF CV from YAML data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cv-generate data/cv.yaml output/cv.pdf
  cv-generate data/cv.yaml output/cv.pdf --template ./custom-templates
        """,
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Path to the YAML file containing CV data",
    )
    parser.add_argument(
        "output",
        type=Path,
        help="Path where the PDF will be saved",
    )
    parser.add_argument(
        "--template",
        "-t",
        type=Path,
        default=None,
        help="Custom template directory (default: built-in templates)",
    )

    args = parser.parse_args()

    # Validate input file exists
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Create output directory if needed
    args.output.parent.mkdir(parents=True, exist_ok=True)

    try:
        generate_cv(args.input, args.output, args.template)
    except Exception as e:
        print(f"Error generating CV: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
