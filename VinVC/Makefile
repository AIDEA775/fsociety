PY = python
MAN = manage.py
APPS = video user login chat_room friendship video_room

all:
	rm -f db.sqlite3
	$(PY) $(MAN) makemigrations $(APPS)
	$(PY) $(MAN) migrate
	$(PY) $(MAN) runserver

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

test:
	$(PY) $(MAN) test

.PHONY: clean

clean:
	  rm -f db.sqlite3

clean_all:
	rm -rf video/migrations user/migrations login/migrations
	rm -rf chat_room/migrations friendship/migrations video_room/migrations
	rm -rf video/__pycache__ user/__pycache__ login/__pycache__
	rm -rf chat_room/__pycache__ friendship/__pycache__ video_room/__pycache__
