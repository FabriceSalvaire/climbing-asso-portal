####################################################################################################
#
# Climbing Asso Portal - A Portal for Climbing Club (Association)
# Copyright (C) 2018 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

__all__ = [
    'ArgumentParser',
]

####################################################################################################

import argparse

from . import Defaults

####################################################################################################

class ArgumentParser:

    ##############################################

    def __init__(self, shell):

        self._shell = shell

        self._parser = argparse.ArgumentParser(description='Boostrap Climbing Asso Portal.')

        subparsers = self._parser.add_subparsers(
            dest='subparser_name',
            title='subcommands',
            description='valid subcommands',
            help='additional help',
        )

        ################################

        shell_parser = subparsers.add_parser(
            'shell',
            help='Run shell',
        )

        # shell_parser.set_defaults(func=shell.cmdloop)

        ################################

        all_setup_parser = subparsers.add_parser(
            'all',
            help='Run all setup commands',
        )

        # all_setup_parser.set_defaults(func=shell.do_all_setup)

        ################################

        check_parser = subparsers.add_parser(
            'check',
            help='Check setup',
        )

        check_parser.set_defaults(func=shell.do_check)

        ################################

        migrate_parser = subparsers.add_parser(
            'migrate',
            help='Migrate database',
        )

        migrate_parser.set_defaults(func=shell.do_migrate)

        ################################

        collect_static_parser = subparsers.add_parser(
            'collect_static',
            help='Collect static',
        )

        collect_static_parser.set_defaults(func=shell.do_collect_static)

        ################################

        create_superuser_parser = subparsers.add_parser(
            'create_superuser',
            help='Create superuser',
        )

        create_superuser_parser.add_argument(
            '--superuser', default=Defaults.SUPERUSER,
            help='Super user name',
        )

        create_superuser_parser.add_argument(
            '--superuser-email', default=Defaults.SUPERUSER_EMAIL,
            help='Super user email',
        )

        create_superuser_parser.set_defaults(func=shell.do_create_superuser)

        ################################

        load_data_parser = subparsers.add_parser(
            'load_data',
            help='Load data',
        )

        load_data_parser.set_defaults(func=shell.do_load_data)

        ################################

        create_initial_revisions_parser = subparsers.add_parser(
            'create_initial_revisions',
            help='Create initial revisions',
        )

        create_initial_revisions_parser.set_defaults(func=shell.do_create_initial_revisions)

        ################################

        drop_migrations_parser = subparsers.add_parser(
            'drop_migrations',
            help='Drop migrations',
        )

        drop_migrations_parser.set_defaults(func=shell.do_drop_migrations)

        ################################

        dump_data_parser = subparsers.add_parser(
            'dump_data',
            help='Dump data',
        )

        dump_data_parser.add_argument(
            '--indent',
            action='store_true',
            help='Indent JSON',
        )

        dump_data_parser.add_argument(
            'model', metavar='MODEL',
            help='model python path',
        )

        dump_data_parser.add_argument(
            'fixture', metavar='FIXTURE',
            help='fixture base name',
        )

        dump_data_parser.set_defaults(func=shell.do_dump_data)

    ##############################################

    def parse(self):

        args = self._parser.parse_args()

        # Call command
        if args.subparser_name == 'shell':
            self._shell.cmdloop()
        elif 'func' in args:
            args.func(args)
        else:
            self._parser.print_help()
