import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from dataclasses import dataclass
from matplotlib.gridspec import GridSpec

core = 4  # number of Cores
deadline = 120  # Deadline
Max_freq = 2  # Max Freq. in GHz

Task_color = 'darkgrey'
ov_color = 'red'
fault_color = 'green'


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


# T = Task('T2', 10, 2, 1, 10)

T = [Task() for _ in range(4)]

# T[0] = Task('$T_1$', 12, 1.6, 2, 30)
T[0] = Task('$T_1$', 12, 2, 1, 0)
T[1] = Task('$T_2$', 8, 2, 2, 12)
T[2] = Task('$T_3$', 7, 2, 3, 12)
T[3] = Task('$T_4$', 4, 2, 3, 20)

T_lo = [Task_lo() for _ in range(1)]
T_lo[0] = Task('$T_5$', 5, 2, 4, 20)

ov = [overrun() for _ in range(2)]

ov[0] = Task('$T^o_1$', 4, 2, 2, 50)
ov[1] = Task('$T^o_2$', 2, 2, 2, 10)

f = [fault() for _ in range(2)]

f[0] = Task('$T^f_1$', 4, 2, 3, 50)
f[1] = Task('$T^f_2$', 2, 2, 3, 10)

bold_text = {'ha': 'center', 'va': 'center', 'family': 'sans-serif', 'fontweight': 'bold'}
regular_text = {'ha': 'center', 'va': 'center', 'family': 'sans-serif', 'fontweight': 'regular'}

# fig = plt.figure(figsize=(deadline/4, 2.5 * core))
fig = plt.figure(constrained_layout=True,figsize=[10,5])
# figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
ax = fig.add_subplot(111)

# ax.grid()

plt.xlim([-10, deadline + 10])
plt.ylim([-10, 40 * core])

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
t=1
for i in range(2, (core*2) + 2,2):
    plt.text(-6, 8 + (20 * (i - 1)), 'Core ' + str(t), color='black', size=12, **regular_text)
    ax.arrow(0, (20 * (i - 1)), deadline + 2, 0, head_width=1, head_length=1, fc='k', ec='k')
    t+=1
#####

# Write Time under Axes
for i in range(0, deadline + 10, 10):
    plt.text(i, -2.5, str(i), color='black', size=10, **regular_text)
# Add Tick for Axes
for i in range(5, deadline + 5, 5):
    for j in range(1, (core*2),2):
        x = [i, i]
        y = [20 * j - 0.5, 20 * j]
        plt.plot(x, y, '-', color='black')
######

for x in T:
    rect1 = Rectangle((x.start, 20+ (x.core-1) * 40), x.Wcet, 12 * x.Freq / Max_freq, facecolor=Task_color,
                      edgecolor='black')
    ax.add_patch(rect1)
    plt.text(x.start + (x.Wcet / 2), 20+ (40 * (x.core-1 )) + 6 * x.Freq / Max_freq, x.name, color='black', size=12,
             **regular_text)

for x in ov:
    rect1 = Rectangle((x.start, 20+ (x.core-1) * 40), x.Wcet, 12 * x.Freq / Max_freq, facecolor='none', hatch="x",
                      edgecolor=ov_color)
    ax.add_patch(rect1)
    plt.text(x.start + (x.Wcet / 2), 20+(40 * (x.core - 1)) + 6 * x.Freq / Max_freq, x.name, color='black', size=12,
             **regular_text)

for x in f:
    rect1 = Rectangle((x.start, 20+ (x.core - 1) * 40), x.Wcet, 12 * x.Freq / Max_freq, facecolor='none', hatch="//",
                      edgecolor=fault_color)
    ax.add_patch(rect1)
    plt.text(x.start + (x.Wcet / 2), 20+(40 * (x.core - 1)) + 6 * x.Freq / Max_freq, x.name, color='black', size=12,
             **regular_text)

for x in T_lo:
    rect1 = Rectangle((x.start, 20+(x.core - 1) * 40), x.Wcet, 12 * x.Freq / Max_freq, facecolor='none',
                      edgecolor='black')
    ax.add_patch(rect1)
    plt.text(x.start + (x.Wcet / 2), 20+(40 * (x.core - 1)) + 6 * x.Freq / Max_freq, x.name, color='black', size=12,
             **regular_text)

plt.axis('off')

#fig=plt.figure(constrained_layout=True)
gs = GridSpec(8, 1,left=0.11)
#ax = fig.add_subplot(gs[2, 0])
#fig, ax = plt.subplots(gs[1, 0],figsize=(15,15))
#fig.set_figheight(15)
plt.show()

# someX, someY = 0.5, 0.5
# plt.figure()
# currentAxis = plt.gca()
# currentAxis.add_patch(Rectangle((someX - .1, someY - .1), 0.2, 0.2, color = 'c', alpha=0.5))
# plt.grid()
