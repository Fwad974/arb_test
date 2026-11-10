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
# Services. Each entry is one page, with the text of the matching page on the live
# site (https://www.elevatearabia.com/, crawled November 2026), obvious typos corrected.
# FAQs and related links are this site's own additions.
# ---------------------------------------------------------------------------
SERVICES = [
    dict(
        slug='advisory',
        label='Advisory',
        option='Advisory: strategy, finance or governance',
        short='Strategy, finance, governance and operating structure, joined up in one plan.',
        tag='Strategy, finance & governance',
        title='Integrated advisory for growth, structure and execution',
        intro='Elevate Arabia helps businesses strengthen their strategy, governance, financial discipline, legal coordination, accounting structure, and operational readiness through a practical and integrated advisory platform.',
        overview='Strong businesses require more than ambition. They need clear strategy, disciplined control, sound governance, practical legal structuring, and an operating model that supports growth.',
        overview_more='Good advisory does not just describe what should happen. It helps the business make it happen.',
        needs=['Strategic advisory', 'Business planning', 'Governance and oversight frameworks', 'Financial advisory',
               'Accounting support', 'Audit readiness', 'Legal coordination', 'Operational structuring'],
        challenges_title='Why advisory often fails',
        challenges=['Too generic and not tailored to the business', 'Strong analysis but weak execution support',
                    'Fragmented input across functions', 'Overly theoretical recommendations',
                    'Weak follow-through and accountability', 'Poor alignment with business priorities'],
        why=['We connect advice to implementation', 'We integrate strategy, finance, governance, and operations',
             'We help improve business control and discipline', 'We support practical execution, not advice alone',
             'We build stronger management and operating foundations'],
        examples=['Strengthening governance and reporting in a growing company',
                  'Improving financial and operating discipline and aligning strategy with business planning and execution',
                  'Supporting audit readiness and accounting structure and coordinating governance, finance, and legal workstreams'],
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
        title='Building ventures that are structured, investable and ready to scale',
        intro='We help founders, investors, and innovation-led businesses turn promising ideas into commercially credible ventures through stronger strategy, financial planning, governance, investor readiness, and execution support.',
        overview='Strong ventures are not built on ideas alone. They are built on clear commercial logic, disciplined planning, credible financial structure, and a practical route to growth.',
        overview_more='We help turn ventures into structured businesses with clearer strategy and stronger execution readiness.',
        needs=['Startup and venture design', 'Business planning and commercial structure',
               'Financial modelling and growth planning', 'Governance and founder-investor alignment',
               'Investor readiness and capital support', 'Market-entry and commercialization planning'],
        challenges_title='Why ventures fail',
        challenges=['Unclear commercial logic', 'Weak financial structure', 'Poor governance and decision-making',
                    'Premature investor engagement', 'Overexpansion too early', 'Weak execution architecture',
                    'Fragmented support'],
        why=['We build the structure behind the opportunity', 'We connect ambition to execution',
             'We help improve investor confidence', 'We bring integrated support',
             'We understand Saudi opportunity and execution', 'We work well with complex and high-potential ventures'],
        examples=['Structuring a new venture from concept to launch', 'Preparing a venture for investor engagement',
                  'Building the business and financial model for growth',
                  'Aligning founders, investors, and governance frameworks',
                  'Supporting phased commercialization and expansion'],
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
        title='Building investor-ready businesses',
        intro='Elevate Arabia helps businesses and ventures prepare for capital through stronger strategy, financial modelling, governance, investor materials, and commercially disciplined structuring.',
        overview='Capital is rarely secured on vision alone. Investors look for clarity, financial discipline, governance confidence, and a credible route to execution.',
        overview_more='Capital follows structure, credibility, and execution confidence. We help build all three.',
        needs=['Investor readiness', 'Financial modelling', 'Investment case development', 'Investor materials',
               'Capital planning and funding strategy', 'Due diligence preparation',
               'Strategic introductions where appropriate'],
        challenges_title='Why capital preparation often fails',
        challenges=['Weak financial logic', 'Poorly structured investment cases', 'Inconsistent documentation',
                    'Weak governance and reporting', 'Approaching investors too early', 'Unclear use of capital',
                    'Limited readiness for diligence'],
        why=['We strengthen the business behind the funding request',
             'We improve the quality of investor discussions',
             'We combine strategy, finance, governance, and structure', 'We support disciplined capital planning',
             'We help businesses become more credible and investable'],
        examples=['Preparing a startup for serious investor engagement', 'Building a capital roadmap and financial model',
                  'Refining an investment case for Saudi market entry',
                  'Strengthening governance before funding discussions',
                  'Supporting investor-facing materials and diligence preparation'],
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
        title='Entering Saudi Arabia with structure and confidence',
        intro='Elevate Arabia helps companies, investors, and ventures design and execute practical market-entry strategies for Saudi Arabia through commercial planning, operating model design, governance, financial structuring, legal coordination, and stakeholder alignment.',
        overview='Saudi Arabia offers major opportunity, but successful entry requires more than presence alone. Businesses need the right structure, operating model, governance framework, financial planning, and market logic to enter effectively and grow with confidence.',
        overview_more='We help businesses do more than enter Saudi Arabia. We help them enter properly.',
        needs=['Market-entry strategy', 'Commercial positioning', 'Business model localization', 'Operating model design',
               'Financial planning and structuring', 'Governance and legal coordination',
               'Stakeholder and partnership alignment', 'Phased expansion planning'],
        challenges_title='Why market entry often fails',
        challenges=['Unclear local strategy', 'Weak operating model design', 'Poor financial and governance structure',
                    'Limited stakeholder alignment', 'Overcommitting too early',
                    'Weak localization of the business model', 'Fragmented launch execution'],
        why=['We treat entry as a business-building process', 'We combine strategy, finance, governance, and execution',
             'We help align market ambition with local reality', 'We support both launch and scale-up thinking',
             'We help create stronger commercial foundations in Saudi Arabia'],
        examples=['Developing a Saudi market-entry strategy', 'Structuring a local platform for a new venture',
                  'Designing the operating and governance model for launch',
                  'Refining financial and execution architecture before entry',
                  'Supporting phased launch and growth in the Kingdom'],
        faq=[
            ('Does this include company registration?',
             'Our focus is entry strategy, operating structure and legal coordination. Tell us about your licensing and registration needs and we will confirm what is in scope.'),
            ('Do you support businesses already operating in Saudi Arabia?',
             'Yes. We support both initial entry and further expansion within the Kingdom.'),
        ],
    ),
    # The live site has no detail pages for the next two: their lead, overview and support areas
    # come from the Services page's own text for them (SERVICE_AREAS, matched by `area`).
    dict(
        slug='industrial',
        area='industrial',
        label='Automotive Industrial Consultancy',
        short='Automotive, industrial operations and manufacturing transformation.',
        tag='Industry & operations',
        title='Strengthen industrial readiness from strategy to the factory floor',
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
        area='construction-technology',
        label='Construction Technology',
        short='Technology-led construction systems, delivery models and commercialization.',
        tag='Built environment',
        title='Advance construction through technology-led delivery',
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
    title='Building life sciences ventures for Saudi Arabia',
    intro='Elevate Arabia supports life sciences businesses, startups, and investors with strategy, structuring, investor readiness, governance, financial planning, and commercialization support across biotechnology, regenerative medicine, therapeutics, diagnostics, and healthcare innovation.',
    overview='Life sciences ventures require more than technical excellence. They need strong commercial architecture, disciplined financial planning, investor confidence, governance, and a practical route to market.',
    overview_more='We help life sciences ventures become structured, investable, and ready for execution.',
    needs=['Biotechnology', 'Regenerative medicine', 'Therapeutic products and services',
           'Diagnostics and precision health', 'Healthcare innovation platforms',
           'Research and commercialization initiatives'],
    challenges_title='Why life sciences ventures fail',
    challenges=['Weak route from science to market', 'Poor regulatory and commercialization planning',
                'Long timelines with weak capital discipline', 'Weak governance and business structure',
                'Premature scaling', 'Fragmented execution across technical and business functions'],
    why=['We connect science to commercial structure', 'We help improve investor and stakeholder confidence',
         'We support complex and innovation-led ventures', 'We bring strategy, finance, governance, and execution together',
         'We help shape practical pathways in Saudi Arabia'],
    examples=['Structuring a life sciences venture for Saudi entry',
              'Preparing a biotech or therapeutic platform for investors',
              'Building the business and capital case for a health innovation platform and supporting governance, finance, and commercialization planning',
              'Aligning institutions, investors, and operating partners'],
    faq=[
        ('Do you run clinical trials?',
         'No. Our work is commercial, financial, governance and venture support. Clinical operations are outside that scope.'),
        ('Does the service include regulatory approvals?',
         'We support regulatory and market planning and coordination. Responsibility for regulatory approvals is scoped and agreed with you directly.'),
    ],
)

# ---------------------------------------------------------------------------
# The Services page's eight services, in the live site's order, with the live text for each:
# the home page's one-line description (`home`), "Our Approach" (`approach`), "Typical Support
# Areas" (`support`) and "What This Helps to Achieve" (`outcomes`). `page` is the detail page
# that covers it; the first three share the Advisory page.
# ---------------------------------------------------------------------------
SERVICE_AREAS = [
    dict(id='strategy', page='advisory', label='Strategy, Planning & Growth',
         home='Clear direction, practical business planning, and scalable growth models.',
         approach='We help businesses define where they are going, how they will get there, and what must be in place to support sustainable growth. This includes strategic planning, business-model refinement, opportunity assessment, growth-roadmap development, and commercial prioritization. Our focus is on turning ambition into a practical plan that management can act on with clarity and discipline.',
         support=['Strategic planning and direction setting', 'Business-model design and refinement',
                  'Growth strategy and expansion planning', 'Commercial prioritization',
                  'Market positioning and proposition clarity', 'Phased roadmap development',
                  'Decision-support frameworks for management'],
         outcomes=['Clearer direction and better alignment', 'Stronger business logic behind growth',
                   'More disciplined planning and prioritization',
                   'Improved readiness for investment, partnerships, or expansion']),
    dict(id='finance', page='advisory', label='Finance, Accounting & Audit Readiness',
         home='Financial planning, reporting discipline, accounting support, and stronger control.',
         approach='We help businesses strengthen their financial foundations so that management, investors, and stakeholders can operate with greater confidence. Our support includes financial planning, management reporting, accounting structure, internal financial discipline, and audit readiness. The objective is to improve visibility, strengthen control, and ensure the business is supported by credible financial architecture.',
         support=['Financial planning and forecasting', 'Management reporting frameworks',
                  'Accounting structure and support', 'Internal financial controls', 'Budgeting and cost visibility',
                  'Audit readiness and documentation discipline', 'Financial architecture for investor confidence'],
         outcomes=['Stronger visibility over business performance', 'Improved financial discipline and control',
                   'Better management decision-making', 'Greater readiness for investors, lenders, or auditors']),
    dict(id='governance', page='advisory', label='Governance, Legal Coordination & Risk',
         home='Better structures, clearer decision-making, and more robust oversight.',
         approach='We help businesses establish stronger governance frameworks, clearer accountability, and more disciplined decision-making. Our support includes governance design, role clarity, reporting lines, oversight structures, and coordination of legal workstreams to ensure they align with the commercial and operating needs of the business. We also help clients address risk through better structure, better controls, and stronger management discipline.',
         support=['Governance design and management frameworks', 'Role clarity and decision rights',
                  'Board and oversight support logic', 'Risk and control architecture',
                  'Internal accountability structures', 'Legal coordination aligned with business needs',
                  'Governance preparation for investors or expansion'],
         outcomes=['Clearer authority and accountability', 'More confident and disciplined decision-making',
                   'Reduced operational and governance risk',
                   'Stronger trust from investors, partners, and stakeholders']),
    dict(id='ventures', page='ventures', label='Ventures',
         home='Support for startup creation, venture structuring, and commercialization planning.',
         approach='We support founders, investors, and innovation-led businesses in turning ideas into structured, investable, and executable ventures. This includes venture design, business planning, commercial structuring, governance alignment, financial modelling, investor readiness, and phased growth planning. Our role is to help ensure that a venture is not only promising in concept, but also credible in structure and practical in execution.',
         support=['Venture design and business architecture', 'Startup structuring and commercial logic',
                  'Business planning and growth roadmap creation',
                  'Governance alignment between founders and investors', 'Venture financial modelling',
                  'Investor readiness for early-stage and growth-stage ventures',
                  'Phased launch and commercialization planning'],
         outcomes=['Stronger commercial foundations for the venture', 'Improved investor credibility',
                   'Clearer execution logic and phased growth',
                   'Reduced risk of underbuilt business architecture']),
    dict(id='capital', page='capital', label='Capital',
         home='Investor readiness, financial modelling, capital planning, and funding support.',
         approach='We help businesses become capital-ready by strengthening the quality of the opportunity behind the funding request. Our support includes investor readiness, financial modelling, investment-case development, investor-facing materials, capital planning, and due-diligence preparation. Where appropriate, we also support strategic introductions. The goal is to help clients approach capital discussions with stronger credibility, clearer numbers, and more disciplined business logic.',
         support=['Investor readiness and capital preparation', 'Financial modelling for investment scenarios',
                  'Investment-case design and refinement', 'Investor presentations and supporting materials',
                  'Capital planning and staged funding strategy', 'Due-diligence preparation support',
                  'Strengthening governance for investor confidence'],
         outcomes=['Better-quality capital discussions', 'Stronger credibility with investors and stakeholders',
                   'Improved clarity on capital needs and growth logic', 'More disciplined funding preparation']),
    dict(id='market-entry', page='market-entry', label='Market Entry',
         home='Practical support for entering and growing in Saudi Arabia.',
         approach='We help businesses enter Saudi Arabia with stronger commercial logic, operating structure, and execution readiness. Our support includes market-entry strategy, business-model localization, operating-model design, stakeholder alignment, governance planning, financial structuring, and phased expansion logic. We focus on helping clients build a practical route into the Kingdom rather than treating entry as a simple launch exercise.',
         support=['Saudi market-entry strategy', 'Localization of business models and commercial approach',
                  'Operating-model design for local launch', 'Governance and structuring logic',
                  'Financial planning for entry and scale-up', 'Stakeholder and partnership alignment',
                  'Phased expansion planning'],
         outcomes=['More credible and practical entry into Saudi Arabia',
                   'Stronger alignment between ambition and operating reality',
                   'Improved readiness for local execution and expansion',
                   'Reduced risk of fragmented or premature entry']),
    dict(id='industrial', page='industrial', label='Automotive Industrial Consultancy',
         home='Strategic and operational support for automotive and industrial projects, including transformation, EV and AV readiness, factory and production-system setup, launch planning, ramp-up support, specialist capability deployment, and industrial platform development in Saudi Arabia.',
         approach='We provide specialist support for automotive and industrial initiatives requiring strategic, operational, and execution-focused guidance. This includes transformation planning, EV and AV readiness, production-system design, factory and operations setup, launch support, ramp-up planning, and deployment of short-term specialist expertise where critical capability gaps exist. We also support strategic industrial projects in Saudi Arabia where manufacturing, automation, localization, and long-term industrial platform development are central to success.',
         support=['Automotive and industrial strategy', 'EV and AV readiness planning',
                  'Production-system and factory setup support', 'Launch and ramp-up readiness',
                  'Industrial capability deployment and specialist support',
                  'Manufacturing transformation and automation planning',
                  'Strategic industrial project support in Saudi Arabia'],
         outcomes=['Stronger industrial and operational readiness',
                   'Better coordination between strategy and production reality',
                   'Improved launch confidence and execution discipline',
                   'More credible industrial platform development']),
    dict(id='construction-technology', page='construction-technology', label='Construction Technology',
         home='We support construction technology ventures through strategic planning, structuring, commercialization support, partnership alignment, and growth planning across smart construction, digital delivery, automation, and industrialized building methods.',
         approach_title='Quadratech: your project is 40% faster',
         approach='Quadratech delivers advanced construction technology solutions that combine Quadraframe™, a precision-engineered light gauge steel framework, with Quadracrete™, a high-performance lightweight concrete system. This integrated approach supports the development of durable, energy-efficient, and cost-effective buildings while reducing construction time by up to 40%. The system also enhances thermal insulation and provides built-in fireproofing, waterproofing, and acoustic performance, making it well suited to smart, modular, and sustainability-led building solutions.',
         support=['Smart and modular building systems', 'Light gauge steel and lightweight concrete construction solutions',
                  'Fast-track construction delivery models', 'Energy-efficient and thermally enhanced building platforms',
                  'Sustainable and environmentally focused construction systems',
                  'Fireproof, waterproof, and acoustic-performance building solutions',
                  'Technology-led construction design and execution support'],
         outcomes=['Faster project delivery and reduced construction time',
                   'Stronger cost efficiency and build performance',
                   'Improved thermal, fire, water, and acoustic protection',
                   'More durable and sustainable building outcomes',
                   'Better support for modular and smart construction methods',
                   'More scalable and technology-driven construction solutions']),
]

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
    # An optional third value links the logo to the company's website.
    ('flopexa', 'Flopexa', 'https://www.flopexa.com/'),
    ('blue-camel', 'Blue Camel'), ('cellular-therapeutics-center', 'Cellular Therapeutics Center'),
    ('saudi-ai', 'Saudi AI'), ('saudi-nih', 'Saudi NIH'), ('fsgene', 'FSGene'),
    ('thuraya-healthcare', 'Thuraya Healthcare'), ('ilf', 'ILF'), ('al-bakri', 'Al Bakri'), ('neem', 'Neem'),
    ('omixcube', 'OMIXCUBE'), ('skylight', 'Skylight'),
    ('hijaz-green', 'Hijaz Green'), ('xgenome', 'XGenome Biotech Company'),
]
# CLIENTS_GLOBAL is the live logo ticker shown under the "1,500+ companies" claim.
# Both the logos and the 1,500+ figure appear to describe the partner Hirayama
# Holdings, not Elevate (see docs/review-status.md, finding 2). They stay hidden
# until confirmed. Set SHOW_PARTNER_CLIENTS = True only with written permission
# for each logo; they then appear on the About page, labelled as the partner's.
# Home page header photo, in assets/images/brand/ (see the README, "Home page photo"). The tall
# crop fills the panel beside the headline from 1200px wide; the wide crop is the band above it
# on smaller screens. focus_* place each crop in its frame (CSS object-position). author,
# license, license_url and source_url give the credit the licence asks for, shown on the photo;
# leave author empty for a public-domain or CC0 photo.
HERO_PHOTO = dict(
    tall='jeddah-fountain-portrait', tall_widths=(480, 800, 1200),
    wide='jeddah-fountain-landscape', wide_widths=(800, 1280, 1920),
    focus_tall='50% 50%', focus_wide='50% 30%',
    author='', license='', license_url='', source_url='',
)

SHOW_PARTNER_CLIENTS = False
PARTNER_CLIENTS_LABEL = 'Clients of our partner Hirayama Holdings'
CLIENTS_GLOBAL = [
    ('toyota', 'Toyota'), ('siemens', 'Siemens'), ('samsung', 'Samsung'), ('hitachi', 'Hitachi'),
    ('panasonic', 'Panasonic'), ('mercedes-benz', 'Mercedes-Benz'), ('mitsubishi-motors', 'Mitsubishi Motors'),
    ('huawei', 'Huawei'), ('nippon-steel', 'Nippon Steel'), ('isuzu', 'Isuzu'), ('cimc', 'CIMC'),
    ('johnson-johnson', 'Johnson & Johnson'),
]

VALUES = [
    ('Respect, integrity & accountability',
     'Our core principles are built on the foundations of respect, integrity and accountability in everything we do.'),
    ('Continuously improving',
     'The ideal conditions for making things are created when machines, facilities and people work together to add value without generating any waste.'),
    ('Innovation & branding',
     'The rapid pace of technological advancement coupled with highly competitive markets necessitates business innovation and brand differentiation, creating mission-driven services which shape demand, while driving measurable social impact that fosters goodwill and success.'),
    ('Teamwork & partnerships',
     'Fostering a culture that enhances individual creativity and teamwork value, while honouring mutual trust and respect between labour and management. By committing to a higher purpose and working together, we aspire to increase partnership opportunities with other organisations and people working towards a similar goal.'),
    ('Community outreach',
     "Here at Elevate, we invest in the community through building connections that are helping to shape a more sustainable future. We want to make a positive difference in people's lives."),
    ('Environment', 'Keep every site secure, tidy and safe for everyone.'),
]

# (name, role, photo slug in assets/images/team/ or None for initials). Roles as on the live site.
TEAM_SAUDI = [
    ('Sheikh Hamza Albakry', 'Chairman and Co-Founder', 'hamza-albakry'),
    ('Mohamed Chaudhry', 'CEO and Co-Founder', 'mohamed-chaudhry'),
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
    ('Hiromitsu Hayashida', 'Former deputy plant manager of Tahara plant, Toyota Motor Corp. (OB)', 'hiromitsu-hayashida'),
    ('Toshio Morishima', 'Denso OB, former plant manager of Denso Malaysia and former plant manager of Denso Brazil', 'toshio-morishima'),
    ('Kouichi Kakizawa', 'Expert Specialist', 'kouichi-kakizawa'),
    ('Tadashi Mori', 'Former Chief Leader of Takaoka plant, Toyota Motor Corporation (OB)', 'tadashi-mori'),
    ('Mitsuru Suzuki', 'Former Chief Leader of Vehicle Quality Production Engineering Division at Toyota Motor Corporation (OB)', 'mitsuru-suzuki'),
    ('Tsutomu Orito', 'Toyota Motor Corporation (Manager, Production Control Dept. at Head office factory / GPC); DENSO TEN alumni (Production Management Department / Logistics Management Department, manager level)', 'tsutomu-orito'),
    ('Ishikawa Hisayoshi', 'Professional Engineer (Engineering management field)', 'ishikawa-hisayoshi'),
    ('Tadamasa Ishigaki', 'Former Chief Leader of Headquarter plant, Toyota Motor Corporation (OB)', 'tadamasa-ishigaki'),
    ('Toshio Takeuchi', 'Gemba Kaizen (work-site improvement) Consultant', 'toshio-takeuchi'),
    ('Kenichi Sawada', 'Former employee of Sony Corporation (OB)', 'kenichi-sawada'),
    ('Maresuke Ishii', '20 years of experience at Sony Corporation. Genba Kaizen and overseas expansion consultant', 'maresuke-ishii'),
    ('Shigeyuki Obara', 'RICOH Production Engineering Department', 'shigeyuki-obara'),
    ('Miyuky Honda', 'Manager of Consulting Division', 'miyuky-honda'),
    ('Kazuhiro Tsuchiya', 'Management consultant, Doctor of engineering', 'kazuhiro-tsuchiya'),
]

STEPS = [
    ('Understand', 'Define the objectives, constraints, stakeholders and opportunities.'),
    ('Structure', 'Build the commercial, governance and financial approach.'),
    ('Execute', 'Turn decisions into prioritized action and practical support.'),
]

# Only figures that are verifiably Elevate's own. The live site's "1,500+" belongs
# to the partner (see SHOW_PARTNER_CLIENTS above).
STATS = [
    (str(len(SERVICE_AREAS)), 'service areas, from strategy to market entry'),
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
LANG = dict(code='en', dir='ltr', locale='en_US', path='', name='English', short='EN', sep=', ')

UI = dict(
    # layout
    skip='Skip to content', nav_label='Main', menu_open='Open menu', menu_close='Close menu',
    nav_services='Services', nav_sectors='Sectors', nav_about='About', nav_contact='Contact',
    home_alt='Elevate Arabia home', new_tab=' (opens in a new tab)', breadcrumb_label='Breadcrumb', home='Home',
    footer_services='Services', footer_company='Company', footer_contact='Contact', footer_follow='Follow',
    maps='Open in Google Maps', privacy='Privacy Policy', terms='Terms & Conditions',
    language='Language', period='.', form_note_end='.',
    # home
    home_title='Strategy, capital and Saudi market entry',
    home_desc='Elevate Arabia helps businesses, founders and investors structure, finance, govern and scale their operations in Saudi Arabia.',
    hero_eyebrow='Strategy · Capital · Market entry',
    hero_title='Building companies, capital pathways [and market‑ready ventures.]',
    hero_lead='Elevate Arabia helps businesses, founders and investors structure, finance, govern and scale their operations in Saudi Arabia through integrated advisory, capital readiness, venture support and market-entry execution.',
    cta_discuss='Discuss a project', explore_services='Explore services', all_services='All services',
    services_eyebrow='Services', services_heading='Our [services.]',
    services_intro='Our model brings strategy, finance, governance, and execution together under one platform.',
    how_eyebrow='How we work', how_heading='From complexity [to clarity.]',
    how_intro='Every engagement is different, but the work generally moves from understanding the problem to building the right structure and supporting execution.',
    who_eyebrow='Who we are', who_heading='Who [we are.]',
    who_body='We help turn business ambition into structured, investable, and executable platforms. From strategy and financial planning to governance, investor readiness, and commercialization support, we provide practical guidance across the full business journey through:',
    partner_eyebrow='International partner', partner_short_name='Hirayama Holdings',

    our_partnership='Our partnership', about_link='About Elevate Arabia',
    clients_eyebrow='Clients', clients_heading='Network & [partners.]',
    clients_intro='Clients and partners across life sciences, technology, sustainability and finance.',
    sectors_eyebrow='Sectors', sectors_heading='Industry [typology.]',
    sectors_intro='We apply advisory and business-building capabilities across innovation, advanced industry and Saudi growth sectors.',
    all_sectors='All sectors',
    home_cta_title='Let’s build what comes next.',
    home_cta_body='Talk to the team about your business, investment or Saudi market opportunity.',
    # services page
    services_title='Services',
    services_desc='Advisory, ventures, capital, Saudi market entry, automotive industrial consultancy and construction technology from Elevate Arabia.',
    services_hero_title='Your dedicated partner in [business transformation.]',
    services_hero_lead='Guiding you towards unprecedented success with proven strategies.',
    areas_eyebrow='Services', areas_heading='Integrated services for growth, structure [and execution.]', areas_intro='Elevate Arabia provides integrated business services that help companies, founders, investors, and strategic partners build stronger foundations for growth. Our work combines strategy, commercial structuring, financial discipline, governance, legal coordination, investor readiness, and market execution support so that businesses are not only well planned, but also properly built for implementation, confidence, and scale.',
    journey_eyebrow='Services', journey_heading='How our services [work together.]',
    journey_body='Our services are designed to operate as an integrated system rather than as disconnected offerings. A client may begin with strategy, then require financial structuring, governance support, investor readiness, and market-entry execution. Another client may begin with capital preparation, then require deeper advisory support or venture architecture. Our role is to provide continuity across these stages so that business progress is supported by one coherent commercial framework.',

    services_cta_title='Need a combination of capabilities?',
    services_cta_body='Describe the business challenge and we can help determine a suitable starting point.',
    # service and sector detail pages
    discuss_service='Discuss this service', discuss_project='Discuss your project', where_help_link='Where we can help',
    overview_eyebrow='Overview', overview_heading='Our [approach.]',
    support_eyebrow='We support', support_heading='Where we can help.',
    outcomes_eyebrow='Why Elevate', outcomes_heading='What makes [the difference.]',
    challenges_title='Common challenges', challenges_sub='Typical issues we help resolve.',
    outputs_title='Typical outputs', outputs_sub='Every engagement is scoped to your situation.',
    faq_eyebrow='Questions', faq_heading='Good to know.', related_eyebrow='Related', related_heading='Related services.',
    detail_cta_title='Have a specific challenge in mind?',
    detail_cta_body='Share your objectives and the team can discuss the relevant workstreams.',
    enquire_service='Enquire about this service',
    # sectors page
    sectors_title='Sectors',
    sectors_desc='Sectors served by Elevate Arabia, from life sciences and advanced industry to education, agriculture, media and national development.',
    sectors_hero_title='Sector-focused support for growth, capital [and market execution.]',
    sectors_hero_lead='Elevate Arabia supports businesses, ventures, and investors across high-potential sectors through integrated strategy, financial structuring, governance, investor readiness, and Saudi market-entry support.',
    focus_eyebrow='Sector areas', focus_heading='Where we work.',
    focus_intro='Seven focus sectors across innovation, industry, capital and consumer markets.',
    why_eyebrow='Why sector focus matters', why_heading='Different sectors. [Shared disciplines.]',
    why_body='Sector familiarity improves the quality of strategic decisions, investment preparation, commercial positioning, and execution planning.',
    ls_link='Life sciences in detail',
    sectors_cta_title='Working in a specialized sector?',
    sectors_cta_body='Tell us about the sector, geography and stage of your project.', sectors_cta_label='Discuss your sector',
    # about page
    about_title='About',
    about_desc='Elevate Arabia is a strategic growth and integrated advisory firm in Jeddah, working with businesses, founders and investors.',
    about_hero_title='A strategic growth and [integrated advisory firm.]',
    about_hero_lead='Elevate Arabia supports businesses, ventures, and investors through strategy, financial discipline, governance, legal coordination, and execution support.',
    about_who_heading='What defines [us.]',

    about_statement='We help clients build stronger businesses with greater clarity, control, and confidence.',
    values_eyebrow='Values', values_heading='What we [value.]',
    partnership_eyebrow='International partnership',
    partner_location='Tokyo, Japan. Manufacturing capability, continuous improvement and industrial consulting.',
    visit_partner='Visit Hirayama Holdings',
    team_eyebrow='Meet the team', team_heading='Experience behind [the work.]',
    team_intro='Our team in Saudi Arabia, supported by international specialists in manufacturing and continuous improvement.',
    team_saudi='Elevate team', team_international='Japan team',
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
    privacy_contact='If you have any questions or requests regarding your personal data, please contact us at:',
    # messaging apps (numbers and IDs live in site.env)
    messaging='Message us', whatsapp='WhatsApp', whatsapp_action='Chat on WhatsApp',
    whatsapp_text='Hello Elevate Arabia, I would like to discuss a project.',
    wechat='WeChat', wechat_hint='Search for this ID in WeChat to add us.', copy='Copy ID', copied='Copied',
    hero_photo_alt="King Fahd's Fountain on the Jeddah waterfront at night",
    marquee_pause='Pause the moving logos', marquee_play='Play the moving logos',
    wechat_qr_alt='WeChat QR code for Elevate Arabia', line='LINE', line_action='Add us on LINE',
    # 404
    nf_eyebrow='Error 404', nf_title='Page not found.', nf_lead='The page you are looking for does not exist or has moved.',
    nf_home='Back to home', nf_contact='Contact us',
    about_us_eyebrow='About us',
    who_list=[
        'Strategy, planning, and growth',
        'Finance, accounting, and audit readiness',
        'Governance, legal coordination, and risk',
        'Ventures and business creation',
        'Capital readiness and investor support',
        'Saudi market entry and expansion',
    ],
    who_statement='From concept to capital to commercialization, we help build businesses properly.',
    read_more='Read more',
    capabilities_eyebrow='Capabilities',
    home_partner_eyebrow='Our international partner',
    home_partner_heading='Driven by [performance.]',
    partner_body='Our strategic and international partner is the Japanese consulting business of Hirayama Holdings Co., Ltd. (TSE: 7781), a Tokyo-based firm founded in 1955 that specializes in manufacturing outsourcing, engineer dispatching, and Genba Kaizen consulting. As of late 2024, the group, which operates extensively across Asia, reported sustained growth, with Q1 FY2025 revenue rising to JPY 8.84 billion (approx. USD 57 million), maintaining a strong focus on on-site improvement.',
    partner_body_more='The firm’s primary goal remains enhancing “Monozukuri” (manufacturing prowess) by combining human resource dispatch with specialized on-site improvement consulting.',
    customer_base_eyebrow='Customer base',
    areas_intro_more='We do not treat business challenges in isolation. We help clients connect direction, structure, finance, oversight, and execution into one coherent platform that supports stronger decision-making and more credible long-term growth.',
    approach_label='Our approach',
    support_label='Typical support areas',
    achieve_label='What this helps to achieve',
    journey_statement='We help clients move from strategy to structure, from structure to confidence, and from confidence to execution.',
    areas_detail_eyebrow='Advisory areas',
    areas_detail_heading='Three disciplines, [one plan.]',
    why_title='Why Elevate',
    examples_eyebrow='Example support',
    examples_heading='How it looks [in practice.]',
    sectors_overview='Different sectors face different commercial realities, but the need for structure, financial discipline, governance, investor confidence, and execution readiness remains constant.',
    sector_why=[
        'We bring strategy, finance, governance, and execution together',
        'We support both established businesses and advanced startups',
        'We help build stronger investor confidence',
        'We understand Saudi growth and expansion dynamics and we work across both established sectors and frontier opportunities',
    ],
    sector_examples=[
        'Building a venture platform in life sciences or healthcare',
        'Preparing investor-ready models for sector growth',
        'Structuring Saudi entry for international operators',
        'Refining commercial models in advanced industry and technology',
        'Supporting expansion across training, media, and innovation platforms',
    ],
    about_who_list=[
        'Strategic and commercially focused',
        'Integrated across business disciplines',
        'Built for execution, not advice alone',
        'Aligned with Saudi growth opportunities',
        'Relevant to both established firms and new ventures',
    ],
    story_heading='Our [story.]',
    story_body=[
        'Elevate is about constantly striving for good changes, from small improvements to big achievements. We believe that, following this concept, we can do something to care more for ourselves, for others, and for the planet.',
        'It is with this in mind that both Elevate and Hirayama made the conscious and strategic decision to introduce the true ethos of Kaizen to the Middle East. This is not just about training. Rather, it is all about changing a mindset to embrace continuous success through nurturing improvement in oneself and the company to create efficiency.',
    ],
    values_intro=[
        'To become the prominent Middle East company focusing on the Japanese-based Kaizen Management System and imparting its true values into our regional process-driven companies.',
        'Our mission acts as a compass, influencing key strategic decisions in the ethos of continuously improving, branding, product innovation, partnerships and much more.',
        'By being a mission with a company, rather than a company with a mission, we leverage our brand to solve problems for individuals, companies, and our region. In turn, we gain insights into services that push the boundaries of what’s possible, to grow our business and build a better world for our region.',
    ],
    hero_photo_place="King Fahd's Fountain, Jeddah",
    photo_credit='Photo',
)
