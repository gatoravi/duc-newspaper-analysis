from __future__ import print_function, division
import signal, json
from datetime import datetime

import click

from newsponder.downloader import Downloader

from .version import __version__

@click.group()
@click.version_option(version=__version__)
def cli():
    # to make this script/module behave nicely with unix pipes
    # http://newbebweb.blogspot.com/2012/02/python-head-ioerror-errno-32-broken.html
    signal.signal(signal.SIGPIPE,signal.SIG_DFL)

@cli.command()
@click.option('--dump-dir', required=True, type=click.Path(),
              help="Base directory to dump article data into")
@click.option('--start', required=True, type=click.STRING,
              metavar='YYYY-MM-DD',
              help="Start Date [inclusive]")
@click.option('--end', required=True, type=click.STRING,
              metavar='YYYY-MM-DD',
              help="End date [exclusive]")
@click.option('--section', default="sports", type=click.STRING,
              help='The newspaper section of interest [default=sports]')
@click.option('--subsection', default=None, type=click.STRING,
              help='The newspaper subsection of interest [default=None]')
def download(start, end, section, subsection, dump_dir):
    d = Downloader(dump_dir)
    d.dump_articles(
        start=start,
        end=end,
        section=section,
        subsection=subsection,
    )

@cli.command()
@click.option('--day', required=True, type=click.STRING,
              metavar='YYYY-MM-DD',
              help="Day of interest format")
def articleindex(day):
    daytime = datetime.strptime(day, '%Y-%m-%d')

    d = Downloader()
    index = d.get_paper_index(daytime)
    print(json.dumps(index, indent=4))

@cli.command()
def analyze():
    click.echo("Please implement me!")

if __name__ == '__main__':
    cli()
