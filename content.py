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
    legal=dict(
        privacy='https://www.elevatearabia.com/privacy-policy',
        terms='https://www.elevatearabia.com/terms-and-coniditions',
    ),
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
        short='Technology-led construction systems and commercialization, featuring Quadratech.',
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

VALUES = [
    ('Integrity & accountability', 'Respectful relationships and clear responsibility.'),
    ('Continuous improvement', 'An emphasis on Kaizen and practical operational learning.'),
    ('Innovation & brand', 'Commercial innovation and differentiated propositions.'),
    ('Partnerships', 'Collaboration built on mutual trust and complementary expertise.'),
    ('Community', 'Long-term contribution and meaningful local connections.'),
    ('Environment & safety', 'Responsible, safe and well-managed workplaces.'),
]

TEAM_SAUDI = [
    ('Sheikh Hamza Albakry', 'Chairman & Co-Founder'),
    ('Mohamed Chaudhry', 'CEO & Co-Founder'),
    ('Osama Albakry', 'GM & Co-Founder'),
    ('Eyad Albakry', 'Legal Counsel'),
    ('Waddah Swar', 'Head of Eastern Province'),
    ('Ibrahim AlBakry', 'CFO'),
    ('Mohammed Batarfi', 'Financial Consultant'),
    ('Mohammed Saqib Bashir', 'Automotive Industrial Consultant'),
    ('Abdelrafea Fakher', 'Lean Management Specialist'),
    ('Bahaa Mohammed', 'Administrative Manager'),
    ('Rama Abdulnaser Hussain Charam', 'Strategic Analytics'),
]

TEAM_INTERNATIONAL = [
    ('Akihiro Ito', 'Process improvement consultant'),
    ('Hiromitsu Hayashida', 'Former deputy plant manager, Toyota Tahara'),
    ('Toshio Morishima', 'Former Denso plant manager'),
    ('Kouichi Kakizawa', 'Expert specialist'),
    ('Tadashi Mori', 'Former Toyota chief leader'),
    ('Mitsuru Suzuki', 'Former Toyota production engineering leader'),
    ('Tsutomu Orito', 'Toyota and DENSO TEN alumnus'),
    ('Ishikawa Hisayoshi', 'Professional engineer'),
    ('Tadamasa Ishigaki', 'Former Toyota chief leader'),
    ('Toshio Takeuchi', 'Gemba Kaizen consultant'),
    ('Kenichi Sawada', 'Sony alumnus'),
    ('Maresuke Ishii', 'Kaizen and overseas expansion consultant'),
    ('Shigeyuki Obara', 'RICOH production engineering'),
    ('Miyuky Honda', 'Manager, Consulting Division'),
    ('Kazuhiro Tsuchiya', 'Management consultant, doctorate in engineering'),
]

STEPS = [
    ('Understand', 'Define the objectives, constraints, stakeholders and opportunities.'),
    ('Structure', 'Build the commercial, governance and financial approach.'),
    ('Execute', 'Turn decisions into prioritized action and practical support.'),
]

STATS = [
    ('1,500+', 'companies have found their solutions with us'),
    ('Saudi-focused', 'local market and execution context'),
    ('Hirayama Holdings', 'our strategic international partner, Japan'),
]
