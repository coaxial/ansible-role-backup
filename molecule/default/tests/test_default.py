import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_tarsnap_presence(host):
    tarsnap = host.package('tarsnap')

    assert tarsnap.is_installed
    assert tarsnap.version.startswith('1.0')


def test_tarsnap_config_file(host):
    conf_file = host.file('/etc/tarsnap.conf')

    assert conf_file.exists
    assert conf_file.is_file
    assert conf_file.user == 'root'
    assert conf_file.group == 'root'
    assert conf_file.mode == 0o644


def test_tarsnap_key(host):
    key_file = host.file('/root/tarsnap.key')

    assert key_file.exists
    assert key_file.is_file
    assert key_file.user == 'root'
    assert key_file.group == 'root'
    assert key_file.mode == 0o600


def test_tarsnapper_presence(host):
    tarsnapper = host.pip_package.get_packages()['tarsnapper']

    assert tarsnapper['version'].startswith('0.4')


def test_tarsnapper_config_file(host):
    conf_file = host.file('/etc/tarsnapper.yml')
    custom_deltas = r"  default: '1d 7d 30d 360d'"
    job = (
            "  default:\n"
            "    sources:\n"
            "      - /etc/fstab\n"
            "    exec_before: uname -a\n"
            "    exec_after: '/var/log/tarsnapper.log >> \"`date +%Y-%m-%d`"
            ": default job ran\"'\n"
            "    delta: default")

    assert conf_file.exists
    assert conf_file.is_file
    assert conf_file.user == 'root'
    assert conf_file.group == 'root'
    assert conf_file.mode == 0o600
    assert conf_file.contains(custom_deltas)
    assert conf_file.contains(job)


def test_backup_cronjob(host):
    crontab = host.file('/var/spool/cron/crontabs/root')
    cron_line = (
            r"28 3 \* \* \* sudo /usr/local/bin/tarsnapper -c "
            "/etc/tarsnapper\.yml make >> /var/log/tarsnapper\.log 2>&1")

    assert crontab.contains(cron_line)
