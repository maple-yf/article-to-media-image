# Information Chart Templates

## Slide Card Layout

All templates now use the **Independent Card Viewport** design:
- Each semantic paragraph is wrapped in a 3:4 card (810x1080px)
- Cards have 80px visual separation
- Organized into 5 style groups for consistent theming

## Template Groups

| Group | Templates | Style Characteristics |
|-------|-----------|---------------------|
| A | style-card-deep-blue, style-dialog-red-blue | Deep gradients, glow effects |
| B | style-nordic, style-magazine | Minimal shadows, light colors |
| C | style-dark-tech, style-retro-future, style-lab-blueprint | Neon glow, animated borders |
| D | infographic, style-business, style-journal | Grid backgrounds, clean borders |
| E | style-newspaper, style-memphis, style-process-blue-green, style-step-blue | Paper texture, custom decorations |

## Core CSS Files

- `templates/core/slide-card-base.css` - Base card layout styles
- `templates/core/slide-themes.css` - Theme variables for 5 groups

## Usage

Each template generates slides with:
- Fixed 3:4 aspect ratio (810×1080px)
- Dark canvas background (#1a1a2e)
- Numbered watermarks on each card
- Semantic section separation

## Validation

Run `scripts/validate-templates.sh` to verify all templates have slide-card structure.
