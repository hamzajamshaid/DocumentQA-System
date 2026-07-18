from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

doc = SimpleDocTemplate("matw_knowledge_base.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor='#667eea',
    spaceAfter=30,
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=11,
    leading=18,
    spaceAfter=12,
)

title = Paragraph("MATW Project - Muslims Around The World", title_style)
story.append(title)
story.append(Spacer(1, 0.3*inch))

content = [
    "MATW Project is a registered charity dedicated to providing humanitarian aid to vulnerable communities across the globe. Founded in 2016 by Ali Banat, MATW has grown into a global organization delivering emergency relief, clean water, orphan support, healthcare, and long-term development assistance to those in greatest need.",
    
    "Our Mission: MATW exists to help people with sincerity, dignity, and compassion. We believe in serving communities with respect and building solutions that restore dignity rather than just solving immediate problems.",
    
    "Where We Operate: MATW currently provides aid in Gaza, Sudan, Yemen, Afghanistan, and Rohingya refugee settlements in Bangladesh. We focus on communities facing ongoing humanitarian crises that have been forgotten by the world's attention.",
    
    "What We Do: We provide emergency food assistance, clean drinking water, shelter, medical care, orphan support, mosque construction, and educational opportunities. Our 100% Donation Policy ensures that after banking fees, 100% of donations go directly to project costs and beneficiary support.",
    
    "Gaza Operations: As the crisis continues, families across Gaza are struggling to meet basic needs. MATW provides food, water, medical care, and essential relief to displaced families. Parents struggle to find enough food for their children while disease spreads through overcrowded shelters.",
    
    "Sudan Crisis: Sudan faces one of the largest humanitarian crises in the world. More than 30 million people need humanitarian assistance. MATW provides emergency food, clean water, and relief to families facing hunger, displacement, and uncertainty.",
    
    "Yemen Emergency: Years of conflict have left millions struggling to access food, clean water, and basic necessities. MATW delivers emergency relief to vulnerable families facing one of the world's longest-running humanitarian crises.",
    
    "Afghanistan Support: Years of crisis have left many families struggling to afford basic necessities. MATW helps deliver food, relief, and essential assistance to those who need it most, particularly during harsh winter months.",
    
    "Rohingya Assistance: Nearly a decade after being forced from their homes, close to one million Rohingya refugees remain in overcrowded settlements in Bangladesh. MATW provides food, water, and essential services to families dependent on humanitarian assistance.",
    
    "How to Donate: MATW accepts all major credit cards, PayPal, and bank transfers. We offer flexible donation options including one-time donations and monthly recurring giving. Every donation makes an immediate difference in people's lives.",
    
    "Zakat and Sadaqah: MATW helps Muslims fulfill their religious obligations through Zakat and Sadaqah giving. We have a Zakat Calculator to help determine your Zakat amount. Sadaqah (voluntary charity) can be given at any time in any amount.",
    
    "Our Promise: We operate with 100% transparency. We are endorsed as a Deductible Gift Recipient (DGR) in Australia. Our annual reports and financial statements are publicly available. Every dollar donated is tracked and accounted for."
]

for paragraph_text in content:
    p = Paragraph(paragraph_text, body_style)
    story.append(p)
    story.append(Spacer(1, 0.15*inch))

doc.build(story)
print("Created matw_knowledge_base.pdf with comprehensive content")

