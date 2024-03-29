#!/usr/bin/env python3
"""
Drawing Tool for Real-time Scheduling
    Copyright © 2020 Pourya Gohari

Usage:
    draw-tool                [options]

Options:
    --chart, -c                         draw power and thermal charts [default: False]
    --deadline=N, -d N                  system deadline in millisecond  [default: 100]
    --output=PATH, -o PATH              PATH of output and format <.pdf | .png | .svg> [default: out.pdf]
    --version, -v                       show version and exit
    --help, -h                          show this message
"""
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from dataclasses import dataclass
import numpy as np
import matplotlib.ticker as ticker
from PIL import Image
import math
from docopt import docopt
from pathlib import Path

from matplotlib.gridspec import GridSpec
if __name__ == "__main__":
    core = 4  # number of Cores
    deadline = 100  # Deadline
    Max_freq = 2  # Max Freq. in GHz
    Max_temp = 60  # Max Temp. in Celsius

    num_Hi = 0
    num_lo = 1
    num_over = 0
    num_fault = 0
    num_faulty = 0
    x_axes_distance = 13
    offset = 1
    ## dealing with OS path
    default_path = Path("inputs/")

    print_over = False
    Faulty_sign = False
    charts = True
    output = 'out.pdf'

    arguments = docopt(__doc__,version='1.1.0')
    charts = arguments['--chart']

    if charts not in [True, False]:
        print('Option --chart must be True | False. given {}.'.format(charts))
        exit(1)

    if arguments['--output']:
        output = arguments['--output']
    #print(output)

    if arguments['--deadline']:
        deadline = int(arguments['--deadline'])
    #print(deadline)
    if(charts):
        x_axes_distance = 26
        offset = x_axes_distance/2

    file = open(default_path/'HI-Tasks.txt', 'r')
    j = 0
    for line in file.readlines()[1:]:
        j += 1
    num_Hi = j

    file = open(default_path/'LO-Tasks.txt', 'r')
    j = 0
    for line in file.readlines()[1:]:
        j += 1
    num_lo = j

    file = open(default_path/'Over-Tasks.txt', 'r')
    j = 0
    for line in file.readlines()[1:]:
        j += 1
    num_over = j

    file = open(default_path/'Fault-Tasks.txt', 'r')
    j = 0
    for line in file.readlines()[1:]:
        j += 1
    num_fault = j

    file = open(default_path/'Faulty.txt', 'r')
    j = 0
    for line in file.readlines()[1:]:
        j += 1
    num_faulty = j

    Task_color = 'darkgrey'
    ov_color = 'red'
    fault_color = 'green'

    bold_text = {'ha': 'center', 'va': 'center', 'family': 'sans-serif', 'fontweight': 'bold',
                 'fontname': 'Palatino Linotype'}
    regular_text = {'ha': 'center', 'va': 'center', 'family': 'sans-serif', 'fontweight': 'regular',
                    'fontname': 'Palatino Linotype'}

    # power_y = [int() for _ in range(deadline)]
    core1 = [float() for _ in range(deadline)]
    core2 = [float() for _ in range(deadline)]
    core3 = [float() for _ in range(deadline)]
    core4 = [float() for _ in range(deadline)]
    temp = [float() for _ in range(deadline)]

    power_y = [int() for _ in range(deadline)]
    temp_max = [int() for _ in range(deadline)]

    for i in range(0, deadline):
        power_y[i] = i
    for i in range(0, deadline):
        temp_max[i] = Max_temp

    if(charts):
        file1 = open(default_path/'core1.txt', 'r')
        file2 = open(default_path/'core2.txt', 'r')
        file3 = open(default_path/'core3.txt', 'r')
        file4 = open(default_path/'core4.txt', 'r')
        file_temp = open(default_path/'Temp.txt', 'r')

        i = 0
        for line in file_temp.readlines()[0:deadline]:
            temp[i] = float(line)
            i += 1

        i = 0
        for line in file1.readlines()[0:deadline]:
            core1[i] = float(line)
            i += 1
        i = 0
        for line in file2.readlines()[0:deadline]:
            core2[i] = float(line)
            i += 1

        i = 0
        for line in file3.readlines()[0:deadline]:
            core3[i] = float(line)
            i += 1

        i = 0
        for line in file4.readlines()[0:deadline]:
            core4[i] = float(line)
            i += 1

    @dataclass
    class Task:
        # Task specification  [ Name, WCET , Freq, Core, Start Time]
        name: str = 'none'
        Wcet: int = 0
        Freq: float = 0
        core: int = 0
        start: int = 0

    @dataclass
    class Task_lo:
        # Task specification  [ Name, WCET , Freq, Core, Start Time]
        name: str = 'none'
        Wcet: int = 0
        Freq: float = 0
        core: int = 0
        start: int = 0

    @dataclass
    class overrun:
        # Task specification  [ Name, WCET , Freq, Core, Start Time]
        name: str = 'none'
        Wcet: int = 0
        Freq: float = 0
        core: int = 0
        start: int = 0

    @dataclass
    class fault:
        # Task specification  [ Name, WCET , Freq, Core, Start Time]
        name: str = 'none'
        Wcet: int = 0
        Freq: float = 0
        core: int = 0
        start: int = 0

    name = 'none'
    WCET = 10
    Freq = 2
    Core = 1
    Start = 0

    # initialize and Read HI Tasks From File
    T = [Task() for _ in range(num_Hi)]
    file = open(default_path/'HI-Tasks.txt', 'r')
    j = 0
    for line in file.readlines()[1:]:
        # print(line)
        inputs = line.split('\t')
        # print(inputs)
        i = 0
        for y in inputs:
            if (i == 0):
                name = "$\\mathrm{"+str(y)+"}$"
                # print(name)
            if (i == 1):
                WCET = int(y)
            if (i == 2):
                Freq = float(y)
            if (i == 3):
                Core = int(y)
            if (i == 4):
                Start = int(y)
            i += 1
        T[j] = Task(name, WCET, Freq, Core, Start)
        j += 1

    # initialize and Read LO Tasks From File
    T_lo = [Task_lo() for _ in range(num_lo)]
    file = open(default_path/'LO-Tasks.txt', 'r')
    j = 0
    for line in file.readlines()[1:]:
        inputs = line.split('\t')
        i = 0
        for y in inputs:
            if (i == 0):
                name = "$\\mathrm{"+str(y)+"}$"
            if (i == 1):
                WCET = int(y)
            if (i == 2):
                Freq = float(y)
            if (i == 3):
                Core = int(y)
            if (i == 4):
                Start = int(y)
            i += 1
        T_lo[j] = Task(name, WCET, Freq, Core, Start)
        j += 1

    # initialize and Read Overrun From File
    ov = [overrun() for _ in range(num_over)]
    file = open(default_path/'Over-Tasks.txt', 'r')
    j = 0
    for line in file.readlines()[1:]:
        inputs = line.split('\t')
        i = 0
        for y in inputs:
            if (i == 0):
                name = str(y)
            if (i == 1):
                WCET = int(y)
            if (i == 2):
                Freq = float(y)
            if (i == 3):
                Core = int(y)
            if (i == 4):
                Start = int(y)
            i += 1
        ov[j] = Task(name, WCET, Freq, Core, Start)
        j += 1

    # ov[0] = Task('$T^o_1$', 4, 2, 2, 50)
    # ov[1] = Task('$T^o_2$', 2, 2, 2, 10)

    # initialize and Read Fault From File
    f = [fault() for _ in range(num_fault)]
    file = open(default_path/'Fault-Tasks.txt', 'r')
    j = 0
    for line in file.readlines()[1:]:
        inputs = line.split('\t')
        i = 0
        for y in inputs:
            if (i == 0):
                name = str(y)
            if (i == 1):
                WCET = int(y)
            if (i == 2):
                Freq = float(y)
            if (i == 3):
                Core = int(y)
            if (i == 4):
                Start = int(y)
            i += 1
        f[j] = Task(name, WCET, Freq, Core, Start)
        j += 1

    f_t = ['none' for _ in range(num_faulty)]
    file = open(default_path/'Faulty.txt', 'r')
    j = 0
    for line in file.readlines()[1:]:
        line = line.rstrip('\n')
        f_t[j] = "$\\mathrm{"+str(line)+"}$"
        j += 1

    # fig = plt.figure(figsize=(deadline/4, 2.5 * core))
    if(charts):
        fig = plt.figure(figsize=[10*deadline/120, 8])
    else:
        fig = plt.figure(figsize=[10*deadline/120, 4])
    # figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
    if(charts):
        ax = fig.add_axes([0, 0.25, 1, 1])
    else:
        ax = fig.add_subplot(111)
    plt.axis('off')

    # ax.grid()

    plt.xlim([-10, deadline + 10])
    if(charts):
        plt.ylim([-10, (x_axes_distance+10) * core + 10])
    else:
        plt.ylim([0, x_axes_distance * core + 5])

    # Draw Deadline
    x = [deadline, deadline]
    y = [0, x_axes_distance * core - 1]
    plt.plot(x, y, '--', color='r', zorder=20)
    plt.text(deadline, x_axes_distance * core + 1,
             'Deadline', color='r', size=11, **regular_text)

    ###########
    # Time Label Foy Y Axes
    plt.text(deadline / 2, -6, 'Time(ms)',
             color='black', size=11, **regular_text)

    # write Cores Name and Draw Axes for each core
    x = [0, 0]
    y = [0, x_axes_distance * core + 1]
    plt.plot(x, y, '-', color='black')
    t = 1
    if(charts):
        for i in range(2, (core * 2) + 2, 2):
            plt.text(-5, 5 + (x_axes_distance/2 * (i - 1)), 'Core ' +
                     str(t), color='black', size=12, **bold_text)
            ax.arrow(0, (x_axes_distance/2 * (i - 1)), deadline + 2,
                     0, head_width=1, head_length=1, fc='k', ec='k')
            t += 1
    else:
        for i in range(1, (core * 2), 2):
            plt.text(-5, offset+5 + (x_axes_distance/2 * (i - 1)),
                     'Core ' + str(t), color='black', size=12, **bold_text)
            ax.arrow(0, offset+(x_axes_distance/2 * (i - 1)), deadline +
                     2, 0, head_width=1, head_length=1, fc='k', ec='k')
            t += 1

    #####

    # Write Time under Axes
    for i in range(0, deadline+1, 5):
        if(i % 10 == 0):
            plt.text(i, -2.5, str(i), color='black', size=10, **regular_text)
    # Add Tick for Axes
    if(charts):
        for i in range(5, deadline + 5, 5):
            for j in range(1, (core * 2), 2):
                x = [i, i]
                y = [x_axes_distance/2 * j - 0.5, x_axes_distance/2 * j]
                plt.plot(x, y, '-', color='black')
    else:
        for i in range(5, deadline + 5, 5):
            for j in range(0, core*2, 2):
                x = [i, i]
                y = [x_axes_distance/2 * j - 0.5 +
                     offset, x_axes_distance/2 * j+offset]
                plt.plot(x, y, '-', color='black')
    ######

    for x in T:
        rect1 = Rectangle((x.start, offset + (x.core - 1) * x_axes_distance), x.Wcet, 10 * x.Freq / Max_freq, facecolor=Task_color,
                          edgecolor='black')
        ax.add_patch(rect1)
        plt.text(x.start + (x.Wcet / 2), offset + (x_axes_distance * (x.core - 1)) + 5 * x.Freq / Max_freq, x.name, color='black', size=17,
                 **regular_text)

    for x in ov:
        rect1 = Rectangle((x.start, offset + (x.core - 1) * x_axes_distance), x.Wcet, 10 * x.Freq / Max_freq, facecolor='none', hatch="////",
                          edgecolor=ov_color)
        ax.add_patch(rect1)
        if (print_over):
            plt.text(x.start + (x.Wcet / 2), offset + (x_axes_distance * (x.core - 1)) + 5 * x.Freq / Max_freq, x.name, color='black',
                     size=12, **regular_text)

    for x in f:
        rect1 = Rectangle((x.start, offset + (x.core - 1) * x_axes_distance), x.Wcet, 10 * x.Freq / Max_freq, facecolor='none', hatch="////",
                          edgecolor=fault_color)
        ax.add_patch(rect1)
        plt.text(x.start + (x.Wcet / 2), offset + (x_axes_distance * (x.core - 1)) + 5 * x.Freq / Max_freq, x.name, color='black', size=12,
                 **regular_text)

    for x in T_lo:
        rect1 = Rectangle((x.start, offset + (x.core - 1) * x_axes_distance), x.Wcet, 10 * x.Freq / Max_freq, facecolor='none',
                          edgecolor='black')
        ax.add_patch(rect1)
        plt.text(x.start + (x.Wcet / 2), offset + (x_axes_distance * (x.core - 1)) + 5 * x.Freq / Max_freq, x.name, color='black', size=17,
                 **regular_text)

    if(charts):
        # Core1 Power Chart
        #ax2 = fig.add_axes([0.072, 0.31, 0.856, 0.07])
        #ax2 = fig.add_axes([0.102, 0.31, 0.8, 0.07])
        #ax2 = fig.add_axes([0.126, 0.31, 0.744, 0.07])
        z = deadline
        x = 0.2533524 - 0.002975714*z + 0.00001623545 * \
            math.pow(z, 2) - 3.359788e-8*math.pow(z, 3)
        y = 0.3695238 + 0.009609524*z - 0.00006597884 * \
            math.pow(z, 2) + 1.640212e-7*math.pow(z, 3)
        # print(x)
        ax2 = fig.add_axes([x, 0.31, y, 0.07], zorder=-2)

        ax2.axes.get_xaxis().set_visible(False)
        ax2.set_xlim(0, deadline)
        ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))
        ax2.tick_params(axis='both', which='major', labelsize=7)
        ax2.set_ylim(0, 4)
        ax2.set_ylabel('Core 1\nPower(W)', fontname='Palatino Linotype')
        ax2.plot(power_y, core1, color='green')
        ax2.grid(True)

        # Core2 Power Chart
        #ax3 = fig.add_axes([0.072, 0.47, 0.856, 0.07])
        ax3 = fig.add_axes([x, 0.47, y, 0.07], zorder=-2)
        ax3.axes.get_xaxis().set_visible(False)
        ax3.set_xlim(0, deadline)
        ax3.yaxis.set_major_locator(ticker.MultipleLocator(1))
        ax3.tick_params(axis='both', which='major', labelsize=7)
        ax3.set_ylim(0, 4)
        ax3.set_ylabel('Core 2\nPower(W)', fontname='Palatino Linotype')
        ax3.grid(True)
        ax3.plot(power_y, core2, color='green')

        # Core3 Power Chart
        #ax4 = fig.add_axes([0.072, 0.63, 0.856, 0.07])
        ax4 = fig.add_axes([x, 0.63, y, 0.07], zorder=-2)
        ax4.axes.get_xaxis().set_visible(False)
        ax4.set_xlim(0, deadline)
        ax4.yaxis.set_major_locator(ticker.MultipleLocator(1))
        ax4.tick_params(axis='both', which='major', labelsize=7)
        ax4.set_ylim(0, 4)
        ax4.set_ylabel('Core 3\nPower(W)', fontname='Palatino Linotype')
        ax4.grid(True)
        ax4.plot(power_y, core3, color='green')

        # Core4 Power Chart
        #ax5 = fig.add_axes([0.072, 0.79, 0.856, 0.07])
        ax5 = fig.add_axes([x, 0.79, y, 0.07], zorder=-2)
        ax5.axes.get_xaxis().set_visible(False)
        ax5.set_xlim(0, deadline)
        ax5.yaxis.set_major_locator(ticker.MultipleLocator(1))
        ax5.tick_params(axis='both', which='major', labelsize=7)
        ax5.set_ylim(0, 4)
        ax5.set_ylabel('Core 4\nPower(W)', fontname='Palatino Linotype')
        ax5.grid(True)
        ax5.plot(power_y, core4, color='green')

        # Tempreture Chart
        #ax6 = fig.add_axes([0.072, 0.05, 0.856, 0.2])
        ax6 = fig.add_axes([x, 0.05, y, 0.2], zorder=-2)
        # ax6.axes.get_xaxis().set_visible(False)
        ax6.set_xlim(0, deadline)
        ax6.yaxis.set_major_locator(ticker.MultipleLocator(10))
        ax6.tick_params(axis='both', which='major', labelsize=8)
        ax6.set_ylim(0, 80)
        ax6.set_ylabel(
            'Max. Temperature[°C]', fontsize=12, fontname='Palatino Linotype')
        ax6.grid(True)
        ax6.plot(power_y, temp)
        ax6.plot(power_y, temp_max, '--', color='darkred')

    # Add Fault Sign To Tasks
    if(Faulty_sign):
        im = Image.open('fault.png')
        height = int(im.size[1]/10)
        width = int(im.size[0]/10)
        # print(width)
        im = im.resize((width, height), Image.NEAREST)
        im = np.array(im).astype(np.float) / 255
        for x in f_t:
            #print(x+ "FAULTY")
            for y in T:
                # print(y.name)
                if (y.name == x):
                    fig.figimage(im, int(y.start)*8+(y.Wcet)
                                 * 3+10, 225+((y.core)*125))
                    # print(y.Wcet)

    # plt.plot(np.arange(10), 4 * np.arange(10))

    plt.savefig(output)
    plt.savefig('test.png')
    plt.savefig('test.svg')
    plt.show()

    # someX, someY = 0.5, 0.5
    # plt.figure()
    # currentAxis = plt.gca()
    # currentAxis.add_patch(Rectangle((someX - .1, someY - .1), 0.2, 0.2, color = 'c', alpha=0.5))
    # plt.grid()
