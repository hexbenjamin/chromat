from typing import Any, List
from coloraide.types import ColorInput, VectorLike

from coloraide import Color, util


class ChroColor(Color):
    def __init__(
        self,
        color: ColorInput,
        data: VectorLike | None = None,
        alpha: float = util.DEF_ALPHA,
        **kwargs: Any,
    ) -> None:
        super().__init__(color, data, alpha, **kwargs)

    @property
    def hex(self) -> str:
        return self.to_string(hex=True, upper=True)

    @property
    def rgb(self) -> List[int]:
        return [round(255 * c) for c in self.convert("srgb").to_dict()["coords"]]

    @property
    def hsl(self) -> List[int]:
        return [
            round(a * b)
            for a, b in zip(
                self.convert("hsl").to_dict()["coords"],
                [1, 100, 100],
            )
        ]

    @property
    def lch(self) -> List[int]:
        return [round(a) for a in self.convert("lch").to_dict()["coords"]]
