# terminal_pinger

`terminal_pinger` is a Python-based application that sends a specified number of pings to a target host and provides detailed statistics about the operation. It is designed to be run in a terminal environment and provides real-time updates on the progress of the pinging operation.

## Features

- Sends a user-specified number of pings to a target host.
- Calculates and displays the average ping time.
- Tracks and displays the percentage of packet loss.
- Provides a quality indicator based on the average ping time and previous average ping time.
- Handles unexpected errors gracefully and logs them for further investigation.
- Colorizes console output for better readability.

## Usage

To use `terminal_pinger`, follow these steps:

1. Install the required dependencies by running `pip install -r requirements.txt` in your terminal.
2. Run the `main.py` script in your terminal.
3. When prompted, enter the number of pings you wish to send. If you press enter without providing a number, the default number of pings will be used.
4. Next, enter the target host you wish to ping. If you press enter without providing a host, the default host will be used.
5. The script will then begin sending pings to the target host and display real-time updates on the operation's progress.

## Code Structure

The main functions in the `main.py` script are:

- `ping(destination_host, unit="ms")`: Sends a single ping to the target host and returns the ping time in the specified unit.
- `signal_quality(avg_ping, prev_avg)`: Calculates a quality indicator based on the average ping time and the previous average ping time.
- `print_status(success, **kwargs)`: Prints a status message based on the success of the operation and various optional arguments.
- `main()`: Handles user input, sends and processes pings, and prints status messages.

## Logging

`terminal_pinger` logs all operations and any unexpected errors to a file named `pinger.log`. This log file can be used for troubleshooting and further investigation of any issues that may arise during the operation of the script.

## Requirements

- Python 3.6 or higher
- Windows operating system
- colorama library
- ping3 library

## Contributing

Contributions to `terminal_pinger` are welcome. Please fork the repository and create a pull request with your changes.

## License

`terminal_pinger` is open-source software licensed under the MIT license.