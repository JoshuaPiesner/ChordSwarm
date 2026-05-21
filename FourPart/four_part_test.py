import json
import matplotlib.pyplot as plt
from four_part_helper import *
import numpy as np
import random
import pandas as pd

# Default Chords: I IV V 1
C = np.matrix([
    [9,  2,  4,  9, 11,  4,  9,  9,  4,  9,  1,  2,  4,  4,  4,  6,  9,  2],
    [1,  6,  8,  1,  2,  8,  1,  1,  8,  1,  4,  6,  8,  8,  8,  9,  1,  6],
    [4,  9, 11,  4,  6, 11,  4,  4, 11,  4,  8,  9, 11, 11, 11,  1,  4,  9],
])

chord_sum_means = []
continu_sum_means = []
chord_strength_record = []
continu_strength_record = []

chord_strengths = np.linspace(3,5, 10)
continu_strengths = np.linspace(0.0175, 0.03, 10)

for chord_strength in chord_strengths:
  for continu_strength in continu_strengths:
    for __ in range(5):
      X = np.matrix([[random.randint(0,88) for j in range(C.shape[1])] for i in range(4)])
      chord_sums = []
      continu_sums = []
      for _ in range(3_000):
          X, chord_sum, continu_sum = update(X, C, chord_sim_strength=chord_strength, continu_strength=continu_strength)
          chord_sums.append(chord_sum)
          continu_sums.append(continu_sum)
          

      chord_sums = np.array(chord_sums)
      continu_sums = np.array(continu_sums)
      chord_sum_mean = chord_sums.mean()
      continu_sum_mean = continu_sums.mean()
      # plt.plot(chord_sums)
      # plt.plot(continu_sums)
      # plt.axhline(chord_sum_mean, label=f"ChordSumMean: {chord_sum_mean}")
      # plt.axhline(continu_sum_mean, label=f"ContinuSumMean: {continu_sum_mean}")
      # plt.legend()
      # plt.show()

      # colors = np.linspace(0, 1, len(chord_sums))  # Generate a color gradient
      # plt.scatter(chord_sums, continu_sums, c=colors, cmap='viridis', alpha=0.07, edgecolors='none')
      # colorbar = plt.colorbar(label='Index in Array')  # Add a colorbar to indicate the mapping
      # colorbar.solids.set_alpha(1)  # Set the opacity of the colorbar to 1
      # plt.show()

      chord_sum_means.append(chord_sum_mean)
      continu_sum_means.append(continu_sum_mean)
      chord_strength_record.append(chord_strength)
      continu_strength_record.append(continu_strength)
# Combine the data into a DataFrame
data = {
        "chord_sum_mean": chord_sum_means,
        "continu_sum_mean": continu_sum_means,
        "chord_strength": chord_strength_record,
        "continu_strength": continu_strength_record,
}

df = pd.DataFrame(data)
df.to_csv("/Users/joshuapiesner/Documents/VSCode/Quant/Music/four_part_test4.csv", )
