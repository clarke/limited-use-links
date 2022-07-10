FROM python:3.8-slim

COPY app/ ./app/
COPY requirements.txt config.py gunicorn.conf.py wsgi.py ./
RUN python3 -m pip install -r requirements.txt
EXPOSE 8000
ENV SQLALCHEMY_DATABASE_URI=sqlite:////db/database.db
CMD ["gunicorn", "wsgi:app"]
