import time
import logging
from ping3 import ping
from colorama import just_fix_windows_console, Fore
just_fix_windows_console()

NO_OF_PINGS = 10
DESTINATION_HOST = "google.com"

logging.basicConfig(filename='pinger.log', encoding='utf-8', level=logging.INFO)


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
        quality = f"{Fore.LIGHTRED_EX}????"

    if prev_avg:
        trend_arrow = f"{Fore.RESET} -"  # Default is stable
        if avg_ping and prev_avg:  # If both values are valid for comparison
            if avg_ping > prev_avg + 2:
                trend_arrow = f"{Fore.LIGHTRED_EX} ↓"
            elif avg_ping < prev_avg - 2:
                trend_arrow = f"{Fore.LIGHTGREEN_EX} ↑"
        quality += trend_arrow

    return quality


def print_status(status_type, **kwargs):
    if status_type == 'current_ping':
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
    elif status_type == 'unexpected_error':
        print(f"\r{Fore.LIGHTRED_EX}"
              f"!!!            UNEXPECTED ERROR:  Check Logs            !!!"
              f"{Fore.RESET}", end='', flush=True)


def main():
    logging.info(f"Sending {NO_OF_PINGS} pings to {DESTINATION_HOST}")
    ping_list = []
    prev_avg = 0
    losses = []

    while True:
        try:
            last_ping = ping(DESTINATION_HOST, unit="ms")

            if last_ping == 0.0 or last_ping is None or False:
                losses.append(True)
            else:
                losses.append(False)
                ping_list.append(round(last_ping, 1))
                last_ping = round(last_ping, 1)
            losses = losses[-NO_OF_PINGS:]
            loss = round(int((sum(losses) / NO_OF_PINGS) * 100), 1)

            if len(ping_list) >= NO_OF_PINGS:
                avg_ping = round(sum(ping_list) / len(ping_list))
                print_status('current_ping',
                             last_ping=last_ping if last_ping else 0, avg_ping=avg_ping,
                             prev_avg=prev_avg, loss=loss)
                ping_list = ping_list[-NO_OF_PINGS:]
                prev_avg = avg_ping
            else:
                progress_str = f"{len(ping_list)} of {NO_OF_PINGS}"
                print_status('current_ping',
                             last_ping=last_ping, progress_str=progress_str)
        except Exception as e:
            logging.exception(f"An unexpected error occurred: {e}")
            print_status('unexpected_error')
        time.sleep(0.2)


if __name__ == '__main__':
    main()
