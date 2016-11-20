#!/bin/sh

../auction_env/bin/python manage.py dumpdata flatpages --indent=2 > backup/flatpages.json
../auction_env/bin/python manage.py dumpdata treemenus --indent=2 > backup/treemenus.json
../auction_env/bin/python manage.py dumpdata menu_extension --indent=2 > backup/treemenus_ext.json
../auction_env/bin/python manage.py dumpdata sites --indent=2 > backup/sites.json
../auction_env/bin/python manage.py dumpdata auth.group --indent=2 > backup/auth_group.json
