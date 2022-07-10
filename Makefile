run:
	env FLASK_ENV=development FLASK_APP=app.py SQLALCHEMY_DATABASE_URI="sqlite:///db/database.db" python3 run.py

run_production:
	env FLASK_ENV=production gunicorn wsgi:app

setup: install_requirements init_db
	mkdir -p sharable/files
	python3 scripts/add_user.py

init_db:
	python3 app/db/init_db.py

reset_db:
	python3 app/db/reset_db.py

run_container:
	docker container run -i -p 8000:8000 -v `pwd`/app/db/:/db/  -v `pwd`/sharable/:/sharable/ limited_use_links

build_image:
	docker build -t limited_use_links .

lint:
	python3 -m flake8 app config.py run.py wsgi.py

install_requirements:
	python3 -m pip install -r requirements.txt

test:
	python3 -m pytest tests/test_*.py

shell:
	env FLASK_ENV=development FLASK_APP=app.py SQLALCHEMY_DATABASE_URI="sqlite:///db/database.db" flask shell

clean_docker_image:
	for c in `docker container ls -a | grep limited_use_links | awk '{print $$1}'`; do \
		docker container rm $$c; \
	done;
	for c in `docker image ls -a | grep limited_use_links | awk '{print $$3}'`; do \
		docker image rm $$c; \
	done;

clean:
	rm -f sharable/files/*.zip
