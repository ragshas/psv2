# ---- Base image ----
FROM python:3.11-slim

# ---- Set working directory ----
WORKDIR /app

# ---- Copy requirements and install ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project code ----
COPY . .

# ---- Expose port ----
EXPOSE 5000

# ---- Run the Flask app with app factory ----
CMD ["python", "run.py"]
