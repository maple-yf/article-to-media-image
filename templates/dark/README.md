# Dark Template

**Night Coding Theme**

A developer-focused dark mode template featuring GitHub-inspired color palette, code syntax highlighting, and terminal-style aesthetics perfect for technical content.

## Design Features

- **GitHub Dark Colors**: Authentic GitHub dark mode color scheme
- **Syntax Highlighting**: Keyword, string, function, variable colors
- **Terminal Aesthetic**: macOS-style window dots (red/yellow/green)
- **Code Comments**: JSDoc-style comment formatting
- **Glow Effect**: Subtle blue glow on title card
- **Monospace Font**: JetBrains Mono for consistent code display

## Color Scheme

```css
Backgrounds:
  Deep:    #0D1117 (GitHub dark background)
  Card:    #161B22 (Card background)
  Elevated: #21262D (Elevated elements)

Text:
  Primary:   #F0F6FC (White-ish)
  Secondary: #8B949E (Gray)
  Tertiary:  #6E7681 (Dark gray)

Syntax:
  Keyword:  #FF7B72 (Red)
  String:   #A5D6FF (Light blue)
  Function: #D2A8FF (Purple)
  Variable: #FFA657 (Orange)
  Comment:  #8B949E (Gray)

Accents:
  Blue:   #58A6FF (GitHub blue)
  Green:  #3FB950 (GitHub green)
  Border: #30363D (Subtle border)
```

## Typography

- **Primary Font**: System fonts (SF Pro, Segoe UI)
- **Code Font**: JetBrains Mono (Google Fonts)
- **Title Size**: 40px, Bold (700 weight)
- **Body Size**: 17px for content, 18px for quotes
- **Code Size**: 14px monospace
- **Comment Style**: Italic, gray, 13px

## Layout Structure

1. **Card Index**: Top-left corner (// 01, // 02 format)
2. **Title Card**: Comment + centered title
3. **Content Card**: Standard paragraph
4. **Quote Card**: Left border + large quote mark
5. **Highlight Card**: Styled as code syntax
6. **Code Card**: Terminal window + code

## Component Styling

### Title Card
- Gradient header bar (red → blue → purple)
- JSDoc comment: `/** Article Title */`
- Centered large title (40px)
- No meta information (clean, minimal)

### Quote Card
- Left border: 3px blue accent
- Large quote bracket (48px, 50% opacity)
- Italic text styling
- White text color

### Highlight Card
- Styled as JavaScript code: `const highlight = "text";`
- Syntax coloring (keyword, variable, operator, string)
- Semicolon in gray
- Elevated background (#21262D)

### Code Card
- Terminal header with 3 dots (red/yellow/green)
- Deep background (#0D1117)
- JetBrains Mono font
- No syntax highlighting (plain gray text)

## Use Cases

- **Technical Tutorials**: Programming guides, code explanations
- **API Documentation**: Code examples, usage patterns
- **Developer Blogs**: Technical articles, best practices
- **Code Snippets**: Function examples, algorithm demos
- **Developer Tools**: CLI tools, terminal outputs
- **Night Reading**: Comfortable dark mode for developers

## Technical Details

- **Container Width**: 460px max-width
- **Card Spacing**: 24px between cards
- **Border Radius**: 12px for card corners
- **Shadow**: Dark shadow with blue glow on title card
- **Glow Effect**: `0 0 20px rgba(88, 166, 255, 0.15)`
- **Responsive**: Centered container with horizontal padding

## Special Effects

### Glow Effect
Applied only to title card (first card):
- Enhanced shadow with blue glow
- Blue border color
- Creates visual hierarchy

### Hover Effect
- Background darkens on hover
- Smooth transition
- Interactive feedback
