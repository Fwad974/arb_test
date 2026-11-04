# Website review: status in this version

Status of each finding in *Website Review & Solutions – Elevate Arabia* (Flopexa, 28 October 2026)
against this repository's build.

**Fixed** means resolved here and, where marked *(QA)*, checked automatically by `build.py` or
`scripts/qa.cjs`. **Needs input** means the code is ready but a fact, file or decision has to
come from Elevate Arabia. **Not done** means still open.

**Summary:** 27 fixed · 9 fixed but needing input or sign-off · 0 not done.

| # | Finding | Status | In this version |
|---|---|---|---|
| 1 | Contact links go to template data | Fixed | Every email and both phone numbers are working `mailto:` / `tel:` links, in the footer and on the Contact page. |
| 2 | Client logos and "1,500+" belong to the partner | Fixed · needs input | Elevate's stats show only its own figures: 8 service areas, 26 team members and the Hirayama partnership. The 12 global logos and the 1,500+ figure are hidden. With written permission, set `SHOW_PARTNER_CLIENTS = True` to show the logos on the About page, labelled "Clients of our partner Hirayama Holdings". |
| 3 | No way to reach the company | Fixed | A Contact button is in the header of every page. "Discuss a project" appears on the first screen, after the services list and in a panel above the footer. Contact is also in the footer. |
| 4 | Research notes in the Terms | Fixed · needs sign-off | Terms and Privacy are hosted on this site with all six notes removed *(QA fails if they return)*. A lawyer still needs to review both. |
| 5 | Social links go to Wix's accounts | Fixed · needs input | There are no links to Wix accounts. The live site has no real profiles to copy, so add the URLs to `SITE['social']` and they appear in the footer and on the Contact page. |
| 6 | No clear message | Fixed | One positioning statement (the live hero line) leads the home page, and every page and the footer tagline use the same story. The conflicting Kaizen and "transformation partner" lines are gone. |
| 7 | Construction Technology describes another company | Fixed · needs input | The service is described as Elevate's own work. Quadratech appears only in the FAQ, with its "up to 40%" claim attributed to it. Confirm the relationship (partner, client or licence) and the right to use the names. |
| 8 | Logo animation | Fixed | No animation. The logo appears once, in the header. |
| 9 | Hamburger menu on desktop | Fixed | A horizontal menu on desktop. The hamburger is used only below 760px and includes Contact. |
| 10 | Chaotic colours, too much red, two reds | Fixed | White and sand content, navy only for the footer and one call-to-action panel, charcoal text, and a single red `#C00000` for buttons, numbers and small markers, never a background. |
| 11 | Inconsistent font sizes and families | Fixed | One family, IBM Plex Sans (self-hosted, three weights) with IBM Plex Sans Arabic for Arabic, and one type scale on every page. Layout tested from 320 to 2560px in both languages *(QA)*. |
| 12 | "Our Services" hard to read | Fixed | Dark text on white with 19px titles and descriptions, small red numbers and compact rows. Each row is a full-width link, so it works on touch screens. The review suggests cards; compact rows were chosen to keep all 8 services scannable. |
| 13 | Messy logo presentation | Fixed · needs input | Logos are grey, the same maximum height, in equal boxes, with the last row centred so there is no empty slot. Elevate Financial Express was removed from the client grid, and the grey box behind "saudi**ai**" was removed. Nothing is cut off. On phones they show 3 per row in about 100px boxes. OMIXCUBE is still an illustration, so ask for a flat logo. |
| 14 | Labels that repeat or don't match | Fixed | Each label describes its own section, with no section numbers and no repeats. The same 8-service list appears on Home, Services and in the footer. |
| 15 | Stock and AI images | Fixed | None. The only photos are real: the Elevate and Hirayama team photo, shown full width on About, and team headshots. |
| 16 | No Arabic version | Fixed · needs sign-off | A full Arabic site at `/ar/` (14 pages), right-to-left, in IBM Plex Sans Arabic, with a language switch on every page and hreflang tags for search engines. The form messages and the prepared email are in Arabic too. Translations live in `content_ar.py`, and the build fails if one is missing *(QA checks lang/dir, untranslated text, the switch and the Arabic form)*. A native speaker should review the translation; people's names stay in Latin script, as on the live site. |
| 17 | Header overlaps the content | Fixed | A solid sticky header that never hides. Anchors and sticky headings are offset below it *(QA)*. |
| 18 | Scroll animations hide content | Fixed | No scroll animations. All content is visible on load. |
| 19 | Headline below the first screen | Fixed | Headline, intro and button are visible at 1280×720 and 1366×768, and the headline at 375×667 *(QA)*. |
| 20 | One- or two-word last lines | Fixed (modern browsers) | Headings use `text-wrap: balance`; paragraphs, list items and titles use `text-wrap: pretty`. Browsers without support fall back to normal wrapping. |
| 21 | Inconsistent team section | Fixed | One card design, a job title for everyone, "Albakry" and "Gemba" spelled one way, and the groups labelled Saudi Arabia and International. Rama Charam has no photo on the live site, so initials are shown. |
| 22 | Wix page addresses and a typo | Fixed · needs input | Clean addresses such as `/services`, `/ventures` and `/terms`. The nine old addresses redirect to the new pages *(QA)*. GitHub Pages can't send true 301s; for those, put a CDN such as Cloudflare in front and add the same rules there. |
| 23 | Stats inside an image | Fixed | The stats are real text. |
| 24 | Outdated partner paragraph | Fixed | Two sentences, with no financial figures and no heading markup. It links to Hirayama's official site, `hirayamastaff.co.jp`, the address given in its Tokyo Stock Exchange filings. |
| 25 | About page typos | Fixed | The text was rewritten, consistently in US spelling. |
| 26 | Footer problems | Fixed · needs input | A navy footer with the beige logo (6.6:1), equal link styles, legal links side by side and a Contact link. It still shows `ceo@` and `os@`: confirm a general inbox such as `info@` exists, then change `SITE['emails']`. |
| 27 | "READ MORE" button too small | Fixed | Buttons are at least 48px tall and text links at least 44px. |
| 28 | No dates, cookies without a notice | Fixed · needs sign-off | Both legal pages show "Last updated". The site sets no cookies *(QA)*, so no notice is needed, and the Privacy Policy now says so. This needs a lawyer's review. |
| 29 | Missing descriptions and alt text | Fixed | Every page has a description. Logos use the company name as alt text, and headshots are marked decorative next to the visible name. No alt text is a file name. |
| 30 | Broken structure | Fixed | One `<h1>` per page, labels are paragraphs and titles are headings. The build fails on empty headings or invisible characters *(QA)*. |
| 31 | Inconsistent punctuation and capitalisation | Fixed | Every description ends with a full stop, text is in sentence case, there are no stray colons, and job titles use "&" throughout. |
| 32 | Logo alt "eelvate" | Fixed | The logo's alt text is "Elevate Arabia home". |
| 33 | Text too big on phones | Fixed | Headings scale with the screen and body text is 17px. |
| 34 | Hidden "Play video" buttons | Fixed | There are no videos. |
| 35 | Incomplete sharing and search setup | Fixed | The Elevate favicon and app icon, a title and description on every page, a 1200×630 share image, and company details for Google (name, Jeddah address, phones, email, logo) as structured data. The share image and logo URLs are filled in when deployed. |
| 36 | Oversized images | Fixed | Logos are at most 360px wide and photos at most 1200px, as WebP. All images total about 0.8 MB, down from about 72 MB of originals. |

## Platform recommendation (review §3 G)

The review recommends a CMS where content is entered once, in English and Arabic. Here,
every service, team member, logo, stat, contact detail and legal text lives once in
`content.py` (English) and `content_ar.py` (Arabic) and appears everywhere automatically. This already fixes the drift the review
describes, such as three service lists that disagreed. Editing still means changing a file in
Git, though. If non-technical staff need a web editor, a Git-based CMS such as Decap CMS can
sit on top of the same content without changing the hosting.

## Decisions for Elevate Arabia

1. Are the global brands Elevate's own clients? If so, provide written permission; if not, keep them hidden (#2).
2. What are the real social profile URLs, and which platforms are actually used (#5)?
3. What is Quadratech's relationship to Elevate, and can its names and figures be used (#7)?
4. Which general inbox should replace `ceo@` and `os@` (#26)?
5. Who will do the lawyer's review of the Terms and Privacy text (#4, #28)?
6. Is the navy version of the wordmark for light backgrounds approved?
7. Who will review the Arabic translation (#16)? Please also confirm the Arabic spelling of the office address ("سلطان سنتر"), whether names should appear in Arabic script, and which language version of the legal text prevails.
