# PDF Filler.py
#
# Copyright (C) 2025 Bennett Steers
#
# This file forms part of the PDF Filler Tool
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Runs the PDF Editor with the user interface

import traceback
from src.errorHandling import fatalError

try:
    import os
    from src.userInterface import *
    import src.PDFFiller as PDFFiller

    # Get the absolute path of the directory containing the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Change the current working directory to the script's directory
    os.chdir(script_dir)

    #Only runs program if the UI subroutine returns TRUE when it is closed
    if userInterface():
        PDFFiller.run()

except Exception as error:
    with open('log.txt', 'w') as f:
        f.write(traceback.format_exc())
    fatalError(999,traceback.format_exc())