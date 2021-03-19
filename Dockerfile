FROM python:3.9

WORKDIR /lfwp

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY *.py /lfwp/

ENTRYPOINT ["python", "./process_widgets.py"]
