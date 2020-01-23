import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


core=4 #number of Cores
deadline =100
T1 = [10, 2]  # Task specification  [ Run Time , Freq]


bold_text = {'ha': 'center', 'va': 'center', 'family': 'sans-serif','fontweight': 'bold'}
regular_text = {'ha': 'center', 'va': 'center', 'family': 'sans-serif','fontweight': 'regular'}
fig = plt.figure()
#figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
ax = fig.add_subplot(111)
rect1 = matplotlib.patches.Rectangle((0, 1), 5, 0.5, color='c')

ax.add_patch(rect1)
# ax.grid()

plt.xlim([-10, deadline+10])
plt.ylim([0, 20*core])

#Draw Deadline
x = [deadline,deadline]
y = [0,20*core]
plt.plot(x,y,'--', color='r')
plt.text(deadline, 20*core+1, 'Deadline', color='r', size=10,**regular_text)
###########

#write Cores Name
for i in range(1, core+1):
    plt.text(-5, (20*core+10)-(20*i), 'Core '+str(i), color='black', size=10,**regular_text)
#####


#ax = plt.axes()
ax.arrow(0, 0, 0.5, 0.5, head_width=0.05, head_length=0.1, fc='k', ec='k')

plt.axis('off')
plt.show()

# someX, someY = 0.5, 0.5
# plt.figure()
# currentAxis = plt.gca()
# currentAxis.add_patch(Rectangle((someX - .1, someY - .1), 0.2, 0.2, color = 'c', alpha=0.5))
# plt.grid()
