# importing required libraries
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtPrintSupport import *
import os
import sys
import subprocess

# Custom QWebEngineView to handle target="_blank"
class CustomWebEngineView(QWebEngineView):
    def createWindow(self, _type):
        # Create a new tab in the main window
        new_tab = CustomWebEngineView()
        window.add_new_tab(label="New Tab")  # Add a new tab with a placeholder label
        # Get the newly created tab's browser widget
        browser = window.tabs.currentWidget()
        return browser  # Return the browser widget to load the new URL

# Main window
class MainWindow(QMainWindow):
    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.resize(1280, 720)

        # creating a tab widget
        self.tabs = QTabWidget()

        # making document mode true
        self.tabs.setDocumentMode(True)

        # adding action when double clicked
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)

        # adding action when tab is changed
        self.tabs.currentChanged.connect(self.current_tab_changed)

        # making tabs closeable
        self.tabs.setTabsClosable(True)

        # adding action when tab close is requested
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        # creating a sidebar
        self.sidebar = QWidget()
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)

        # creating another text view
        self.text_view = QTextEdit()
        self.text_view.setReadOnly(True)
        self.text_view.setPlaceholderText("Text view area")

        # creating buttons for sidebar
        self.run_first_btn = QPushButton("Run first.py")
        self.run_second_btn = QPushButton("Run second.py")
        self.run_third_btn = QPushButton("Run third.py")
        self.run_fourth_btn = QPushButton("Run fourth.py")
        self.run_fifth_btn = QPushButton("Run fifth.py")
        self.run_sixth_btn = QPushButton("Run sixth.py")

        # creating a text field
        self.text_field = QLineEdit()
        self.text_field.setPlaceholderText("Enter text here")

        # creating a grid layout for buttons
        self.button_grid = QGridLayout()
        self.button_grid.addWidget(self.run_first_btn, 0, 0)
        self.button_grid.addWidget(self.run_second_btn, 0, 1)
        self.button_grid.addWidget(self.run_third_btn, 0, 2)
        self.button_grid.addWidget(self.run_fourth_btn, 1, 0)
        self.button_grid.addWidget(self.run_fifth_btn, 1, 1)
        self.button_grid.addWidget(self.run_sixth_btn, 1, 2)

        # adding the grid layout to the sidebar layout
        self.sidebar_layout.addLayout(self.button_grid)

        # adding the text field to the sidebar layout
        self.sidebar_layout.addWidget(self.text_field)

        # adding the text view to the sidebar layout
        self.sidebar_layout.addWidget(self.text_view)

        # connecting buttons to actions
        self.run_first_btn.clicked.connect(self.run_first_script)
        self.run_second_btn.clicked.connect(self.run_second_script)
        self.run_third_btn.clicked.connect(self.run_third_script)
        self.run_fourth_btn.clicked.connect(self.run_fourth_script)
        self.run_fifth_btn.clicked.connect(self.run_fifth_script)
        self.run_sixth_btn.clicked.connect(self.run_sixth_script)

        # creating a main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.sidebar, 1)
        self.main_layout.addWidget(self.tabs, 4)

        # creating a central widget
        self.central_widget = QWidget()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # creating a status bar
        self.status = QStatusBar()

        # setting status bar to the main window
        self.setStatusBar(self.status)

        # creating a tool bar for navigation
        navtb = QToolBar("Navigation")

        # adding tool bar to the main window
        self.addToolBar(navtb)

        # creating back action
        back_btn = QAction("<", self)

        # setting status tip
        back_btn.setStatusTip("Back to previous page")

        # adding action to back button
        # making current tab to go back
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

        # adding this to the navigation tool bar
        navtb.addAction(back_btn)

        # similarly adding next button
        next_btn = QAction(">", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        # similarly adding reload button
        reload_btn = QAction("@", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        # creating home action
        home_btn = QAction("H", self)
        home_btn.setStatusTip("Go home")

        # adding action to home button
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        save_btn = QAction("S", self)
        save_btn.setStatusTip("Save page")
        save_btn.triggered.connect(self.save_current_page)
        navtb.addAction(save_btn)

        # adding a separator
        navtb.addSeparator()

        # creating a line edit widget for URL
        self.urlbar = QLineEdit()

        # adding action to line edit when return key is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        # adding line edit to tool bar
        navtb.addWidget(self.urlbar)

        # similarly adding stop action
        stop_btn = QAction("X", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        # similarly adding go action
        go_btn = QAction("Go", self)
        go_btn.setStatusTip("Go loading current page")
        navtb.addAction(go_btn)
        go_btn.triggered.connect(self.navigate_to_url)

        # creating first tab
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        # showing all the components
        self.show()

        # setting window title
        self.setWindowTitle("Pervisor - journal of titles")

    def save_current_page(self):
        # Get the current browser widget
        browser = self.tabs.currentWidget()

        browser.page().toHtml(lambda html: self.save_html_to_file(html, "data/page.html"))

    def save_html_to_file(self, html, file_name):
        # Write the HTML content to the file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(html)

        # Show a message box to inform the user
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Save Complete")
        msg_box.setText(f"Page saved to {file_name}")
        msg_box.open()
        QTimer.singleShot(3000, msg_box.close)

    # method for adding new tab
    def add_new_tab(self, qurl=None, label="Blank"):
        # if url is blank
        if qurl is None:
            # creating a google url
            qurl = QUrl('http://www.google.com')

        # creating a CustomWebEngineView object
        browser = CustomWebEngineView()

        # setting url to browser
        browser.setUrl(qurl)

        # setting tab index
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # adding action to the browser when url is changed
        # update the url
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        # adding action to the browser when loading is finished
        # set the tab title
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()[:16]))

    # when double clicked is pressed on tabs
    def tab_open_doubleclick(self, i):
        # checking index i.e
        # No tab under the click
        if i == -1:
            # creating a new tab
            self.add_new_tab()

    # when tab is changed
    def current_tab_changed(self, i):
        # get the curl
        qurl = self.tabs.currentWidget().url()

        # update the url
        self.update_urlbar(qurl, self.tabs.currentWidget())

        # update the title
        self.update_title(self.tabs.currentWidget())

    # when tab is closed
    def close_current_tab(self, i):
        # if there is only one tab
        if self.tabs.count() < 2:
            # do nothing
            return

        # else remove the tab
        self.tabs.removeTab(i)

    # method for updating the title
    def update_title(self, browser):
        # if signal is not from the current tab
        if browser != self.tabs.currentWidget():
            # do nothing
            return

        # get the page title
        title = self.tabs.currentWidget().page().title()

        # set the window title
        self.setWindowTitle("% s - Pervisor" % title)

    # action to go to home
    def navigate_home(self):
        # go to google
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    # method for navigate to url
    def navigate_to_url(self):
        # get the line edit text
        # convert it to QUrl object
        q = QUrl(self.urlbar.text())

        # if scheme is blank
        if q.scheme() == "":
            # set scheme
            q.setScheme("http")

        # set the url
        self.tabs.currentWidget().setUrl(q)

    # method to update the url
    def update_urlbar(self, q, browser=None):
        # If this signal is not from the current tab, ignore
        if browser != self.tabs.currentWidget():
            return

        # set text to the url bar
        self.urlbar.setText(q.toString())

        # set cursor position
        self.urlbar.setCursorPosition(0)

    # method to run first.py
    def run_first_script(self):
        try:
            subprocess.run(["python", "first.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running first.py: {e}")

    # method to run second.py
    def run_second_script(self):
        try:
            subprocess.run(["python", "second.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running second.py: {e}")

    # method to run third.py
    def run_third_script(self):
        try:
            subprocess.run(["python", "third.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running third.py: {e}")

    # method to run fourth.py
    def run_fourth_script(self):
        try:
            subprocess.run(["python", "fourth.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running fourth.py: {e}")

    # method to run fifth.py
    def run_fifth_script(self):
        try:
            subprocess.run(["python", "fifth.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running fifth.py: {e}")

    # method to run sixth.py
    def run_sixth_script(self):
        try:
            subprocess.run(["python", "sixth.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running sixth.py: {e}")

# creating a PyQt6 application
app = QApplication(sys.argv)

# creating MainWindow object
window = MainWindow()

# loop
app.exec()