import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from dataclasses import dataclass
import numpy as np
import matplotlib.ticker as ticker

from matplotlib.gridspec import GridSpec

core = 4  # number of Cores
deadline = 120  # Deadline
Max_freq = 2  # Max Freq. in GHz

num_Hi = 4
num_lo = 1

Task_color = 'darkgrey'
ov_color = 'red'
fault_color = 'green'

# power_y = [int() for _ in range(deadline)]
core1 = [float() for _ in range(deadline)]
core2 = [float() for _ in range(deadline)]
core3 = [float() for _ in range(deadline)]
core4 = [float() for _ in range(deadline)]
power_y = [int() for _ in range(deadline)]

for i in range(0, deadline):
    power_y[i] = i

file1 = open('core1.txt', 'r')
file2 = open('core2.txt', 'r')
file3 = open('core3.txt', 'r')
file4 = open('core4.txt', 'r')

i = 0;
for line in file1.readlines():
    core1[i] = float(line)
    i += 1
i = 0;
for line in file2.readlines():
    core2[i] = float(line)
    i += 1

i = 0;
for line in file3.readlines():
    core3[i] = float(line)
    i += 1

i = 0;
for line in file4.readlines():
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

## initialize and Read HI Tasks From File
T = [Task() for _ in range(num_Hi)]
file = open('HI-Tasks.txt', 'r')
j = 0
for line in file.readlines()[1:]:
    # print(line)
    inputs = line.split('\t')
    # print(inputs)
    i = 0
    for y in inputs:
        if (i == 0):
            name = str(y)
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

T_lo = [Task_lo() for _ in range(num_lo)]
file = open('LO-Tasks.txt', 'r')
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
    T_lo[j] = Task(name, WCET, Freq, Core, Start)
    j += 1

ov = [overrun() for _ in range(2)]

ov[0] = Task('$T^o_1$', 4, 2, 2, 50)
ov[1] = Task('$T^o_2$', 2, 2, 2, 10)

f = [fault() for _ in range(2)]

f[0] = Task('$T^f_1$', 4, 2, 3, 50)
f[1] = Task('$T^f_2$', 2, 2, 3, 10)

bold_text = {'ha': 'center', 'va': 'center', 'family': 'sans-serif', 'fontweight': 'bold'}
regular_text = {'ha': 'center', 'va': 'center', 'family': 'sans-serif', 'fontweight': 'regular'}

# fig = plt.figure(figsize=(deadline/4, 2.5 * core))
fig = plt.figure(figsize=[10, 5])
# figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
# ax = fig.add_subplot(111)
ax = fig.add_axes([0, 0, 1, 1])

# ax.grid()

plt.xlim([-10, deadline + 10])
plt.ylim([-10, 40 * core + 10])

# Draw Deadline
x = [deadline, deadline]
y = [0, 40 * core]
plt.plot(x, y, '--', color='r')
plt.text(deadline, 40 * core + 1, 'Deadline', color='r', size=11, **regular_text)
###########

# write Cores Name and Draw Axes for each core
x = [0, 0]
y = [0, 40 * core + 1]
plt.plot(x, y, '-', color='black')
t = 1
for i in range(2, (core * 2) + 2, 2):
    plt.text(-6, 8 + (20 * (i - 1)), 'Core ' + str(t), color='black', size=12, **regular_text)
    ax.arrow(0, (20 * (i - 1)), deadline + 2, 0, head_width=1, head_length=1, fc='k', ec='k')
    t += 1
#####

# Write Time under Axes
for i in range(0, deadline + 10, 10):
    plt.text(i, -2.5, str(i), color='black', size=10, **regular_text)
# Add Tick for Axes
for i in range(5, deadline + 5, 5):
    for j in range(1, (core * 2), 2):
        x = [i, i]
        y = [20 * j - 0.5, 20 * j]
        plt.plot(x, y, '-', color='black')
######

for x in T:
    rect1 = Rectangle((x.start, 20 + (x.core - 1) * 40), x.Wcet, 12 * x.Freq / Max_freq, facecolor=Task_color,
                      edgecolor='black')
    ax.add_patch(rect1)
    plt.text(x.start + (x.Wcet / 2), 20 + (40 * (x.core - 1)) + 6 * x.Freq / Max_freq, x.name, color='black', size=12,
             **regular_text)

for x in ov:
    rect1 = Rectangle((x.start, 20 + (x.core - 1) * 40), x.Wcet, 12 * x.Freq / Max_freq, facecolor='none', hatch="x",
                      edgecolor=ov_color)
    ax.add_patch(rect1)
    plt.text(x.start + (x.Wcet / 2), 20 + (40 * (x.core - 1)) + 6 * x.Freq / Max_freq, x.name, color='black', size=12,
             **regular_text)

for x in f:
    rect1 = Rectangle((x.start, 20 + (x.core - 1) * 40), x.Wcet, 12 * x.Freq / Max_freq, facecolor='none', hatch="//",
                      edgecolor=fault_color)
    ax.add_patch(rect1)
    plt.text(x.start + (x.Wcet / 2), 20 + (40 * (x.core - 1)) + 6 * x.Freq / Max_freq, x.name, color='black', size=12,
             **regular_text)

for x in T_lo:
    rect1 = Rectangle((x.start, 20 + (x.core - 1) * 40), x.Wcet, 12 * x.Freq / Max_freq, facecolor='none',
                      edgecolor='black')
    ax.add_patch(rect1)
    plt.text(x.start + (x.Wcet / 2), 20 + (40 * (x.core - 1)) + 6 * x.Freq / Max_freq, x.name, color='black', size=12,
             **regular_text)

plt.axis('off')

## Core1 Power Chart
ax2 = fig.add_axes([0.072, 0.06, 0.856, 0.09])
ax2.axes.get_xaxis().set_visible(False)
ax2.set_xlim(0, deadline)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))

ax2.set_ylim(0, 4)
ax2.set_ylabel('Core 1\nPower')
ax2.plot(power_y, core1)
ax2.grid(True)

## Core2 Power Chart
ax3 = fig.add_axes([0.072, 0.28, 0.856, 0.09])
ax3.axes.get_xaxis().set_visible(False)
ax3.set_xlim(0, deadline)
ax3.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax3.set_ylim(0, 4)
ax3.set_ylabel('Core 2\nPower')
ax3.grid(True)
ax3.plot(power_y, core2)

## Core3 Power Chart
ax4 = fig.add_axes([0.072, 0.51, 0.856, 0.09])
ax4.axes.get_xaxis().set_visible(False)
ax4.set_xlim(0, deadline)
ax4.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax4.set_ylim(0, 4)
ax4.set_ylabel('Core 3\nPower')
ax4.grid(True)
ax4.plot(power_y, core3)

## Core4 Power Chart
ax5 = fig.add_axes([0.072, 0.73, 0.856, 0.09])
ax5.axes.get_xaxis().set_visible(False)
ax5.set_xlim(0, deadline)
ax5.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax5.set_ylim(0, 4)
ax5.set_ylabel('Core 4\nPower')
ax5.grid(True)
ax5.plot(power_y, core4)

plt.show()
# plt.savefig('test.png')

# someX, someY = 0.5, 0.5
# plt.figure()
# currentAxis = plt.gca()
# currentAxis.add_patch(Rectangle((someX - .1, someY - .1), 0.2, 0.2, color = 'c', alpha=0.5))
# plt.grid()
