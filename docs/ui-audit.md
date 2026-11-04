# UI/UX audit: modes, devices, languages

An audit of the build at commit `5349228` (English and Arabic) in light mode, dark mode
and browser-forced dark mode, on a 390px phone, a 768px tablet and a 1440px desktop.
It follows feedback from a phone in dark mode showing the deployed site. That deploy
(`main` at PR #2) was two commits behind the branch, but the problems below also apply
to the latest build unless noted.

## Critique

### Modes

| # | Issue | Why it matters |
|---|---|---|
| 1 | **No dark theme.** On phones in dark mode, Samsung Internet, Chrome's auto-dark and Opera repaint the page themselves. The navy header logo disappears, logos baked onto white or cream boxes glare, black logos (saudi**ai**, ILF, Al Bakri) vanish, and logo tiles turn muddy. | This is what the phone screenshots show. The site looks broken to a large share of mobile visitors, and we can't control what the browser does unless the site supplies its own dark theme. |
| 2 | The browser's top-bar colour (`theme-color`) is always white. | It flashes a white bar above a dark page. |
| 3 | Several colours are hard-coded white: inputs, logo tiles, the mobile menu, the header and the dropdown arrow. | They break in any theme other than light. |

### Brand and logos

| # | Issue | Why it matters |
|---|---|---|
| 4 | **The client logo wall looks uneven.** A grey filter was laid over full-colour artwork that still has its own white or cream boxes (iGene, neem, OMIXCUBE, the camel). Sizes come from bounding boxes, so sparse marks (Thuraya's dots) look tiny and solid ones (the camel) look huge. | A logo wall only builds trust if it looks curated: one ink colour, one visual weight, no stray boxes. |
| 5 | The header uses the navy wordmark everywhere. | It's right on white but invisible on a dark background. |

### Typography

| # | Issue | Why it matters |
|---|---|---|
| 6 | **The Arabic typeface (IBM Plex Sans Arabic) reads as narrow and technical**, and its body text looks small next to the Latin. | Arabic is the first language of most of the audience, so its typeface carries the brand. |
| 7 | The hero stats mix numbers with a name ("8", "26", "Hirayama Holdings"). | A stats row should compare like with like; the odd one out reads like filler. |

### Layout and navigation

| # | Issue | Why it matters |
|---|---|---|
| 8 | On phones, the language switch is hidden inside the menu. | On a bilingual site the language choice should be visible without opening anything. |
| 9 | The hero has a lot of top padding. On a 1280×720 laptop the Arabic button only just fits (625px of 720). | The first screen should hold the headline, intro and button comfortably. |
| 10 | The home page is about 8,300px long on a phone, partly because the sectors are listed with full descriptions, repeating the Sectors page. | Long pages hide the call to action. On the home page the sector names are enough. |
| 11 | On phones the footer is one long column with 8 service links. | Two columns halve its height. |

### What already works (keep)

- One clear message, real contact links, Contact in the header on every page.
- A calm palette (white and sand, navy, one red), AA contrast, 44px-plus tap targets.
- A light-mode layout that holds from 320px to 2560px in both languages, with mirrored right-to-left Arabic.
- No animation, no stock images, small pages (the largest page loads under 1 MB).

## Plan

1. **Native dark theme.** Every colour becomes a design token, with a dark set chosen to keep
   AA contrast. Declare `color-scheme: light dark` so browsers use our theme instead of
   repainting the page. Add a dark `theme-color`. The header switches to the beige wordmark
   in dark mode. *(Fixes 1, 2, 3, 5.)*
2. **Logo assets rebuilt** with `scripts/prepare_logos.py`: monochrome ink on transparent,
   backgrounds removed, contrast normalised, every logo sized by the amount of ink it carries
   on the same 360×160 canvas. They show grey in light mode and inverted in dark mode, in an
   even grid whose last row is centred. *(Fixes 4.)*
3. **Arabic typeface: Readex Pro.** I compared eight professional Arabic faces with the
   site's real copy (Plex Sans Arabic, Noto Kufi, Noto Sans Arabic, Readex Pro, Tajawal,
   Cairo, Almarai, Alexandria). Readex Pro has the crispest headlines, the most comfortable
   body text and even stroke weight. It is co-designed by Nadine Chahine, open source, and
   about 10 KB per weight. *(Fixes 6.)*
4. **Stats:** 8 service areas, 7 focus sectors, 26 team members, all real numbers drawn
   from the content. *(Fixes 7.)*
5. **Language switch visible in the phone header.** *(Fixes 8.)*
6. **Tighter hero spacing**, so the first screen fits comfortably in both languages. *(Fixes 9.)*
7. **Home page sectors as a compact list of names**, with descriptions kept on the Sectors
   page. *(Fixes 10.)*
8. **Two-column footer links on phones.** *(Fixes 11.)*
9. **QA for every mode.** The browser checks run in light and dark mode, including the contrast
   check, and confirm that forced dark mode no longer changes the page.

## Status

All nine steps are done. `scripts/qa.cjs` passes on all 29 pages (English and Arabic), at 7
widths, in light and dark mode. With forced dark mode switched on, the page now renders
pixel-identical to the built-in dark theme; before this change, the browser repainted it.
