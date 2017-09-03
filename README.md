[![Build Status](https://travis-ci.org/coaxial/ansible-role-backup.svg?branch=master)](https://travis-ci.org/coaxial/ansible-role-backup)

Backup role
=========

This Ansible role will install and configure tarsnap + tarsnapper to make
encrypted backups at regular intervals.

These backups are stored with tarsnap which uses Amaozn S3.

Laern more about [Tarsnap, online backups for the truly paranoid](https://tarsnap.com).

Requirements
------------

- A tarsnap account with funds on it
- This role has only been tested on Ubuntu 16.04 (I'll expand it to other
  platforms if there is any interest, let me know by opening an issue)
- A tarsnapper config file at `templates/tarsnapper.yml.j2` in your playbook ([how to write a tarsnapper config file](https://github.com/miracle2k/tarsnapper#using-a-configuration-file)
- A tarsnap config file at `templates/tarsnap.conf.j2` in your playbook ([how to write a tarsnap config file](https://www.tarsnap.com/man-tarsnap.conf.5.html))

Role Variables
--------------

variable | default value | purpose
--- | --- | ---
`backup__tarsnap_cachedir` | `/usr/local/tarsnap-cache` | Sets the directory tarsnap will use to cache backups (cf. [tarsnap.conf man page](https://www.tarsnap.com/man-tarsnap.conf.5.html)
`backup__tarsnap_keyfile` | `/root/tarsnap.key` | Sets the path where the tarsnap key will be saved
`backup__tarsnap_apt_key` | `40B98B68F04DE775` | ID for the key used to sign the tarsnap package
`backup__tarsnap_username` | `changeme@example.com` | Username for tarsnap.com (only required if you want to generate a new tarsnap key)
`backup__tarsnap_password` | `encrypt me` | Password for tarsnap.com (only required if you want to generate a new tarsnap key)
`backup__tarsnapper_config_file` | `/etc/tarsnapper.yml` | Sets the path where the tarsnapper jobs configuration will be saved on the target host
`backup__tarsnapper_log_file` | `/var/log/tarsnapper.log` | Sets the path to where the cronjob logs will be written
`backup__cron_{minute,hour,dom,month,dow}` | respectively: `28`, `3`, `*`, `*`, `*` | Interval at which to run tarsnap for backups

Notes
-----

If there is no tarsnap key file found at `files/{{ ansible_hostname }}.yml`, a
new Tarsnap key will be generated using the `backup__tarsnap_username` and
`backup__tarsnap_password` variables, and a new machine will be registered as
`{{ ansible_host }}`.

If there is a tarsnap key at `files/{{ ansible_hostname }}.yml`, then that key
will be used instead and no new key generation or machine registration will
occur.


Dependencies
------------

None.

Example Playbook
----------------

```yaml
- hosts: all
  roles:
    - role: coaxial.backup
```

License
-------

MIT

Author Information
------------------

Coaxial <[64b.it](https://64b.it)>
