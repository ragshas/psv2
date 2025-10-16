# ---- Base image ----
FROM python:3.11-slim

# ---- Install SQLite CLI ----
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# ---- Set working directory ----
WORKDIR /app

# ---- Copy requirements and install ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project code ----
COPY . .

# ---- Expose port ----
EXPOSE 5000

# ---- Run the Flask app ----
CMD ["python", "run.py", "--host=0.0.0.0", "--port=5000"]
