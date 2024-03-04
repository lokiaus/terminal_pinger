import time
import logging
from ping3 import ping
from colorama import just_fix_windows_console, Fore
just_fix_windows_console()

NO_OF_PINGS = 10
DESTINATION_HOST = "google.com"

logging.basicConfig(filename='pinger.log', encoding='utf-8', level=logging.DEBUG)


def signal_quality(avg_ping, prev_avg=None):
    if avg_ping is None:  # Indicates an error
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
    else:  # This wouldn't happen logically
        quality = f"{Fore.LIGHTRED_EX}UNKNOWN"

    if prev_avg:
        trend_arrow = f"{Fore.RESET} -"  # Default is stable
        if avg_ping and prev_avg:  # If both values are valid for comparison
            if avg_ping > prev_avg:
                trend_arrow = f"{Fore.LIGHTRED_EX} ↓"
            elif avg_ping < prev_avg:
                trend_arrow = f"{Fore.LIGHTGREEN_EX} ↑"
        quality += trend_arrow

    return quality


def main():
    logging.info(f"Sending {NO_OF_PINGS} pings to {DESTINATION_HOST}")
    ping_list = []
    prev_avg = None
    while True:
        try:
            last_ping = ping(DESTINATION_HOST, unit="ms")

            if last_ping == 0.0 or last_ping is None or False:
                logging.info(f"last_ping: {last_ping}, ping_list: {ping_list}")
                print(f"\r{Fore.RED}!!!   CONNECTION ERROR:  Host Unreachable   !!!{Fore.RESET}", end='', flush=True)
            else:
                last_ping = round(last_ping, 1)
                # logging.info(f"ping_list: {ping_list}")
                ping_list.append(round(last_ping, 1))
                if len(ping_list) >= NO_OF_PINGS:
                    avg_ping = round(sum(ping_list) / len(ping_list))
                    print(f"\r{Fore.LIGHTMAGENTA_EX}current:{Fore.RESET} {int(last_ping):05}ms, "
                          f"{Fore.LIGHTMAGENTA_EX}avg:{Fore.RESET} {avg_ping:05}ms, "
                          f"{Fore.LIGHTMAGENTA_EX}quality:{Fore.RESET} "
                          f"{signal_quality(avg_ping, prev_avg)}{Fore.RESET}",
                          end='', flush=True)
                    ping_list = ping_list[-NO_OF_PINGS:]
                    prev_avg = avg_ping
                else:
                    progress_str = f"{len(ping_list)} of {NO_OF_PINGS}"
                    print(f"\r{Fore.LIGHTMAGENTA_EX}current:{Fore.RESET} {int(last_ping):05}ms, "
                          f"{Fore.LIGHTMAGENTA_EX}progress:{Fore.RESET} {progress_str}", end='', flush=True)
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            print(f"\r{Fore.RED}!!!An error occurred. Check logs for details!!!{Fore.RESET}", end='', flush=True)
        time.sleep(0.2)


if __name__ == '__main__':
    main()
