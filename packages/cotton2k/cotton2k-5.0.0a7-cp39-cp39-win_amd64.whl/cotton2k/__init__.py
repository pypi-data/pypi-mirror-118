"""Cotton2k model."""
import datetime
from argparse import ArgumentParser
from importlib.metadata import metadata, version
from pathlib import Path
from typing import Union

from appdirs import user_data_dir
from sqlalchemy import create_engine
from sqlalchemy.orm.session import Session

from .io import prepare_database, read_input, write_output
from .models import (
    AgronomyOperation,
    Climate,
    Cultivar,
    Profile,
    Simulation,
    Site,
    Soil,
    SoilHydrology,
    State,
    association_table,
)

__all__ = ("run",)

__version__ = version(__name__)
meta = metadata(__name__)
__author__: str = meta["Author"]
__license__: str = meta["License"]


DATA_DIR = Path(user_data_dir(__name__, __author__))
DB_PATH = DATA_DIR / (__name__ + ".sqlite3")
ENGINE_URL = f"sqlite+pysqlite:///{DB_PATH}"
if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True)


prepare_database(ENGINE_URL)


def run(profile_path: Union[Path, str, dict, Profile], *, output: bool = False):
    start_at = datetime.datetime.now()
    session = Session(bind=create_engine(ENGINE_URL))
    sim = read_input(profile_path, session)
    sim.run()
    execute_time = (datetime.datetime.now() - start_at).total_seconds()
    if output:
        write_output(sim, ENGINE_URL, session, start_at, execute_time)
    return sim


def main():
    parser = ArgumentParser()
    parser.add_argument("profile", help="Profile file path or name")
    parser.add_argument(
        "--output",
        action="store_true",
        help="Dump simulation result to user data directory.",
    )
    args = parser.parse_args()
    if (path := Path(args.profile)).exists():
        run(path, output=args.output)
    else:
        session = Session(bind=create_engine(ENGINE_URL))
        profile = (
            session.query(Profile).where(Profile.name == args.profile).one_or_none()
        )
        if profile is None:
            raise FileNotFoundError(f"Cannot found the profile {args.profile}")
        run(profile, output=args.output)


if __name__ == "__main__":
    main()
