FROM python:3.14.6

WORKDIR /web_app


COPY web_app/requirements.txt

RUN pip install -r requirements.txt

COPY web_app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]