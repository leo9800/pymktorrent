import libtorrent
import pathlib


class InvalidFileException(Exception):
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f"Invalid file path: {self.path}"


class InvalidArgumentException(Exception):
    def __init__(self, reason: str):
        self.reason = reason

    def __repr__(self):
        return f"Invalid argument: {self.reason}"


def create_torrent(
    filepath: str,
    trackers: list[str] = [],
    size_exp: int = 20,
    comment: str = None,
    date: bool = True,
    priv: bool = False,
    v2_only: bool = False,
    v1_only: bool = False,
    url_seed: list[str] = [],
) -> bytes:
    if v1_only and v2_only:
        raise InvalidArgumentException(
            "The flag 'v1_only' and 'v2_only' could not be set simultaneously."
        )

    file_storage = libtorrent.file_storage()
    path = pathlib.Path(filepath)
    parent = path.parent

    if not path.exists():
        raise InvalidFileException(filepath)

    if path.is_file():
        file_storage.add_file(str(path.name), path.stat().st_size)

    if path.is_dir():
        pass  # TBD

    flags = 0

    if v2_only:
        flags |= libtorrent.create_torrent.v2_only

    if v1_only:
        flags |= libtorrent.create_torrent.v1_only

    torrent = libtorrent.create_torrent(
        file_storage,
        piece_size=2**size_exp,
        flags=flags
    )

    torrent.set_creator(f"{libtorrent.__name__}/{libtorrent.__version__}")
    torrent.set_comment(comment)
    torrent.set_priv(priv)

    for t in trackers:
        torrent.add_tracker(t)

    for us in url_seed:
        torrent.add_url_seed(us)

    libtorrent.set_piece_hashes(torrent, str(parent))
    return libtorrent.bencode(torrent.generate())
