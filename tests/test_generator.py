import pytest
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph

from flashcard_generator import FlashCard, FlashCardGenerator

# You might need to adjust the import statement above based on how you've structured your project


def test_format_markdown():
    assert FlashCard._format_markdown("**bold**") == "<b>bold</b>"
    assert FlashCard._format_markdown("*italic*") == "<i>italic</i>"
    assert FlashCard._format_markdown("__underline__") == "<u>underline</u>"
    assert (
        FlashCard._format_markdown("**bold** and *italic* and __underline__")
        == "<b>bold</b> and <i>italic</i> and <u>underline</u>"
    )
    assert FlashCard._format_markdown("normal text") == "normal text"


def test_create_front_paragraph():
    generator = FlashCardGenerator()
    style = generator._create_front_paragraph.__func__.__globals__["ParagraphStyle"](
        "test"
    )

    entry1 = FlashCard("Original", "Translation", "Extra")
    para1 = generator._create_front_paragraph(entry1, style)
    assert isinstance(para1, Paragraph)
    assert "Original<br/><font size=8>Extra</font>" in para1.text

    entry2 = FlashCard("**Bold**", "Translation", "*Italic Extra*")
    para2 = generator._create_front_paragraph(entry2, style)
    assert "<b>Bold</b><br/><font size=8><i>Italic Extra</i></font>" in para2.text

    entry3 = FlashCard("No Extra", "Translation")
    para3 = generator._create_front_paragraph(entry3, style)
    assert (
        para3.text == "No Extra"
    )  # No <br/> or <font> tags when there's no extra text


def test_generator_configuration():
    generator = FlashCardGenerator()
    generator.set_filename("test.pdf").set_cards_per_row(4).set_page_size(
        (10 * cm, 15 * cm)
    ).set_margins(top=1 * cm, bottom=1 * cm, left=1 * cm, right=1 * cm).set_card_height(
        3 * cm
    )

    assert generator.filename == "test.pdf"
    assert generator.cards_per_row == 4
    assert generator.page_size == (10 * cm, 15 * cm)
    assert generator.top_margin == 1 * cm
    assert generator.bottom_margin == 1 * cm
    assert generator.left_margin == 1 * cm
    assert generator.right_margin == 1 * cm
    assert generator.card_height == 3 * cm


def test_add_entries():
    generator = FlashCardGenerator()
    generator.add_entry("Word1", "Translation1", "Extra1").add_entry(
        "Word2", "Translation2"
    ).add_entry("Word3", "Translation3", "Extra3")

    assert len(generator.entries) == 3
    assert generator.entries[0] == FlashCard("Word1", "Translation1", "Extra1")
    assert generator.entries[1] == FlashCard("Word2", "Translation2", "")
    assert generator.entries[2] == FlashCard("Word3", "Translation3", "Extra3")


def test_generate_flashcards(tmp_path):
    pdf_file = tmp_path / "test_flashcards.pdf"
    generator = FlashCardGenerator()
    generator.set_filename(str(pdf_file)).add_entry(
        "Word1", "Translation1", "Extra1"
    ).add_entry("Word2", "Translation2").add_entry(
        "Word3", "Translation3", "Extra3"
    ).generate()

    assert pdf_file.exists()
    # You might want to add more assertions here to check the content of the PDF


def test_padding_in_generate_flashcards(monkeypatch):
    called_with = []

    def mock_place_on_page(self, card_height, card_width, cards_per_row, data, story):
        called_with.append(len(data[0]))  # Append the number of cards in a row

    monkeypatch.setattr(FlashCardGenerator, "_place_on_page", mock_place_on_page)

    generator = FlashCardGenerator()
    generator.set_cards_per_row(5)
    for i in range(1, 7):
        generator.add_entry(f"Word{i}", f"Translation{i}")
    generator.generate()

    assert called_with == [5, 5]  # Should be padded to two rows of 5


def test_no_padding_for_single_row(monkeypatch):
    called_with = []

    def mock_place_on_page(_1, _2, _3, _4, data, _5):
        called_with.append(len(data[0]))

    monkeypatch.setattr(FlashCardGenerator, "_place_on_page", mock_place_on_page)

    generator = FlashCardGenerator()
    generator.set_cards_per_row(5)
    for i in range(1, 4):
        generator.add_entry(f"Word{i}", f"Translation{i}")
    generator.generate()

    assert called_with == [3, 3]  # Should not be padded, just one row of 3


if __name__ == "__main__":
    pytest.main()
