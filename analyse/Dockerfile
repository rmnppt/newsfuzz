# start with python image
FROM python:3.8-slim

# copy the Pipfile
# this ensures that any downstream changes don't cause pipenv to unnecessarily
# re-run the locking process which takes a while, this will only happen if we
# need new dependencies
WORKDIR /app
COPY Pipfile* ./

# This fixes a bug in gcloud/pipenv, see here: https://github.com/pypa/pipenv/issues/4174
ENV PIPENV_VENV_IN_PROJECT 1

# setup python stuff
RUN pip install pipenv &&\
    pipenv install

# copy the gcp credentials
COPY ./gcp_auth.json .

# copy our source
COPY utils ./utils
COPY analysis ./analysis
COPY app.py ./

# install our modules
RUN pipenv run python ./utils/setup.py install
RUN pipenv run python ./analysis/setup.py install

EXPOSE $PORT

# lets go!
ENTRYPOINT ["pipenv", "run"]
CMD gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
