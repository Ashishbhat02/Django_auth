FROM python:3.11
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set work directory
RUN mkdir /django
WORKDIR /django
# Copy requirements first (for better Docker caching)
COPY requirements.txt /django
# Install dependencies
RUN pip install -r requirements.txt
# Copy the rest of the project
COPY . /django
# Expose port 8000
EXPOSE 8000
# Start server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
