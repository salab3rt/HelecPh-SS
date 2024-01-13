import keyboard
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5 import QtGui
from helpers.screenshot import take_screenshot_and_modify, serialized_icon



def exit_application():
    app.quit()

# Create an application and a system tray icon
app = QApplication([])
tray_icon = QSystemTrayIcon()
app.setQuitOnLastWindowClosed(False)

# Create a context menu for the system tray icon
context_menu = QMenu()

# Add a 'Take Screenshot' action to the menu
take_screenshot_action = QAction('Take Screenshot', triggered=take_screenshot_and_modify)
context_menu.addAction(take_screenshot_action)

# Add an 'Exit' action to the menu
exit_action = QAction('Exit', triggered=exit_application)
context_menu.addAction(exit_action)

# Set the context menu for the system tray icon
tray_icon.setContextMenu(context_menu)

# Register the keyboard shortcut for taking a screenshot
keyboard.add_hotkey("ctrl+space", take_screenshot_and_modify)

# Register the keyboard shortcut for exiting
keyboard.add_hotkey("ctrl+alt+e", exit_application)

# Load the icon image

# Serialize the icon image

# Set the icon for the system tray
tray_icon.setIcon(QtGui.QIcon(QtGui.QPixmap.fromImage(QtGui.QImage.fromData(serialized_icon))))
tray_icon.setVisible(True)

# Run the application
app.exec_()
