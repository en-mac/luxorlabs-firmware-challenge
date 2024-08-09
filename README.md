# luxor-firmware-challenge
This project is a control application for managing the operation of a fleet of miners. The miner can operate in different modes based on the time of day, controlled via an API.

## Functionality

- Upon starting, the application will initially update the miner settings based on the current time.
- It will then schedule updates at the following times:
    - 00:00 to 06:00: Overclock
    - 06:00 to 12:00: Normal
    - 12:00 to 18:00: Underclock
    - 18:00 to 00:00: Curtail
- You can also manually set the profile for an individual miner to override the schedule.

## Assumptions
- app.py cannot be modified.

## Requirements

- Python 3.6+
- Virtual environment (optional but recommended)

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/en-mac/luxor-firmware-challenge.git
    cd luxor-firmware-challenge
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On macOS/Linux:
        ```sh
        source venv/bin/activate
        ```
    - On Windows:
        ```sh
        venv\Scripts\activate
        ```

4. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start the API Server:**
    - In one terminal, run:
        ```sh
        python app.py
        ```

2. **Set the mode for testing or production:**
    - For testing mode (to run updates every 15 seconds):
      ```sh
      export TEST_MODE=true
      ```
    - For production mode (default behavior):
      ```sh
      export TEST_MODE=false
      ```

3. **In a separate terminal, start the Flask web server:**
    ```sh
    python web_server.py
    ```

## Endpoints

- **GET /miner_configuration**
  - Description: Get the current configuration (state and profile) of all miners.
  - Access: [http://localhost:8000/miner_configuration](http://localhost:8000/miner_configuration)
  - Response: JSON with the current configuration of miners.

- **GET /miner_configuration/<miner_ip>**
  - Description: Get the configuration (state and profile) of a specific miner.
  - Access: [http://localhost:8000/miner_configuration/<miner_ip>](http://localhost:8000/miner_configuration/<miner_ip>)
  - Response: JSON with the configuration of the specified miner, or an error message if not found.

- **GET /logs**
  - Description: Get the logs of all miners.
  - Access: [http://localhost:8000/logs](http://localhost:8000/logs)
  - Response: JSON with logs for all miners.

- **GET /logs/<miner_ip>**
  - Description: Get the logs of a specific miner.
  - Access: [http://localhost:8000/logs/<miner_ip>](http://localhost:8000/logs/<miner_ip>)
  - Response: JSON with the logs of the specified miner, or an error message if not found.

- **POST /set_profile/<miner_ip>/<profile>**
  - Description: Set the profile for a specific miner.
  - Access: Must be done via curl.
  - Example Usage:
    ```sh
    curl -X POST http://localhost:8000/set_profile/192.168.1.1/overclock
    ```
  - Response: JSON with a success message or an error message.

- **POST /set_state/<miner_ip>/<state>**
  - Description: Set the state for a specific miner.
  - Access: Must be done via curl.
  - Example Usage:
    ```sh
    curl -X POST http://localhost:8000/set_state/192.168.1.1/active
    ```
  - Response: JSON with a success message or an error message.

## Testing

To run tests, use the following command:

```sh
python -m unittest discover -s tests
```
