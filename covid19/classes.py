import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import logging


logging.basicConfig(level=logging.INFO)


class Graph:

    def __init__(self, *args):
        if len(args) == 1:
            if args[0] == "no_display":
                self.display = False
                self.country = "US"
            else:
                self.display = True
                self.country = args[0]
        else:
            self.display = True
            self.country = "US"
        self.d = DFWrapper(self.country)
        self._data = self.d.data
        self.fc = forecaster(self._data)
        self._x, self._y = self.fc.run_forecast(10)
        self._plot(forecast=False)

    def _plot(self, forecast=True):

        plt.style.use('dark_background')
        fig, ax = plt.subplots(2, 1, sharex=True)
        
        ax2 = ax[0].twinx()

        ax[0].stackplot(range(self._data['Dates'].shape[0]),
                        self._data["Daily Confirmed"],
                        labels=["Daily Cases - " + str(self._data["Daily Confirmed"].values[-1])],
                        colors=["y"],
                        zorder=100,
                        alpha=1)

        d_idxs, d_strings = self._create_ticks()
        
        ax[0].grid(zorder=-1, alpha=0.2)
        ax[0].set_title("Daily")
        
        ax2.stackplot(range(self._data['Dates'].shape[0]),
                      self._data["Daily Deaths"],
                      labels=["Daily Deaths - " + str(self._data["Daily Deaths"].values[-1])],
                      colors=["r"],
                      zorder=100,
                      alpha=0.5)
        ax2.xaxis.label.set_color("red")
        ax2.tick_params(axis="y", colors="red")
                      
        ax[0].xaxis.label.set_color("yellow")
        ax[0].tick_params(axis="y", colors="yellow")
        
        handles0, labels0 = ax[0].get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        
        ax[0].legend((handles0[0], handles2[0]), (labels0[0], labels2[0]), loc="upper left")
        
        ax[1].set_xticks(d_idxs)
        ax[1].set_xticklabels(d_strings, rotation=45)
        ax[1].stackplot(range(self._data['Dates'].shape[0]),
                        self._data["Confirmed"],
                        labels=["Cases - " + str(self._data["Confirmed"].values[-1])],
                        colors=["y"],
                        zorder=5.5,
                        alpha=1)
                        
        ax[1].grid(zorder=-1, alpha=0.2)
        ax[1].set_title("Cumulative")
                      
        ax[1].xaxis.label.set_color("yellow")
        ax[1].tick_params(axis="y", colors="yellow")
        
        ax3 = ax[1].twinx()
                        
        ax3.stackplot(range(self._data['Dates'].shape[0]),
                        self._data["Deaths"],
                        labels=["Deaths - " + str(self._data["Deaths"].values[-1])],
                        colors=["r"],
                        zorder=-1,
                        alpha=0.4)
        ax3.xaxis.label.set_color("red")
        ax3.tick_params(axis="y", colors="red")
        
        handles1, labels1 = ax[1].get_legend_handles_labels()
        handles3, labels3 = ax3.get_legend_handles_labels()
        ax[1].legend((handles1[0], handles3[0]), (labels1[0], labels3[0]), loc="upper left")

        fig.suptitle("COVID-19: " + self.country, fontsize=16)

        if self.display:
            plt.show()
        else:
            plt.savefig("../figs/{0}.png".format(self.country))

    def _create_ticks(self):

        # date_idxs = [0]
        # date_strings = [self._data["Dates"].values[0][:5]]
        date_idxs = []
        date_strings = []

        for idx, date in enumerate(self._data["Dates"].values):
            if (date.split("-")[1] == "01"):
                date_idxs.append(idx)
                date_strings.append(date[:5])

        if self._data["Dates"].values[-1].split("-")[1] != "01":
            if int(self._data["Dates"].values[-1].split("-")[1]) > 5:
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
                    self.trash = US_df

                confirmed = US_df["Confirmed"].sum()
                deaths = US_df["Deaths"].sum()
                confirm_list.append(confirmed)
                death_list.append(deaths)

        daily_confirm = [confirm_list[ii] - confirm_list[ii-1] for ii in range(1, len(confirm_list))]
        daily_confirm.insert(0, 0)
        daily_death = [death_list[ii] - death_list[ii-1] for ii in range(1, len(death_list))]
        daily_death.insert(0, 0)



        self.data = pd.DataFrame({"Dates": fnames,
                                  "Confirmed": confirm_list,
                                  "Deaths": death_list,
                                  "Daily Confirmed": daily_confirm,
                                  "Daily Deaths": daily_death})

