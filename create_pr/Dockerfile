FROM python:3.10-slim

RUN apt-get update && apt-get install -y git
WORKDIR /work
ADD create_pr.py .
RUN chmod +x create_pr.py

ENTRYPOINT ["/work/create_pr.py"]
