# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only requirements to leverage Docker's layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download el_core_news_sm


# Copy the rest of the application code
COPY . .

EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app/app.py"]