# KYC API

KYC API is a backend service built with FastAPI to handle Know Your Customer (KYC) processes. It provides authentication, user management, and other KYC-related functionalities.

## Features

- **Authentication**: Secure user authentication with token-based mechanisms.
- **User Management**: APIs for managing user data.
- **CORS Support**: Configured to allow frontend and backend communication during development.
- **Redis Integration**: Utilizes Redis for caching or other data storage needs.
- **Middleware**: Custom middleware for token blacklisting.

## Requirements

- Python 3.8+
- Redis server
- FastAPI framework

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/kyc_api.git
   cd kyc_api

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate

3. Install dependencies:
    ```bash
    pip install -r requirements.txt

4. Set up environment variables: Create a .env file in the core directory and configure the following variables:
    ```bash
    PROJECT_NAME=KYC API
    VERSION=1.0.0
    REDIS_HOST=localhost
    REDIS_PORT=6379

5. Run the application:
    ```bash
    uvicorn app.main:app --reload    