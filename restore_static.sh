#!/bin/sh

../auction_env/bin/python manage.py loaddata backup/flatpages.json
../auction_env/bin/python manage.py loaddata backup/treemenus.json
../auction_env/bin/python manage.py loaddata backup/treemenus_ext.json
../auction_env/bin/python manage.py loaddata backup/sites.json
../auction_env/bin/python manage.py loaddata backup/auth_group.json
