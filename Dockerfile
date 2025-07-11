FROM python:latest	

WORKDIR /sympa-auditor

ENV MAILING_LIST_URL='https://lists.ncsa.illinois.edu'
ENV OUTPUT_FILE='audit.json' 
ENV USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
ENV CONFIG_PATH='config.yaml'

COPY audit.py audit.py
COPY requirements.txt requirements.txt
COPY config.yaml config.yaml

RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the app
CMD ["python", "audit.py"]