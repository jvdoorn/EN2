from math import atan, pi, sqrt

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import stats
import numpy as np


def atan_error(width, error_width, height, error_height):
    a = sqrt((error_width / width) ** 2 + 4 * (error_height / height) ** 2) * ((2 * height) / width)
    return a / (1 + a ** 2)


average_angle_list = []
average_angle_error_list = []

for object_name in ["circle", "oval", "square"]:
    data = pd.read_csv("data/{0}.csv".format(object_name))
    data.set_index(keys=['width'], drop=False, inplace=True)
    widths = data['width'].unique().tolist()

    average_width_list = []
    average_width_error_list = []
    average_height_list = []
    average_height_error_list = []

    angle_list = []
    angle_error_list = []

    eccentricity_list = []
    eccentricity_error_list = []

    for i in widths:
        series = data.loc[data.width == i]

        average_width = i
        average_width_error = series['error_width'].mean()

        average_height = series['height'].mean()
        average_height_error = series['error_height'].mean()

        average_width_list.append(average_width)
        average_width_error_list.append(average_width_error)

        average_height_list.append(average_height)
        average_height_error_list.append(average_height_error)

        angle = atan((2 * average_height) / average_width) * (180 / pi)
        angle_error = atan_error(average_width, average_width_error, average_height, average_height_error) * (180 / pi)

        angle_list.append(angle)
        angle_error_list.append(angle_error)


        if 'eccentricity' in series.columns:
            eccentricity_list.append(series['eccentricity'].mean())
            eccentricity_error_list.append(series['error_eccentricity'].mean())

    average_angle_list.append(np.average(angle_list))
    average_angle_error_list.append(np.average(angle_error_list))

    slope, intercept, r_value, p_value, std_err = stats.linregress(average_width_list, angle_list)
    print(object_name)
    print(np.average(angle_list))
    print(slope)
    print(std_err)

    plt.clf()
    plt.errorbar(x=average_width_list, y=average_height_list, xerr=average_width_error_list,
                 yerr=average_height_error_list, fmt="o")
    plt.xlabel("Width of the {0} (cm)".format(object_name))
    plt.ylabel("Height of the pile (cm)")
    plt.savefig("results/{0}-wh.png".format(object_name))

    plt.clf()
    plt.errorbar(x=average_width_list, y=angle_list, xerr=average_width_error_list, yerr=angle_error_list, fmt="o")
    plt.ylim(15, 60)
    plt.xlabel("Width of the {0} (cm)".format(object_name))
    plt.ylabel("Angle of repose (\xb0)")
    plt.savefig("results/{0}-angle.png".format(object_name))

    if len(eccentricity_list) > 0:
        plt.clf()
        plt.errorbar(x=eccentricity_list, y=angle_list, xerr=eccentricity_error_list, yerr=angle_error_list, fmt="o")
        plt.ylim(15, 60)
        plt.xlabel("Eccentricity")
        plt.ylabel("Angle of repose (\xb0)")
        plt.savefig("results/{0}-angle-ecc.png".format(object_name))

        slope, intercept, r_value, p_value, std_err = stats.linregress(eccentricity_list, angle_list)
        print(slope)
        print(std_err)

print("Average angle of measurements: {0}".format(np.average(average_angle_list)))
print("Average angle error of measurements: {0}".format(np.average(average_angle_error_list)))
