import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from dataclasses import dataclass

core = 4  # number of Cores
deadline = 100  # Deadline
Max_freq = 2  # Max Freq. in GHz

Task_color = 'darkgrey'


@dataclass
class Task:
    # Task specification  [ Name, WCET , Freq, Core, Start Time]
    name: str = 'none'
    Wcet: int = 0
    Freq: float = 0
    core: int = 0
    start: int = 0

@dataclass
class Task_MC:
    # Task specification  [ Name, WCET , Freq, Core, Start Time]
    name: str = 'none'
    Wcet: int = 0
    Freq: float = 0
    core: int = 0
    start: int = 0


# T = Task('T2', 10, 2, 1, 10)

T = [Task() for _ in range(3)]

T[0] = Task('$T_1$', 20, 1.6, 2, 30)
T[1] = Task('$T_2$', 10, 2, 1, 10)
T[2] = Task('$T_3$', 20, 1.2, 1, 20)

bold_text = {'ha': 'center', 'va': 'center', 'family': 'sans-serif', 'fontweight': 'bold'}
regular_text = {'ha': 'center', 'va': 'center', 'family': 'sans-serif', 'fontweight': 'regular'}
fig = plt.figure()
# figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
ax = fig.add_subplot(111)

# ax.grid()

plt.xlim([-10, deadline + 10])
plt.ylim([-10, 20 * core])

# Draw Deadline
x = [deadline, deadline]
y = [0, 20 * core]
plt.plot(x, y, '--', color='r')
plt.text(deadline, 20 * core + 1, 'Deadline', color='r', size=11, **regular_text)
###########

# write Cores Name and Draw Axes for each core
for i in range(1, core + 1):
    plt.text(-6, 8 + (20 * (i - 1)), 'Core ' + str(i), color='black', size=12, **regular_text)
    ax.arrow(0, (20 * (i - 1)), deadline + 2, 0, head_width=1, head_length=1, fc='k', ec='k')
    ax.arrow(0, (20 * (i - 1)), 0, 15, head_width=1, head_length=1, fc='k', ec='k')
#####

# Write Time under Axes
for i in range(0, deadline + 10, 10):
    plt.text(i, -2.5, str(i), color='black', size=10, **regular_text)
# Add Tick for Axes
for i in range(5, deadline + 5, 5):
    for j in range(0, core):
        x = [i, i]
        y = [20 * j - 0.5, 20 * j]
        plt.plot(x, y, '-', color='black')
######

for x in T:
    rect1 = Rectangle((x.start, (x.core - 1) * 20), x.Wcet, 12 * x.Freq / Max_freq, facecolor=Task_color,
                      edgecolor='black')
    ax.add_patch(rect1)
    plt.text(x.start + (x.Wcet / 2), (20 * (x.core - 1)) + 6 * x.Freq / Max_freq, x.name, color='black', size=12,
             **regular_text)

plt.axis('off')
plt.show()

# someX, someY = 0.5, 0.5
# plt.figure()
# currentAxis = plt.gca()
# currentAxis.add_patch(Rectangle((someX - .1, someY - .1), 0.2, 0.2, color = 'c', alpha=0.5))
# plt.grid()
