from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    PageBreak,
    SimpleDocTemplate,
    Table,
    TableStyle,
)

if TYPE_CHECKING:  # pragma: no cover
    import sys

    if sys.version_info >= (3, 11):
        from typing import Self
    else:
        Self = "FlashCardGenerator"


# Register a default font that supports various styles
pdfmetrics.registerFont(TTFont("DejaVuSans", "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Oblique", "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-BoldOblique", "DejaVuSans-BoldOblique.ttf"))


@dataclass
class FlashCard:
    original: str
    translation: str
    extra: str = ""  # Placed at the front in smaller letters
    index: str = ""  # Placed at the front right bottom in small letters

    def __post_init__(self) -> None:
        self.original = self._format_markdown(self.original)
        self.translation = self._format_markdown(self.translation)
        self.extra = self._format_markdown(self.extra)
        self.index = self._format_markdown(self.index)

    @staticmethod
    def _format_markdown(text: str) -> str:
        text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)  # Bold
        text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)  # Italic
        return re.sub(r"__(.*?)__", r"<u>\1</u>", text)  # Underline


class IndexedCardContent(Flowable):
    def __init__(self, card: FlashCard, style: ParagraphStyle):
        Flowable.__init__(self)
        self.card = card
        self.style = style
        self.style.fontName = "DejaVuSans"

    def wrap(self, avail_width, avail_height):
        self.width = avail_width
        self.height = avail_height
        return avail_width, avail_height

    def draw(self):
        canvas = self.canv
        canvas.saveState()

        # Calculate the space available for the main content
        main_content_height = self.height - (2 * self.style.leading)  # Reserve space for extra and index

        self._draw_wrapped_text(self.card.original, self.style.fontSize, main_content_height, self.width, self.width / 2, self.height / 2)

        if self.card.extra:
            extra_style = ParagraphStyle("Extra", parent=self.style, fontSize=8, leading=10)
            self._draw_wrapped_text(self.card.extra, extra_style.fontSize, self.style.leading, self.width, self.width / 2, 17, style=extra_style)

        if self.card.index:
            index_style = ParagraphStyle("Index", parent=self.style, fontSize=6, leading=8)
            self._draw_text(self.card.index, index_style.fontSize, 2, self.width - 2, align="right", style=index_style)

        canvas.restoreState()

    def _draw_wrapped_text(self, text, font_size, max_height, max_width, x, y, align="center", style=None):
        if style is None:
            style = self.style

        lines = text.split("<br/>")
        wrapped_lines = []

        for line in lines:
            wrapped_lines.extend(simpleSplit(line, style.fontName, font_size, max_width))

        total_height = len(wrapped_lines) * style.leading
        if total_height > max_height:
            # If text is too tall, reduce font size
            while total_height > max_height and font_size > 6:
                font_size -= 1
                wrapped_lines = []
                for line in lines:
                    wrapped_lines.extend(simpleSplit(line, style.fontName, font_size, max_width))
                total_height = len(wrapped_lines) * style.leading

        # Calculate starting y position for vertical centering
        start_y = y + (total_height / 2) - (style.leading / 2)

        for line in wrapped_lines:
            self._draw_text(line, font_size, start_y, x, align, style)
            start_y -= style.leading

    def _calculate_start_position(self, x, align, line_width):
        if align == "center":
            return x - line_width / 2

        if align == "right":
            return x - line_width

        # left align
        return x

    def _draw_text(self, text, font_size, y, x, align="center", style=None):
        if style is None:
            style = self.style

        canvas = self.canv
        fragments = re.split(r"(<[^>]+>)", text)
        line_width = sum(stringWidth(f, style.fontName, font_size) for f in fragments if not f.startswith("<"))

        # Calculate starting x position
        start_x = self._calculate_start_position(x, align, line_width)

        current_x = start_x
        current_font = style.fontName
        for fragment in fragments:
            if fragment.startswith("<"):
                current_font = self._interpret_fragment(current_font, fragment, style)
            else:
                canvas.setFont(current_font, font_size)
                canvas.drawString(current_x, y, fragment)
                f_width = stringWidth(fragment, current_font, font_size)
                if getattr(self, "underline", False):
                    canvas.line(current_x, y - 2, current_x + f_width, y - 2)
                current_x += f_width

    def _interpret_fragment(self, current_font, fragment, style):
        if fragment == "<b>":
            current_font = self._get_font_variation(style.fontName, "Bold")
        elif fragment == "</b>":
            current_font = style.fontName
        elif fragment == "<i>":
            current_font = self._get_font_variation(style.fontName, "Oblique")
        elif fragment == "</i>":
            current_font = style.fontName
        elif fragment == "<u>":
            self.underline = True
        elif fragment == "</u>":
            self.underline = False
        return current_font

    @staticmethod
    def _get_font_variation(base_font, variation):
        return f"{base_font}-{variation}"


@dataclass
class FlashCardGenerator:
    entries: list[FlashCard] = field(default_factory=list)
    cards_per_row: int = 5
    filename: Path = Path("flashcards.pdf")
    page_size: tuple[float, float] = A4
    top_margin: float = 0.5 * cm
    bottom_margin: float = 0.5 * cm
    left_margin: float = 0.5 * cm
    right_margin: float = 0.5 * cm
    card_height: float = 2.3 * cm

    def add_entry(self, original: str, translation: str, extra: str = "", index: str = "") -> Self:
        self.entries.append(FlashCard(original, translation, extra, index))
        return self

    def set_cards_per_row(self, count: int) -> Self:
        self.cards_per_row = count
        return self

    def set_filename(self, filename: str | Path) -> Self:
        self.filename = Path(filename)
        return self

    def set_page_size(self, size: tuple[float, float]) -> Self:
        self.page_size = size
        return self

    def set_margins(
        self,
        *,
        top: float | None = None,
        bottom: float | None = None,
        left: float | None = None,
        right: float | None = None,
    ) -> Self:
        if top is not None:
            self.top_margin = top
        if bottom is not None:
            self.bottom_margin = bottom
        if left is not None:
            self.left_margin = left
        if right is not None:
            self.right_margin = right
        return self

    def set_card_height(self, height: float) -> Self:
        self.card_height = height
        return self

    def generate(self) -> None:
        doc = SimpleDocTemplate(
            str(self.filename.resolve().absolute()),
            pagesize=self.page_size,
            topMargin=self.top_margin,
            bottomMargin=self.bottom_margin,
            leftMargin=self.left_margin,
            rightMargin=self.right_margin,
        )
        story = []

        page_width, page_height = self.page_size
        card_width = page_width / self.cards_per_row - 0.2 * cm

        cards_per_page = self.cards_per_row * math.floor((page_height - 1 * cm) / self.card_height)

        if len(self.entries) > self.cards_per_row:
            while len(self.entries) % self.cards_per_row != 0:
                self.entries.append(FlashCard("", "", ""))

        styles = getSampleStyleSheet()
        centered_style = ParagraphStyle(name="Centered", parent=styles["Normal"], alignment=TA_CENTER, fontName="DejaVuSans")

        for i in range(0, len(self.entries), cards_per_page):
            page_entries = self.entries[i : i + cards_per_page]

            front_data = [
                [self._create_front_content(entry, centered_style) for entry in page_entries[j : j + self.cards_per_row]]
                for j in range(0, len(page_entries), self.cards_per_row)
            ]

            self._place_on_page(self.card_height, card_width, self.cards_per_row, front_data, story)

            back_data = [
                [
                    IndexedCardContent(FlashCard(entry.translation, "", index=entry.index), centered_style)
                    for entry in reversed(page_entries[j : j + self.cards_per_row])
                ]
                for j in range(0, len(page_entries), self.cards_per_row)
            ]

            self._place_on_page(self.card_height, card_width, self.cards_per_row, back_data, story)

        doc.build(story)

    @classmethod
    def _create_front_content(cls, entry: FlashCard, style: ParagraphStyle) -> IndexedCardContent:
        return IndexedCardContent(entry, style)

    @staticmethod
    def _place_on_page(card_height: float, card_width: float, cards_per_row: int, data: list[list[Flowable]], story: list[Flowable]) -> None:
        table = Table(
            data,
            colWidths=[card_width] * cards_per_row,
            rowHeights=[card_height] * len(data),
        )
        table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 2, colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )
        story.append(table)
        story.append(PageBreak())
