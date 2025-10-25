# Markdown to PDF Converter - Sample Document

## Introduction

This sample document demonstrates the various **Markdown features** supported by our converter. It includes examples of:

- Text formatting
- Code blocks with syntax highlighting
- Tables
- Lists
- Links and images
- Blockquotes
- And much more!

## Text Formatting

### Basic Formatting

You can use **bold text**, *italic text*, ***bold and italic***, and ~~strikethrough~~.

You can also use `inline code` for technical terms.

### Paragraphs and Line Breaks

This is the first paragraph. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

This is the second paragraph. Notice the spacing between paragraphs. You can also force  
a line break by ending a line with two spaces.

## Headers

### Level 3 Header

#### Level 4 Header

##### Level 5 Header

###### Level 6 Header

## Code Blocks

### Python Example

```python
def fibonacci(n):
    """Generate Fibonacci sequence up to n terms."""
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    
    sequence = [0, 1]
    for i in range(2, n):
        next_num = sequence[-1] + sequence[-2]
        sequence.append(next_num)
    
    return sequence

# Example usage
print(fibonacci(10))
# Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### JavaScript Example

```javascript
// Async function example
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching user data:', error);
        return null;
    }
}

// Usage
fetchUserData(123).then(user => {
    if (user) {
        console.log('User:', user);
    }
});
```

### SQL Example

```sql
-- Complex query with JOIN and aggregation
SELECT 
    c.customer_name,
    COUNT(o.order_id) as total_orders,
    SUM(o.total_amount) as total_spent,
    AVG(o.total_amount) as avg_order_value
FROM 
    customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE 
    o.order_date >= '2024-01-01'
GROUP BY 
    c.customer_id, c.customer_name
HAVING 
    COUNT(o.order_id) > 5
ORDER BY 
    total_spent DESC
LIMIT 10;
```

## Tables

### Simple Table

| Feature | Support | Notes |
|---------|---------|-------|
| Headers | ✓ | Multiple levels supported |
| **Bold** | ✓ | Works in tables |
| *Italic* | ✓ | Also works |
| `Code` | ✓ | Inline code supported |
| Links | ✓ | [Example](https://example.com) |

### Complex Table with Alignment

| Left Aligned | Center Aligned | Right Aligned | Number |
|:-------------|:--------------:|--------------:|-------:|
| Row 1        | Centered       | Right         | 123.45 |
| Row 2        | Also centered  | Also right    | 678.90 |
| Row 3        | Middle         | End           | 1011.12 |

### Performance Metrics Table

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Response Time | 245ms | <300ms | ✅ Pass |
| Error Rate | 0.02% | <0.1% | ✅ Pass |
| Throughput | 1,250 req/s | >1,000 req/s | ✅ Pass |
| CPU Usage | 78% | <80% | ⚠️ Warning |
| Memory Usage | 4.2 GB | <8 GB | ✅ Pass |

## Lists

### Unordered List

- First item
- Second item
  - Nested item 1
  - Nested item 2
    - Deeply nested item
- Third item
- Fourth item with **bold** and *italic*

### Ordered List

1. First step
2. Second step
   1. Sub-step A
   2. Sub-step B
3. Third step
4. Fourth step

### Task List

- [x] Completed task
- [x] Another completed task
- [ ] Pending task
- [ ] Future task

### Definition List

Term 1
:   Definition for term 1. This can span
    multiple lines.

Term 2
:   Definition for term 2 with *emphasis*.
:   Second definition for term 2.

## Blockquotes

> This is a blockquote. It can contain multiple paragraphs.
>
> Here's the second paragraph in the blockquote.
>
> > You can even nest blockquotes.
> > This is a nested quote.

## Links and References

### Inline Links

Visit [GitHub](https://github.com) for code hosting.
Check out [Google](https://www.google.com "Search Engine") with a title.

### Reference Links

This is [an example][1] reference-style link.
You can also use [link text itself].

[1]: https://www.example.com "Example Site"
[link text itself]: https://www.example.com

### Automatic Links

<https://www.example.com>
<user@example.com>

## Images

![Python Logo](https://www.python.org/static/img/python-logo.png)

### Image with Alt Text and Title

![Markdown Logo](https://markdown-here.com/img/icon256.png "Markdown Logo Title")

## Horizontal Rules

Three or more hyphens:

---

Three or more asterisks:

***

Three or more underscores:

___

## Advanced Features

### Footnotes

Here's a sentence with a footnote[^1].

You can also use inline footnotes^[This is an inline footnote.].

[^1]: This is the footnote text that appears at the bottom.

### Abbreviations

The HTML specification is maintained by the W3C.

*[HTML]: Hyper Text Markup Language
*[W3C]: World Wide Web Consortium

### Math (LaTeX)

When $a \ne 0$, there are two solutions to $(ax^2 + bx + c = 0)$:

$$x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$$

### Admonitions

!!! note "Important Note"
    This is an important note that stands out from the regular text.

!!! warning "Warning"
    Be careful with this operation!

!!! danger "Danger"
    This could be destructive!

!!! success "Success"
    Operation completed successfully!

## HTML in Markdown

<div class="center">
This text is centered using HTML.
</div>

<div class="page-break"></div>

## Emoji Support

Common emojis: 😀 😃 😄 😁 😆 😅 😂 🤣 ☺️ 😊

## Special Characters

Copyright © 2024  
Registered ®  
Trademark ™  
Ellipsis…  
En-dash – Em-dash —

## Code Output Examples

### JSON

```json
{
  "name": "Markdown to PDF Converter",
  "version": "1.0.0",
  "features": {
    "syntax_highlighting": true,
    "tables": true,
    "custom_css": true,
    "themes": ["default", "github", "academic"]
  },
  "requirements": [
    "markdown>=3.5.0",
    "weasyprint>=60.0",
    "pygments>=2.16.0"
  ]
}
```

### YAML

```yaml
application:
  name: Markdown to PDF Converter
  version: 1.0.0
  
features:
  - syntax_highlighting
  - table_support
  - custom_css
  - multiple_themes
  
configuration:
  theme: github
  page_numbers: true
  toc: true
  
output:
  format: pdf
  quality: high
```

## Conclusion

This document has demonstrated the comprehensive feature set of our Markdown to PDF converter. The converter supports:

1. **Complete Markdown Syntax**: All standard Markdown features plus extensions
2. **Syntax Highlighting**: Beautiful code blocks with language-specific highlighting
3. **Professional Formatting**: Multiple themes and custom CSS support
4. **Advanced Features**: Tables, footnotes, math, and more
5. **PDF Optimizations**: Page numbers, table of contents, and print-ready output

For more information, visit our [GitHub repository](https://github.com/example/markdown-to-pdf) or check the documentation.

---

*Generated by Markdown to PDF Converter v1.0.0*
