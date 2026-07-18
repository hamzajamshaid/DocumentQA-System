from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("sample_matw.pdf", pagesize=letter)
c.setFont("Helvetica-Bold", 16)
c.drawString(50, 750, "MATW Charity FAQ Document")

c.setFont("Helvetica", 12)
y = 700
faqs = [
    ("What is MATW?", "MATW is a global charity providing humanitarian aid to vulnerable communities."),
    ("Where do you operate?", "We operate in Gaza, Sudan, Yemen, Afghanistan, and Rohingya refugee settlements."),
    ("How can I donate?", "Visit our website and choose your donation amount. We accept all major payment methods."),
    ("Is my donation secure?", "Yes, all transactions are encrypted and processed through secure payment gateways."),
]

for q, a in faqs:
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, q)
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, a)
    y -= 30

c.save()
print("Created sample_matw.pdf")

