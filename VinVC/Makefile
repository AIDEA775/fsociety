PY = python
MAN = manage.py
APPS = video user login chat_room

main:
	 $(PY) $(MAN) makemigrations $(APPS)
	 $(PY) $(MAN) migrate

run:
	$(PY) $(MAN) runserver

shell:
	$(PY) $(MAN) shell

db:
	$(PY) $(MAN) dbshell

admin:
	$(PY) $(MAN) createsuperuser

.PHONY: clean

clean:
	  rm -f db.sqlite3
	  rm -rf video/migrations search/migrations login/migrations user/migrations chat_room/migrations
