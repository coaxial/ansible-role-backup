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
`backup__rebuild_cache` | `false` | Will skip `tarsnap --fsck`
`backup__tarsnap_cachedir` | `/usr/local/tarsnap-cache` | Sets the directory tarsnap will use to cache backups (cf. [tarsnap.conf man page](https://www.tarsnap.com/man-tarsnap.conf.5.html)
`backup__tarsnap_keyfile` | `/root/tarsnap.key` | Sets the path where the tarsnap key will be saved
`backup__tarsnap_apt_key` | `40B98B68F04DE775` | ID for the key used to sign the tarsnap package
`backup__tarsnap_username` | `changeme@example.com` | Username for tarsnap.com (only required if you want to generate a new tarsnap key)
`backup__tarsnap_password` | `encrypt me` | Password for tarsnap.com (only required if you want to generate a new tarsnap key)
`backup__tarsnap_local_key` | `` | Path to already generated tarsnap key
`backup__tarsnapper_config_file` | `/etc/tarsnapper.yml` | Sets the path where the tarsnapper jobs configuration will be saved on the target host
`backup__tarsnapper_log_file` | `/var/log/tarsnapper.log` | Sets the path to where the cronjob logs will be written
`backup__tarsnapper_enabled` | `true` | Enables tarsnapper installation
`backup__cron_{minute,hour,dom,month,dow}` | respectively: `28`, `3`, `*`, `*`, `*` | Interval at which to run tarsnap for backups
`backup__install_pip` | `true` | Enables python-pip installation

Notes
-----

If there is no tarsnap key specified with `backup__tarsnap_local_key` , a
new Tarsnap key will be generated using the `backup__tarsnap_username` and
`backup__tarsnap_password` variables, and a new machine will be registered as
`{{ ansible_host }}`.

If tarsnap key is specified with `backup__tarsnap_local_key`, then that key
will be used instead and no new key generation or machine registration will
occur.

If the `Add tarsnap apt key` task fails, it means the package's key has changed
but I haven't updated the role yet. Check what the current key is at
https://www.tarsnap.com/pkg-deb.html, override its value with the
`backup__tarsnap_apt_key` variable, and open an issue so I can update the role
with the new key.


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
