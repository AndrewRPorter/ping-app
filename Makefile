all: clean train test build docker-run

run:
	gunicorn --bind 0.0.0.0:8000 --workers 4 app.wsgi

start-cron:
	python3 schedule.py --start

stop-cron:
	python3 start_cron.py --end
	python3 schedule.py --end

test:
	python3 -m pytest -rav tests

clean:
	rm -rf *__pycache__
	rm -rf *.pyc

.PHONY: clean test run all
