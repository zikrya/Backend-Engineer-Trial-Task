# Django Stock Prediction and Backtesting System

This is a Django-based backend system designed to fetch financial data, run a basic backtesting strategy, integrate with a pre-trained machine learning model for stock price predictions, and generate reports. The system is containerized, deployed on AWS using EC2 and RDS, and uses GitHub Actions for CI/CD.

---

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Environment Variables](#environment-variables)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Endpoints](#endpoints)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [CI/CD Pipeline](#ci/cd-pipeline)
- [Contributing and Contact](#contributing-and-contact)

---

## Features
- Fetches financial data from Alpha Vantage API and stores it in a PostgreSQL database.
- Implements a backtesting strategy with buy/sell logic based on moving averages.
- Integrates a pre-trained machine learning model for predicting stock prices.
- Generates reports in both JSON and PDF formats with visual comparisons.
- Deployed on AWS using Docker, EC2, and RDS.
- CI/CD pipeline for automated deployment using GitHub Actions.

---

## Requirements
- Python 3.10+
- Django 4.0+
- PostgreSQL
- Docker and Docker Compose
- AWS account (for deployment)
- Alpha Vantage API key

---

## Environment Variables
The following environment variables are required:

- `ALPHA_VANTAGE_API_KEY`: Your Alpha Vantage API key for fetching financial data.
- `DATABASE_URL`: The PostgreSQL database URL in the format `postgres://USER:PASSWORD@HOST:PORT/DBNAME`.
- `SECRET_KEY`: Django’s secret key.
- `SECRET_KEY`: Django’s secret key, used for cryptographic signing.
- `ALLOWED_HOSTS`: Comma-separated list of hosts/domains allowed to connect to this Django instance.

Create a `.env` file in the root directory and add these variables:

```bash
ALPHA_VANTAGE_API_KEY=your_api_key_here
DATABASE_URL=your_postgres_database_url_here
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=your_allowed_hosts_here
DEBUG=True
```

---

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/stock-backend.git
   cd stock-backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   Run the migrations to set up the PostgreSQL database schema.
   ```bash
   python manage.py migrate
   ```

5. **Fetch sample data**:
   Run the management command to fetch stock data.
   ```bash
   python manage.py fetch_stock_data AAPL
   ```

6. **Run the server**:
   ```bash
   python manage.py runserver
   ```

---

## Running the Application

To start the Django development server, use:

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## Endpoints

- `/fetch/<symbol>/`: Fetch financial data for stock symbol.
- `/backtest/<symbol>/?initial_investment=[value]`: Run a backtest for stock symbol.
- `/predict/<symbol>/`: Predict stock prices for the next 30 days.
- `/report/<symbol>/?format=json|pdf`: Generate a report in JSON or PDF format.

---

## Running Tests

To run the test suite, execute the following command:

```bash
python manage.py test
```

Tests are available for each service:
- Fetching financial data from the Alpha Vantage API.
- Backtesting logic.
- Predicting stock prices using the pre-trained model.
- Generating reports (both JSON and PDF).

---

## Deployment

### Docker Setup

1. **Build the Docker image**:
   ```bash
   docker-compose build
   ```

2. **Run the application**:
   ```bash
   docker-compose up
   ```

### AWS Deployment

1. **EC2 Instance Setup**:
   - Launch an EC2 instance using Amazon Linux or Ubuntu.
   - Install Docker, Docker Compose, and Git.

2. **RDS Setup**:
   - Create an RDS PostgreSQL instance on AWS.
   - Use the `DATABASE_URL` format for the connection string.

3. **Deploy the app**:
   - SSH into the EC2 instance.
   - Clone the repository and pull the latest Docker image.
   - Run `docker-compose up` on the EC2 instance.

---

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment. Upon pushing code to the repository:
- Tests are automatically run.
- If tests pass, the code is built and deployed to the EC2 instance.

The GitHub Actions workflow is defined in the `.github/workflows/deploy.yml` file. Make sure to set up your AWS credentials in the GitHub secrets for seamless deployment.


