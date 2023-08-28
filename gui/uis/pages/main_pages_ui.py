# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_pages.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QSizePolicy,
    QStackedWidget, QVBoxLayout, QWidget)

class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(860, 600)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1.setStyleSheet(u"font-size: 14pt;\n"
"background: #44475a;")
        self.page_1_layout = QVBoxLayout(self.page_1)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName(u"page_1_layout")
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)
        self.pages.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setStyleSheet(u"background: #44475a;")
        self.page_2_layout = QVBoxLayout(self.page_2)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.frame = QFrame(self.page_2)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 150))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        self.frame.setFont(font)
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.file_browser_layout = QHBoxLayout(self.frame)
        self.file_browser_layout.setSpacing(0)
        self.file_browser_layout.setObjectName(u"file_browser_layout")
        self.file_browser_layout.setContentsMargins(50, 20, 50, 20)

        self.page_2_layout.addWidget(self.frame)

        self.frame_2 = QFrame(self.page_2)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.table_layout = QHBoxLayout(self.frame_2)
        self.table_layout.setSpacing(0)
        self.table_layout.setObjectName(u"table_layout")
        self.table_layout.setContentsMargins(50, 0, 50, 20)

        self.page_2_layout.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.page_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 100))
        self.frame_3.setMaximumSize(QSize(16777215, 100))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.analysis_btn_layout = QHBoxLayout(self.frame_3)
        self.analysis_btn_layout.setSpacing(0)
        self.analysis_btn_layout.setObjectName(u"analysis_btn_layout")
        self.analysis_btn_layout.setContentsMargins(0, 0, 0, 0)

        self.page_2_layout.addWidget(self.frame_3)

        self.pages.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setStyleSheet(u"background: #44475a;\n"
"\n"
"QFrame {\n"
"	font-size: 16pt;\n"
"}")
        self.page_3_layout = QVBoxLayout(self.page_3)
        self.page_3_layout.setObjectName(u"page_3_layout")
        self.page_3_pages = QStackedWidget(self.page_3)
        self.page_3_pages.setObjectName(u"page_3_pages")
        self.no_videos_page = QWidget()
        self.no_videos_page.setObjectName(u"no_videos_page")
        self.horizontalLayout = QHBoxLayout(self.no_videos_page)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.no_videos_page)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.no_videos_layout = QVBoxLayout(self.frame_4)
        self.no_videos_layout.setObjectName(u"no_videos_layout")
        self.no_videos_layout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.addWidget(self.frame_4)

        self.page_3_pages.addWidget(self.no_videos_page)
        self.videos_page = QWidget()
        self.videos_page.setObjectName(u"videos_page")
        self.verticalLayout = QVBoxLayout(self.videos_page)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.videos_page)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMaximumSize(QSize(16777215, 200))
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.percentage_layout = QHBoxLayout(self.frame_5)
        self.percentage_layout.setSpacing(0)
        self.percentage_layout.setObjectName(u"percentage_layout")
        self.percentage_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.frame_5)

        self.frame_6 = QFrame(self.videos_page)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.results_table_layout = QHBoxLayout(self.frame_6)
        self.results_table_layout.setSpacing(0)
        self.results_table_layout.setObjectName(u"results_table_layout")
        self.results_table_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.frame_6)

        self.page_3_pages.addWidget(self.videos_page)

        self.page_3_layout.addWidget(self.page_3_pages)

        self.pages.addWidget(self.page_3)

        self.main_pages_layout.addWidget(self.pages)


        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(2)
        self.page_3_pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
    # retranslateUi

