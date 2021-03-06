"""
click-man - Generate man pages for click application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides a click CLI command to
generate man pages from a click application.

:copyright: (c) 2016 by Timo Furrer.
:license: MIT, see LICENSE for more details.
"""

import os
import click
from pkg_resources import iter_entry_points, get_distribution

from click_man.core import write_man_pages, write_asciidoc_pages


@click.command(context_settings={'help_option_names': ['-h', '--help']})
@click.option('--target', '-t', default=os.path.join(os.getcwd(), 'man'),
              type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
              help='Target location for the man pages')
@click.option('--asciidoc', '-a', default=False, is_flag=True,
              help='Generate asciidoc instead of man pages')
@click.option('--mansect', '-m', default=1, help='The section number in which the man page should be placed')
@click.option('--source', '-s', default='Python', help='The source of the command.')
@click.option('--manual', '-T', default='Commands', help='The title of the manual')
@click.version_option(get_distribution('click-man').version, '-V', '--version')
@click.argument('name')
def cli(target, asciidoc, name, mansect, source, manual):
    """
    Generate man pages for the scripts defined in the ``console_acripts`` entry point.

    The cli application is gathered from entry points of installed packages.

    The generated man pages are written to files in the directory given
    by ``--target``.
    """
    console_scripts = [ep for ep in iter_entry_points('console_scripts', name=name)]
    if len(console_scripts) < 1:
        raise click.ClickException('"{0}" is not an installed console script.'.format(name))
    # Only generate man pages for first console script
    entry_point = console_scripts[0]
    
    # create target directory if it does not exist yet
    try:
        os.makedirs(target)
    except OSError:
        pass

    click.echo('Load entry point {0}'.format(name))
    cli = entry_point.resolve()
    if asciidoc:
        click.echo('Generate asciidoc pages for {0} in {1}'.format(name, target))
        write_asciidoc_pages(name, cli, version=entry_point.dist.version, target_dir=target, mansect=mansect, source=source, manual=manual)
    else:
        click.echo('Generate man pages for {0} in {1}'.format(name, target))
        write_man_pages(name, cli, version=entry_point.dist.version, target_dir=target, mansect=mansect, source=source, manual=manual)


if __name__ == '__main__':
    cli()
