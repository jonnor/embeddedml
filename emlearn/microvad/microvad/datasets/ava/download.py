
"""
Downloading tools for AVA Speech, a part of the AVA Spoken Activity Datasets

Official dataset website: https://research.google.com/ava/

Dataset description paper: https://arxiv.org/abs/1808.00606
"""

import os.path

import pandas
import numpy

from ..utils import download_files, ensure_dir

ava_speech_file_prefix = 'https://s3.amazonaws.com/ava-dataset/trainval' # [file_name]


def load_annotations_file(labels_dir=None,
        labels_filename='ava_speech_labels_v1.csv'):

    here = os.path.dirname(__file__)
    if labels_dir is None:
        labels_dir = here

    column_names = [
        'clip',
        'start',
        'end',
        'label',
    ]
    path = os.path.join(labels_dir, labels_filename)

    df = pandas.read_csv(path, names=column_names)
    df = df.set_index('clip')

    return df

def load_files(files_dir=None, files_filename='ava_speech_file_names_v1.txt'):
    
    here = os.path.dirname(__file__)
    if files_dir is None:
        files_dir = here

    path = os.path.join(files_dir, files_filename)
    df = pandas.read_csv(path, names=['file'])

    def clip_id_from_filename(filename):
        clip = os.path.splitext(filename)[0]
        return clip

    df['clip'] = df['file'].apply(clip_id_from_filename)
    df = df.set_index('clip')

    return df

def load_annotations():
    """

    """

    annotations = load_annotations_file()
    files = load_files()
    annotations['file'] = files['file']

    return annotations


def file_download_url(filename):
    out = f'{ava_speech_file_prefix}/{filename}'
    return out

def make_downloads(annotations, out_dir):

    filenames = annotations['file']

    df = pandas.DataFrame({
        'url': [ file_download_url(f) for f in filenames ],
        'path': [ os.path.join(out_dir, f) for f in filenames ],
    }, index=annotations.index)
    df = df.drop_duplicates()

    return df


def main():

    out_dir = 'data/ava/'
    ensure_dir(out_dir)
    
    annotations = load_annotations()
    print(annotations)

    downloads = make_downloads(annotations, out_dir=out_dir)

    stats = download_files(downloads, verbose=3)
    print(stats)

if __name__ == '__main__':
    main()
