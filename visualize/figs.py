import matplotlib.pyplot as plt
import numpy as np
from typing import List
from matplotlib.pyplot import Figure, Axes
from pandas import DataFrame

plt.style.use("ggplot")

def base_fig(f):
    fig, ax = plt.subplots(1, 1)
    def generate_fig(data, lines):
        ax.clear()
        f(data, lines, ax)
        return fig
    return generate_fig

@base_fig
def hour_consumption(
        data: DataFrame,
        lines: List[str],
        ax: Axes
        ) -> Figure:
    colors = {
            "std": "#83A59755",
            "mean": "#448488",
            "min": "#272727",
            "max": "#989719"
            }

    for l in lines:
        if l == "std":
            low_cint = (data["mean"] - data["std"]).copy()
            low_cint[low_cint < 0] = 0

            ax.fill_between(
                    data["hora"], 
                    low_cint,
                    data["mean"] + data["std"],
                    color=colors[l],
                    label=l
                    )
        else:
            ax.plot(
                    data["hora"], data[l],
                    color=colors[l], label=l
                    )
    ax.set_xticks(np.arange(24))
    ax.set_xlabel("Hora")
    ax.set_ylabel("Energía [Wh]")
    ax.set_xlim([0, 23])
    ax.legend()
