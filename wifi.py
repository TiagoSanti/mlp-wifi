import pywifi
import pandas as pd
import os

def scan_wifi(df: pd.DataFrame) -> pd.DataFrame:
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    data = []

    iface.scan()
    results = iface.scan_results()

    scan_dict = {}
    for i in results:
        scan_dict[i.ssid] = i.signal

    print('Existing classes:')
    i = 0
    for y in df['class'].unique():
        print(f'{i}: {y}')
    target = input('Insert the class (number) or add new: ')
    if target.isdigit():
        target = df['class'].unique()[int(target)]
    else:
        print(f'Adding new class {target} to the list of classes')

    scan_dict['class'] = target

    data.append(scan_dict)

    return pd.DataFrame(data)

if __name__ == "__main__":
    input_file = input('Insert the input file:')
    if os.path.isfile(input_file):
        print(f'File {input_file} exists')
        df = pd.read_csv(input_file)
        print(df)
    else:
        print(f'File {input_file} does not exist')
        df = pd.DataFrame()

    print('\nStarting scan...')
    while True:
        scan = input('\nScan? (y/n): ')
        if scan == 'n':
            break
        else:
            df = df.append(scan_wifi(df))
    print(df)

    output_file = input('\nInsert the output file name:')
    df.reset_index(drop=True, inplace=True)
    df.to_csv(output_file, index=False)