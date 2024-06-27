# https://github.com/python-poetry/poetry/issues/1178#issuecomment-998549092
FROM python:3.12 AS builder

# Don't buffer `stdout`:
ENV PYTHONUNBUFFERED=1
# Don't create `.pyc` files:
ENV PYTHONDONTWRITEBYTECODE=1

ADD pyproject.toml poetry.lock /app/

RUN pip install poetry
RUN poetry config virtualenvs.in-project true

WORKDIR /app
COPY . .

RUN poetry install --only main


#########################

FROM python:3.12-alpine

WORKDIR /app

COPY --from=builder /app /app

# # For options, see https://boxmatrix.info/wiki/Property:adduser
# RUN adduser app -DHh ${WORKDIR} -u 1000
# USER 1000
#
EXPOSE 8000/tcp
CMD "/app/docker-entrypoint.sh"
