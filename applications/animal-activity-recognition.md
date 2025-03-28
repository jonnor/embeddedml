
# Animal Activity Recognition

Wild animals, domestic animals and livestock.

## Datasets

- [Generic online animal activity recognition on collar tags](https://b2find.dkrz.de/dataset/542f06ce-46cd-582e-9561-da151e38e68b)
4 individual goats and 2 sheep that exercised 9 different activities.
Accelerometer, gyroscope, magnetometer, temperature, and pressure sensors.
1 day of data for each animal.
The sensor units were always placed around the neck of the animals and the orientation was not fixed (the collars were prone to rotation around the neck).
200Hz sample rate.
ProMove-mini tags from Inertia Technology.
- [Movement Sensor Dataset for Dog Behavior Classification](https://data.mendeley.com/datasets/vxhx934tbn/1).
Sensors placed on the collar and the harness of a dog.
Recorded while the dog is given tasks: galloping, lying on chest, sitting, sniffing, standing, trotting, and walking.
The movement sensors used are: ActiGraph GT9X Link, include 3D accelerometer and 3D gyroscope. 100 Hz sample rate.
45 middle to large sized dogs participated in the study.
Kaggle: [1](https://www.kaggle.com/datasets/benjamingray44/inertial-data-for-dog-behaviour-classification)
[2](https://www.kaggle.com/datasets/arashnic/animal-behavior-analysis).
- [Inertial sensor dataset for Dog Posture Recognition ](https://data.mendeley.com/datasets/mpph6bmn7g/1).
Inertial data collected from 42 healthy apprentice dogs.
Five postures (Standing, Sitting, Lying down, Walking, and Body shake) were annotated.
IMUs in three locations (back, neck, and chest) simultaneously.
Sensors ued ActiGraph GT9X Links, with three-axial accelerometer, gyroscope and magnetometer.
100Hz sampling rate.
- [Horsing Around -- A Dataset Comprising Horse Movement](https://data.4tu.nl/articles/dataset/Horsing_Around_--_A_Dataset_Comprising_Horse_Movement/12687551).
Movement data was collected at a riding stable over the course of 7 days.
The dataset comprises data from 18 individual horses with more than 1.2 million 2-second data samples, of which 93303 samples are labeled.
Data from 11 subjects was labeled but for 6 subjects the data was labeled more extensively for 6 activities.


## Works


- [Generic online animal activity recognition on collar tags](https://dl.acm.org/doi/10.1145/3123024.3124407).
Kamminga et al., 2021.
Selection of features.
Decision Tree did almost as well as Multi-layer Perceptron.
! did not test decision tree ensembles.
Focused on embedded device usecases. However only tested and reported resource usage on a desktop machine.

- [A novel biomechanical approach for animal behaviour recognition using accelerometers](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.13172).
Defines meaningful features by considering the orientation of collar-mounted sensor wrt animal movement.
Denotes directionsas: Surge, Heave and Sway.
Shows a case study of Kalahari Meerkats.
