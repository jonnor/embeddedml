
"""
Generic utilities for dataset manipulation
"""

import os.path
import time

import structlog
import requests
import pandas
import joblib
import subprocess

log = structlog.get_logger()

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def ensure_dir_for_file(path):
    directory = os.path.dirname(path)
    if directory:
        ensure_dir(directory)

def download_file(uri, path, headers = {}):
    """
    Download a single HTTP(s) URL to specified @path
    """

    r = requests.get(uri, stream=True, headers=headers)
    if r.status_code != 200:
        raise ValueError(f'Status {r.status_code} for GET {uri}')

    with open(path, 'wb') as f:
        for chunk in r:
            f.write(chunk)

def download_convert_audio(uri, path, sr=16000, ffmpeg_bin='ffmpeg', bitrate=192e3):

    args = [
        ffmpeg_bin,
        '-y', # allow overwrite
        '-i', uri,
        '-f', 'ogg',
        '-ac', '0', # mono
        '-ab', str(bitrate),
        '-ar', str(sr),
        '-vn', # no video?
        '-ss', '00:00:00',
        '-t', '00:30:00',
        path,
    ]
    cmd = ' '.join(args)

    log.info('download-convert-audio-start', command=repr(cmd))    

    subprocess.check_output(cmd, shell=True)


def download_files(files : pandas.DataFrame,
        n_jobs=10,
        verbose=1,
        exists='skip',
        errors='log') -> pandas.DataFrame:

    """
    Download many files in parallell. Over HTTP(s)
    
    Must have columns .url for the inputs, and .path for the outputs

    Captures statistics about the download size/time et.c. and returns it.
    """

    def fetch(url, out):
        duration = 0.0
        download = True
        file_size = None
        start_time = None

        # TODO: move the filtering of existing files out to a pre-step
        if os.path.exists(out) and exists == 'skip':
            file_size = os.path.getsize(out)
            if file_size == 0:
                os.unlink(out)
            else:
                download = False
        if os.path.exists(out) and exists == 'error':
            raise ValueError(f'File "{out}" already exists')

        basedir = os.path.dirname(out)
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        error = None
        if download:
            start_time = time.time()

            try:
                download_convert_audio(url, out)
            except (requests.exceptions.ConnectionError, ValueError, subprocess.CalledProcessError) as e:
                error = e
                if errors == 'log':
                    log.error('download-files-fetch-failed',
                            url=url,
                            out=out,
                            error=str(e),
                    )
                else:
                    raise e
            else:
                file_size = os.path.getsize(out)
            finally:
                end_time = time.time()
                duration = end_time - start_time

        metrics = {
            'download_time': duration,
            'download_size': file_size,
            'download_start': pandas.to_datetime(start_time),
            'error': str(error),
        }

        if verbose >= 2:
            log.debug('download-fetch', url=url, path=out, **metrics)


        return metrics

    jobs = [ joblib.delayed(fetch)(r.url, r.path) for _, r in files.iterrows() ]
    out = joblib.Parallel(n_jobs=n_jobs, verbose=verbose)(jobs)
    df = pandas.DataFrame.from_records(out)

    return df
