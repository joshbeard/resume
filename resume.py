#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Build script for my resume
#
# This sources the "resume.yaml" and produces the resume in several formats
# from Jinja2 templates, including HTML, plain text, Markdown, and Gemini.
# -----------------------------------------------------------------------------
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import json
import markdown
import os
import re
import sys
import yaml
from enum import Enum, auto


class Format(Enum):
    RAW = auto()
    PLAIN = auto()
    HTML = auto()


@dataclass
class FormatConfig:
    template: str
    out: str
    css_src: Optional[str] = None
    narrow_template: Optional[str] = None
    narrow_out: Optional[str] = None


@dataclass
class AppConfig:
    template_dir: Path
    resume_yaml: Path
    html: FormatConfig
    markdown: FormatConfig
    gemini: FormatConfig
    txt: FormatConfig
    json: FormatConfig

    @classmethod
    def from_env(cls) -> 'AppConfig':
        """Create config from environment variables with defaults."""
        return cls(
            template_dir=Path(os.environ.get('RESUME_TEMPLATE_DIR', 'templates')),
            resume_yaml=Path(os.environ.get('RESUME_YAML', 'resume.yaml')),
            html=FormatConfig(
                template=os.environ.get('RESUME_HTML_TEMPLATE', 'resume.html'),
                out=os.environ.get('RESUME_HTML_OUT', 'dist/index.html'),
                css_src=os.environ.get('RESUME_CSS_TEMPLATE', 'style.css'),
            ),
            markdown=FormatConfig(
                template=os.environ.get('RESUME_MD_TEMPLATE', 'resume.md'),
                out=os.environ.get('RESUME_MD_OUT', 'README.md'),
            ),
            gemini=FormatConfig(
                template=os.environ.get('RESUME_GMI_TEMPLATE', 'resume.gmi'),
                out=os.environ.get('RESUME_GMI_OUT', 'dist/resume.gmi'),
            ),
            txt=FormatConfig(
                template=os.environ.get('RESUME_TXT_TEMPLATE', 'resume.txt'),
                out=os.environ.get('RESUME_TXT_OUT', 'dist/resume.txt'),
                narrow_template=os.environ.get('RESUME_TXT_NARROW_TEMPLATE', 'resume-narrow.txt'),
                narrow_out=os.environ.get('RESUME_TXT_NARROW_OUT', 'dist/resume-narrow.txt'),
            ),
            json=FormatConfig(
                template='',  # JSON doesn't need a template
                out=os.environ.get('RESUME_JSON_OUT', 'dist/resume.json'),
            )
        )


class ResumeBuilder:
    def __init__(self, config: AppConfig):
        self.config = config
        self.base_dir = Path(__file__).parent
        self.year = datetime.datetime.now().strftime("%Y")

    @staticmethod
    def md_strip(text: str) -> str:
        """Remove Markdown URLs and emphasis from text."""
        text = re.sub(r"\[([\w\s]+)\]\([\w\d\/\-\.:]+\)", r"\1", text)
        text = re.sub(r"(\s+)__?(.*)__?(\s+)?", r"\1\2\3", text)
        return text

    def load_resume(self, output_format: Format) -> Dict:
        """Load and process resume data based on output format."""
        with open(self.config.resume_yaml) as f:
            data = yaml.safe_load(f)

        if output_format == Format.RAW:
            return data

        for job in data.get('experience', []):
            if 'details' in job:
                details = []
                for detail in job['details']:
                    if output_format == Format.PLAIN:
                        details.append(self.md_strip(detail))
                    elif output_format == Format.HTML:
                        html = markdown.markdown(detail, output_format='html5')
                        details.append(html)
                job['details'] = details

        return data

    def load_css(self) -> str:
        """Load CSS content."""
        css_path = self.config.template_dir / self.config.html.css_src
        return css_path.read_text()

    def render_template(self, template_name: str, output_format: Format) -> str:
        """Render a Jinja2 template."""
        env = Environment(
            loader=FileSystemLoader(self.config.template_dir),
            autoescape=select_autoescape(enabled_extensions=('html')),
            extensions=['jinja2.ext.do', 'jinja2.ext.loopcontrols']
        )
        env.filters['safe'] = lambda x: x

        template = env.get_template(template_name)
        return template.render(
            resume=self.load_resume(output_format),
            css=self.load_css() if template_name == self.config.html.template else None,
            year=self.year
        )

    def write_output(self, content: str, output_path: Union[str, Path]) -> None:
        """Write content to output file."""
        output_path = self.base_dir / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)
        print(f"-> Wrote {output_path}")

    def generate_html(self) -> None:
        """Generate HTML resume."""
        content = self.render_template(self.config.html.template, Format.HTML)
        self.write_output(content, self.config.html.out)

    def generate_markdown(self) -> None:
        """Generate Markdown resume."""
        content = self.render_template(self.config.markdown.template, Format.RAW)
        self.write_output(content, self.config.markdown.out)

    def generate_gemini(self) -> None:
        """Generate Gemini resume."""
        content = self.render_template(self.config.gemini.template, Format.PLAIN)
        self.write_output(content, self.config.gemini.out)

    def generate_txt(self) -> None:
        """Generate text resume versions."""
        content = self.render_template(self.config.txt.template, Format.PLAIN)
        self.write_output(content, self.config.txt.out)

        if self.config.txt.narrow_template and self.config.txt.narrow_out:
            narrow_content = self.render_template(self.config.txt.narrow_template, Format.PLAIN)
            self.write_output(narrow_content, self.config.txt.narrow_out)

    def generate_json(self) -> None:
        """Generate JSON resume."""
        content = json.dumps(self.load_resume(Format.PLAIN), indent=2)
        self.write_output(content, self.config.json.out)

    def build_all(self) -> None:
        """Generate all resume formats."""
        self.generate_html()
        self.generate_markdown()
        self.generate_gemini()
        self.generate_txt()
        self.generate_json()


def main():
    config = AppConfig.from_env()
    builder = ResumeBuilder(config)

    actions = {
        'all': builder.build_all,
        'html': builder.generate_html,
        'md': builder.generate_markdown,
        'markdown': builder.generate_markdown,
        'gmi': builder.generate_gemini,
        'gemini': builder.generate_gemini,
        'txt': builder.generate_txt,
        'text': builder.generate_txt,
        'gopher': builder.generate_txt,
        'json': builder.generate_json,
    }

    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action in actions:
            actions[action]()
        elif action in ['-h', '--help', 'help']:
            print(f"{sys.argv[0]} [{ ' | '.join(actions.keys()) }]")
        else:
            print(f"Unknown argument: {action}")
            print(f"{sys.argv[0]} [{ ' | '.join(actions.keys()) }]")
    else:
        print("Building everything")
        builder.build_all()


if __name__ == '__main__':
    main()
