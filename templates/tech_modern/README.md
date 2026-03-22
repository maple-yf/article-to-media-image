# Tech Modern Template

**Professional Tech Style**

A modern, tech-focused template featuring glassmorphism effects, gradient accents, and clean typography optimized for contemporary tech content and professional presentations.

## Design Features

- **Glassmorphism**: Frosted glass effect with backdrop blur
- **Gradient Accents**: Multi-color gradient bars (success → primary → warning)
- **Hero Card**: Dark gradient background for title card
- **Animated Badge**: Pulsing green dot on hero card
- **Card Connectors**: Gradient lines connecting cards
- **Responsive Layout**: Optimized for 3:4 aspect ratio

## Color Scheme

```css
Primary Colors:
  Primary:   #0EA5E9 (Sky Blue)
  Accent:    #38BDF8 (Light Blue)
  Deep Blue: #0284C7 (Darker Blue)
  Dark Blue: #0369A1 (Darkest Blue)

Dark Colors:
  Dark:       #0F172A (Slate Dark)
  Dark Light: #1E293B (Slate Medium)

Accent Colors:
  Success:  #22C55E (Green)
  Warning:  #F59E0B (Orange)

Text:
  Primary:   #1E293B (Dark Slate)
  Secondary: #64748B (Slate Gray)

Backgrounds:
  Light Blue: #F0F9FF (Very Light Blue)
  Border:     #BAE6FD (Light Blue Border)
```

## Typography

- **Primary Font**: Inter (Google Fonts) with Noto Sans SC
- **Hero Title**: 48px, Black (900 weight), white
- **Body Text**: 18px, regular weight
- **Quote**: 20px, Semi-bold (600 weight)
- **Code**: Courier New, 14px, light blue
- **Meta Tags**: 13px, Medium (500 weight)

## Layout Structure

1. **Top Gradient Bar**: 4px colored bar on each card
2. **Hero Badge**: "ARTICLE" badge with pulsing dot
3. **Hero Title**: Large, bold, white text
4. **Meta Tags**: Pill-shaped tags on hero card
5. **Content Areas**: Centered with flex layout
6. **Card Connectors**: Gradient lines between cards

## Component Styling

### Hero Card (Title Card)
- Dark gradient background (slate dark → slate medium)
- Multi-color gradient bar (green → blue → orange)
- "ARTICLE" badge with pulsing green dot
- Large white title (48px, black weight)
- Meta tags in semi-transparent white pills
- Section count and "Generated with AI" labels

### Quote Card
- Left gradient line (blue gradient, 4px)
- Large bold text (20px, 600 weight)
- Dark blue text color
- 24px left padding

### Highlight Card
- Light blue background (#F0F9FF)
- Lightning bolt emoji (⚡) as icon
- Border: 1px light blue
- Rounded corners (16px)
- Bold text (600 weight)

### Code Card
- Dark background (#0F172A)
- macOS-style window dots (red/yellow)
- Courier New monospace font
- Light blue code text (#38BDF8)
- Rounded corners (12px)

### Card Connectors
- 2px wide gradient line
- 16px height
- Blue to transparent gradient
- Centered below each card (except last)

## Use Cases

- **Tech Articles**: Modern tech blog posts, industry insights
- **Product Launches**: Feature announcements, product highlights
- **Startup Pitch**: Startup presentations, investor updates
- **Social Media**: LinkedIn carousels, Twitter threads
- **Conference Talks**: Slide content, speaker notes
- **Newsletters**: Tech news, curated content

## Technical Details

- **Container Width**: 480px max-width
- **Card Spacing**: 24px between cards
- **Border Radius**: 20px for card corners
- **Aspect Ratio**: 3:4 portrait orientation
- **Backdrop Filter**: blur(20px) for glass effect
- **Box Shadow**: `0 8px 32px rgba(14, 165, 233, 0.1)`
- **Background Gradient**: Linear gradient (135deg, light blue tones)

## Animations

### Pulse Animation (Hero Badge)
```css
@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}
```
- 2-second infinite loop
- Applied to green dot on hero badge
- Creates attention-grabbing effect

## Glassmorphism Effect

- Semi-transparent white background: `rgba(255, 255, 255, 0.7)`
- Backdrop blur: `blur(20px)`
- Subtle white border: `rgba(255, 255, 255, 0.8)`
- Creates depth and modern aesthetic
