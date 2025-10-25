#!/usr/bin/env python3
"""
Markdown to PDF Converter
A production-grade converter with syntax highlighting, custom CSS, and professional formatting.

Usage:
    python markdown_to_pdf.py input.md [options]
    
Options:
    -o, --output       Output PDF filename (default: input_name.pdf)
    -c, --css          Custom CSS file path
    -t, --theme        Built-in theme: default, github, academic (default: github)
    --toc              Include table of contents
    --page-numbers     Add page numbers
    --landscape        Use landscape orientation
    
Examples:
    python markdown_to_pdf.py README.md
    python markdown_to_pdf.py doc.md -o report.pdf --toc --page-numbers
    python markdown_to_pdf.py notes.md -c custom.css
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import re

# Third-party imports
try:
    import markdown
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
    from pygments.formatters import HtmlFormatter
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install required packages: pip install markdown weasyprint pygments")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MarkdownPDFConverter:
    """Production-grade Markdown to PDF converter with advanced features."""
    
    # Built-in themes
    THEMES = {
        'default': """
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 2rem;
                font-size: 16px;
            }
            h1, h2, h3, h4, h5, h6 {
                margin-top: 1.5em;
                margin-bottom: 0.5em;
                font-weight: 600;
            }
            h1 { font-size: 2em; border-bottom: 2px solid #e1e4e8; padding-bottom: 0.3em; }
            h2 { font-size: 1.5em; border-bottom: 1px solid #e1e4e8; padding-bottom: 0.2em; }
            h3 { font-size: 1.25em; }
            code {
                background-color: #f6f8fa;
                padding: 0.2em 0.4em;
                border-radius: 3px;
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
                font-size: 0.85em;
            }
            pre {
                background-color: #f6f8fa;
                padding: 16px;
                overflow: auto;
                border-radius: 6px;
                line-height: 1.45;
            }
            pre code {
                background-color: transparent;
                padding: 0;
            }
            blockquote {
                border-left: 4px solid #dfe2e5;
                padding: 0 1em;
                color: #6a737d;
                margin: 1em 0;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
            }
            table th, table td {
                border: 1px solid #dfe2e5;
                padding: 8px 12px;
                text-align: left;
            }
            table th {
                background-color: #f6f8fa;
                font-weight: 600;
            }
            table tr:nth-child(even) {
                background-color: #f9fbfc;
            }
            a {
                color: #0366d6;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            img {
                max-width: 100%;
                height: auto;
            }
            ul, ol {
                padding-left: 2em;
                margin: 1em 0;
            }
            li {
                margin: 0.25em 0;
            }
            hr {
                border: none;
                border-top: 2px solid #e1e4e8;
                margin: 2em 0;
            }
        """,
        
        'github': """
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
                font-size: 16px;
                line-height: 1.7;
                color: #24292f;
                background-color: #ffffff;
                max-width: 980px;
                margin: 0 auto;
                padding: 32px;
            }
            h1, h2, h3, h4, h5, h6 {
                margin-top: 24px;
                margin-bottom: 16px;
                font-weight: 600;
                line-height: 1.25;
            }
            h1 {
                font-size: 2em;
                border-bottom: 1px solid #d1d9e0;
                padding-bottom: 0.3em;
            }
            h2 {
                font-size: 1.5em;
                border-bottom: 1px solid #eaecef;
                padding-bottom: 0.3em;
            }
            h3 { font-size: 1.25em; }
            h4 { font-size: 1em; }
            h5 { font-size: 0.875em; }
            h6 { font-size: 0.85em; color: #57606a; }
            pre {
                background-color: #f6f8fa;
                border-radius: 6px;
                padding: 16px;
                overflow: auto;
                font-size: 85%;
                line-height: 1.45;
            }
            code {
                background-color: rgba(175, 184, 193, 0.2);
                padding: 0.2em 0.4em;
                border-radius: 3px;
                font-family: ui-monospace, SFMono-Regular, 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace;
                font-size: 85%;
            }
            pre code {
                background: transparent;
                padding: 0;
                font-size: 100%;
            }
            blockquote {
                border-left: 0.25em solid #d0d7de;
                color: #57606a;
                padding: 0 1em;
                margin: 0 0 16px 0;
            }
            table {
                border-spacing: 0;
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 16px;
            }
            table th {
                font-weight: 600;
                padding: 6px 13px;
                border: 1px solid #d1d9e0;
                background-color: #f6f8fa;
            }
            table td {
                padding: 6px 13px;
                border: 1px solid #d1d9e0;
            }
            table tr:nth-child(2n) {
                background-color: #f9fbfc;
            }
            ul, ol {
                padding-left: 2em;
                margin-bottom: 16px;
            }
            ul ul, ul ol, ol ul, ol ol {
                margin-bottom: 0;
            }
            li + li {
                margin-top: 0.25em;
            }
            a {
                color: #0969da;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            img {
                max-width: 100%;
                box-sizing: content-box;
                background-color: #ffffff;
            }
            hr {
                height: 0.25em;
                padding: 0;
                margin: 24px 0;
                background-color: #d1d9e0;
                border: 0;
            }
        """,
        
        'academic': """
            @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600&family=Source+Sans+Pro:wght@400;600&display=swap');
            body {
                font-family: 'Crimson Text', Georgia, serif;
                font-size: 11pt;
                line-height: 1.8;
                color: #000;
                max-width: 6.5in;
                margin: 1in auto;
                text-align: justify;
                hyphens: auto;
            }
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Source Sans Pro', 'Helvetica Neue', Arial, sans-serif;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
                font-weight: 600;
                text-align: left;
            }
            h1 {
                font-size: 18pt;
                margin-top: 0;
                text-align: center;
            }
            h2 { font-size: 14pt; }
            h3 { font-size: 12pt; }
            h4 { font-size: 11pt; }
            p {
                margin-bottom: 1em;
                text-indent: 0.5in;
            }
            p:first-of-type,
            h1 + p, h2 + p, h3 + p, h4 + p, h5 + p, h6 + p,
            blockquote + p {
                text-indent: 0;
            }
            code {
                font-family: 'Courier New', Courier, monospace;
                font-size: 10pt;
                background-color: #f5f5f5;
                padding: 0.1em 0.2em;
            }
            pre {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                padding: 0.5em;
                overflow-x: auto;
                font-size: 10pt;
                margin: 1em 0;
            }
            blockquote {
                margin: 1em 0.5in;
                font-size: 10pt;
                line-height: 1.5;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
                font-size: 10pt;
            }
            table caption {
                margin-bottom: 0.5em;
                font-weight: 600;
            }
            table th, table td {
                border: 1px solid #000;
                padding: 0.3em 0.5em;
                text-align: left;
            }
            table th {
                background-color: #f0f0f0;
                font-weight: 600;
            }
            ul, ol {
                margin: 1em 0;
                padding-left: 2em;
            }
            a {
                color: #000;
                text-decoration: underline;
            }
            hr {
                border: none;
                border-top: 1px solid #000;
                margin: 2em 0;
            }
            @page {
                size: letter;
                margin: 1in;
                @bottom-center {
                    content: counter(page);
                    font-size: 10pt;
                }
            }
        """
    }
    
    def __init__(self, theme: str = 'github', custom_css: Optional[str] = None):
        """
        Initialize converter with theme and optional custom CSS.
        
        Args:
            theme: Built-in theme name ('default', 'github', 'academic')
            custom_css: Path to custom CSS file
        """
        self.theme = theme
        self.custom_css = custom_css
        self.font_config = FontConfiguration()
        
        # Configure markdown extensions
        self.md_extensions = [
            'extra',           # Tables, footnotes, abbreviations
            'codehilite',      # Syntax highlighting
            'toc',             # Table of contents
            'meta',            # Metadata support
            'admonition',      # Note/warning blocks
            'nl2br',           # New line to break
            'sane_lists',      # Better list handling
            'smarty',          # Smart quotes
            'attr_list',       # Attribute lists
            'def_list',        # Definition lists
            'fenced_code',     # Fenced code blocks
            'tables',          # Tables support
        ]
        
        # Configure code highlighting
        self.md_extension_configs = {
            'codehilite': {
                'css_class': 'highlight',
                'linenums': False,
                'guess_lang': True,
            },
            'toc': {
                'permalink': True,
                'permalink_class': 'toc-link',
                'toc_depth': 3,
            }
        }
    
    def get_css(self) -> str:
        """
        Get CSS content based on theme and custom CSS.
        
        Returns:
            Combined CSS string
        """
        # Start with base theme
        css_content = self.THEMES.get(self.theme, self.THEMES['default'])
        
        # Add syntax highlighting CSS
        pygments_css = HtmlFormatter(style='default').get_style_defs('.highlight')
        css_content += '\n' + pygments_css
        
        # Add custom CSS if provided
        if self.custom_css:
            try:
                with open(self.custom_css, 'r', encoding='utf-8') as f:
                    custom_content = f.read()
                    css_content += '\n/* Custom CSS */\n' + custom_content
                    logger.info(f"Loaded custom CSS from {self.custom_css}")
            except Exception as e:
                logger.warning(f"Could not load custom CSS: {e}")
        
        return css_content
    
    def preprocess_markdown(self, content: str) -> str:
        """
        Preprocess markdown content for better PDF rendering.
        
        Args:
            content: Raw markdown content
            
        Returns:
            Preprocessed markdown
        """
        # Fix common issues
        
        # Ensure proper spacing around code blocks
        content = re.sub(r'```(\w*)\n', r'\n```\1\n', content)
        content = re.sub(r'\n```', r'\n\n```', content)
        
        # Fix table formatting
        content = re.sub(r'\|(?=[^\n]*\|)', r'|', content)
        
        # Ensure images have alt text
        content = re.sub(r'!\[\]\(([^)]+)\)', r'![Image](\1)', content)
        
        return content
    
    def add_page_numbers(self, html: str) -> str:
        """
        Add page numbers to HTML for PDF.
        
        Args:
            html: HTML content
            
        Returns:
            HTML with page number CSS
        """
        page_css = """
        <style>
            @page {
                @bottom-center {
                    content: counter(page);
                    font-size: 10pt;
                    color: #666;
                }
            }
            @page :first {
                @bottom-center {
                    content: '';
                }
            }
        </style>
        """
        return html.replace('</head>', page_css + '</head>')
    
    def add_table_of_contents(self, html: str, toc_html: str) -> str:
        """
        Add table of contents to HTML.
        
        Args:
            html: Main HTML content
            toc_html: TOC HTML from markdown
            
        Returns:
            HTML with TOC
        """
        toc_section = f"""
        <div class="toc">
            <h2>Table of Contents</h2>
            {toc_html}
        </div>
        <div style="page-break-after: always;"></div>
        """
        
        # Insert TOC after body tag
        return html.replace('<body>', f'<body>{toc_section}')
    
    def convert(
        self,
        input_file: Path,
        output_file: Path,
        include_toc: bool = False,
        page_numbers: bool = False,
        landscape: bool = False
    ) -> None:
        """
        Convert markdown file to PDF.
        
        Args:
            input_file: Path to markdown file
            output_file: Path for output PDF
            include_toc: Include table of contents
            page_numbers: Add page numbers
            landscape: Use landscape orientation
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            Exception: For conversion errors
        """
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        logger.info(f"Converting {input_file} to {output_file}")
        
        try:
            # Read markdown content
            with open(input_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Preprocess markdown
            md_content = self.preprocess_markdown(md_content)
            
            # Initialize markdown converter
            md = markdown.Markdown(
                extensions=self.md_extensions,
                extension_configs=self.md_extension_configs
            )
            
            # Convert to HTML
            html_body = md.convert(md_content)
            
            # Get TOC if needed
            toc_html = ""
            if include_toc and hasattr(md, 'toc'):
                toc_html = md.toc
            
            # Build complete HTML document
            html_template = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{input_file.stem}</title>
                <style>
                    {self.get_css()}
                </style>
            </head>
            <body>
                {html_body}
            </body>
            </html>
            """
            
            # Add table of contents if requested
            if include_toc and toc_html:
                html_template = self.add_table_of_contents(html_template, toc_html)
            
            # Add page numbers if requested
            if page_numbers:
                html_template = self.add_page_numbers(html_template)
            
            # Prepare CSS for WeasyPrint
            css_list = [CSS(string=self.get_css())]
            
            # Add landscape CSS if needed
            if landscape:
                landscape_css = CSS(string="@page { size: landscape; }")
                css_list.append(landscape_css)
            
            # Convert HTML to PDF
            html_doc = HTML(
                string=html_template,
                base_url=str(input_file.parent),
                encoding='utf-8'
            )
            
            html_doc.write_pdf(
                output_file,
                stylesheets=css_list,
                font_config=self.font_config
            )
            
            logger.info(f"Successfully created PDF: {output_file}")
            
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            raise


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='Convert Markdown files to PDF with professional formatting',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        'input',
        type=str,
        help='Input markdown file'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Output PDF file (default: input_name.pdf)'
    )
    
    parser.add_argument(
        '-t', '--theme',
        type=str,
        choices=['default', 'github', 'academic'],
        default='github',
        help='Built-in theme (default: github)'
    )
    
    parser.add_argument(
        '-c', '--css',
        type=str,
        help='Custom CSS file path'
    )
    
    parser.add_argument(
        '--toc',
        action='store_true',
        help='Include table of contents'
    )
    
    parser.add_argument(
        '--page-numbers',
        action='store_true',
        help='Add page numbers'
    )
    
    parser.add_argument(
        '--landscape',
        action='store_true',
        help='Use landscape orientation'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Configure logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Prepare file paths
    input_file = Path(args.input)
    
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = input_file.with_suffix('.pdf')
    
    # Initialize converter
    converter = MarkdownPDFConverter(
        theme=args.theme,
        custom_css=args.css
    )
    
    try:
        # Perform conversion
        converter.convert(
            input_file=input_file,
            output_file=output_file,
            include_toc=args.toc,
            page_numbers=args.page_numbers,
            landscape=args.landscape
        )
        
        print(f"✓ PDF created successfully: {output_file}")
        
    except FileNotFoundError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Conversion failed: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
