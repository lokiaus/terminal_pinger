import time
import logging
from ping3 import ping
from colorama import just_fix_windows_console, Fore

NO_OF_PINGS = 20  # Number of pings to send
DESTINATION_HOST = "google.com"  # Destination host to ping


def signal_quality(avg_ping, prev_avg=None):
    """
    Function to determine the quality of the signal based on the average ping time.
    """
    if avg_ping is None:
        quality = f"{Fore.LIGHTRED_EX}FAIL"
    elif avg_ping > 150:
        quality = f"{Fore.LIGHTRED_EX}POOR"
    elif avg_ping > 100:
        quality = f"{Fore.YELLOW}POOR"
    elif avg_ping > 50:
        quality = f"{Fore.LIGHTGREEN_EX}FINE"
    elif avg_ping > 20:
        quality = f"{Fore.LIGHTGREEN_EX}GOOD"
    elif avg_ping > 0:
        quality = f"{Fore.LIGHTCYAN_EX}BEST"
    else:
        quality = f"{Fore.LIGHTRED_EX}????"

    if prev_avg:  # Calculate trend if there is a previous average
        trend_threshold = prev_avg * 0.1
        trend_arrow = f"{Fore.RESET} -"
        if avg_ping and prev_avg:
            if avg_ping > prev_avg + trend_threshold:
                trend_arrow = f"{Fore.LIGHTRED_EX} ↓"
            elif avg_ping < prev_avg - trend_threshold:
                trend_arrow = f"{Fore.LIGHTGREEN_EX} ↑"
        quality += trend_arrow

    return quality


def print_status(success, **kwargs):
    """
    Function to print the status of the pinging process.
    """
    if success:
        last_ping = kwargs['last_ping']
        progress_str = kwargs.get('progress_str')
        print_str = f"\r{Fore.LIGHTMAGENTA_EX}current:{Fore.RESET} {int(last_ping):05}ms, "
        if progress_str:
            print_str += f"{Fore.LIGHTMAGENTA_EX}progress:{Fore.RESET} {progress_str}"
        else:
            avg_ping = kwargs['avg_ping']
            prev_avg = kwargs['prev_avg']
            loss = kwargs['loss']
            lc = Fore.LIGHTRED_EX if loss > 50 else Fore.LIGHTGREEN_EX if loss < 10 else Fore.LIGHTYELLOW_EX
            print_str += (f"{Fore.LIGHTMAGENTA_EX}avg:{Fore.RESET} {avg_ping:05}ms, "
                          f"{Fore.LIGHTMAGENTA_EX}loss:{Fore.RESET} {lc}{loss:03}%{Fore.RESET}, "
                          f"{Fore.LIGHTMAGENTA_EX}quality:{Fore.RESET} "
                          f"{signal_quality(avg_ping if last_ping else None, prev_avg)}{Fore.RESET}")
        print(print_str, end='', flush=True)
    else:
        print(f"\r{Fore.LIGHTRED_EX}"
              f"!!!            UNEXPECTED ERROR:  Check Logs            !!!"
              f"{Fore.RESET}", end='', flush=True)


def main():
    """
    Main function to send pings and print the status.
    """
    no_of_pings = NO_OF_PINGS
    destination_host = DESTINATION_HOST
    inp = input(f"Number of pings ({NO_OF_PINGS}): ")
    if inp.isdigit() and int(inp) > 0:
        no_of_pings = int(inp)
        inp = input(f"Target host ({DESTINATION_HOST}): ")
        if inp:
            destination_host = inp

    logging.info(f"Sending {no_of_pings} pings to {destination_host}")
    ping_list = []
    prev_avg = 0
    losses = []

    while True:
        try:
            last_ping = ping(destination_host, unit="ms")

            if last_ping == 0.0 or last_ping is None or False:  # Check for loss
                losses.append(True)
            else:
                losses.append(False)
                ping_list.append(round(last_ping, 1))
                last_ping = round(last_ping, 1)
            losses = losses[-no_of_pings:]  # Keep only the last NO_OF_PINGS losses
            loss = round(int((sum(losses) / no_of_pings) * 100), 1)

            if len(ping_list) >= no_of_pings:  # If there are enough pings, calculate the average and print the status
                avg_ping = round(sum(ping_list) / len(ping_list))
                print_status(True,
                             last_ping=last_ping if last_ping else 0, avg_ping=avg_ping,
                             prev_avg=prev_avg, loss=loss)
                ping_list = ping_list[-no_of_pings:]  # Keep only the last NO_OF_PINGS pings
                prev_avg = avg_ping
            else:
                progress_str = f"{len(ping_list)} of {no_of_pings}"
                print_status(True,
                             last_ping=last_ping, progress_str=progress_str)
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            print_status(False)
        time.sleep(0.2)


if __name__ == '__main__':
    just_fix_windows_console()  # Fix console for Windows
    logging.basicConfig(filename='pinger.log', encoding='utf-8', level=logging.INFO)  # Set up logging
    main()
