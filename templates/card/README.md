# Card Template

**Information Block Design**

A professional information card template featuring clean layouts, numbered cards, and subtle color accents for organized article presentation.

## Design Features

- **Numbered Card System**: Each card displays its index in a circular badge
- **Left Accent Bar**: 4px primary color indicator on each card's left edge
- **Alternating Backgrounds**: Main card uses white background, alternate cards use light gray
- **Fixed Aspect Ratio**: 3:4 portrait orientation for consistent card sizing
- **Meta Information**: Displays article stats and metadata on title card

## Color Scheme

```css
Primary:      #059669 (Emerald Green)
Light:        #D1FAE5 (Light Green)
Dark:         #047857 (Dark Emerald)
Background:   #F1F5F9 (Slate)
Card:         #FFFFFF (White)
Text Primary: #1E293B (Dark Slate)
Text Secondary: #64748B (Slate Gray)
```

## Typography

- **Font Family**: System fonts with Noto Sans SC for Chinese
- **Title Size**: 38px, Bold (700 weight)
- **Body Size**: 17px for content, 18px for quotes
- **Code Font**: Courier New monospace

## Layout Structure

1. **Card Indicator**: 4px left border in primary color
2. **Card Number**: Circular badge (32px) positioned top-right
3. **Content Area**: Centered with 20px left padding
4. **Title Card**: Gradient top bar + title + meta info
5. **Content Card**: Standard paragraph text
6. **Quote Card**: Large quote icon (48px) + italic text
7. **Highlight Card**: Light green background + badge
8. **Code Card**: Header bar + monospace code

## Component Styling

### Title Card
- Gradient header bar (primary to light)
- Large bold title (38px)
- Meta information with bullet separators

### Quote Card
- Left-aligned quote icon (48px, 30% opacity)
- Italic text styling
- Primary color for quote mark

### Highlight Card
- Light green background (#D1FAE5)
- "Key Point" badge (pill-shaped, uppercase)
- Bold text (600 weight)
- Dark emerald text color

### Code Card
- Light gray header
- Language indicator (uppercase, small)
- Monospace font family
- 16px padding around code

## Use Cases

- **Educational Content**: Tutorial series, lesson cards
- **Product Documentation**: Feature breakdowns, specs
- **Blog Posts**: Article summaries, key takeaways
- **Social Media**: Carousel content, infographic cards
- **Knowledge Base**: Concept explanations, definitions

## Technical Details

- **Container Width**: 460px max-width
- **Card Spacing**: 24px between cards
- **Border Radius**: 16px for card corners
- **Shadow**: Subtle (0 4px 12px rgba(0, 0, 0, 0.08))
- **Responsive**: Centered container with horizontal padding
