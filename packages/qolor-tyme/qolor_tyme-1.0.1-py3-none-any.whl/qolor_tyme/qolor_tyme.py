#  Qolor Tyme - a Toastmaters-inspired speech timer for online scrum meetings.
#  Copyright (C) 2021 Tromgy (tromgy@yahoo.com)
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer

class _QolorRect(QtWidgets.QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.MinimumExpanding,
            QtWidgets.QSizePolicy.MinimumExpanding
        )

        self._padding = 5 # pixels

        # canvas color
        self._bg_color = QtGui.QColor('gray')

    def sizeHint(self):
        return QtCore.QSize(40, 120)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        painter = QtGui.QPainter(self)
        brush = QtGui.QBrush()
        
        brush.setColor(self._bg_color)
        brush.setStyle(Qt.SolidPattern)

        rect = QtCore.QRect(0, 0, painter.device().width(), painter.device().height())
        painter.fillRect(rect, brush)

        painter.end()

    def _trigger_refresh(self):
        self.update()

class QolorTymeDisplay(QtWidgets.QWidget):

    def __init__(self, total_count = 90, time_warning = 20, time_alarm = 5, time_critical = 0, *args, **kwargs):
        super(QolorTymeDisplay, self).__init__(*args, **kwargs)

        self.setWindowTitle('Qolor Tyme')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self._total_count = total_count
        self._time_warning = time_warning
        self._time_alarm = time_alarm
        self._time_critical = time_critical

        self._count = self._total_count

        layout = QtWidgets.QVBoxLayout()
        self._rect = _QolorRect()
        layout.addWidget(self._rect)

        self._time = QtWidgets.QLabel()
        self._time.setFont(QtGui.QFont('Courier New', 18, 75))
        self._time.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._time)

        self._update_label()

        self._start = QtWidgets.QPushButton('Start')
        self._start.pressed.connect(self._start_timer)
        layout.addWidget(self._start)

        self._pause = QtWidgets.QPushButton('Pause')
        self._pause.pressed.connect(self._pause_timer)
        self._pause.setEnabled(False)
        layout.addWidget(self._pause)
        self._paused = False

        self._stop = QtWidgets.QPushButton('Stop')
        self._stop.pressed.connect(self._stop_timer)
        self._stop.setEnabled(False)
        layout.addWidget(self._stop)
        
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_timer)
        
        self.setLayout(layout)

    def _update_label(self):
        minutes = int(self._count) // 60
        seconds = int(self._count) % 60

        self._time.setText('{:02d}:{:02d}'.format(minutes, seconds))

    def _update_pause_label(self, paused):
        if paused:
            self._pause.setText('Resume')
        else:
            self._pause.setText('Pause')
        
        self._paused = paused

    def _start_timer(self):
        self._update_pause_label(False)
        self._count = self._total_count
        self._update_label()
        self._timer.start(500)  # 2 times a second for better flash
        self.set_color('green')
        self._pause.setEnabled(True)
        self._stop.setEnabled(True)

    def _pause_timer(self):
        self._paused = not self._paused

        self._update_pause_label(self._paused)
        
        if self._paused:
            self._timer.stop()
        else:
            self._timer.start(500)

    def _stop_timer(self):
        self._timer.stop()
        self._count = self._total_count
        self._update_label()
        self._update_pause_label(False)
        self.set_color('gray')
        self._pause.setEnabled(False)
        self._stop.setEnabled(False)

    def _update_timer(self):
        self._count -= 0.5 # Updates come twice every second
        
        if self._count >= 0:
            self._update_label()

        if self._count <= self._time_critical:
            if self._count == int(self._count):
                self.set_color('black')
            else:
                self.set_color('red')
        elif self._count < self._time_alarm:
            self.set_color('red')
        elif self._count < self._time_warning:
            self.set_color('yellow')

    def set_color(self, color):
        self._rect._bg_color = QtGui.QColor(color)
        self._rect.update()
