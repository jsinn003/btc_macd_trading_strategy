import numpy as np
import pandas as pd
import os
import requests
import zipfile
from datetime import datetime, timedelta


def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def append_to_csv(data, csv_file, write_header=False):
    data.to_csv(csv_file, mode='a', header=write_header, index=False)


def download_and_process_data(start_date, end_date, symbol='BTCUSDC', interval='1m'):
    output_csv = 'btc_usdc_data/full_btc_usdc_data.csv'
    headers = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
               'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore']
    append_to_csv(pd.DataFrame(columns=headers), output_csv, write_header=True)
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        # url = f'https://data.binance.vision/data/spot/daily/klines/{symbol}/{interval}/{symbol}-{interval}-{date_str}.zip'
        url = f'https://data.binance.vision/data/futures/um/daily/klines/{symbol}/{interval}/{symbol}-{interval}-{date_str}.zip'
        file_name = f'{date_str}.zip'
        file_path = os.path.join('btc_usdc_data', file_name)
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(file_path, 'wb') as file:
                file.write(response.content)
            unzip_file(file_path, 'btc_usdc_data')
            os.remove(file_path)
            unzipped_file_path = f'btc_usdc_data/{symbol}-{interval}-{date_str}.csv'
            daily_data = pd.read_csv(unzipped_file_path)
            append_to_csv(daily_data, output_csv, write_header=False)
            os.remove(unzipped_file_path)
            print(f'Processed data for {date_str}')
        except requests.RequestException as e:
            print(f'Error for {date_str}: {e}')
        current_date += timedelta(days=1)
    print("Data saved to full_btc_usdc_data.csv")


if not os.path.exists('btc_usdc_data'):
    os.makedirs('btc_usdc_data')

start_date = datetime(2024, 1, 4)
# end_date = datetime.now()
end_date = datetime(2025, 1, 4)
download_and_process_data(start_date, end_date)