import torrent as t
import cli as c
import pathlib


if __name__ == '__main__':
    parser = c.create_parser()
    args = vars(parser.parse_args())

    print(args)

    # Modify the arguments
    comment = None if args['comment'] == '' else args['comment']

    match args['torrent_mode']:
        case 'v1':
            torrent_mode = t.TorrentFormat.V1
        case 'v2':
            torrent_mode = t.TorrentFormat.V2
        case 'mixed':
            torrent_mode = t.TorrentFormat.Hybrid

    default_output = str(pathlib.Path(args['filepath']).name) + '.torrent'
    output = default_output if args['output'] is None or '' else args['output']

    torrent_bytes = t.create_torrent(
        filepath=args['filepath'],
        trackers=args['trackers'],
        size_exp=args['size_exp'],
        comment=comment,
        date=args['date'],
        priv=args['priv'],
        torrent_format=torrent_mode,
        url_seeds=args['url_seeds']
    )

    with open(output, 'xb') as f:
        f.write(torrent_bytes)
