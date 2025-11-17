
FROM python:3.9


WORKDIR /code

# Копируем Pipfile и Pipfile.lock
COPY ./requirements.txt /code/

# Устанавливаем зависимости из Pipfile.lock
RUN pip install -r requirements.txt && \
    pip install sqlalchemy-utils && \
    pip install websockets

COPY ./src /code/src

# Добавляем src в PYTHONPATH
ENV PYTHONPATH=/code/src

# Запускаем как модуль
CMD ["python", "-m", "vafs"]
