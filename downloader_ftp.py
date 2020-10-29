import ftplib
import os


basepath = 'routers/dlink'

url = 'ftp.dlink.eu'
ftp = ftplib.FTP(url)
ftp.login()

print('Logged into FTP server\n')

ftp.cwd('Products')

total_series = 0
total_devices = 0
for series, series_facts in ftp.mlsd(facts=['type']):
    if series_facts['type'] == 'dir' and series != 'Temp':
        total_series += 1
        print(f'Found series {series} (total = {total_series})')
        ftp.cwd(series)

        total_devices_series = 0
        for device, device_facts in ftp.mlsd(facts=['type']):
            if device_facts['type'] == 'dir' and device[0] != '@':
                total_devices += 1
                print(
                    f'Found device {device} (total = {total_devices}, in series = {total_devices_series})')
                ftp.cwd(device)
                for folder, folder_facts in ftp.mlsd(facts=['type']):
                    if folder_facts['type'] == 'dir' and folder == 'driver_software':
                        print(f'Found firmwares')
                        ftp.cwd(folder)

                        total_devices_series += 1

                        os.makedirs(f'{basepath}/{device}', exist_ok=True)
                        total_files = 0
                        for filename, file_facts in ftp.mlsd(facts=['type']):
                            if file_facts['type'] == 'file':
                                total_files += 1
                                filepath = f'{basepath}/{device}/{filename}'
                                if os.path.exists(filepath):
                                    print('File already present, skipping')
                                    continue

                                print(f'Downloading file {total_files}')
                                with open(filepath, 'wb') as file:
                                    ftp.retrbinary(
                                        f'RETR {filename}', file.write)
                        ftp.cwd('..')
                ftp.cwd('..')
        print(f'Done with series, found {total_devices_series} devices\n')
        ftp.cwd('..')

print(
    f'Downloaded a total of {total_series} series and {total_devices} devices')
