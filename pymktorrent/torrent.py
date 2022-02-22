import libtorrent
import pathlib
import enum


class InvalidFileException(Exception):
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f"Invalid file path: {self.path}"


class TorrentFormat(enum.Enum):
    Hybrid = 0
    V1 = 1
    V2 = 2


def create_torrent(
    filepath: str,
    trackers: list[str] = [],
    size_exp: int = 20,
    comment: str = None,
    date: bool = True,
    priv: bool = False,
    torrent_format: TorrentFormat = TorrentFormat.Hybrid,
    url_seed: list[str] = [],
) -> bytes:
    file_storage = libtorrent.file_storage()
    path = pathlib.Path(filepath)
    parent = path.parent
    flags = 0

    if not path.exists():
        raise InvalidFileException(filepath)

    if path.is_file():
        file_storage.add_file(str(path.name), path.stat().st_size)

    if path.is_dir():
        pass  # TBD

    match torrent_format:
        case TorrentFormat.Hybrid:
            pass
        case TorrentFormat.V1:
            flags |= libtorrent.create_torrent.v1_only
        case TorrentFormat.V2:
            flags |= libtorrent.create_torrent.v2_only

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
