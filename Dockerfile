FROM python:3.10

RUN mkdir $HOME/prj
WORKDIR $HOME/prj

RUN python -m pip install --upgrade pip \
    && curl -sSL https://install.python-poetry.org | python3 -

COPY ./pyproject.toml .
COPY ./poetry.lock .

RUN /root/.local/bin/poetry install --no-root

COPY dashboard.py .
ENTRYPOINT /usr/local/bin/streamlit run dashboard.py
