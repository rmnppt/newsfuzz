# start with python image
FROM python:3.8-slim

# copy the Pipfile
# this ensures that any downstream changes don't cause pipenv to unnecessarily
# re-run the locking process which takes a while, this will only happen if we
# need new dependencies
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY Pipfile* ./

# setup python stuff
RUN pip install pipenv &&\
    pipenv install --dev

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
# CMD exec pipenv run gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
