# Markdown to PDF Converter

A production-grade Markdown to PDF converter with syntax highlighting, custom CSS support, and professional formatting.

## Features

- **Multiple Themes**: Choose from default, GitHub, or academic styles
- **Syntax Highlighting**: Automatic code highlighting with Pygments
- **Custom CSS**: Apply your own styling
- **Table of Contents**: Auto-generate TOC with navigation
- **Page Numbers**: Optional page numbering
- **Landscape Mode**: Support for landscape orientation
- **Professional Output**: High-quality PDF generation with WeasyPrint

## Installation

### Quick Setup

Run the setup script to automatically install dependencies:

```bash
bash setup.sh
```

### Manual Installation

1. Install system dependencies:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
```

**macOS:**
```bash
brew install cairo pango gdk-pixbuf libffi
```

2. Install Python packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python markdown_to_pdf.py input.md
```

### Advanced Options

```bash
# Specify output file
python markdown_to_pdf.py input.md -o output.pdf

# Use different theme
python markdown_to_pdf.py input.md -t academic

# Add table of contents and page numbers
python markdown_to_pdf.py input.md --toc --page-numbers

# Use custom CSS
python markdown_to_pdf.py input.md -c styles/custom.css

# Landscape orientation
python markdown_to_pdf.py input.md --landscape
```

### Available Themes

- `default` - Clean, modern design
- `github` - GitHub-style formatting
- `academic` - Professional academic paper style

## Examples

Check the `examples/` directory for sample Markdown files and their PDF output.

## Project Structure

```
.
├── markdown_to_pdf.py    # Main converter script
├── requirements.txt      # Python dependencies
├── setup.sh             # Installation script
├── README.md            # This file
├── styles/              # Custom CSS files
│   └── custom.css
└── examples/            # Sample files
    ├── sample.md
    └── sample_output.pdf
```

## License

MIT License
