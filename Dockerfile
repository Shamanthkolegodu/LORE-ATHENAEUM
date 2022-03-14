FROM python:3.8
COPY . .
RUN pip3 install -r requirements.txt
ENV PYTHONUNBUFFERED=1
CMD ["python3", "-u", "app.py"]  # -u and PYTHONUNBUFFERED=1 for print statements
