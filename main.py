import time
import logging
from ping3 import ping
from colorama import just_fix_windows_console, Fore

NO_OF_PINGS: int = 20  # Number of pings to send
DESTINATION_HOST: str = "google.com"  # Destination host to ping


def get_trend(avg_ping: float, prev_avg: float = None) -> str:
    """
    Function to determine the trend based on the average ping time.

    Parameters:
    avg_ping (float): The average ping time in milliseconds.
    prev_avg (float, optional): The previous average ping time in milliseconds. Default is None.

    Returns:
    str: A string representing the trend arrow.
    """
    if avg_ping is None:
        return f"{Fore.LIGHTRED_EX}  X"
    if prev_avg is None or avg_ping == prev_avg:
        return f"{Fore.RESET}  -"

    change: float = avg_ping - prev_avg

    if abs(change) > 0.5:
        thresholds: list[tuple] = [
            (-prev_avg * 0.3, f"{Fore.LIGHTCYAN_EX} ↑↑"),
            (-prev_avg * 0.2, f"{Fore.LIGHTCYAN_EX}  ↑"),
            (-prev_avg * 0.1, f"{Fore.LIGHTGREEN_EX}  ↑"),
            (0, f"{Fore.RESET}  ↑"),
            (prev_avg * 0.1, f"{Fore.RESET}  ↓"),
            (prev_avg * 0.2, f"{Fore.LIGHTYELLOW_EX}  ↓"),
            (prev_avg * 0.3, f"{Fore.LIGHTRED_EX}  ↓"),
            (float('inf'), f"{Fore.LIGHTRED_EX} ↓↓")
        ]

        for threshold, trend in thresholds:
            if change < threshold:
                return trend

    return f"{Fore.RESET}  -"


def signal_quality(avg_ping: float) -> str:
    """
    Function to determine the quality of the signal based on the average ping time.

    Parameters:
    avg_ping (float): The average ping time in milliseconds.

    Returns:
    str: A string representing the quality of the signal.
    """
    quality: str = (f"{Fore.LIGHTRED_EX}FAIL" if avg_ping is None else
                    f"{Fore.LIGHTRED_EX}POOR" if avg_ping > 150 else
                    f"{Fore.LIGHTYELLOW_EX}POOR" if avg_ping > 100 else
                    f"{Fore.LIGHTGREEN_EX}FINE" if avg_ping > 50 else
                    f"{Fore.LIGHTGREEN_EX}GOOD" if avg_ping > 20 else
                    f"{Fore.LIGHTCYAN_EX}BEST" if avg_ping > 0 else
                    f"{Fore.LIGHTRED_EX}????")

    return quality


def print_status(success: bool, **kwargs) -> None:
    """
    Function to print the status message.

    Parameters:
    success (bool): A boolean indicating whether the operation was successful.
    **kwargs: Variable length argument list containing the following optional arguments:
        - last_ping (float): The last recorded ping time in milliseconds.
        - progress_str (str): A string representing the progress of the operation.
        - avg_ping (float): The average ping time in milliseconds.
        - prev_avg (float): The previous average ping time in milliseconds.
        - loss (int): The percentage of packet loss.

    """
    if success:
        last_ping: float = kwargs['last_ping']
        progress_str: str = kwargs.get('progress_str')
        print_str: str = f"\r{Fore.LIGHTMAGENTA_EX}current:{Fore.RESET} {last_ping:05.0f}ms, "
        if progress_str:
            print_str += f"{Fore.LIGHTMAGENTA_EX}progress:{Fore.RESET} {progress_str}"
        else:
            avg_ping: float = kwargs['avg_ping']
            prev_avg: float = kwargs['prev_avg']
            loss: int = kwargs['loss']
            lc = Fore.LIGHTRED_EX if loss > 30 else Fore.LIGHTYELLOW_EX if loss > 0 else Fore.LIGHTGREEN_EX
            print_str += (f"{Fore.LIGHTMAGENTA_EX}avg:{Fore.RESET} {avg_ping:05.0f}ms, "
                          f"{Fore.LIGHTMAGENTA_EX}loss:{Fore.RESET} {lc}{loss:03}%{Fore.RESET}, "
                          f"{Fore.LIGHTMAGENTA_EX}quality:{Fore.RESET} "
                          f"{signal_quality(avg_ping if last_ping else None)}"
                          f"{get_trend(avg_ping if last_ping else None, prev_avg)}{Fore.RESET} ")
        print(print_str, end='', flush=True)
    else:
        print(f"\r{Fore.LIGHTRED_EX}"
              f"!!!            UNEXPECTED ERROR:  Check Logs            !!!"
              f"{Fore.RESET}", end='', flush=True)


def main() -> None:
    """
    Main function to handle inputs and send and process pings.

    The function prompts the user for the number of pings and the target host.
    It then sends the specified number of pings to the target host,
    calculates the average ping time, and prints the status message.

    """
    no_of_pings: int = NO_OF_PINGS
    destination_host: str = DESTINATION_HOST
    inp: str = input(f"Number of pings ({NO_OF_PINGS}): ")
    if inp.isdigit() and int(inp) > 0:
        no_of_pings = int(inp)
        inp = input(f"Target host ({DESTINATION_HOST}): ")
        destination_host = inp if inp else DESTINATION_HOST

    ping_list: list[float] = []
    losses: list[bool] = []
    prev_avg: float = 0.0
    
    logging.info(f"Sending {no_of_pings} pings to {destination_host}")
    progress_str: str = f"0 of {no_of_pings}"
    print_status(True, last_ping=0, progress_str=progress_str)
    
    time.sleep(0.2)

    while True:
        try:
            last_ping: float = ping(destination_host, unit="ms")

            is_loss: bool = last_ping == 0.0 or last_ping is None or False  # Check for loss
            losses.append(is_loss)
            losses = losses[-no_of_pings:]  # Keep only the last NO_OF_PINGS losses

            if not is_loss:
                ping_list.append(last_ping)
                ping_list = ping_list[-no_of_pings:]  # Keep only the last NO_OF_PINGS pings

            if len(ping_list) >= no_of_pings:  # If there are enough pings, calculate average and print status
                loss: int = int(sum(losses) / no_of_pings * 100)
                avg_ping: float = sum(ping_list) / len(ping_list)
                print_status(True, last_ping=last_ping if last_ping else 0,
                             avg_ping=avg_ping, prev_avg=prev_avg, loss=loss)
                prev_avg = avg_ping
            else:
                progress_str: str = f"{len(ping_list)} of {no_of_pings}"
                print_status(True, last_ping=last_ping if last_ping else 0, progress_str=progress_str)
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            print_status(False)
        time.sleep(0.2)


if __name__ == '__main__':
    just_fix_windows_console()  # Fix console for Windows
    logging.basicConfig(filename='pinger.log', level=logging.DEBUG)  # Set up logging
    main()
