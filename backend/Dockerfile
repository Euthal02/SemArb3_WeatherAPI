# Base python package
FROM python:3.12-slim

# Working directory
WORKDIR /app

# Copy the dependencies
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt

COPY . .

# Executable commands
# adhoc just because it is easier to implement
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
