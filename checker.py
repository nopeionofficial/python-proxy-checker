try:
    import os
    import sys
    import json
    import time
    import requests
    from concurrent.futures import ThreadPoolExecutor
    from colorama import init, Fore, Style
except ModuleNotFoundError:
    print('Error: missing dependencies. Run "install.bat".')
    sys.exit()

sys.stdout.write('\x1b]2;Proxy Checker | Starting\x07')
os.system('cls' if os.name == 'nt' else 'clear')
init()

with open('config.json') as f:
    config = json.load(f)

print(Fore.GREEN + r'''
____________ _______   ____   __  _____  _   _  _____ _____  _   __ ___________ 
| ___ \ ___ \  _  \ \ / /\ \ / / /  __ \| | | ||  ___/  __ \| | / /|  ___| ___ \
| |_/ / |_/ / | | |\ V /  \ V /  | /  \/| |_| || |__ | /  \/| |/ / | |__ | |_/ /
|  __/|    /| | | |/   \   \ /   | |    |  _  ||  __|| |    |    \ |  __||    / 
| |   | |\ \\ \_/ / /^\ \  | |   | \__/\| | | || |___| \__/\| |\  \| |___| |\ \ 
\_|   \_| \_|\___/\/   \/  \_/    \____/\_| |_/\____/ \____/\_| \_/\____/\_| \_|
''' + Style.RESET_ALL)
print(Fore.CYAN + f'''
Make sure you have a config.json file in the same directory as this script.
Check out the README.md for more information.

Using these settings from config.json:
    Threads: {config['thread']}
    Timeout: {config['timeout']}
    Max ms: {config['max_ms']}
    Import: {', '.join(config['import'])}
    Export: {config['export']}
    Host: {config['host']}

Starting proxy checker in 5 seconds.
''' + Style.RESET_ALL)
time.sleep(4)

proxies = []
for file_path in config['import']:
    try:
        with open(file_path) as f:
            proxies.extend(f.readlines())
    except FileNotFoundError:
        print(Fore.RED + f'Error: file "{file_path}" not found.' + Style.RESET_ALL)
proxies_length = len(proxies)

if proxies_length == 0:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.RED + 'Error: no proxies found.' + Style.RESET_ALL)
    sys.exit()

print(Fore.CYAN + f'Checking {proxies_length} proxies...' + Style.RESET_ALL)
time.sleep(1)
sys.stdout.write('\x1b]2;Proxy Checker | Checking\x07')

checked = 0
def check(proxy):
    global checked
    try:
        proxies = {'https': f'http://{proxy}', 'http': f'http://{proxy}'} # HTTP proxy
        response = requests.get('https://ipinfo.io/json', proxies=proxies, timeout=config['timeout'])

        if response.status_code == 200 and response.json()['ip'] == proxy.split(':')[0]:
            start_time = time.perf_counter()
            response = requests.get(config['host'], proxies=proxies, timeout=config['timeout'])
            end_time = time.perf_counter()
            elapsed_time_ms = round((end_time - start_time) * 1000)
            if response.status_code == 200:
                if elapsed_time_ms < config['max_ms']:
                    print(Fore.GREEN + f'{proxy} | {elapsed_time_ms}ms' + Style.RESET_ALL)
                    with open(config['export'], '+a') as export:
                        export.write(f'{proxy}\n')
                else:
                    print(Fore.YELLOW + f'{proxy} | {elapsed_time_ms}ms' + Style.RESET_ALL)
            else:
                print(Fore.RED + f'{proxy} | {response.status_code}' + Style.RESET_ALL)
        else:
            print(Fore.RED + f'{proxy} | Invalid response' + Style.RESET_ALL)
    except:
        print(Fore.RED + f'{proxy} | Exception occurred' + Style.RESET_ALL)
        raise
    finally:
        checked += 1
        sys.stdout.write(f"\x1b]2;Checking proxies ({checked}/{proxies_length})\x07")
        if checked == proxies_length:
            print(Fore.GREEN + f'Finished checking {proxies_length} proxies.' + Style.RESET_ALL)
            sys.stdout.write('\x1b]2;Proxy Checker | Finished\x07')
            time.sleep(3)
            sys.exit()

with ThreadPoolExecutor(max_workers=config['thread']) as executor:
    for proxy in proxies:
        executor.submit(check, proxy.replace('\n', ''))
    executor.shutdown(wait=True)