import matplotlib.pyplot as plt
import csv
from csv import reader

import numpy as np


class Chart:
    string_labels = ["100", "200", "400", "800", "1600", "3200", "6400", "12800"]
    @staticmethod
    def disc_read_chart():
        data = np.genfromtxt("myResults/disc_read.csv", delimiter=",", names=["x", "y"])
        plt.plot(data["y"], data["x"], marker='s')
        plt.xlabel('liczba rekordow')
        plt.ylabel('ilość operacji')
        plt.title('operacje zapisu na dysku, a ilość rekordow')
        plt.xscale('log')
        plt.grid()
        plt.xticks(data["y"], Chart.string_labels)
        plt.show()

    @staticmethod
    def disc_sum_chart():
        data1 = np.genfromtxt("myResults/disc_sum.csv", delimiter=",", names=["x", "y"])
        data2 = np.genfromtxt("theoreticalResults/disc_sum_theory.csv", delimiter=",", names=["x", "y"])
        plt.plot(data1["y"], data1["x"], marker='s', label='suma operacji (symulacja)')
        plt.plot(data2["y"], data2["x"], marker='s', label='suma operacji (teoria)')
        plt.xlabel('liczba rekordow')
        plt.ylabel('ilość operacji')
        plt.title('operacje zapisu + odczytu na dysku, a ilość rekordow')
        plt.xscale('log')
        plt.legend()
        plt.grid()
        plt.xticks(data1["y"], Chart.string_labels)
        plt.show()

    @staticmethod
    def phase_chart():
        data1 = np.genfromtxt("myResults/phase.csv", delimiter=",", names=["x", "y"])
        data2 = np.genfromtxt("theoreticalResults/phase_theory.csv", delimiter=",", names=["x", "y"])
        plt.plot(data1["y"], data1["x"], marker='s', label='liczba faz (symulacja)')
        plt.plot(data2["y"], data2["x"], marker='s', label='liczba faz (teoria)')
        plt.xlabel('liczba rekordow')
        plt.ylabel('liczba faz')
        plt.title('liczba faz, a ilość rekordow')
        plt.xscale('log')
        plt.legend()
        plt.grid()
        plt.xticks(data1["y"], Chart.string_labels)
        plt.show()

    @staticmethod
    def write_disc_csv(row):
        f = open('myResults/disc_read.csv', 'a')
        writer = csv.writer(f)
        writer.writerow(row)
        f.close()

    @staticmethod
    def write_phase_csv(row):
        f = open('myResults/phase.csv', 'a')
        writer = csv.writer(f)
        writer.writerow(row)
        f.close()
