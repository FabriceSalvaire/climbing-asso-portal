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

####################################################################################################

from pathlib import Path
import cmd
import glob
import json
import os
import subprocess

import colors # ansicolors @PyPI

from . import Defaults
from . import LogPrinting
from . import Translation

####################################################################################################

BASE_DIR = Path(__file__).parents[2].resolve()

####################################################################################################

class FakeArgument:

    ##############################################

    def __init__(self, args, defaults=None):

        self._args = dict(defaults) if defaults else {}
        for arg in args.split():
            if arg:
                if '=' in arg:
                    key, value = arg.split('=')
                    self._args[key] = value
                else:
                    self._args[arg] = True

    ##############################################

    def __getattr__(self, key):

        return self._args.get(key, None)

####################################################################################################

class Shell(cmd.Cmd):

    intro = 'Manage ClimbingAssoPortal.   Type help or ? to list commands.\n'
    prompt = colors.green('CAP > ')

    ##############################################

    def _print_banner(self, title, width=100):

        print(
            colors.red(
                LogPrinting.format_message_header(
                    title,
                    width=width,
                    centered=True,
                    margin=True,
                    border=True,
                    bottom_rule=True,
                    newline=False,
                )
            )
        )

    ##############################################

    def _yes_no(self, message, default='y'):

        response = input(message + ' : y/n [{}]'.format(default)).lower().strip()
        if not response:
            response = default
        return response == 'y'

    ##############################################

    def _manage(self, *args):

        try:
            subprocess.check_call(('manage.py', *args))
        except (subprocess.CalledProcessError, FileNotFoundError) as exception:
            rule = colors.red(LogPrinting.solid_wide_filet.horizontal * 100)
            print(rule)
            print(exception)
            print(rule)
            print(colors.red('Failed'))

    ##############################################

    def _check_args(self, args):

        if isinstance(args, str):
            return FakeArgument(args)
        else:
            return args

    ##############################################

    def do_quit(self, arg=None):

        'Quit shell'

        return True

    ##############################################

    def do_check(self, args=None):

        'Check'

        self._print_banner('Check')
        self._manage('check')

    ##############################################

    # Dangerous action !
    def do_drop_migrations(self, args=None):

        'Drop all migrations'

        self._print_banner('Drop migrations')
        pattern = str(BASE_DIR.joinpath(Defaults.APPLICATION, 'migrations', '0*.py'))
        migrations = glob.glob(pattern)
        migrations.sort()
        for path in migrations:
            if self._yes_no('Drop {} ?'.format(path), default='n'):
                os.unlink(path)

    ##############################################

    def do_migrate(self, args=None):

        'Migrate the database'

        self._print_banner('Migrate database')
        self._manage('makemigrations')
        self._manage('migrate')

    ##############################################

    def do_collect_static(self, args=None):

        'Collect static'

        self._print_banner('Collect static')
        self._manage(
            'collectstatic',
            '--noinput',
            '--clear',
            '--link',
        )

    ##############################################

    def do_create_superuser(self, args=None):

        'Create superuser'

        args = self._check_args(args)

        self._print_banner('Create superuser / admin')

        # Fixme: how ot pass for all
        if args is None:
            # superuser = create_superuser_parser.get_default('superuser')
            # superuser_email = create_superuser_parser.get_default('superuser_email')
            superuser = Defaults.SUPERUSER
            superuser_email = Defaults.SUPERUSER_EMAIL
        else:
            superuser = args.superuser
            superuser_email = args.superuser_email

        self._manage(
            'createsuperuser',
            # '--noinput',
            '--username', superuser,
            '--email', superuser_email,
        )

    ##############################################

    def do_load_data(self, args=None):

        'Load data'

        self._print_banner('Load Data')
        # pattern = str(BASE_DIR.joinpath(Defaults.APPLICATION, 'fixtures', '*.json'))
        pattern = str(BASE_DIR.joinpath('fixtures', '*.json'))
        fixtures = glob.glob(pattern)
        fixtures.sort()
        for fixture in fixtures:
            # print('load', fixture)
            if self._yes_no('Load {} ?'.format(fixture), default='y'):
                self._manage('loaddata', fixture)
        # _manage('loaddata', *fixtures)
        if self._yes_no('Update french cities ?', default='y'):
            # _manage('update_french_cities')
            json_path = BASE_DIR.joinpath('data', 'base_des_communes', 'laposte_hexasmal.json')
            self._manage('update_french_cities', '--laposte-hexasmal-json', json_path)
        if self._yes_no('Update routes ?', default='y'):
            self._manage('update_routes')
        # _manage('import_members')

    ##############################################

    def do_create_initial_revisions(self, args=None):

        'Create initial revisions'

        self._print_banner('Create initial revisions')
        self._manage(
            'createinitialrevisions',
            Defaults.APPLICATION + '.UserProfile',
            '--comment', 'Initial revision.'
        )

    ##############################################

    def do_dump_data(args=None):

        'Dump data'

        args = self._check_args(args)

        self._print_banner('Dump Data')

        output_path = BASE_DIR.joinpath('fixtures', args.fixture + '.json')
        print('Dump {} to {}'.format(args.model, output_path))
        self._manage(
            'dumpdata',
            args.model,
            # '--indent', 4,
            '-o', output_path
        )

        if args.indent:
            with open(output_path) as fh:
                json_data = json.load(fh)
            with open(output_path, 'w') as fh:
                json.dump(json_data, fh, indent=4, sort_keys=True)

    ##############################################

    def do_make_message(self, args=None):

        'Make Message'

        args = self._check_args(args)

        make_message = Translation.MakeMessage(Defaults.APPLICATION)

        if args.update:
            make_message.extract()
            if args.init:
                make_message.init()
            make_message.update()
        if args.compile:
            make_message.compile()

        # poedit
        # linguist-qt5

    ##############################################

    def do_all_setup(self, args=None):

        'Run all'

        self.do_check()
        self.do_migrate()
        self.do_collect_static()
        self.do_create_superuser()
        self.do_load_data()
        self.do_create_initial_revisions()
