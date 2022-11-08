FROM python:3.10

RUN mkdir $HOME/prj
WORKDIR $HOME/prj

RUN python -m pip install --upgrade pip \
    && curl -sSL https://install.python-poetry.org | python3 -

COPY ./pyproject.toml .
COPY ./poetry.lock .
COPY stocks_playground/dashboard.py ./stocks_playground/dashboard.py
COPY README.md .
RUN /root/.local/bin/poetry config virtualenvs.in-project true \
    && /root/.local/bin/poetry install

ENTRYPOINT .venv/bin/streamlit run stocks_playground/dashboard.py
