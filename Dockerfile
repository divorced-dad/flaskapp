# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app/
COPY . /usr/src/app/
ENV FLASK_APP=/usr/src/app/__init__.py

# Install pip requirements
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /usr/src/app/
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]

# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
# CMD ["flask", "run", "--host", "0.0.0.0", "-p", "5000"]
CMD ["flask", "run", "--host=0.0.0.0"]
# ENTRYPOINT ["python", "run.py"]
