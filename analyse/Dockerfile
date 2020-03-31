# start with python image
FROM python:3.8-slim

# copy the Pipfile
WORKDIR /usr/src/app
COPY Pipfile* ./

# setup python stuff
RUN pip install pipenv &&\
    pipenv install

# copy our source
# COPY analysis ./analysis
# COPY utils ./utils

# install our modules
# RUN pipenv run python ./utils/setup.py install

# just to make it run?
ENTRYPOINT ["bash"]
