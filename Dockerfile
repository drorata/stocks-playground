FROM python:3.10

RUN mkdir $HOME/prj
WORKDIR $HOME/prj

COPY ./Pipfile* .

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

COPY dashboard.py .
ENTRYPOINT /usr/local/bin/streamlit run dashboard.py
