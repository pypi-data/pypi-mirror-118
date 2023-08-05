from abc import ABC, abstractmethod
import tkinter as tk

from overrides import overrides
from overrides.enforce import EnforceOverrides

from ..model.cell import CellValue, CellValueAsString
from ..utils import FinalDecorator
from .icons import get_flag_icon, get_mine_icon, get_no_icon


class CellButtonConfigurator(ABC, EnforceOverrides):  # pylint: disable=too-few-public-methods
    """
    Handles the configuration of a button according to its cell value.
    """

    @FinalDecorator()
    def configure_button(self, button: tk.Button, cell_value: CellValue):
        if cell_value == CellValueAsString.NOT_REVEALED.value:
            self._configure_for_not_revealed(button)
        elif cell_value == CellValueAsString.REVEALED_ZERO_NEIGHBOUR.value:
            self._configure_for_zero_neighbour(button)
        elif cell_value == CellValueAsString.FLAGGED.value:
            self._configure_for_flagged(button)
        elif cell_value == CellValueAsString.MINE.value:
            self._configure_for_mine(button)
        else:
            assert isinstance(cell_value, int)
            self._configure_for_revealed_with_neighbours(
                button, nbr=cell_value)

    @FinalDecorator()
    @staticmethod
    def set_image(button: tk.Button, image):
        button.configure(image=image)

    @abstractmethod
    def _configure_for_not_revealed(self, button: tk.Button):
        pass

    @abstractmethod
    def _configure_for_flagged(self, button: tk.Button):
        pass

    @abstractmethod
    def _configure_for_mine(self, button: tk.Button):
        pass

    @abstractmethod
    def _configure_for_zero_neighbour(self, button: tk.Button):
        pass

    @abstractmethod
    def _configure_for_revealed_with_neighbours(self, button: tk.Button, nbr: int):
        pass


class MfranCellButtonConfigurator(CellButtonConfigurator):
    """Configurator for Mfranceschi theme."""

    @overrides
    def _configure_for_not_revealed(self, button: tk.Button):
        button.configure(state=tk.NORMAL, text=" ",
                         bg="blue", image=get_no_icon())

    @overrides
    def _configure_for_flagged(self, button: tk.Button):
        button.configure(state=tk.NORMAL, text=" ",
                         bg="yellow", image=get_no_icon())

    @overrides
    def _configure_for_mine(self, button: tk.Button):
        button.configure(state=tk.DISABLED, text=" ",
                         bg="red", image=get_no_icon())

    @overrides
    def _configure_for_zero_neighbour(self, button: tk.Button):
        button.configure(state=tk.DISABLED, text=" ",
                         bg="grey", image=get_no_icon())

    @overrides
    def _configure_for_revealed_with_neighbours(self, button: tk.Button, nbr: int):
        button.configure(state=tk.DISABLED, text=str(nbr),
                         bg="white", image=get_no_icon())


class WindowsXpCellButtonConfigurator(CellButtonConfigurator):
    """Configurator for Windows XP version theme."""

    @overrides
    def _configure_for_not_revealed(self, button: tk.Button):
        button.configure(state=tk.NORMAL, text=" ",
                         bg="dark gray", image=get_no_icon())

    @overrides
    def _configure_for_flagged(self, button: tk.Button):
        button.configure(state=tk.NORMAL, text="",
                         bg="yellow", image=get_flag_icon())

    @overrides
    def _configure_for_mine(self, button: tk.Button):
        button.configure(state=tk.DISABLED, text="",
                         bg="red", image=get_mine_icon())

    @overrides
    def _configure_for_zero_neighbour(self, button: tk.Button):
        button.configure(state=tk.DISABLED, text=" ",
                         bg="light gray", image=get_no_icon())

    @overrides
    def _configure_for_revealed_with_neighbours(self, button: tk.Button, nbr: int):
        button.configure(state=tk.DISABLED, text=str(nbr),
                         bg="white", image=get_no_icon())
