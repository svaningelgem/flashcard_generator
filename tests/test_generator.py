import pytest
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph
from flashcard_generator.generator import FlashCard, format_markdown, create_front_paragraph, create_flashcards


def test_format_markdown():
    assert format_markdown("**bold**") == "<b>bold</b>"
    assert format_markdown("*italic*") == "<i>italic</i>"
    assert format_markdown("__underline__") == "<u>underline</u>"
    assert format_markdown("**bold** and *italic* and __underline__") == "<b>bold</b> and <i>italic</i> and <u>underline</u>"
    assert format_markdown("normal text") == "normal text"

def test_create_front_paragraph():
    styles = getSampleStyleSheet()
    centered_style = ParagraphStyle(name='Centered', parent=styles['Normal'], alignment=TA_CENTER)

    entry1 = FlashCard("Original", "Translation", "Extra")
    para1 = create_front_paragraph(entry1, centered_style)
    assert isinstance(para1, Paragraph)
    assert "Original<br/><font size=8>Extra</font>" == para1.text

    entry2 = FlashCard("**Bold**", "Translation", "*Italic Extra*")
    para2 = create_front_paragraph(entry2, centered_style)
    assert "<b>Bold</b><br/><font size=8><i>Italic Extra</i></font>" == para2.text

    entry3 = FlashCard("No Extra", "Translation")
    para3 = create_front_paragraph(entry3, centered_style)
    assert "No Extra" == para3.text

def test_create_flashcards(tmp_path):
    # This test will create an actual PDF file
    pdf_file = tmp_path / "test_flashcards.pdf"
    entries = [
        FlashCard("Word1", "Translation1", "Extra1"),
        FlashCard("Word2", "Translation2"),
        FlashCard("Word3", "Translation3", "Extra3"),
    ]
    create_flashcards(str(pdf_file), entries, cards_per_row=3)
    assert pdf_file.exists()
    # You might want to add more assertions here to check the content of the PDF

def test_padding_in_create_flashcards(monkeypatch):
    # This test checks if padding is applied correctly
    called_with = []

    def mock_place_on_page(card_height, card_width, cards_per_row, data, story):
        called_with.append(len(data[0]))  # Append the number of cards in a row

    monkeypatch.setattr("flashcard_generator.generator.place_on_page", mock_place_on_page)

    entries = [FlashCard(f"Word{i}", f"Translation{i}") for i in range(1, 7)]
    create_flashcards("dummy.pdf", entries, cards_per_row=5)

    assert called_with == [5, 5]  # Should be padded to two rows of 5

def test_no_padding_for_single_row(monkeypatch):
    called_with = []

    def mock_place_on_page(card_height, card_width, cards_per_row, data, story):
        called_with.append(len(data[0]))

    monkeypatch.setattr("flashcard_generator.generator.place_on_page", mock_place_on_page)

    entries = [FlashCard(f"Word{i}", f"Translation{i}") for i in range(1, 4)]
    create_flashcards("dummy.pdf", entries, cards_per_row=5)

    assert called_with == [3, 3]  # Should not be padded, just one row of 3
