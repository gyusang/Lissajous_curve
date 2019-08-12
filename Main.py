import numpy as np
import matplotlib.pyplot as plt

from DragVector import DragVector
from matplotlib.widgets import Slider, Button


fig = plt.figure(figsize=(10,6))
fig.suptitle("리사주 곡선")
ax_1, ax_2 = fig.subplots(1, 2)
plt.subplots_adjust(bottom=0.3)

curve = None

axcolor = 'lightgoldenrodyellow'
ax_omega_x = plt.axes([0.1, 0.2, 0.7, 0.03], facecolor=axcolor)
ax_omega_y = plt.axes([0.1, 0.15, 0.7, 0.03], facecolor=axcolor)
ax_t = plt.axes([0.1, 0.1, 0.7, 0.03], facecolor=axcolor)

s_omega_x = Slider(ax_omega_x, r'$\omega_x$', 1, 10, valinit=1, valstep=1)
s_omega_y = Slider(ax_omega_y, r'$\omega_y$', 1, 10, valinit=1, valstep=1)
s_t = Slider(ax_t, 'Time', 0, 100, valinit=10, valstep=1)

ax_pi = plt.axes([0.87, 0.2, 0.05, 0.03])
ax_e = plt.axes([0.87, 0.15, 0.05, 0.03])
ax_restart = plt.axes([0.87, 0.1, 0.05, 0.03])
ax_reset = plt.axes([0.87, 0.05, 0.05, 0.03])

btn_pi = Button(ax_pi, r'$\pi$', color=axcolor)
btn_e = Button(ax_e, '$e$', color=axcolor)
btn_restart = Button(ax_restart, 'Restart', color=axcolor)
btn_reset = Button(ax_reset, 'Reset', color=axcolor)

def set_pi(event):
    s_omega_x.set_val(np.pi)

def set_e(event):
    s_omega_y.set_val(np.e)


btn_pi.on_clicked(set_pi)
btn_e.on_clicked(set_e)

ax_1.axis('equal')
ax_2.axis('equal')

ax_1.set_xlim(-5, 5)
ax_1.set_ylim(-5, 5)
ax_2.set_xlim(-5, 5)
ax_2.set_ylim(-5, 5)

dv = DragVector(ax_1, s_omega_x, s_omega_y, s_t.val, ax_2)
dv.connect()

s_omega_x.on_changed(dv.update_curveField)
s_omega_y.on_changed(dv.update_curveField)
dv.update_curveField()
s_t.on_changed(dv.update_t)
btn_restart.on_clicked(lambda event: dv.start_curveAnim())
btn_reset.on_clicked(lambda event: dv.reset())

plt.show()