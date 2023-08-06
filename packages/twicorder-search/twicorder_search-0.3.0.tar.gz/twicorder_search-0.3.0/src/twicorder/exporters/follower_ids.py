
from pathlib import Path
from typing import Dict, Generator

from twicorder.utils import readlines


def get_files_by_user(root: Path) -> Dict[str, Generator[Path, None, None]]:
    return {d.name: d.glob("**/followers/ids/*.zip") for d in root.iterdir() if d.is_dir()}


def dump(root: Path, name: str, paths: Generator[Path, None, None]):
    ids = set()
    for path in paths:
        ids.update(readlines(str(path)))
    if not ids:
        return
    root.mkdir(parents=True, exist_ok=True)
    file_path = root.joinpath(f"{name}.txt")
    with open(file_path, "w") as handle:
        handle.writelines(sorted(ids, key=lambda x: int(x)))


def main():
    root = Path("/Users/thimic/Dropbox/Apps/Twicorder/data/search")
    out_root = Path("/Users/thimic/Desktop/follower_ids")
    for user, paths in get_files_by_user(root).items():
        dump(out_root, user, paths)


if __name__ == '__main__':
    main()
