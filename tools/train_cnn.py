"""
Created by: Tapan Sharma
Date: 04/08/20
"""

import json

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from predictCO2.models.deep_learning_model import DeepLearningModel
from predictCO2.models.tune_cnn2 import CNN2
from predictCO2.preprocessing import utils
from predictCO2.preprocessing.generate_data import CountryPolicyCarbonData, PolicyCategory
from sklearn.model_selection import TimeSeriesSplit

matplotlib.use('Qt5Agg')

with open('cfg/cnn_config.json') as f:
    training_config = json.load(f)

countries = training_config['countries']
# train_features = pd.DataFrame()
# train_labels = pd.DataFrame()
# test_features = pd.DataFrame()
# test_labels = pd.DataFrame()
norm_data = training_config['training']['normalize']

# Collect data
# for country in countries:
#     countryPolicyCarbonData = CountryPolicyCarbonData('training_data.yaml', country, include_flags=False,
#                                                       policy_category=PolicyCategory.SOCIAL_INDICATORS,
#                                                       normalize=norm_data)
#     train_x, train_y, test_x, test_y = countryPolicyCarbonData.split_train_test(fill_nan=False)
#     train_features = train_features.append(train_x)
#     test_features = test_features.append(test_x)
#     train_labels = train_labels.append(train_y)
#     test_labels = test_labels.append(test_y)

# train_features.to_pickle('dataset/train/train_features')
# train_labels.to_pickle('dataset/train/train_labels')
# test_features.to_pickle('dataset/train/test_features')
# test_labels.to_pickle('dataset/train/test_labels')

train_features = pd.read_pickle('dataset/train/train_features')
train_labels = pd.read_pickle('dataset/train/train_labels')
test_features = pd.read_pickle('dataset/train/test_features')
test_labels = pd.read_pickle('dataset/train/test_labels')

train_features, train_labels = utils.generate_time_series_df(train_features, train_labels,
                                                             training_config['time_steps'])
test_features, test_labels = utils.generate_time_series_df(test_features, test_labels, training_config['time_steps'])
print(train_features.shape)
print(train_labels.shape)
print(test_features.shape)
print(test_labels.shape)

# Train model with 5 fold cross validation
tss = TimeSeriesSplit()
_, n_features = train_features.shape
# cnns = CNN2(training_config, num_features=n_features, num_outputs=1)
# tuner = cnns.tuning(method="hyperband")
# X, Y = utils.data_sequence_generator(train_features, train_labels, training_config['time_steps'])
# X_val, Y_val = utils.data_sequence_generator(test_features, test_labels, training_config['time_steps'])
# tuner.search(X, Y, epochs=100, validation_data=(X_val, Y_val))
# tuner.results_summary()
cnn = DeepLearningModel(training_config, num_features=n_features, num_outputs=1)
cnn.plot_and_save_model("content/model_arch/CNN_TAPAN.png")
print(cnn.model.summary())
losses = []
val_losses = []
start = time.time()
for train_idx, test_idx in tss.split(train_features):
    X, X_val = train_features.iloc[train_idx], train_features.iloc[test_idx]
    Y, Y_val = train_labels.iloc[train_idx], train_labels.iloc[test_idx]
    features, labels = utils.data_sequence_generator(X, Y, training_config['time_steps'])
    val_f, val_l = utils.data_sequence_generator(X_val, Y_val, training_config['time_steps'])
    h = cnn.train_with_validation_provided(features, labels, val_f, val_l)
    losses.append(h.history['loss'])
    val_losses.append(h.history['val_loss'])
end = time.time()
print("TRAINING TIME: {}".format(end - start))

# # Plot training loss
loss_arr = np.zeros((100, 1))
for loss_per_fold in losses:
    for j, loss in enumerate(loss_per_fold):
        loss_arr[j] = loss_arr[j] + loss
loss_arr = loss_arr / 5
val_loss_arr = np.zeros((50, 1))
for loss_per_fold in val_losses:
    for j, loss in enumerate(loss_per_fold):
        val_loss_arr[j] = val_loss_arr[j] + loss
loss_arr = loss_arr / 5
fig1, ax1 = plt.subplots()
ax1.plot(range(len(loss_arr)), loss_arr, label='Training Loss')
# ax1.plot(range(0, len(loss_arr), 2), val_loss_arr, '-.', label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(loc='upper right')
plt.title('Loss')
plt.show()

# # # Prediction
test_start = time.time()
test_f, test_l = utils.data_sequence_generator(test_features, test_labels, training_config['time_steps'])
model_eval = cnn.model.evaluate(test_f, test_l)
test_end = time.time()
print("TESTING TIME: {}".format(test_end - test_start))
y = cnn.model.predict(test_f)
print("FORMAT: {}".format(type(y)))
print("{}: {}".format(test_l, y))
print("\n\nTesting Loss: {}\nTesting Accuracy: {}".format(model_eval[0], model_eval[1]))
cnn.save("CNN_TAPAN")
