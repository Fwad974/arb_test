"""Site content for elevatearabia.com.

Edit copy here, then run `python3 build.py`. Templates live in build.py.

Headline syntax: text inside [square brackets] renders in the lighter second
tone, e.g. "Built around the challenges [you need to solve.]"

Content is rewritten from the public pages of https://www.elevatearabia.com/
(checked November 2026). Items marked CONFIRM in docs/REVIEW.md should be
signed off by the company before the site replaces the live domain.
"""

SITE = dict(
    name='Elevate Arabia',
    tagline='Integrated strategy, finance, governance and execution for growth in Saudi Arabia.',
    enquiry_email='ceo@elevatearabia.com',
    emails=['ceo@elevatearabia.com', 'os@elevatearabia.com'],
    phones=[('+966 53 333 7712', '+966533337712'), ('+966 56 221 1666', '+966562211666')],
    address=['7th Floor, Sultan Center', 'Madinah Road', 'Jeddah, Saudi Arabia'],
    maps='https://www.google.com/maps/search/?api=1&query=Sultan+Center%2C+Madinah+Road%2C+Jeddah',
    # Social profiles, shown in the footer and on the contact page once filled in.
    # The live site has none: its icons point to Wix template accounts. Add the
    # real URLs here, e.g. ('LinkedIn', 'https://www.linkedin.com/company/...').
    social=[],
)

# ---------------------------------------------------------------------------
# Services. Each entry is one page. The live site lists eight numbered service
# areas; the first three (strategy, finance, governance) share the Advisory
# page, so Advisory carries them as `areas` with their own anchors.
# ---------------------------------------------------------------------------
SERVICES = [
    dict(
        slug='advisory',
        label='Advisory',
        option='Advisory: strategy, finance or governance',
        short='Strategy, finance, governance and operating structure, joined up in one plan.',
        tag='Strategy, finance & governance',
        title='Integrated advisory for growth, structure and execution',
        intro='Bring strategy, finance, governance and operational priorities into one coherent plan for your business.',
        overview='Strong businesses need more than a plan. They need clear decision rights, usable financial information, sound governance and an operating structure that supports delivery.',
        areas=[
            dict(id='strategy', label='Strategy, Planning & Growth',
                 short='Growth strategy and business planning, with the operating structure to deliver it.',
                 items=['Strategy and growth planning', 'Operational structuring and execution planning']),
            dict(id='finance', label='Finance, Accounting & Audit Readiness',
                 short='Reliable numbers and controls that support decisions and stand up to scrutiny.',
                 items=['Management reporting and audit readiness', 'Accounting and internal financial controls']),
            dict(id='governance', label='Governance, Legal Coordination & Risk',
                 short='Clear accountability, with legal workstreams coordinated alongside the business plan.',
                 items=['Governance and decision-rights design', 'Legal workstream coordination']),
        ],
        challenges=['Advice that stays theoretical', 'Siloed advice across finance, legal and operations',
                    'Weak reporting and unclear accountability', 'Recommendations without ownership'],
        deliverables=['Business and growth roadmap', 'Financial controls and reporting framework',
                      'Governance and accountability structure', 'Implementation priorities and responsibilities'],
        faq=[
            ('Is this only for large companies?',
             'No. We work with established companies and with growing businesses that need stronger foundations.'),
            ('Do you provide legal representation?',
             'Our role is legal coordination alongside strategy, finance and governance. If you need regulated legal advice or representation, raise it at the start so the scope can be confirmed with you.'),
        ],
    ),
    dict(
        slug='ventures',
        label='Ventures',
        short='Commercial structure and execution planning for emerging businesses.',
        tag='From idea to launch',
        title='Build ventures that are structured, investable and ready to scale',
        intro='Turn a promising idea into a business with clear commercial logic, disciplined financial planning and a practical route to launch.',
        overview='For many early-stage ventures the challenge is not a shortage of ideas. It is the gap between the concept and a business that can be operated, funded and grown responsibly.',
        needs=['Startup and venture design', 'Commercial models and business planning',
               'Financial modelling and staged growth planning', 'Founder–investor governance alignment',
               'Investment readiness', 'Commercialization and Saudi market-entry plans'],
        challenges=['Unclear business economics', 'Premature fundraising',
                    'Governance gaps between founders and investors', 'Scaling before the business is ready to operate'],
        deliverables=['Venture model and launch thesis', 'Business plan and financial assumptions',
                      'Phased commercialization roadmap', 'Investor readiness and governance priorities'],
        faq=[
            ('At what stage can a founder engage?',
             'At any point from concept to launch, and onward through preparation for investment and expansion.'),
            ('Is funding guaranteed?',
             'No. Capital readiness improves your preparation; it does not guarantee investment.'),
        ],
    ),
    dict(
        slug='capital',
        label='Capital',
        short='Financial models, investor materials and disciplined funding preparation.',
        tag='Investment preparation',
        title='Build an investor-ready business',
        intro='Clarify the investment case, financial model and governance position before approaching potential capital partners.',
        overview='Investor conversations are more credible when a business can explain what it needs, how funds will be used and why its growth plan is realistic.',
        needs=['Investment case development', 'Financial models and scenario analysis',
               'Funding strategy and capital planning', 'Investor presentations and supporting documents',
               'Due diligence preparation', 'Governance readiness', 'Strategic introductions where appropriate'],
        challenges=['Weak or inconsistent numbers', 'Unclear capital requirements',
                    'Unprepared due diligence materials', 'Approaching investors too early'],
        deliverables=['Investment narrative and materials', 'Financial and funding model',
                      'Due diligence preparation checklist', 'Capital readiness priorities'],
        faq=[
            ('Do you invest directly?',
             'Our role is to prepare you for investment: the investment case, financial model, materials and governance. Working with us does not guarantee investment.'),
            ('Can an established company use this service?',
             'Yes. Capital readiness support is available to established businesses as well as new ventures.'),
        ],
    ),
    dict(
        slug='market-entry',
        label='Market Entry',
        short='Localized commercial and operating models for entering the Kingdom.',
        tag='Entry & expansion',
        title='Enter Saudi Arabia with structure and confidence',
        intro='Connect market opportunity to the right local commercial model, governance arrangements and phased execution plan.',
        overview='Successful entry takes more than opening a local presence. The strategy must fit Saudi operating realities, partnership expectations, financial needs and an achievable pace of launch.',
        needs=['Saudi market-entry strategy', 'Commercial positioning and localization', 'Operating-model design',
               'Financial planning for launch and scale', 'Governance and legal coordination',
               'Stakeholder and partnership alignment', 'Phased expansion roadmap'],
        challenges=['Insufficient localization', 'Overcommitting before readiness',
                    'Weak stakeholder alignment', 'Fragmented market-entry workstreams'],
        deliverables=['Entry strategy and market thesis', 'Localized commercial and operating model',
                      'Partner and stakeholder priorities', 'Sequenced launch and expansion roadmap'],
        faq=[
            ('Does this include company registration?',
             'Our focus is entry strategy, operating structure and legal coordination. Tell us about your licensing and registration needs and we will confirm what is in scope.'),
            ('Do you support businesses already operating in Saudi Arabia?',
             'Yes. We support both initial entry and further expansion within the Kingdom.'),
        ],
    ),
    dict(
        slug='industrial',
        label='Automotive Industrial Consultancy',
        short='Automotive, industrial operations and manufacturing transformation.',
        tag='Industry & operations',
        title='Strengthen industrial readiness from strategy to the factory floor',
        intro='Specialist advisory for manufacturing projects, EV and AV readiness, production systems, ramp-up and industrial capability building.',
        overview='Industrial ventures need the commercial case and the operational reality to work together. We link factory and production planning with launch discipline and local capability development.',
        needs=['Automotive and industrial strategy', 'EV and AV readiness planning',
               'Factory and production-system setup', 'Operational transformation and automation',
               'Launch and ramp-up readiness', 'Short-term specialist expertise', 'Industrial projects in Saudi Arabia'],
        challenges=['Disconnect between planning and production', 'Gaps in technical capability',
                    'Launch or ramp-up uncertainty', 'Inadequate manufacturing readiness'],
        deliverables=['Industrial readiness assessment', 'Operational transformation priorities',
                      'Production launch action plan', 'Capability and specialist support map'],
        faq=[
            ('Is this limited to automotive?',
             'No. We also support broader industrial and manufacturing projects.'),
            ('How does Kaizen fit in?',
             'Through our strategic partnership with Japan-based Hirayama Holdings, the work brings an emphasis on Gemba Kaizen and continuous improvement.'),
        ],
    ),
    dict(
        slug='construction-technology',
        label='Construction Technology',
        short='Technology-led construction systems, delivery models and commercialization.',
        tag='Built environment',
        title='Advance construction through technology-led delivery',
        intro='Strategic and commercialization support for modular, technology-driven and industrialized building methods.',
        overview='We support smart construction, light-gauge steel and lightweight concrete systems, and delivery models designed to improve efficiency, building performance and scalability.',
        needs=['Modular and smart building systems', 'Light-gauge steel construction models',
               'Lightweight concrete systems', 'Delivery and commercialization planning',
               'Energy-efficient building methods', 'Partnership and growth alignment'],
        challenges=['Slow and fragmented delivery models', 'Difficulty scaling innovative construction systems',
                    'Gaps between technology and market', 'Inconsistent performance planning'],
        deliverables=['Commercialization and market model', 'Partnership and growth priorities',
                      'Execution and delivery roadmap', 'Technology adoption considerations'],
        faq=[
            ('What is Quadratech?',
             'Quadratech is the construction technology featured in this service, together with its Quadraframe and Quadracrete systems.'),
            ('How much faster is construction?',
             'Quadratech reports construction time reductions of up to 40%. Actual results depend on the project, so we will discuss what is realistic for yours.'),
        ],
    ),
]

# Sector detail page (shares the service page template).
LIFE_SCIENCES = dict(
    slug='life-sciences',
    label='Life Sciences & Healthcare',
    short='Biotech, regenerative medicine, diagnostics and healthcare innovation.',
    tag='Sector specialism',
    title='Build life sciences ventures for Saudi Arabia',
    intro='Sector-focused strategy, structuring and commercialization support for biotechnology, regenerative medicine, therapeutics, diagnostics and healthcare innovation.',
    overview='Scientific merit needs to be backed by a viable business structure, investor confidence, sound governance and a credible commercialization plan.',
    needs=['Biotechnology', 'Regenerative medicine', 'Therapeutic products and services',
           'Diagnostics and precision health', 'Healthcare innovation platforms',
           'Research and commercialization initiatives'],
    challenges=['Weak path from research to commercialization', 'Capital-intensive development cycles',
                'Regulatory and market planning gaps', 'Premature scaling'],
    deliverables=['Life sciences commercialization roadmap', 'Governance and business structure',
                  'Investment case and financial plan', 'Saudi market-entry priorities'],
    faq=[
        ('Do you run clinical trials?',
         'No. Our work is commercial, financial, governance and venture support. Clinical operations are outside that scope.'),
        ('Does the service include regulatory approvals?',
         'We support regulatory and market planning and coordination. Responsibility for regulatory approvals is scoped and agreed with you directly.'),
    ],
)

# `link` is the most relevant page, or None when no dedicated page exists.
SECTORS = [
    dict(slug='life-sciences', label='Life Sciences & Healthcare', category='Innovation',
         desc='Biotech, regenerative medicine, diagnostics, therapeutics and healthcare innovation.',
         link='life-sciences.html', link_label='Life sciences in detail'),
    dict(slug='technology', label='Technology & Advanced Industry', category='Industry',
         desc='Advanced manufacturing, innovation-led ventures and technical operating platforms.',
         link='industrial.html', link_label='Automotive Industrial Consultancy'),
    dict(slug='investment', label='Investment, Financial & Asset Platforms', category='Capital',
         desc='Business models, readiness and structures supporting investment and asset platforms.',
         link='capital.html', link_label='Capital'),
    dict(slug='education', label='Education & Capability Platforms', category='Innovation',
         desc='Commercial models for learning, training and capability-building businesses.',
         link=None),
    dict(slug='agriculture', label='Food, Agriculture & Sustainability Innovation', category='Industry',
         desc='Growth and commercialization in agrifood, sustainability and resource-focused businesses.',
         link=None),
    dict(slug='media', label='Media, Entertainment & Consumer Ventures', category='Consumer',
         desc='Strategy and structure for audience-led, entertainment and consumer-facing ventures.',
         link=None),
    dict(slug='made-in-saudi', label='Made in Saudi & National Development Platforms', category='Industry',
         desc='Localization, national capability development and Saudi industrial growth.',
         link='market-entry.html', link_label='Market Entry'),
]

PARTNER = dict(
    name='Hirayama Holdings Co., Ltd.',
    url='https://www.hirayamastaff.co.jp/en/',  # official site per its Tokyo Stock Exchange filings (code 7781)
    photo='brand/elevate-hirayama-team.webp',
    photo_alt='Elevate Arabia with the Hirayama Holdings team',
)

# Logos shown on the live homepage. Files: assets/images/clients/<slug>.webp
# CLIENTS_NETWORK is the live "Clients / Network & Partners" strip.
CLIENTS_NETWORK = [
    ('blue-camel', 'Blue Camel'), ('cellular-therapeutics-center', 'Cellular Therapeutics Center'),
    ('saudi-ai', 'Saudi AI'), ('saudi-nih', 'Saudi NIH'), ('igene', 'iGene'),
    ('thuraya-healthcare', 'Thuraya Healthcare'), ('ilf', 'ILF'), ('al-bakri', 'Al Bakri'), ('neem', 'Neem'),
    ('omixcube', 'OMIXCUBE'), ('skylight', 'Skylight'),
    ('hijaz-green', 'Hijaz Green'), ('xgenome', 'XGenome Biotech Company'),
]
# CLIENTS_GLOBAL is the live logo ticker shown under the "1,500+ companies" claim.
# Both the logos and the 1,500+ figure appear to describe the partner Hirayama
# Holdings, not Elevate (see docs/review-status.md, finding 2). They stay hidden
# until confirmed. Set SHOW_PARTNER_CLIENTS = True only with written permission
# for each logo; they then appear on the About page, labelled as the partner's.
SHOW_PARTNER_CLIENTS = False
PARTNER_CLIENTS_LABEL = 'Clients of our partner Hirayama Holdings'
CLIENTS_GLOBAL = [
    ('toyota', 'Toyota'), ('siemens', 'Siemens'), ('samsung', 'Samsung'), ('hitachi', 'Hitachi'),
    ('panasonic', 'Panasonic'), ('mercedes-benz', 'Mercedes-Benz'), ('mitsubishi-motors', 'Mitsubishi Motors'),
    ('huawei', 'Huawei'), ('nippon-steel', 'Nippon Steel'), ('isuzu', 'Isuzu'), ('cimc', 'CIMC'),
    ('johnson-johnson', 'Johnson & Johnson'),
]

VALUES = [
    ('Integrity & accountability', 'Respectful relationships and clear responsibility.'),
    ('Continuous improvement', 'An emphasis on Kaizen and practical operational learning.'),
    ('Innovation & brand', 'Commercial innovation and differentiated propositions.'),
    ('Partnerships', 'Collaboration built on mutual trust and complementary expertise.'),
    ('Community', 'Long-term contribution and meaningful local connections.'),
    ('Environment & safety', 'Responsible, safe and well-managed workplaces.'),
]

# (name, role, photo slug in assets/images/team/ or None for initials)
TEAM_SAUDI = [
    ('Sheikh Hamza Albakry', 'Chairman & Co-Founder', 'hamza-albakry'),
    ('Mohamed Chaudhry', 'CEO & Co-Founder', 'mohamed-chaudhry'),
    ('Osama Albakry', 'GM & Co-Founder', 'osama-albakry'),
    ('Eyad Albakry', 'Legal Counsel', 'eyad-albakry'),
    ('Waddah Swar', 'Head of Eastern Province', 'waddah-swar'),
    ('Ibrahim Albakry', 'CFO', 'ibrahim-albakry'),
    ('Mohammed Batarfi', 'Financial Consultant', 'mohammed-batarfi'),
    ('Mohammed Saqib Bashir', 'Automotive Industrial Consultant', 'mohammed-saqib-bashir'),
    ('Abdelrafea Fakher', 'Lean Management Specialist', 'abdelrafea-fakher'),
    ('Bahaa Mohammed', 'Administrative Manager', 'bahaa-mohammed'),
    ('Rama Abdulnaser Hussain Charam', 'Strategic Analytics', None),
]

TEAM_INTERNATIONAL = [
    ('Akihiro Ito', 'Process improvement consultant', 'akihiro-ito'),
    ('Hiromitsu Hayashida', 'Former deputy plant manager, Toyota Tahara', 'hiromitsu-hayashida'),
    ('Toshio Morishima', 'Former Denso plant manager', 'toshio-morishima'),
    ('Kouichi Kakizawa', 'Expert specialist', 'kouichi-kakizawa'),
    ('Tadashi Mori', 'Former Toyota chief leader', 'tadashi-mori'),
    ('Mitsuru Suzuki', 'Former Toyota production engineering leader', 'mitsuru-suzuki'),
    ('Tsutomu Orito', 'Toyota and DENSO TEN alumnus', 'tsutomu-orito'),
    ('Ishikawa Hisayoshi', 'Professional engineer', 'ishikawa-hisayoshi'),
    ('Tadamasa Ishigaki', 'Former Toyota chief leader', 'tadamasa-ishigaki'),
    ('Toshio Takeuchi', 'Gemba Kaizen consultant', 'toshio-takeuchi'),
    ('Kenichi Sawada', 'Sony alumnus', 'kenichi-sawada'),
    ('Maresuke Ishii', 'Kaizen and overseas expansion consultant', 'maresuke-ishii'),
    ('Shigeyuki Obara', 'RICOH production engineering', 'shigeyuki-obara'),
    ('Miyuky Honda', 'Manager, Consulting Division', 'miyuky-honda'),
    ('Kazuhiro Tsuchiya', 'Management consultant, doctorate in engineering', 'kazuhiro-tsuchiya'),
]

STEPS = [
    ('Understand', 'Define the objectives, constraints, stakeholders and opportunities.'),
    ('Structure', 'Build the commercial, governance and financial approach.'),
    ('Execute', 'Turn decisions into prioritized action and practical support.'),
]

# Only figures that are verifiably Elevate's own. The live site's "1,500+" belongs
# to the partner (see SHOW_PARTNER_CLIENTS above).
STATS = [
    (str(sum(len(s.get('areas') or [s]) for s in SERVICES)), 'service areas, from strategy to market entry'),
    (str(len(SECTORS)), 'focus sectors, from life sciences to national development'),
    (str(len(TEAM_SAUDI) + len(TEAM_INTERNATIONAL)), 'team members in Saudi Arabia and Japan'),
]

# ---------------------------------------------------------------------------
# Legal pages. Text from the live site (November 2026) with the research notes
# removed and the cookie statement corrected for this site, which sets no
# cookies. Have both reviewed by a lawyer before launch; update LEGAL_UPDATED
# whenever the text changes.
# ---------------------------------------------------------------------------
LEGAL_UPDATED = '4 November 2026'

TERMS = dict(
    disclaimer=[
        'The information on this website is provided for general informational purposes only and does not constitute legal, financial, tax, audit, regulatory, investment, or other professional advice under the laws and regulations of the Kingdom of Saudi Arabia. Any reliance on this website or its content is at the user’s own risk.',
        'Elevate Arabia makes reasonable efforts to ensure that website content is accurate and up to date. However, no representation or warranty, express or implied, is given as to the accuracy, completeness, reliability, or suitability of any content on this website. Content may be updated, amended, or removed without notice.',
        'Nothing on this website creates any client, advisory, fiduciary, legal, audit, employment, partnership, or other professional relationship unless and until formally agreed in writing.',
        'References on this website to Saudi legal, regulatory, governance, privacy, compliance, or market matters are general in nature only. Users should obtain independent professional advice appropriate to their specific circumstances before making any commercial, legal, financial, regulatory, or operational decision.',
        'Any personal data collected through this website will be handled in accordance with applicable laws and regulations in the Kingdom of Saudi Arabia, including the Saudi Personal Data Protection Law.',
        'This website may contain links to third-party websites or external resources. Elevate Arabia does not control and is not responsible for the content, availability, security, or privacy practices of any third-party site.',
        'All intellectual property rights in this website and its contents, unless otherwise stated, are reserved.',
    ],
    intro='By accessing or using this website, you agree to these Terms of Use. If you do not agree, please do not use this website.',
    clauses=[
        ('Website purpose', 'This website is provided for general information about Elevate Arabia, its services, sectors, and areas of activity. Nothing on this website constitutes legal, financial, tax, audit, investment, regulatory, or other professional advice.'),
        ('No professional relationship', 'Your use of this website does not create any client, advisory, fiduciary, partnership, employment, or other professional relationship with Elevate Arabia. Any professional engagement will be subject to separate written agreement.'),
        ('Permitted use', 'You may use this website only for lawful purposes and in a way that does not damage, disrupt, misuse, or interfere with the website, its content, or its operation.'),
        ('Accuracy of information', 'We make reasonable efforts to keep website content accurate and up to date. However, we do not guarantee that all content will always be complete, accurate, or current. Content may be updated, amended, or removed without notice.'),
        ('Third-party links', 'This website may include links to third-party websites for convenience only. Elevate Arabia does not control and is not responsible for the content, availability, or practices of any third-party website.'),
        ('Intellectual property', 'Unless otherwise stated, all content on this website, including text, layout, branding, graphics, and other materials, is owned by or licensed to Elevate Arabia and is protected by applicable laws. You may not copy, reproduce, republish, distribute, modify, or commercially exploit website content without prior written permission.'),
        ('Privacy', 'Any personal data submitted through this website will be handled in accordance with our Privacy Policy and applicable laws and regulations in the Kingdom of Saudi Arabia, including the Saudi Personal Data Protection Law.'),
        ('Limitation of liability', 'To the fullest extent permitted by applicable law, Elevate Arabia shall not be liable for any direct, indirect, incidental, consequential, or other loss or damage arising from or related to the use of, or reliance on, this website or its content.'),
        ('Governing law', 'These Terms of Use shall be governed by and interpreted in accordance with the laws and regulations of the Kingdom of Saudi Arabia.'),
        ('Changes', 'We may update these Terms of Use from time to time. Any updates will be posted on this page with the revised “Last updated” date.'),
    ],
)

PRIVACY = dict(
    contact='os@elevatearabia.com',
    paragraphs=[
        'Elevate Arabia respects your privacy and is committed to protecting personal data in accordance with applicable laws and regulations in the Kingdom of Saudi Arabia.',
        'We may collect personal data such as your name, company name, job title, email address, phone number, and any information you provide through our website, email, or other communications. We may also collect limited technical data such as IP address and browser information.',
        'We use personal data to respond to enquiries, provide our services, manage business relationships, improve our website and operations, and comply with legal or regulatory obligations.',
        'We do not sell personal data. We may share personal data only where necessary with service providers, professional advisers, or authorities where required by law.',
        'We take reasonable technical and organizational measures to protect personal data from unauthorized access, misuse, loss, or disclosure.',
        'Where applicable under Saudi law, you may have rights to request access to your personal data, request correction, request deletion where permitted, and withdraw consent where consent is the basis for processing.',
        'If personal data is transferred outside Saudi Arabia, we will do so in accordance with applicable legal requirements.',
        'This website does not set cookies and does not use analytics or advertising trackers. The enquiry form does not send or store your details; it opens a pre-filled email in your own mail app.',
    ],
    changes='We may update this Privacy Policy from time to time. Any updates will be posted on this page with the revised “Last updated” date.',
)

# ---------------------------------------------------------------------------
# Language and interface text used by the page templates in build.py.
# content_ar.py has the same keys in Arabic; the build fails if one is missing.
# Placeholders in {braces} are filled in by the templates or by app.js.
# ---------------------------------------------------------------------------
LANG = dict(code='en', dir='ltr', locale='en_US', path='', name='English')

UI = dict(
    # layout
    skip='Skip to content', nav_label='Main', menu_open='Open menu', menu_close='Close menu',
    nav_services='Services', nav_sectors='Sectors', nav_about='About', nav_contact='Contact',
    home_alt='Elevate Arabia home', new_tab=' (opens in a new tab)', breadcrumb_label='Breadcrumb', home='Home',
    footer_services='Services', footer_company='Company', footer_contact='Contact', footer_follow='Follow',
    maps='Open in Google Maps', privacy='Privacy Policy', terms='Terms & Conditions',
    lang_switch_label='Read this page in English',
    # home
    home_title='Strategy, capital and Saudi market entry',
    home_desc='Elevate Arabia helps businesses, founders and investors structure, finance, govern and scale their operations in Saudi Arabia.',
    hero_eyebrow='Strategy · Capital · Market entry',
    hero_title='Building companies, capital pathways [and market‑ready ventures.]',
    hero_lead='Elevate Arabia helps businesses, founders and investors structure, finance, govern and scale their operations in Saudi Arabia through integrated advisory, capital readiness, venture support and market-entry execution.',
    cta_discuss='Discuss a project', explore_services='Explore services', all_services='All services',
    services_eyebrow='Services', services_heading='Built around the challenges [you need to solve.]',
    services_intro='Rather than separate disciplines, we join business direction, financial structure and implementation into one connected approach.',
    how_eyebrow='How we work', how_heading='From complexity [to clarity.]',
    how_intro='Every engagement is different, but the work generally moves from understanding the problem to building the right structure and supporting execution.',
    who_eyebrow='Who we are', who_heading='One integrated perspective. [Multiple disciplines.]',
    who_body='We work with established firms, entrepreneurs and investors, combining commercial planning, financial discipline, governance and sector understanding, with a focus on execution rather than advice in isolation.',
    partner_eyebrow='International partner', partner_short_name='Hirayama Holdings',
    partner_short_body='Our Japan-based strategic partner brings manufacturing improvement and Gemba Kaizen expertise.',
    our_partnership='Our partnership', about_link='About Elevate Arabia',
    clients_eyebrow='Clients', clients_heading='Network & [partners.]',
    clients_intro='Clients and partners across life sciences, technology, sustainability and finance.',
    sectors_eyebrow='Sectors', sectors_heading='Sector familiarity. [Business discipline.]',
    sectors_intro='We apply advisory and business-building capabilities across innovation, advanced industry and Saudi growth sectors.',
    all_sectors='All sectors',
    home_cta_title='Let’s build what comes next.',
    home_cta_body='Talk to the team about your business, investment or Saudi market opportunity.',
    # services page
    services_title='Services',
    services_desc='Advisory, ventures, capital, Saudi market entry, automotive industrial consultancy and construction technology from Elevate Arabia.',
    services_hero_title='Business support, [connected end to end.]',
    services_hero_lead='Strategy, commercial planning, financial discipline, governance, investment preparation and Saudi market execution, organized so you can find the right expertise quickly.',
    areas_eyebrow='Service areas', areas_heading='Eight service areas.', areas_intro='Explore each area, or talk to us about a combination.',
    journey_eyebrow='Approach', journey_heading='Not eight separate silos. [One business journey.]',
    journey_body='A client may begin with strategy, then need financial structure, governance, investor readiness and market entry. We bring these together so each step builds on the last.',
    journey_steps=['Strategy', 'Structure', 'Capital', 'Execution'],
    services_cta_title='Need a combination of capabilities?',
    services_cta_body='Describe the business challenge and we can help determine a suitable starting point.',
    # service and sector detail pages
    discuss_service='Discuss this service', discuss_project='Discuss your project', where_help_link='Where we can help',
    overview_eyebrow='Overview', overview_heading='Designed for [practical progress.]',
    support_eyebrow='What we support', support_heading='Where we can help.',
    outcomes_eyebrow='Challenges & outcomes', outcomes_heading='What needs to [work better?]',
    challenges_title='Common challenges', challenges_sub='Typical issues we help resolve.',
    outputs_title='Typical outputs', outputs_sub='Every engagement is scoped to your situation.',
    faq_eyebrow='Questions', faq_heading='Good to know.', related_eyebrow='Related', related_heading='Related services.',
    detail_cta_title='Have a specific challenge in mind?',
    detail_cta_body='Share your objectives and the team can discuss the relevant workstreams.',
    enquire_service='Enquire about this service',
    # sectors page
    sectors_title='Sectors',
    sectors_desc='Sectors served by Elevate Arabia, from life sciences and advanced industry to education, agriculture, media and national development.',
    sectors_hero_title='Sector expertise, [commercial perspective.]',
    sectors_hero_lead='Different sectors face different market realities. The foundations of sound planning, finance, governance and execution remain essential in each.',
    focus_eyebrow='Focus sectors', focus_heading='Where we work.',
    focus_intro='Seven focus sectors across innovation, industry, capital and consumer markets.',
    why_eyebrow='Why it matters', why_heading='Different sectors. [Shared disciplines.]',
    why_body='Sector familiarity supports better commercial assumptions and investment preparation. We combine this context with business modelling, capital readiness and Saudi market execution.',
    ls_link='Life sciences in detail',
    sectors_cta_title='Working in a specialized sector?',
    sectors_cta_body='Tell us about the sector, geography and stage of your project.', sectors_cta_label='Discuss your sector',
    # about page
    about_title='About',
    about_desc='Elevate Arabia is a strategic growth and integrated advisory firm in Jeddah, working with businesses, founders and investors.',
    about_hero_title='A strategic growth and [integrated advisory firm.]',
    about_hero_lead='Elevate Arabia supports businesses, ventures and investors through connected strategy, finance, governance, coordination and execution support.',
    about_who_heading='Clarity, control [and confidence.]',
    about_who_body='We are commercially focused, integrated across disciplines and oriented toward execution. We work with established companies and with new ventures pursuing growth in Saudi Arabia.',
    about_statement='From concept and capital preparation to commercialization and operations, a stronger business starts with the right structure.',
    values_eyebrow='Values', values_heading='How we work.',
    partnership_eyebrow='International partnership', partnership_heading='A shared focus on [improvement.]',
    partnership_body='Japan-based Hirayama Holdings is our strategic international partner, with a focus on Gemba Kaizen, manufacturing performance and continuous improvement.',
    partner_location='Tokyo, Japan. Manufacturing capability, continuous improvement and industrial consulting.',
    visit_partner='Visit Hirayama Holdings',
    team_eyebrow='Team', team_heading='Experience behind [the work.]',
    team_intro='Our team in Saudi Arabia, supported by international specialists in manufacturing and continuous improvement.',
    team_saudi='Saudi Arabia', team_international='International',
    about_cta_title='Work with Elevate Arabia.',
    about_cta_body='Discuss a business challenge, potential engagement or partnership opportunity.', about_cta_label='Contact the team',
    # contact page and form
    contact_title='Contact',
    contact_desc='Contact Elevate Arabia in Jeddah about advisory, ventures, capital readiness or Saudi market entry.',
    contact_hero_title='Let’s discuss [your next move.]',
    contact_hero_lead='Whether you are entering Saudi Arabia, building a venture or preparing for investment, start with a clear conversation.',
    direct_eyebrow='Direct contact', direct_heading='Tell us what [you’re building.]',
    email_label='Email', phone_label='Phone', office_label='Office', social_label='Social', form_heading='Enquiry form',
    required_before='Fields marked', required_sr='with an asterisk', required_after='are required.',
    f_name='Full name', f_name_req='Please enter your name.', f_email='Email', f_email_req='Please enter your email address.',
    f_company='Company', f_phone='Phone', f_interest='How can we help?', f_interest_req='Please choose a service.',
    f_choose='Choose a service', f_other='Something else', f_message='Project details',
    f_message_req='Please tell us a little about your project.', f_message_hint='Your objectives, current stage and the support you need.',
    submit='Prepare email',
    form_note='This opens a pre-filled email in your mail app so you can review it before sending. Nothing is stored on this website. See our',
    js_required='This field is required.', js_email='Please enter a valid email address, like name@company.com.',
    js_min='Please add a little more detail (at least {min} characters, {count} so far).',
    js_fix_one='Please check the highlighted field.', js_fix_many='Please check the {count} highlighted fields.',
    js_ok='Your email app should open with the message ready to review and send. If nothing happened, {manual} or write to {email}.',
    js_ok_manual='open it manually', js_subject='Website enquiry',
    js_lbl_name='Name', js_lbl_email='Email', js_lbl_company='Company', js_lbl_phone='Phone', js_lbl_interest='Interested in',
    # legal pages
    legal_eyebrow='Legal', last_updated='Last updated: {date}',
    terms_lead='The terms that apply to using this website.', terms_desc='The terms that apply to using the Elevate Arabia website.',
    disclaimer_eyebrow='Legal disclaimer', disclaimer_heading='Disclaimer.',
    termsofuse_eyebrow='Terms of use', termsofuse_heading='Terms of use.',
    privacy_lead='How we handle personal data, and how to contact us about it.',
    privacy_desc='How Elevate Arabia handles personal data, and how to contact us about it.',
    privacy_eyebrow='Privacy', privacy_heading='Your personal data.',
    privacy_contact='Questions or requests about your personal data:',
    # 404
    nf_eyebrow='Error 404', nf_title='Page not found.', nf_lead='The page you are looking for does not exist or has moved.',
    nf_home='Back to home', nf_contact='Contact us',
)
