FROM python:latest	

WORKDIR /sympa-auditor

ENV MAILING_LIST_URL='https://lists.ncsa.illinois.edu'
ENV OUTPUT_FILE='/sympa_data/audit.json' 
ENV USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'

COPY audit.py audit.py
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

# Set the default command to run the app
CMD ["python", "audit.py"]