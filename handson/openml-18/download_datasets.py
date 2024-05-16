
import os

import openml
import pandas
import openml.datasets


def download_openml_cc18(out_dir):
    """
    Download datasets that are part of the OpenML CC18 benchmark collection

    NOTE: datasets with missing values are ignored. Around 8 out of 72.

    Takes around 400 MB on disk in total.
    """

    # FIXME: create directories as needed
    tasks_path = os.path.join(out_dir, 'tasks.csv')

    if os.path.exists(tasks_path):
        tasks = pandas.read_csv(tasks_path)

    else:
        # Get list of datasets/tasks
        suite = openml.study.get_suite(99)
        assert suite.name.startswith('OpenML-CC18')
        tasks = openml.tasks.list_tasks(output_format="dataframe")    
        tasks = tasks.query("tid in @suite.tasks")

        # Remove tasks/datasets with missing values
        tasks_missing_values = tasks['NumberOfInstancesWithMissingValues'] > 0
        print('Dropping tasks with missing values')
        print(tasks[tasks_missing_values])
        tasks = tasks[~tasks_missing_values]

        tasks.to_csv(tasks_path)

    for dataset_id in tasks['did']:

        # This is done based on the dataset ID.
        dataset = openml.datasets.get_dataset(dataset_id,
            download_data=False,
            download_qualities=False,
            download_features_meta_data=False,
        )

        print(dataset.description[:100])

        target = dataset.default_target_attribute
        X, y, categorical_indicator, attribute_names = dataset.get_data(target=target)

        data = X.copy()
        data['__target'] = y

        data.to_parquet(os.path.join(out_dir, 'datasets', f'{dataset_id}.parquet'))


if __name__ == '__main__':
    download_openml_cc18('data')
