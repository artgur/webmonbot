commons:
  pkg.installed:
    - pkgs:
      - epel-release
      - python34
      - python34-requests
      - python34-setuptools

Populate /tmp/webmonbot:
  file.copy:
    - name: /tmp/webmonbot
    - source: /vagrant/

Build an egg:
  cmd.run:
   - name: python3 setup.py install
   - cwd: /tmp/webmonbot
   - creates: /usr/lib/python3.4/site-packages/webmonbot-0.0.1-py3.4.egg

copy config file:
  file.copy:
    - source: /tmp/webmonbot/webmonbot.json
    - name: /etc/webmonbot.json

copy systemd.service file:
  file.copy:
    - name: /etc/systemd/system/webmonbot.service
    - source: /tmp/webmonbot/etc/webmonbot.service

run service:
  service.running:
    - name: webmonbot
    - enable: true