from typing import Any, List
from coloraide import Color, util
from coloraide.types import ColorInput, VectorLike


class ChroColor(Color):
    def __init__(
        self,
        color: ColorInput,
        data: VectorLike | None = None,
        alpha: float = util.DEF_ALPHA,
        **kwargs: Any,
    ) -> None:
        super().__init__(color, data, alpha, **kwargs)

    def convert(self, space: str, **kwargs) -> Color:
        converted = super().convert(space=space, **kwargs)
        return ChroColor(converted)

    @property
    def rgb(self) -> List[int]:
        return [round(c * 255) for c in self.convert("srgb").to_dict()["coords"]]

    @property
    def hsl(self) -> List[int]:
        return [
            round(a * b)
            for a, b in zip(self.convert("hsl").to_dict()["coords"], [1, 100, 100])
        ]

    @property
    def hex(self) -> str:
        return self.convert("srgb").to_string(hex=True, upper=True)

    @property
    def accent(self, threshold=0.6):
        r, g, b = self.convert("srgb").to_dict()["coords"]

        if (r * 0.299 + g * 0.587 + b * 0.114) > threshold:
            return ChroColor("#000000")
        else:
            return ChroColor("#FFFFFF")
