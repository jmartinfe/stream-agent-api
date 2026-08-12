# This is a Dockerfile for the stream-agent-api application. 
# It uses the official Python 3.11 slim image as the base image, 
# sets the working directory to /app, copies the requirements.txt file 
# and installs the dependencies, then copies the rest of the application code into the container.
# Finally, it specifies the command to run the application using uvicorn.
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]