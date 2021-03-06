# -*- mode: python; -*-
# Execute this script using Bash script of the same name but without a file
# extension. Use ../pdbwrapper/pdbwrapper instead of pdb for debugging.
"""
GANTT Chart with Matplotlib
Sukhbinder
Inspired from
http://www.clowersresearch.com/main/gantt-charts-in-matplotlib/
"""

import os
import sys
import argparse
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.dates
from matplotlib.dates import WEEKLY, DateFormatter, rrulewrapper, RRuleLocator
import numpy as np


def _create_date(datetxt):
    """Creates the date"""
    day, month, year = datetxt.split('-')
    date = dt.datetime(int(year), int(month), int(day))
    mdate = matplotlib.dates.date2num(date)
    return mdate


def CreateGanttChart(fname):
    """Create gantt charts with matplotlib
    Give file name.
    """
    ylabels = []
    customDates = []
    textlist = open(fname).readlines()

    for tx in textlist:
        if not tx.startswith('#'):
            ylabel, startdate, enddate = tx.split(',')
            ylabels.append(ylabel.replace('\n', ''))
            customDates.append([_create_date(startdate.replace('\n', '')), _create_date(enddate.replace('\n', ''))])

    ilen = len(ylabels)
    pos = np.arange(0.5, ilen * 0.5 + 0.5, 0.5)
    task_dates = {}
    for i, task in enumerate(ylabels):
        task_dates[task] = customDates[i]
    fig = plt.figure(figsize=(20, 8))
    ax = fig.add_subplot(111)
    for i in range(len(ylabels)):
        start_date, end_date = task_dates[ylabels[i]]
        ax.barh((i * 0.5) + 0.5, end_date - start_date, left=start_date, height=0.3, align='center', edgecolor='lightgreen', color='orange', alpha=0.8)
    locsy, labelsy = plt.yticks(pos, ylabels)
    plt.setp(labelsy, fontsize=14)
    # ax.axis('tight')
    ax.set_ylim(ymin=-0.1, ymax=ilen * 0.5 + 0.5)
    ax.grid(color='g', linestyle=':')
    ax.xaxis_date()
    rule = rrulewrapper(WEEKLY, interval=1)
    loc = RRuleLocator(rule)
    # formatter = DateFormatter("%d-%b '%y")
    formatter = DateFormatter("%d-%b")

    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(formatter)
    labelsx = ax.get_xticklabels()
    plt.setp(labelsx, rotation=30, fontsize=10)

    font = font_manager.FontProperties(size='small')
    ax.legend(loc=1, prop=font)

    ax.invert_yaxis()
    fig.autofmt_xdate()
    plt.savefig(fname + '.svg')
    plt.show()


def script_base():
    'The basename of the script file for usage.'
    return os.path.basename(os.path.splitext(sys.argv[0])[0])


description = r"""
{script} -- Basic Gantt Chart

Demonstrate the code at https://sukhbinder.wordpress.com/2016/05/10/quick-gantt-chart-with-matplotlib/

Example:

  {script} -f projectChart.txt

""".format(script=script_base())


def main():
    """
    Main function
    """
    # Parse command-line arguments:
    #    https://docs.python.org/2/howto/argparse.html
    parser = argparse.ArgumentParser(
        prog=os.path.basename(os.path.splitext(sys.argv[0])[0]),  # Avoid showing the .py file extension in the usage help
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--project_file', help='Path to project file.', required=True)
    args = parser.parse_args(sys.argv[1:])

    CreateGanttChart(args.project_file)


if __name__ == '__main__':
    sys.exit(0 if main() else 1)  # Return non-zero exit codes upon failure
