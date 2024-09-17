import math
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib.units import cm

def create_flashcards(filename, word_pairs, cards_per_row=5):
    doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=0.5*cm, bottomMargin=0.5*cm)
    story = []

    # Calculate card size
    page_width, page_height = A4
    card_width = page_width / cards_per_row - 0.2*cm
    card_height = 2.3*cm  # Slightly reduced to fit an extra row

    # Calculate cards per page
    cards_per_page = cards_per_row * math.floor((page_height - 1*cm) / card_height)

    # Pad word_pairs to fill the last page
    while len(word_pairs) % cards_per_page != 0:
        word_pairs.append(("", ""))

    for i in range(0, len(word_pairs), cards_per_page):
        page_pairs = word_pairs[i:i+cards_per_page]

        # Create front side
        front_data = [
            [pair[0] for pair in page_pairs[j:j+cards_per_row]]
            for j in range(0, len(page_pairs), cards_per_row)
        ]

        place_on_page(card_height, card_width, cards_per_row, front_data, story)

        # Create back side (reversed order)
        back_data = [
            [pair[1] for pair in reversed(page_pairs[j:j+cards_per_row])]
            for j in range(0, len(page_pairs), cards_per_row)
        ]

        place_on_page(card_height, card_width, cards_per_row, back_data, story)

    doc.build(story)

def place_on_page(card_height, card_width, cards_per_row, data, story):
    table = Table(data, colWidths=[card_width] * cards_per_row,
                  rowHeights=[card_height] * len(data))
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1.5, colors.black),  # Thicker lines
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
    ]))
    story.append(table)
    story.append(PageBreak())

# Example usage
word_pairs = [
    ("Bonjour", "Hello"),
    ("Merci", "Thank you"),
    ("Au revoir", "Goodbye"),
    ("S'il vous plaît", "Please"),
    ("Oui", "Yes"),
    ("Non", "No"),
    ("Comment allez-vous?", "How are you?"),
    ("Bonne journée", "Have a good day"),
    ("Chat", "Cat"),
    ("Chien", "Dog"),
    ("Maison", "House"),
    ("Arbre", "Tree"),
    ("Soleil", "Sun"),
    ("Lune", "Moon"),
    ("Étoile", "Star"),
    ("Livre", "Book"),
    ("École", "School"),
    ("Voiture", "Car"),
    ("Fleur", "Flower"),
    ("Oiseau", "Bird"),
    ("Pain", "Bread"),
    ("Eau", "Water"),
    # Add more word pairs as needed
]

create_flashcards("flashcards.pdf", word_pairs)