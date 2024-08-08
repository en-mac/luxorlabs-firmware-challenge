# luxor-firmware-challenge
This project is a control application for managing the operation of a fleet of miners. The miner can operate in different modes based on the time of day, controlled via an API.

## Requirements

- Python 3.6+
- Virtual environment (optional but recommended)

## Installation

1. **Clone the repository:**
    ```
    git clone https://github.com/en-mac/luxor-firmware-challenge.git
    cd luxor-firmware-challenge
    ```

2. **Create a virtual environment:**
    ```
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On macOS/Linux:
        ```
        source venv/bin/activate
        ```
    - On Windows:
        ```
        venv\Scripts\activate
        ```

4. **Install the required packages:**
    ```
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start the API Server:**
    - In one terminal, run:
        ```
        python app.py
        ```

2. **Run the Web Server with Scheduler:**
    - In another terminal, run:
        ```
        python web_server.py
        ```

## Functionality

- The application will initially update the miner settings based on the current time.
- It will then schedule updates at the following times:
    - 00:00 to 06:00: Overclock
    - 06:00 to 12:00: Normal
    - 12:00 to 18:00: Underclock
    - 18:00 to 00:00: Curtail

- You can access the current state of the miners by navigating to:
    ```
    http://localhost:8000/state
    ```

- You can also access the logs by navigating to:
    ```
    http://localhost:8000/logs
    ```

## Notes

- The `MinerController` handles authentication and re-authentication if the token expires.
- Logging is enabled to help track the scheduler's actions and any potential issues.

## Troubleshooting

- Ensure the API server is running before starting the web server.

## Directory Structure




# Future improvements
- I would add a database to store the logs of the Miners by IP so that we can query the logs and see the history of the miners.
- I would create a UI to interact with the application and display the state of the miners.
- I tried to set up a re-authentication mechanism in the `MinerController` class but it is not working as expected. Instead I just request a login any time the state/profile is updated.