from pathlib import Path
from typing import List

import pytest

from flashcard_generator import FlashCardGenerator


@pytest.fixture
def mock_place_on_page(monkeypatch: pytest.MonkeyPatch) -> List[int]:
    called_with = []

    def mock(_self: object, _card_height: float, _card_width: float, _cards_per_row: int, data: List, _story: List) -> None:
        called_with.append(len(data[0]))  # Append the number of cards in a row

    monkeypatch.setattr(FlashCardGenerator, "_place_on_page", mock)

    return called_with


@pytest.fixture
def fcg(tmp_path: Path) -> FlashCardGenerator:
    return FlashCardGenerator().set_filename(tmp_path / "test_flashcards.pdf")
