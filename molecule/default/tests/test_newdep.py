import os
import re
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('omero-server-newdep')


OMERO = '/opt/omero/server/OMERO.server/bin/omero'
VERSION_PATTERN = re.compile('(\d+)\.(\d+)\.(\d+)-ice36-')


def test_omero_version(host):
    with host.sudo('data-importer'):
        ver = host.check_output("%s version" % OMERO)
    m = VERSION_PATTERN.match(ver)
    assert m is not None
    assert int(m.group(1)) >= 5
    assert int(m.group(2)) > 2


def test_postgres_version(host):
    ver = host.check_output("psql --version")
    assert ver.startswith('psql (PostgreSQL) 9.6.')
