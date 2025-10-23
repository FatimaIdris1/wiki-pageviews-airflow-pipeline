import requests
import gzip
import urllib.request
from pathlib import Path


def download_pageviews(date_str, out_dir):
    year = date_str[:4]
    year_month = date_str[:4] + '-' + date_str[4:6]
    
    # Construct URL
    url = f'https://dumps.wikimedia.org/other/pageviews/{year}/{year_month}/pageviews-{date_str}.gz'
    out_file = Path(out_dir) / f'pageviews-{date_str}.txt'
    
    print(f"Downloading from: {url}")
    
    try:
        with urllib.request.urlopen(url) as response:
            with gzip.GzipFile(fileobj=response) as uncompressed:
                # Read and write in chunks to handle large files
                with open(out_file, 'wb') as f:
                    f.write(uncompressed.read())
        
        print(f"Downloaded to: {out_file}")
        return str(out_file)
        
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Execution
# download_pageviews('20251002-000000', out_dir='/home/fatima/airflow/Data')