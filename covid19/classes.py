import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


class Graph:

    def __init__(self, *args):
        if len(args) == 1:
            self.country = args[0]
        else:
            self.country = "US"
        self.d = DFWrapper(self.country)
        self._data = self.d.data
        self.fc = forecaster(self._data)
        self._x, self._y = self.fc.run_forecast(10)
        self._plot(forecast=False)

    def _plot(self, forecast=True):

        plt.style.use('dark_background')
        fig, ax = plt.subplots(2, 1, sharex=True)
        ax[0].stackplot(range(self._data['Dates'].shape[0]),
                        self._data["Deaths"],
                        self._data["Confirmed"],
                        labels=["Deaths - " + str(self._data["Deaths"].values[-1]),
                                "Confirmed - " + str(self._data["Confirmed"].values[-1])],
                        colors=["r", "y"],
                        zorder=100,
                        alpha=1)
        if forecast:
            ax[0].plot(self._x, self._y)
        ax[0].legend(loc="upper left")
        ax[0].grid(zorder=-1, alpha=0.2)
        ax[0].set_title("Linear")

        ax[1].stackplot(range(self._data['Dates'].shape[0]),
                        self._data["Deaths"],
                        self._data["Confirmed"],
                        colors=["r", "y"],
                        zorder=100,
                        alpha=1)

        d_idxs, d_strings = self._create_ticks()

        ax[1].set_xticks(d_idxs)
        ax[1].set_xticklabels(d_strings, rotation=45)
        ax[1].grid(zorder=-1, alpha=0.2)
        ax[1].set_yscale("log")
        ax[1].set_title("Logarithmic")

        fig.suptitle("COVID-19: " + self.country, fontsize=16)

        plt.show()

    def _create_ticks(self):

        # date_idxs = [0]
        # date_strings = [self._data["Dates"].values[0][:5]]
        date_idxs = []
        date_strings = []

        for idx, date in enumerate(self._data["Dates"].values):
            if (date.split("-")[1] == "01"):
                date_idxs.append(idx)
                date_strings.append(date[:5])
            else:
                date_idxs.append(idx)
                date_strings.append("")

        if self._data["Dates"].values[-1].split("-")[1] != "01":
            date_idxs.append(self._data["Dates"].values.shape[0]-1)
            date_strings.append(self._data["Dates"].values[-1][:5])
        return date_idxs, date_strings


class forecaster:

    def __init__(self, _df):
        self.df = _df
        self.overshoot = 2
        self.forecast = None

    def run_forecast(self, _degree):
        self.degree = _degree
        self.poly_out = np.polyfit(np.arange(self.df.shape[0]),
                                   self.df["Confirmed"].values,
                                   deg=self.degree)
        self.poly_obj = np.poly1d(self.poly_out)
        self.x = np.arange(self.df.shape[0]*self.overshoot)
        self.y = self.poly_obj(self.x)
        return self.x, self.y


class DFWrapper:

    def __init__(self, country):
        self.path = "../../COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/"
        self._country = country
        self._scrape()
        self.data = None
        self._scrape()

    def _scrape(self):
        fnames = []
        confirm_list = []
        death_list = []
        for f in os.listdir(self.path):
            if f.endswith(".csv"):
                fnames.append(f.split(".")[0])
                raw_df = pd.read_csv(self.path + f)
                try:
                    US_df = raw_df.loc[raw_df['Country/Region'] == self._country]
                except KeyError:
                    US_df = raw_df.loc[raw_df['Country_Region'] == self._country]

                confirmed = US_df["Confirmed"].sum()
                deaths = US_df["Deaths"].sum()
                confirm_list.append(confirmed)
                death_list.append(deaths)

        self.data = pd.DataFrame({"Dates": fnames,
                                  "Confirmed": confirm_list,
                                  "Deaths": death_list})

