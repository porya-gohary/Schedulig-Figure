import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


core=4 #number of Cores
deadline =100
T1 = [10, 2]  # Task specification  [ Run Time , Freq]

fig = plt.figure()
#figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
ax = fig.add_subplot(111)
rect1 = matplotlib.patches.Rectangle((0, 1), 5, 0.5, color='c')

ax.add_patch(rect1)
# ax.grid()
#plt.figure(num=None, figsize=(100, 100), dpi=80, facecolor='w', edgecolor='k')

plt.xlim([0, deadline+10])
plt.ylim([0, 20*core])

x = [deadline,deadline]
y = [0,20*core]
plt.plot(x,y,'--', color='r')
plt.axis('off')
plt.show()

# someX, someY = 0.5, 0.5
# plt.figure()
# currentAxis = plt.gca()
# currentAxis.add_patch(Rectangle((someX - .1, someY - .1), 0.2, 0.2, color = 'c', alpha=0.5))
# plt.grid()
