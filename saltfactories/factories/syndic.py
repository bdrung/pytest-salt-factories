# -*- coding: utf-8 -*-
'''
saltfactories.factories.minion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Minion Factory
'''

# Import Python libs
from __future__ import absolute_import, print_function, unicode_literals

# Import Salt libs
import salt.config
import salt.utils.dictupdate as dictupdate

# Import Salt Factories libs
from saltfactories.utils import compat, ports


class SyndicFactory(object):
    def __init__(self, tempdir, config):
        self.tempdir = tempdir
        self.config = config

    @staticmethod
    def default_config(
        root_dir, syndic_id, default_options=None, config_overrides=None, master_port=None
    ):

        if default_options is None:
            default_options = salt.config.syndic_config(None, None)

        root_dir = root_dir.join('syndics', syndic_id).ensure(dir=True)
        conf_dir = root_dir.join('conf').ensure(dir=True)
        conf_file = conf_dir.join('minion').strpath

        stop_sending_events_file = conf_dir.join('stop-sending-events-{}'.format(syndic_id)).strpath
        with compat.fopen(stop_sending_events_file, 'w') as wfh:
            wfh.write('')

        _default_options = {
            'id': syndic_id,
            'conf_file': conf_file,
            'root_dir': root_dir.strpath,
            'interface': '127.0.0.1',
            'master': '127.0.0.1',
            'master_port': master_port or ports.get_unused_localhost_port(),
            'syndic_master': '127.0.0.1',
            'syndic_master_port': master_port or ports.get_unused_localhost_port(),
            'tcp_pub_port': ports.get_unused_localhost_port(),
            'tcp_pull_port': ports.get_unused_localhost_port(),
            'syndic_pidfile': 'run/syndic.pid',
            'pki_dir': 'pki',
            'cachedir': 'cache',
            'sock_dir': '.salt-unix',
            'syndic_log_file': 'logs/syndic.log',
            'log_level_logfile': 'debug',
            'loop_interval': 0.05,
            'open_mode': True,
            #'multiprocessing': False,
            'log_fmt_console': '[%(levelname)-8s][%(name)-5s:%(lineno)-4d] %(message)s',
            'log_fmt_logfile': '[%(asctime)s,%(msecs)03.0f][%(name)-5s:%(lineno)-4d][%(levelname)-8s] %(message)s',
            'hash_type': 'sha256',
            'transport': 'zeromq',
            'pytest': {
                'log': {'prefix': 'salt-syndic({})'.format(syndic_id)},
                'engine': {
                    'port': ports.get_unused_localhost_port(),
                    'stop_sending_events_file': stop_sending_events_file,
                    #'events': ['pytest/syndic/{}/start'.format(syndic_id)],
                },
            },
        }
        for varname in ('sock_dir',):
            # These are settings which are tested against and provided by Salt's test suite, so,
            # let's not override them if provided
            if varname in default_options:
                _default_options.pop(varname)
        # Merge in the initial default options with the internal _default_options
        dictupdate.update(default_options, _default_options, merge_lists=True)

        if config_overrides:
            # Merge in the default options with the syndic_config_overrides
            dictupdate.update(default_options, config_overrides, merge_lists=True)

        return default_options
