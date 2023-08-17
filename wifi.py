import pywifi
import pandas as pd
import os
import time

def manual_scan(df: pd.DataFrame) -> pd.DataFrame:
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    data = []

    iface.scan()
    results = iface.scan_results()

    scan_dict = {}
    for i in results:
        scan_dict[i.ssid] = i.signal

    try:
        print('Existing classes:')
        i = 0
        for y in df['class'].unique():
            print(f'{i}: {y}')
            i += 1
        target = input('Insert the class (number) or add new: ')
        if target.isdigit():
            target = df['class'].unique()[int(target)]
        else:
            print(f'Adding new class {target} to the list of classes')
    except KeyError:
        print('No classes found, adding new class')
        target = input('Insert the class: ')
    
    scan_dict['class'] = target

    data.append(scan_dict)

    return pd.DataFrame(data)

def automatic_scan(df: pd.DataFrame, interval: int = 1) -> pd.DataFrame:
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    data = []

    target = input('Insert the class: ')

    try:
        while True:
            print('Scanning...', end=' ')
            iface.scan()
            results = iface.scan_results()
            print(f'Found {len(results)} networks')

            scan_dict = {}
            for i in results:
                scan_dict[i.ssid] = i.signal

            scan_dict['class'] = target

            data.append(scan_dict)
            
            print(f'Sleeping for {interval} seconds...\n')
            time.sleep(interval)

    except KeyboardInterrupt:
        print('Scan interrupted')
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    input_file = input('Insert the input file: ')
    input_file = f'data/{input_file}'
    if os.path.isfile(input_file):
        print(f'File {input_file} exists')
        df = pd.read_csv(input_file)
    else:
        print(f'File {input_file} does not exist')
        df = pd.DataFrame()

    scan_type = input('\nManual scan or automatic scan? (m/a): ')
    interval = int(input('Insert the interval between scans (in seconds): '))
    print('\nStarting scan...')
    if scan_type == 'm':
        while True:
            scan = input('\nScan? (y/n): ')
            if scan == 'n':
                break
            else:
                df = df.append(manual_scan(df))
    elif scan_type == 'a':
        df = df.append(automatic_scan(df, interval))

    output_file = input('\nInsert the output file name: ')
    df.fillna(-100, inplace=True)
    df.to_csv(f'data/{output_file}', index=False)