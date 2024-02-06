FROM python:3.8-slim

WORKDIR /app

ENV PYTHONPATH /home/nahuelsuncheski/proyectos/multas/layers/python

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
