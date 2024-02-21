import time
# import logging
from ping3 import ping
from colorama import just_fix_windows_console
just_fix_windows_console()

NO_OF_PINGS = 10
DESTINATION_HOST = "google.com"


class BColors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_C = '\033[0m'


def signal_quality(avg_ping, prev_avg=None):
    if avg_ping > 150:
        quality = f"{BColors.FAIL}POOR"
    elif avg_ping > 100:
        quality = f"{BColors.WARNING}POOR"
    elif avg_ping > 50:
        quality = f"{BColors.OK_GREEN}FINE"
    elif avg_ping > 20:
        quality = f"{BColors.OK_GREEN}GOOD"
    elif avg_ping > 0:
        quality = f"{BColors.OK_CYAN}BEST"
    else:
        quality = f"{BColors.FAIL}FAIL"

    if prev_avg is not None:
        if avg_ping > prev_avg:
            quality += " ↓"  # Down arrow
        elif avg_ping < prev_avg:
            quality += " ↑"  # Up arrow
        else:
            quality += " -"  # Dash

    return quality


def main():
    # logging.basicConfig(filename='pinger.log', encoding='utf-8', level=logging.DEBUG)
    ping_list = []
    progress_dots = 0
    max_dots = NO_OF_PINGS - 1
    prev_avg = None
    while True:
        last_ping = ping(DESTINATION_HOST, unit="ms")
        if last_ping == 0.0 or last_ping is None or False:
            # logging.info(f"last_ping: {last_ping}, ping_list: {ping_list}")
            print(f"\r{BColors.FAIL}!!!   CONNECTION ERROR:  Host Unreachable   !!!{BColors.END_C}", end='', flush=True)
        else:
            last_ping = round(last_ping, 1)
            # logging.info(f"ping_list: {ping_list}")
            ping_list.append(round(last_ping, 1))
            if len(ping_list) >= NO_OF_PINGS:
                avg_ping = round(sum(ping_list) / len(ping_list))
                print(f"\r{BColors.HEADER}current:{BColors.END_C} {int(last_ping):05}ms, "
                      f"{BColors.HEADER}avg:{BColors.END_C} {avg_ping:05}ms, "
                      f"{BColors.HEADER}quality:{BColors.END_C} {signal_quality(avg_ping, prev_avg)}{BColors.END_C}",
                      end='', flush=True)
                ping_list = ping_list[-NO_OF_PINGS:]
                prev_avg = avg_ping
            else:
                progress_dots = (progress_dots + 1) % (max_dots + 1)
                progress_str = "x" * progress_dots
                print(f"\r{BColors.HEADER}current:{BColors.END_C} {int(last_ping):05}ms, "
                      f"{BColors.HEADER}progress:{BColors.END_C} {progress_str}", end='', flush=True)
        time.sleep(0.2)


if __name__ == '__main__':
    main()
