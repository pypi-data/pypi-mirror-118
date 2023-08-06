from getopt import getopt
import sys
from nhentai_downloader import NhentaiDownloader


def main():
    """ nhentai 123456 65431 -p ./path  """
    opts, args = getopt(sys.argv[1:], 'p:f:')
    opt_map = dict(opts)
    filename = ''
    path = './'
    if '-p' in opt_map:
        path = opt_map['-p']
    if '-f' in opt_map:
        filename = opt_map['-f']
    downloader = NhentaiDownloader(
        god_numbers=args,
        filename=filename,
        path=path
    )
    downloader.exec()
