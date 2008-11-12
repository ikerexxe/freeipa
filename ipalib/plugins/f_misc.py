# Authors:
#   Jason Gerard DeRose <jderose@redhat.com>
#
# Copyright (C) 2008  Red Hat
# see file 'COPYING' for use and warranty information
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; version 2 only
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""
Misc frontend plugins.
"""

from ipalib import api, Command, Param, Bool


# FIXME: We should not let env return anything in_server
# when mode == 'production'.  This would allow an attacker to see the
# configuration of the server, potentially revealing compromising
# information.  However, it's damn handy for testing/debugging.
class env(Command):
    """Show environment variables"""

    takes_options = (
        Param('server?', type=Bool(), default=False,
            doc='Show environment variables of server',
        ),
    )

    def run(self, **kw):
        if kw.get('server', False) and not self.api.env.in_server:
            return self.forward()
        return self.execute()

    def execute(self):
        return tuple(
            (key, self.api.env[key]) for key in self.api.env
        )

    def output_for_cli(self, textui, result, **kw):
        textui.print_name(self.name)
        textui.print_keyval(result)
        textui.print_count(result, '%d variable', '%d variables')

api.register(env)
