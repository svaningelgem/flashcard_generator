from __future__ import annotations

from itertools import product
from typing import TYPE_CHECKING

import pytest
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph

from flashcard_generator import FlashCard

if TYPE_CHECKING:
    from flashcard_generator import FlashCardGenerator


def test_format_markdown() -> None:
    assert FlashCard._format_markdown("**bold**") == "<b>bold</b>"
    assert FlashCard._format_markdown("*italic*") == "<i>italic</i>"
    assert FlashCard._format_markdown("__underline__") == "<u>underline</u>"
    assert FlashCard._format_markdown("**bold** and *italic* and __underline__") == "<b>bold</b> and <i>italic</i> and <u>underline</u>"
    assert FlashCard._format_markdown("normal text") == "normal text"


# def test_create_front_paragraph(fcg: FlashCardGenerator) -> None:
#     style = fcg._create_front_paragraph.__func__.__globals__["ParagraphStyle"]("test")
#
#     entry1 = FlashCard("Original", "Translation", "Extra")
#     para1 = fcg._create_front_paragraph(entry1, style)
#     assert isinstance(para1, Paragraph)
#     assert "Original<br/><font size=8>Extra</font>" in para1.text
#
#     entry2 = FlashCard("**Bold**", "Translation", "*Italic Extra*")
#     para2 = fcg._create_front_paragraph(entry2, style)
#     assert "<b>Bold</b><br/><font size=8><i>Italic Extra</i></font>" in para2.text
#
#     entry3 = FlashCard("No Extra", "Translation")
#     para3 = fcg._create_front_paragraph(entry3, style)
#     assert para3.text == "No Extra"  # No <br/> or <font> tags when there's no extra text


@pytest.mark.parametrize(("top_margin", "bottom_margin", "left_margin", "right_margin"), product([None, 1 * cm], repeat=4))
def test_generator_configuration(
    fcg: FlashCardGenerator, top_margin: float | None, bottom_margin: float | None, left_margin: float | None, right_margin: float | None
) -> None:
    fcg.set_cards_per_row(4).set_page_size((10 * cm, 15 * cm)).set_margins(
        top=top_margin, bottom=bottom_margin, left=left_margin, right=right_margin
    ).set_card_height(3 * cm)

    assert fcg.filename.name == "test_flashcards.pdf"
    assert fcg.cards_per_row == 4
    assert fcg.page_size == (10 * cm, 15 * cm)
    assert fcg.top_margin == (top_margin if top_margin is not None else fcg.top_margin)
    assert fcg.bottom_margin == (bottom_margin if bottom_margin is not None else fcg.bottom_margin)
    assert fcg.left_margin == (left_margin if left_margin is not None else fcg.left_margin)
    assert fcg.right_margin == (right_margin if right_margin is not None else fcg.right_margin)
    assert fcg.card_height == 3 * cm


def test_add_entries(fcg: FlashCardGenerator) -> None:
    fcg.add_entry("Word1", "Translation1", "Extra1").add_entry("Word2", "Translation2").add_entry("Word3", "Translation3", "Extra3")

    assert len(fcg.entries) == 3
    assert fcg.entries[0] == FlashCard("Word1", "Translation1", "Extra1")
    assert fcg.entries[1] == FlashCard("Word2", "Translation2", "")
    assert fcg.entries[2] == FlashCard("Word3", "Translation3", "Extra3")


def test_generate_flashcards(fcg: FlashCardGenerator) -> None:
    fcg.add_entry("**Word1**", "__Translation1__", "*Extra1*").add_entry("Word2", "Translation2").add_entry("Word3", "Translation3", "Extra3").add_entry("Word4", "Translation4", index="Index4").generate()

    assert fcg.filename.exists()
    # You might want to add more assertions here to check the content of the PDF


def test_padding_in_generate_flashcards(fcg: FlashCardGenerator, mock_place_on_page: list) -> None:
    fcg.set_cards_per_row(5)
    for i in range(1, 7):
        fcg.add_entry(f"Word{i}", f"Translation{i}")
    fcg.generate()

    assert mock_place_on_page == [5, 5]  # Should be padded to two rows of 5


def test_no_padding_for_single_row(fcg: FlashCardGenerator, mock_place_on_page: list) -> None:
    fcg.set_cards_per_row(5)
    for i in range(1, 4):
        fcg.add_entry(f"Word{i}", f"Translation{i}")
    fcg.generate()

    assert mock_place_on_page == [3, 3]  # Should not be padded, just one row of 3
