# start with python image
FROM python:3.8-slim

# copy the Pipfile
# this ensures that any downstream changes don't cause pipenv to unnecessarily
# re-run the locking process which takes a while, this will only happen if we
# need new dependencies
WORKDIR /usr/src/app
COPY Pipfile* ./

# setup python stuff
RUN pip install pipenv &&\
    pipenv install --dev

# copy the gcp credentials
COPY ./gcp_auth.json .

# copy our source
COPY analysis ./analysis
COPY utils ./utils

# install our modules
# RUN pipenv run python ./utils/setup.py install

# just to make it run?
ENTRYPOINT ["bash"]
