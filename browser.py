from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *

import os
import sys

homepage = "http://pasws.net/projects/tomatobrowser/home.html"
newtab_page = "http://google.com/"

class AboutTSDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title1 = QLabel("tomatoSoup")
        font1 = title1.font()
        font1.setPointSize(20)
        title1.setFont(font1)

        layout.addWidget(title1)

        tslogo = QLabel()
        tslogo.setPixmap(QPixmap("assets/icon/ts-icon-128.png"))
        layout.addWidget(tslogo)

        layout.addWidget(QLabel("=========== tomatoSoup ==========="))
        layout.addWidget(QLabel("VERSION_0.1.1_alpha_PRIVATE_02"))
        layout.addWidget(QLabel("By: PhilipSolo1"))
        layout.addWidget(QLabel("Copyright 2023 PhilipSolo"))
        layout.addWidget(QLabel("Licenced under the Apache Licence"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class CreditsDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(CreditsDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("tomatoBrowser Credits")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        layout.addWidget(QLabel("Created by: PhilipSolo1"))
        layout.addWidget(QLabel("Owned by: PhilipSolo1"))
        layout.addWidget(QLabel("Maintained by: PhilipSolo1"))
        layout.addWidget(QLabel("GUI library by: The Qt Company"))
        layout.addWidget(QLabel("Icons by: Yusuke Kamiyamane"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)

class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok  # No cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title1 = QLabel("tomatoBrowser")
        font1 = title1.font()
        font1.setPointSize(20)
        title1.setFont(font1)

        layout.addWidget(title1)

        logo = QLabel()
        logo.setPixmap(QPixmap("assets/icon/tb-icon-128.png"))
        layout.addWidget(logo)

        layout.addWidget(QLabel("========= tomatoBrowser ========="))
        layout.addWidget(QLabel("VERSION_1.0.0_alpha_PUBLIC_01"))
        layout.addWidget(QLabel("(alpha 1.0.0 build 01)"))
        layout.addWidget(QLabel("By: PhilipSolo1"))
        layout.addWidget(QLabel("Copyright 2023 PhilipSolo"))
        layout.addWidget(QLabel("Licenced under the Apache Licence"))
        layout.addWidget(QLabel("Used under permission by owner"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon("assets/btn/back.png"), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon("assets/btn/forward.png"), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        navtb.addSeparator()

        reload_btn = QAction(QIcon("assets/btn/reload.png"), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        stop_btn = QAction(QIcon("assets/btn/stop-loading.png"), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)

        navtb.addSeparator()

        home_btn = QAction(QIcon("assets/btn/home.png"), "Home", self)
        home_btn.setStatusTip("Go to the homepage")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap("assets/btn/no-ssl.png"))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        file_menu = self.menuBar().addMenu("&File")

        new_tab_action = QAction(QIcon("assets/btn/new-tab.png"), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda _: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon("assets/btn/open-page.png"), "Open file...", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon("assets/btn/save-page.png"), "Save Page As...", self)
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(QIcon("assets/btn/print.png"), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        info_menu = self.menuBar().addMenu("&Info")

        about_action = QAction(QIcon("assets/btn/about.png"), "About tomatoBrowser", self)
        about_action.setStatusTip("Find out more about tomatoBrowser")
        about_action.triggered.connect(self.about)
        info_menu.addAction(about_action)

        about_action = QAction(QIcon("assets/btn/about.png"), "About tomatoSoup //not working yet", self)
        about_action.setStatusTip("Find out more about tomatoSoup")
        about_action.triggered.connect(self.aboutTS)
        info_menu.addAction(about_action)

        about_action = QAction(QIcon("assets/btn/about.png"), "Credits", self)
        about_action.setStatusTip("Credits for tomatoBrowser")
        about_action.triggered.connect(self.credits)
        info_menu.addAction(about_action)

        navigate_help_action = QAction(QIcon("assets/btn/help.png"),
                                       "tomatoBrowser Help page", self)
        navigate_help_action.setStatusTip("Go to the tomatoBrowser Help page")
        navigate_help_action.triggered.connect(self.navigate_help)
        info_menu.addAction(navigate_help_action)

        self.add_new_tab(QUrl(homepage), "Homepage")

        self.resize(QSize(500, 500))
        self.show()

        self.setWindowTitle("tomatoBrowser")
        self.setWindowIcon(QIcon("assets/icon/tb-icon-32.png"))

    def add_new_tab(self, qurl=None, label="Blank"):

        if qurl is None:
            qurl = QUrl(newtab_page)

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:  # No tab under the click
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        q = QUrl(self.urlbar.text())
        q = ""
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(f"{title} - tomatoBrowser")

    def navigate_help(self):
        self.tabs.currentWidget().setUrl(QUrl("http://pasws.net/projects/tomatobrowser/help.html"))

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def credits(self):
        dlg = CreditsDialog()
        dlg.exec_()

    def aboutTS(self):
        dlg = AboutTSDialog()
        dlg.exec_()

    #def settings(self):
    #    dlg = SettingsDialog()
    #    dlg.exec_()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file as website", "", "Hypertext Markup Language (*.htm *.html);;" "All files (*.*)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save website as HTML file", "",
                                                  "Hypertext Markup Language (*.htm *html);;"
                                                  "All files (*.*)")

        if filename:
            html = self.tabs.currentWidget().page().toHtml()
            with open(filename, 'w') as f:
                f.write(html.encode('utf8'))

    def print_page(self):
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.browser.print_)
        dlg.exec_()

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl(homepage))

    def navigate_to_url(self):  # Does not receive the Url
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):

        if not browser.isActiveWindow():
            browser.update()

        if browser != self.tabs.currentWidget():
            return

        if q.scheme() == 'https':
            # secure security icon
            self.httpsicon.setPixmap(QPixmap("assets/btn/ssl.png"))
        elif q.scheme() == 'http':
            # unsecure security icon
            self.httpsicon.setPixmap(QPixmap("assets/btn/no-ssl.png"))
        else:
            # unknown security icon
            self.httpsicon.setPixmap(QPixmap("assets/btn/unknow-ssl.png"))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


app = QApplication(sys.argv)
app.setApplicationName("tomatoBrowser")
app.setOrganizationName("PASWS.net Organization")
app.setOrganizationDomain("pasws.net")

window = MainWindow()

app.exec_()
