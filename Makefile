run:
	env FLASK_ENV=development FLASK_APP=app.py SQLALCHEMY_DATABASE_URI="sqlite:///db/database.db" python3 run.py

init_db:
	python3 app/db/init_db.py

reset_db:
	python3 app/db/reset_db.py

run_container:
	docker container run -i -p 8000:8000 -v `pwd`/app/db/:/db/ limited_use_links

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
