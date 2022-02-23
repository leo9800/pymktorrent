import argparse


def check_size_exp(value) -> int:
    i = int(value)

    if i < 10 or i > 24:
        raise argparse.ArgumentTypeError(
            "block size exponential should be in range of 10 and 24."
        )

    return i


def create_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description='An utility to create torrent files.',
        allow_abbrev=False
    )

    p.add_argument(
        '-a', '--announce',
        metavar='url',
        dest='trackers',
        action='append',
        default=[],
        help='Specify tracker URLs for torrent'
    )

    p.add_argument(
        '-c', '--comment',
        metavar='comment',
        dest='comment',
        default=None,
        help='Add comment to torrent'
    )

    p.add_argument(
        '-d', '--nodate',
        dest='date',
        action='store_false',
        default=True,
        help='Don\'t write creation date for torrent'
    )

    p.add_argument(
        '-l', '--piece-length',
        dest='size_exp',
        type=check_size_exp,
        metavar='N',
        default=20,
        help='Set the piece length to 2^N bytes, default to 20 (1MiB)'
    )

    p.add_argument(
        '-m', '--mode',
        dest='torrent_mode',
        metavar='mode',
        default='mixed',
        choices={'v1', 'v2', 'mixed'},
        help='Set torrent format, \'1\' for v1 only, \'2\' for v2 only'
    )

    p.add_argument(
        '-o', '--output',
        dest='output',
        metavar='path',
        default=None,
        help='Set the path and filename of the created torrent file'
    )

    p.add_argument(
        '-p', '--private',
        dest='priv',
        action='store_true',
        default=False,
        help='Set the private flag, disable DHT, PeX and LSD'
    )

    p.add_argument(
        '-w', '--web-seed',
        dest='url_seeds',
        metavar='url',
        action='append',
        default=[],
        help='Specify web seed URLs for torrent'
    )

    p.add_argument(
        dest='filepath',
        metavar='file',
        type=str,
        help='File/directory to proceed'
    )

    return p
