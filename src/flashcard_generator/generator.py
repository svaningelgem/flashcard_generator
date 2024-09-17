from dataclasses import dataclass
import math
import re
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

@dataclass
class Entry:
    original: str
    translation: str
    extra: str = ""

def create_flashcards(filename, entries, cards_per_row=5):
    doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=0.5*cm, bottomMargin=0.5*cm)
    story = []

    # Calculate card size
    page_width, page_height = A4
    card_width = page_width / cards_per_row - 0.2*cm
    card_height = 2.3*cm

    # Calculate cards per page
    cards_per_page = cards_per_row * math.floor((page_height - 1*cm) / card_height)

    # Pad entries only if more than one row
    if len(entries) > cards_per_row:
        while len(entries) % cards_per_row != 0:
            entries.append(Entry("", "", ""))

    styles = getSampleStyleSheet()
    centered_style = ParagraphStyle(name='Centered', parent=styles['Normal'], alignment=TA_CENTER)

    for i in range(0, len(entries), cards_per_page):
        page_entries = entries[i:i+cards_per_page]

        # Create front side
        front_data = [
            [create_front_paragraph(entry, centered_style) for entry in page_entries[j:j+cards_per_row]]
            for j in range(0, len(page_entries), cards_per_row)
        ]

        place_on_page(card_height, card_width, cards_per_row, front_data, story)

        # Create back side (reversed order within each row)
        back_data = [
            [Paragraph(format_markdown(entry.translation), centered_style) for entry in reversed(page_entries[j:j+cards_per_row])]
            for j in range(0, len(page_entries), cards_per_row)
        ]

        place_on_page(card_height, card_width, cards_per_row, back_data, story)

    doc.build(story)

def create_front_paragraph(entry, style):
    original = format_markdown(entry.original)
    extra = format_markdown(entry.extra) if entry.extra else ""
    return Paragraph(f"{original}<br/><font size=8>{extra}</font>", style)

def format_markdown(text):
    # Basic Markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)      # Italic
    text = re.sub(r'__(.*?)__', r'<u>\1</u>', text)      # Underline
    return text

def place_on_page(card_height, card_width, cards_per_row, data, story):
    table = Table(data, colWidths=[card_width] * cards_per_row,
                  rowHeights=[card_height] * len(data))
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1.5, colors.black),  # Thicker lines
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(table)
    story.append(PageBreak())

# Example usage
entries = [
    Entry("Bonjour", "Hello", "Casual greeting"),
    Entry("Merci", "Thank you", "**Important** phrase"),
    Entry("Au revoir", "Goodbye", "*Formal* farewell"),
    Entry("S'il vous plaît", "Please", "__Polite__ request"),
    Entry("Oui", "Yes"),
    Entry("Non", "No"),
    Entry("Comment allez-vous?", "How are you?", "Formal inquiry"),
    Entry("Bonne journée", "Have a good day"),
    Entry("Chat", "Cat", "Common pet"),
    Entry("Chien", "Dog", "Man's best friend"),
    Entry("Maison", "House", "Place of *residence*"),
    Entry("Arbre", "Tree", "Plant with **trunk**"),
    Entry("Soleil", "Sun", "Center of solar system"),
    Entry("Lune", "Moon", "Earth's natural satellite"),
    Entry("Étoile", "Star", "Celestial body"),
    # Add more entries as needed
]

create_flashcards("flashcards.pdf", entries)