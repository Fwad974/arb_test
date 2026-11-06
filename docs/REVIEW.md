# Review: critique and fixes

A review of the original prototype (commit `a7af671`) against the live site at
https://www.elevatearabia.com/ (fetched 4 November 2026), and what changed.

## 1. Content accuracy

| Problem | Fix |
|---|---|
| The repo had **6** services but the services page said "Our eight service areas". The live site lists **8**: Strategy, Planning & Growth · Finance, Accounting & Audit Readiness · Governance, Legal Coordination & Risk · Ventures · Capital · Market Entry · Automotive Industrial Consultancy · Construction Technology. | All 8 areas, in the live order. Areas 01–03 share the Advisory page, each with its own anchor (`advisory.html#strategy`, `#finance`, `#governance`). |
| Service names had drifted from the live site ("Industrial Solutions", "Venture Building", "Capital Readiness", "Saudi Market Entry"). | Live names used throughout. |
| The homepage headline was invented ("Building businesses for what comes next"). | Live headline and subheadline. |
| Notes meant for stakeholders were shown to visitors: "this prototype does not independently validate it", "The public site describes…", "should be verified before launch", "(company-reported)", and a whole "Proof over promises" section about the website itself. | Copy rewritten in the company's own voice. The caveats now live in §5 below, where they belong. |
| The hero used an AI-generated Riyadh skyline for a company based in Jeddah. | Removed. The hero is now text only. |

## 2. UX and UI bugs

**Navigation**
- **Anchor links landed under the sticky header.** `#what-we-do`, `#partnership` and the sector anchors scrolled their heading under the 86px header. Fixed with `scroll-padding-top`, and QA now checks it.
- **Sector cards linked to themselves.** On the Sectors page, "View relevant expertise" for Education, Agriculture and Media pointed to `sectors.html#…`, the same page. A row now gets a link only when a related page exists.
- **Duplicate link on the homepage.** "Also explore: Automotive & Industrial Consulting" went to the same page as card 05.
- **Mega menus.** They were click-only dropdowns placed with fixed negative offsets, and each held 6–7 links. They are now a three-link nav plus Contact. Every service is one click away on the Services page and listed in the footer.
- **Mobile menu.** The icon never changed to a close icon. It now toggles, and the menu closes on Escape, a click outside, a link click, or resizing to desktop.
- **Sector filter.** Five filter chips for seven items added a step without helping anyone find anything. It is now one scannable list with category labels.

**Contact form**
- **Consent checkbox.** It could be invalid with no visible message, while the form said "review the highlighted fields" and nothing was highlighted. It was removed, because nothing is stored; a short note under the button explains what happens instead.
- **Vague error.** A too-short message got "Please enter a valid value." It now explains the problem and shows the character count.
- **Errors not linked to inputs.** There was no `aria-describedby`, so screen readers didn't announce the error with its field. Fixed.
- **Success shown in error red.** There is now a neutral success state, with a fallback link in case the mail app doesn't open.
- **iOS zoom.** Inputs were 14px, so iOS Safari zoomed in on focus. They are now 16px.
- **Email subject.** It used the raw slug ("market-entry"). It now uses the readable service name.

**Visual design**
- **Low contrast.** Small text in `#8b96a1`, `#84919c` and similar was about 3:1. All text now meets WCAG AA, and QA checks every text element.
- **Font never loaded.** The font stack named Inter but never loaded it, so most visitors saw Arial with tracking (−0.047em) designed for Inter. Now a system UI stack with tracking tuned for it.
- **Tiny labels.** Labels were 10–11px uppercase with wide tracking. The minimum is now 13px.
- **Repeated filler.** Every detail page carried the same quote line ("One connected view of…"), and every section had a numbered kicker (01–06). Both removed.
- **FAQ indicator.** The team disclosure's "+" never changed. FAQs now toggle between + and −.

## 3. Engineering and deployability

- **README overwritten.** `build.py` rewrote `README.md` on every run, wiping any edits.
- **Generated HTML committed.** Built pages sat in git next to their source and could drift from it. They are now built into `dist/` by CI and never committed.
- **Undeclared dependency.** The Jinja2 dependency was never declared. The generator now uses only the standard library.
- **QA script.** `qa_check.py` hard-coded `/usr/bin/chromium` and inlined the CSS and JS, so it never tested real paths or links. It is replaced by a build-time link, anchor and duplicate-id checker that runs in CI, plus `scripts/qa.cjs` for in-browser checks against a real server.
- **Screenshots and dev page published.** 3.2 MB of preview PNGs in the repo root would have been published with the site, and the public footer linked to the internal `design-system.html`. Both removed.
- **Search and 404 handling.** There was no 404 page and no robots or canonical handling, so a public copy of the company's content on github.io could compete with the real site in search. The site now has a 404 page, canonical URLs and a sitemap, and stays **noindex by default** until `INDEXABLE=true`.
- **Footer year.** It was hard-coded; the build now sets it.

## 4. Issues seen on the live site (outside this repo)

- The footer email link points to `info@mysite.com` and the phone link to `tel:123-456-7890`, both template placeholders. The visible text is correct, but clicking either does the wrong thing.
- There are no real social profiles. The menu's social icons link to Wix's own accounts (`instagram.com/wix`, `linkedin.com/company/wix-com`, and so on), and the footer's "LinkedIn · Facebook · Instagram · X" are plain text with no links.
- The Hirayama Holdings link is a Google search URL. The official site, per its Tokyo Stock Exchange filings, is https://www.hirayamastaff.co.jp/.
- Images are served at full size: one wordmark is 7167×1562px and the logo and team files total about 72 MB. This repo ships the same images at about 0.8 MB.
- Typos: "Why Advisory Often Fail", "Cearer direction", "eveyone".
- `/services` returns 404; the services page is at `/home-1`.

## 5. Confirm before this replaces the live domain

- **"Up to 40% faster"** is attributed to Quadratech in the FAQ. Confirm the wording and the rights to use the Quadratech, Quadraframe and Quadracrete names.
- **Team.** Confirm names, roles and permission to publish them.
- **Partnership.** Confirm the Hirayama Holdings wording and photo caption.
- **WeChat and LINE.** `site.env` holds random placeholder IDs. Replace them with the real WeChat ID (and QR code, if wanted) and the LINE Official Account ID, and confirm WhatsApp is active on +966 53 333 7712.
- **Global logos and the 1,500+ figure.** These appear to describe the partner Hirayama Holdings, so both are now hidden (`SHOW_PARTNER_CLIENTS = False`). Show the logos only with written permission, labelled as the partner's clients.
- **Network & partners logos.** Confirm the names used as alt text, especially "Al Bakri" (read from the Arabic logo).
- **Social profiles.** Add the real URLs to `SITE.social` in `content.py`; nothing is shown until you do.
- **Arabic version.** Have a native speaker review `content_ar.py`, confirm the Arabic office address ("سلطان سنتر"), decide whether names should appear in Arabic script, and confirm which language version of the legal text prevails.
- **Team photos.** Rama Abdulnaser Hussain Charam has no photo on the live site, so initials are shown.
- **Legal pages.** The Terms and Privacy text is now hosted on this site, with the live site's research notes removed and the cookie statement corrected. A lawyer should review both before launch.
- **Enquiries** go to `ceo@elevatearabia.com` (`SITE.enquiry_email` in `content.py`). Confirm that is the right inbox. If a server-side form is added later, update the privacy policy.
