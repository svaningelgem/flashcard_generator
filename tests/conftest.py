from typing import List

import pytest

from flashcard_generator import FlashCardGenerator


@pytest.fixture
def mock_place_on_page(monkeypatch: pytest.MonkeyPatch) -> List:
    called_with = []

    def mock_place_on_page(_0: object, _1: float, _2: float, _3: int, data: List, _5: List) -> None:
        called_with.append(len(data[0]))  # Append the number of cards in a row

    monkeypatch.setattr(FlashCardGenerator, "_place_on_page", mock_place_on_page)

    return called_with
