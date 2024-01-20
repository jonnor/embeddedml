
"""
Data loading tools for the PAMAP2 Physical Activity Monitoring dataset
https://archive.ics.uci.edu/dataset/231/pamap2+physical+activity+monitoring
"""

import os

import pandas

def assert_data_correct(data):

    assert len(data) == 2872533, len(data)
    assert len(data.columns) == (3*13)+2, len(data.columns)

    assert data.index.names == ['subject', 'time']
    assert data.dtypes['activity'] == 'category'

    subjects = data.index.levels[0]
    n_subjects = subjects.nunique()
    assert n_subjects == 9, (n_subjects, list(subjects.unique()))

    
def load_data(path) -> pandas.DataFrame:
    """
    Load all data in the dataset

    NOTE: Takes some tens of seconds
    """

    # Prepare metadata
    a = load_activities().items()
    a = sorted(a, key=lambda kv: kv[0])
    activity_categories = list(map(lambda kv: kv[1], a))

    columns = load_column_names()

    # Load the data
    def load_one(path):      
        df = pandas.read_table(path, header=None, sep='\s+', names=columns)
        df['subject'] = os.path.splitext(os.path.basename(path))[0]

        # drop invalid columns
        invalid_columns = [ c for c in df.columns if '_invalid_' in c ]
        df = df.drop(columns=invalid_columns)

        return df

    data_dir = os.path.join(path, 'Protocol')
    assert os.path.exists(data_dir), data_dir

    dfs = [ load_one(os.path.join(data_dir, name)) for name in os.listdir(data_dir) ]
    data = pandas.concat(dfs)

    # Use proper types
    data['time'] = pandas.to_timedelta(data.time, unit='s')
    data['subject'] = data.subject.astype('category')
    data['activity'] = pandas.Categorical(data.activity, categories=activity_categories)

    # Set a reasonable index
    data = data.set_index(['subject', 'time'])

    # Sanity checks
    assert_data_correct(data)

    return data

def load_column_names() -> list[str]:

    base_columns = [
        'time',
        'activity',
        'heartrate',
    ]

    # XXX: we are assuming the order is actually XYZ
    imu_columns = [
        'temperature',

        'acceleration_16g_x',
        'acceleration_16g_y',
        'acceleration_16g_z',

        'acceleration_6g_x',
        'acceleration_6g_y',
        'acceleration_6g_z',

        'gyro_x',
        'gyro_y',
        'gyro_z',

        'magnetometer_x',
        'magnetometer_y',
        'magnetometer_z',
        # there are present but invalid (according to dataset description)
        'invalid_orientation_1',
        'invalid_orientation_2',
        'invalid_orientation_3',
        'invalid_orientation_4',
    ]
    assert len(imu_columns) == 17, len(imu_columns)

    columns = base_columns
    for position in ['hand', 'chest', 'ankle']:
        imu_columns = [ f'{position}_{c}' for c in imu_columns ]
        columns += imu_columns

    assert len(columns) == 54, (len(columns), columns)
    return columns


def load_activities() -> dict[int, str]:
    map = {}
    map[0] = 'transient'
    map[1] = 'lying'
    map[2] = 'sitting'
    map[3] = 'standing'
    map[4] = 'walking'
    map[5] = 'running'
    map[6] = 'cycling'
    map[7] = 'Nordic_walking'
    map[8] = 'UNUSED1'
    map[9] = 'watching_TV'
    map[10] = 'computer_work'
    map[11] = 'car driving'
    map[12] = 'ascending_stairs'
    map[13] = 'descending_stairs'
    map[14] = 'UNUSED2'
    map[15] = 'UNUSED3'
    map[16] = 'vacuum_cleaning'
    map[17] = 'ironing'
    map[18] = 'folding_laundry'
    map[19] = 'house_cleaning'
    map[20] = 'playing_soccer'
    map[21] = 'UNUSED4'
    map[22] = 'UNUSED5'
    map[23] = 'UNUSED6'
    map[24] = 'rope_jumping'

    return map


def main():

    dataset_path = '/data/emlearn/PAMAP2_Dataset/'
    packed_path = 'pamap2.parquet'

    #data = load_data(dataset_path)
    #data.to_parquet(packed_path)

    loaded = pandas.read_parquet(packed_path)
    assert_data_correct(loaded)
    



if __name__ == '__main__':
    main()
