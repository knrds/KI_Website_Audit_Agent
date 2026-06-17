---
name: Audit Intelligence System
colors:
  surface: '#fcf8ff'
  surface-dim: '#dcd8e5'
  surface-bright: '#fcf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f2ff'
  surface-container: '#f0ecf9'
  surface-container-high: '#eae6f4'
  surface-container-highest: '#e4e1ee'
  on-surface: '#1b1b24'
  on-surface-variant: '#464555'
  inverse-surface: '#302f39'
  inverse-on-surface: '#f3effc'
  outline: '#777587'
  outline-variant: '#c7c4d8'
  surface-tint: '#4d44e3'
  primary: '#3525cd'
  on-primary: '#ffffff'
  primary-container: '#4f46e5'
  on-primary-container: '#dad7ff'
  inverse-primary: '#c3c0ff'
  secondary: '#575e70'
  on-secondary: '#ffffff'
  secondary-container: '#d9dff5'
  on-secondary-container: '#5c6274'
  tertiary: '#7e3000'
  on-tertiary: '#ffffff'
  tertiary-container: '#a44100'
  on-tertiary-container: '#ffd2be'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#e2dfff'
  primary-fixed-dim: '#c3c0ff'
  on-primary-fixed: '#0f0069'
  on-primary-fixed-variant: '#3323cc'
  secondary-fixed: '#dce2f7'
  secondary-fixed-dim: '#c0c6db'
  on-secondary-fixed: '#141b2b'
  on-secondary-fixed-variant: '#404758'
  tertiary-fixed: '#ffdbcc'
  tertiary-fixed-dim: '#ffb695'
  on-tertiary-fixed: '#351000'
  on-tertiary-fixed-variant: '#7b2f00'
  background: '#fcf8ff'
  on-background: '#1b1b24'
  surface-variant: '#e4e1ee'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.2'
  label-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  2xl: 48px
  3xl: 64px
  container-max: 1440px
  gutter: 24px
  margin-mobile: 16px
---

## Brand & Style

The design system is engineered for a **Website Audit Agent**, targeting SEO professionals, developers, and digital marketers who require precision and clarity. The brand personality is **authoritative, analytical, and efficient**. It avoids decorative flourishes in favor of a high-utility, data-first aesthetic.

The visual style is **Modern Minimalism**. It utilizes a "Surface-on-Base" architecture where the light-gray background acts as a canvas for crisp white cards. The emotional response should be one of "trust through transparency"—the interface stays out of the way so the audit data can speak for itself. Trust signals are conveyed through rigorous alignment, ample whitespace, and a restrained use of the Indigo accent color.

## Colors

The palette is strictly functional. **Indigo (#4F46E5)** is reserved for primary actions and active states, ensuring high signal-to-noise ratios. **Dark Slate (#111827)** provides maximum legibility for body text and headers.

Status colors (Emerald, Amber, Rose) are used only to communicate audit health scores and system alerts. The background uses **#F9FAFB** to reduce eye strain during long-form data analysis, providing a subtle contrast against the **#FFFFFF** surface containers.

## Typography

This design system utilizes **Inter** for all roles to maintain a unified, systematic appearance. The type hierarchy is built on a tight scale to handle the density of dashboard data.

- **Headlines:** Use Semi-Bold (600) for clear section identification. Display sizes use Bold (700) with slight negative letter spacing for a modern, compact feel.
- **Body:** Set primarily in Regular (400). For German text, which tends to be longer, a line height of 1.5–1.6 is strictly maintained to ensure readability.
- **Labels:** Small labels use an uppercase transform with increased tracking (0.05em) to differentiate metadata from interactive content.

## Layout & Spacing

The layout follows a **Fixed Grid** model for the main dashboard content, centered within a 1440px container. A 12-column system is used for data visualization and card arrangements.

- **Desktop:** 24px gutters between cards. Content is often organized into 3-column or 4-column widgets.
- **Sidebars:** A fixed left-hand navigation (280px) is recommended for SaaS utility.
- **Mobile:** The layout reflows to a single column. Horizontal padding is reduced to 16px to maximize screen real estate for charts and tables.
- **Rhythm:** Spacing units are strictly based on a 4px baseline, ensuring consistent vertical rhythm across varied content blocks.

## Elevation & Depth

This design system uses **Ambient Shadows** and **Tonal Layers** to create depth without visual clutter. 

- **Level 0 (Background):** #F9FAFB. Used for the lowest layer of the interface.
- **Level 1 (Cards/Surface):** #FFFFFF with a 1px solid border (#E5E7EB) and a soft, diffused shadow (0px 1px 3px rgba(0,0,0,0.1)). 
- **Level 2 (Hover/Active):** Slightly more pronounced shadow (0px 10px 15px -3px rgba(0,0,0,0.1)) to indicate interactivity.
- **Level 3 (Modals/Overlays):** High-diffusion shadows with a background backdrop blur (8px) to focus the user's attention.

No heavy inner shadows or skeuomorphic gradients are permitted.

## Shapes

The shape language is defined by a **Rounded (Level 2)** approach. This softens the analytical nature of the data and makes the professional environment feel accessible.

- **Standard Elements:** Buttons, input fields, and small UI components use a 0.5rem (8px) radius.
- **Main Cards:** Large data containers and dashboard widgets use `rounded-xl` (1.5rem / 24px) to create distinct visual groups.
- **Status Pills:** Utilize a fully rounded (pill) shape to differentiate status badges from clickable buttons.

## Components

### Buttons
- **Primary:** Solid Indigo (#4F46E5) with white text. No gradient. 
- **Secondary:** White background with a #E5E7EB border and Dark Slate text.
- **States:** Hover states should involve a slight darkening of the background color (e.g., Indigo 600).

### Cards
Cards are the primary container for audit results. They must include a 24px internal padding and use the `rounded-xl` corner radius. Header areas within cards should have a subtle bottom border (#E5E7EB).

### Inputs & Selects
Form fields use a white background, 1px border (#E5E7EB), and 8px border radius. Focus states use a 2px Indigo ring with an offset to ensure high visibility for accessibility.

### Data Tables
Tables are clean with no vertical borders. Row heights should be generous (min-height: 56px). Use alternating row colors (Zebra striping) only for very dense data sets; otherwise, use thin horizontal dividers.

### Audit Badges (Status)
- **Success:** "Bestanden" (Passed) - Emerald green background at 10% opacity with solid Emerald text.
- **Warning:** "Warnung" (Warning) - Amber background at 10% opacity with solid Amber text.
- **Error:** "Fehler" (Error) - Rose background at 10% opacity with solid Rose text.

### Progress Indicators
Radial gauges for SEO scores should use a stroke width of 8px, using the status colors to indicate performance brackets (0-49: Error, 50-89: Warning, 90-100: Success).