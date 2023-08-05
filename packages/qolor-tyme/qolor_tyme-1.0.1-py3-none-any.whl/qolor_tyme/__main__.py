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

import sys
from PyQt5 import QtWidgets
from .qolor_tyme import QolorTymeDisplay

def main():
    app = QtWidgets.QApplication([])

    display = None

    if len(sys.argv) > 1:
        display = QolorTymeDisplay(total_count = int(sys.argv[1]))
    else:
        display = QolorTymeDisplay()

    display.show()
    app.exec_()

if __name__ == "__main__":
    main()