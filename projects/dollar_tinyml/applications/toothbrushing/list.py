
import subprocess
import os
import json

import plotly.express
import pandas

from har_data2labelstudio import load_har_record

def parse_har_record_filename(f):

    tok = f.replace('.npy', '').split('_')
    datestr, label = tok

    s = pandas.Series({
        'time': pandas.Timestamp(datestr),
        'label': label,
    })
    return s

def video_file_duration(path):

    assert os.path.exists(path), path
    probe = ffprobe(path)
    assert probe.return_code == 0, probe.stderr
    data = json.loads(probe.json)
    # streams = ["streams"]
    # ffmpeg.probe(path)
    #print(streams)
    #for s in streams:
    #    #print(s)
    #    for k, v in s.items():
    #        print(k, v)
    duration = float(data['format']['duration'])
    return duration    

def parse_video_filename(path):
    # Expects filename on form VID_20241231_155240
    basename = os.path.basename(path)
    filename, ext = os.path.splitext(basename)

    tok = filename.split('_')
    vid, date, time = tok

    dt = pandas.to_datetime(filename, format='VID_%Y%m%d_%H%M%S')
    #dt = pandas.to_datetime(date, format='%Y%m%d')
    #print(filename)
    return dt


def read_directory(path):
    names = os.listdir(path)
    paths = [ os.path.join(path, f) for f in names ]
    df = pandas.DataFrame({
        'path': paths,
    })
    return df

from pathlib import Path
from typing import NamedTuple


class FFProbeResult(NamedTuple):
    return_code: int
    json: str
    error: str


def ffprobe(file_path) -> FFProbeResult:
    command_array = ["ffprobe",
                     "-v", "quiet",
                     "-print_format", "json",
                     "-show_format",
                     "-show_streams",
                     file_path]
    result = subprocess.run(command_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return FFProbeResult(return_code=result.returncode,
                         json=result.stdout,
                         error=result.stderr)

# NOTE: exiftool -json PATH also has good info

#def 

def main():


    d = 'data/jonnor-brushing-1/har_record/'
     
    ff = load_har_record(d).reset_index()
    stats = ff.filename.apply(parse_har_record_filename).add_prefix('file_')
    stats= pandas.merge(ff, stats, right_index=True, left_index=True)
    stats['coarse_time'] = stats['file_time'].dt.floor('1min')

    print(stats)

    # XXX: start/stop spans would be clearer
    data_counts = stats.groupby(['coarse_time', 'file_label']).count().reset_index().rename(columns=dict(file_time='files'))
    print(data_counts)



    v = '/home/jon/Downloads/toothbrush-jonnor1/edited'
    videos = read_directory(v)
    print(videos)
    videos['duration'] = videos['path'].apply(video_file_duration)
    videos['file_time'] = videos['path'].apply(parse_video_filename)
    videos['end'] = videos.file_time + pandas.to_timedelta(videos.duration, unit='s')

    print(videos)

    fig = plotly.express.bar(data_counts, x="coarse_time", y="files", color='file_label')
    for path, start, end in zip(videos.path, videos.file_time, videos['end']):
        fig.add_vrect(x0=start, x1=end, line_width=0, fillcolor="red", opacity=0.2,
            label=dict(
                text=os.path.basename(path),
                textposition="start",
                font=dict(size=10, color="black"),
                yanchor="top",
            ),
        )
    fig.show()


main()


