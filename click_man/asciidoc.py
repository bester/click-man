"""
click-man - Generate asciidoc pages for click application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides functionality to
write an asciidoc page from some given information
about a CLI application.

:copyright: (c) 2016 by Timo Furrer.
:license: MIT, see LICENSE for more details.
"""

from datetime import datetime


class AsciidocPage(object):
    """
    Represent an asciidoc page

    :param str command: the name of the command
    """

    def __init__(self, command, mansect, source, manual):
        self.source = source
        self.manual = manual
        self.mansect = mansect
        #: Holds the command of the man page
        self.command = command

        #: Holds the short help of the man page
        self.short_help = ''

        #: Holds the synopsis of the man page
        self.synopsis = ''

        #: Holds the description of the man page
        self.description = ''

        #: Holds the version of the man page
        self.version = '1.0.0'

        #: Holds a list of tuple options of the man page
        #  the first item in the tuple are the option switches
        #  and the second one is the option's description
        self.options = []

        #: Holds the commands of the man page
        self.commands = []

        #: Holds the date of the man page creation time.
        self.date = datetime.now().strftime("%d-%b-%Y")

    def __str__(self):
        """
        Generate and return the string representation
        of this man page.
        """
        lines = []

        # write title and footer
        lines.append('{0}({1})'.format(self.command.replace(' ', '-').upper(), self.mansect))
        lines.append((3 + len(self.command)) * '=')
        lines.append(':doctype:       manpage')
        lines.append(':man source:    {0}'.format(self.source))
        lines.append(':man manual:    {0}'.format(self.manual))
        lines.append('')
        lines.append('NAME')
        lines.append(len('NAME') * '-')
        lines.append('{0} - {1}'.format(self.command, self.short_help))

        # write synopsis
        lines.append('')
        lines.append('SYNOPSIS')
        lines.append(len('SYNOPSIS') * '-')
        lines.append('{0} {1}'.format(self.command, self.synopsis))

        # write the description
        if self.description:
            lines.append('')
            lines.append('DESCRIPTION')
            lines.append(len('DESCRIPTION') * '-')
            lines.append(self.description)

        # write the options
        if self.options:
            lines.append('')
            lines.append('OPTIONS')
            lines.append(len('OPTIONS') * '-')
            self.options = [o for o in self.options if o is not None]
            for option, description in self.options:
                option_unpacked = ['*'+x+'*' for x in option.split('\n')]
                lines.append('    {0}::'.format(' '.join(option_unpacked)))
                lines.extend(description.split("\n"))

        # write commands
        if self.commands:
            lines.append('')
            lines.append('COMMANDS')
            lines.append(len('COMMANDS') * '-')
            for name, description in self.commands:
                lines.append('*{0}*::'.format(name))
                lines.append(description)
                lines.append('    See *{0}-{1}({2})* for full documentation on the *{1}* command.'.format(
                    self.command.replace(' ', '-'), name, self.mansect))

        return '\n'.join(lines)
