import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from Curve import Curve
from matplotlib.animation import FuncAnimation


class DragVector:
    def __init__(self, ax, s_omega_x, s_omega_y, t1=10, ax2=None):
        self.ax = ax
        self.ax2 = ax2
        self.start = None
        self.arrow = None
        self.arrow2 = None
        self.curveField = None
        self.curve = None
        self.curveFunc = None
        self.s_omega_x = s_omega_x
        self.s_omega_y = s_omega_y
        self.t_end = t1
        self.end_curve, = ax2.plot([],[],'b-')
        self.anim_curve, = ax.plot([],[],'b-')
        self.anim_data = [[],[]]
        self.anim = []
        self.vector = None
        self.anim_current, = ax.plot([],[],'b.')

    def connect(self):
        self.cidPress = self.ax.figure.canvas.mpl_connect(
            'button_press_event', self.on_press
        )
        self.cidRelease = self.ax.figure.canvas.mpl_connect(
            'button_release_event', self.on_release
        )
        self.cidMotion = self.ax.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion
        )

    def on_press(self, event):
        if self.ax.figure.canvas.manager.toolbar.mode != '': return
        if event.button != MouseButton.LEFT: return
        if event.inaxes != self.ax: return

        if self.arrow is not None:
            self.arrow.remove()
        if self.arrow2 is not None:
            self.arrow2.remove()
        self.stop_curve()
        self.start = x, y = event.xdata, event.ydata
        self.arrow, = self.ax.plot([x], [y], 'k.')
        self.ax.figure.canvas.draw()

        if self.ax2 is not None:
            self.arrow2, = self.ax2.plot([x], [y], 'k.')
            self.ax2.figure.canvas.draw()

    def on_motion(self, event):
        if self.ax.figure.canvas.manager.toolbar.mode != '': return
        if event.button != MouseButton.LEFT: return
        if event.inaxes != self.ax: return
        if self.start is None: return
        if self.arrow is not None:
            self.arrow.remove()
        if self.arrow2 is not None:
            self.arrow2.remove()
        x0, y0 = self.start
        dx = event.xdata - x0
        dy = event.ydata - y0
        if np.linalg.norm((dx, dy)) < 0.2:
            self.arrow, = self.ax.plot([x0, event.xdata], [y0, event.ydata], 'k.-')
        else:
            self.arrow = self.ax.arrow(
                x0, y0, dx, dy,
                head_width=0.05, head_length=0.1,
                fc='k', ec='k', length_includes_head=True
            )
        self.ax.figure.canvas.draw()

        if self.ax2 is not None:
            if np.linalg.norm((dx, dy)) < 0.2:
                self.arrow2, = self.ax2.plot([x0, event.xdata], [y0, event.ydata], 'k-')
            else:
                self.arrow2 = self.ax2.arrow(
                    x0, y0, dx, dy,
                    head_width=0.05, head_length=0.1,
                    fc='k', ec='k', length_includes_head=True
                )
            self.ax2.figure.canvas.draw()

    def on_release(self, event):
        if self.ax.figure.canvas.manager.toolbar.mode != '': return
        if event.button != MouseButton.LEFT: return
        if event.inaxes != self.ax: return
        x0, y0 = self.start
        dx = event.xdata - x0
        dy = event.ydata - y0
        self.update_vector(x0, y0, dx, dy)
        self.update_curveFunc()
        self.start_curveAnim()
        self.start = None

    def disconnect(self):
        self.ax.figure.canvas.mpl_disconnect(self.cidPress)
        self.ax.figure.canvas.mpl_disconnect(self.cidRelease)
        self.ax.figure.canvas.mpl_disconnect(self.cidMotion)

    def update_curveField(self, _=None):
        self.stop_curve()
        self.curveField = Curve(self.s_omega_x.val, self.s_omega_y.val)
        self.update_curveFunc()
        if self.curveFunc is not None:
            self.start_curveAnim()

    def update_t(self, val):
        self.t_end = val
        self.start_curveAnim()

    def update_curveFunc(self):
        if self.vector is not None:
            self.curveFunc, maxx, maxy = self.curveField.start(*self.vector)
            curMax = self.ax.get_xlim()[1]
            newMax = max(maxx, maxy) * 1.2
            if newMax > curMax:
                self.ax.set_xlim(-newMax, newMax)
                self.ax.set_ylim(-newMax, newMax)
                self.ax2.set_xlim(-newMax, newMax)
                self.ax2.set_ylim(-newMax, newMax)

    def update_vector(self, x, y, vx, vy):
        self.vector = (x, y, vx, vy)

    def stop_curve(self, until=0):
        while len(self.anim) > until:
            self.anim.pop(0).event_source.stop()
        if len(self.anim) == 0:
            self.anim_curve.set_animated(False)

    def start_curveAnim(self):
        t_cs = np.array(range(int(self.t_end) * 1000 + 1))
        t = t_cs / 1000
        frame = t_cs[::40]
        self.anim_data = self.curveFunc(t)

        def update(current_frame):
            self.anim_curve.set_data(self.anim_data[0][:current_frame], self.anim_data[1][:current_frame])
            x = self.anim_data[0][current_frame]
            y = self.anim_data[1][current_frame]
            # minx, maxx = self.ax.get_xlim()
            # miny, maxy = self.ax.get_ylim()
            # if x < minx:
            #     self.ax.set_xlim(x - max(abs(x), 1)*0.1, maxx)
            # elif x > maxx:
            #     self.ax.set_xlim(minx, x + max(abs(x), 1)*0.3)
            # if y < miny:
            #     self.ax.set_ylim(y - max(abs(y), 1) * 0.1, maxy)
            # elif y > maxy:
            #     self.ax.set_ylim(miny, y + max(abs(y), 1) * 0.3)
            self.anim_current.set_data([x], [y])
            # if current_frame == frame[-1]:
                # self.anim_curve.set_animated(False)
                # self.ax.figure.canvas.draw()
            return self.anim_curve, self.anim_current
        self.end_curve.set_data(*self.curveFunc(t))
        self.anim_curve.set_animated(True)
        self.anim.append(FuncAnimation(self.ax.figure, update, frames=frame, interval=40, blit=True, repeat=False))
        self.stop_curve(1)

    def reset(self):
        self.stop_curve()
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax2.set_xlim(-5, 5)
        self.ax2.set_ylim(-5, 5)

#
# if __name__ == '__main__':
#     fig, ax = plt.subplots(1, 1)
#     ax.axis('equal')
#     ax.set_xlim(0, 1)
#     ax.set_ylim(0, 1)
#
#     dv = DragVector(ax, {'val': 1}, {'val': 1})
#     dv.connect()
#     plt.show()
