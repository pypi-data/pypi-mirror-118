
import pathlib

ROOT_FOLDER = pathlib.Path(__file__).parent.parent.parent
RESOURCES_FOLDER = ROOT_FOLDER / "rsc"

FLAG_ICON_PATH: str = str(pathlib.Path(
    (RESOURCES_FOLDER / "flag.png").resolve()))
MINE_ICON_PATH: str = str(pathlib.Path(
    (RESOURCES_FOLDER / "mine.png").resolve()))
