import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import QTimer, Qt  # Import Qt from PyQt5.QtCore
from PyQt5.QtGui import QPixmap

app = QApplication(sys.argv)

# Load the image for the splash screen
splash_pix = QPixmap('splash_image.png')  # Replace with your image path
splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
splash.setFixedSize(splash_pix.size())  # Set the size to the image size
splash.show()

# Close the splash screen and proceed after 5 seconds
QTimer.singleShot(5000, splash.close)

# Start the application (this is just to keep the app running)
sys.exit(app.exec_())
