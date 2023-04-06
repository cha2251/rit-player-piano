import os

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout

from src.user_interface.DragButton import DragButton


class IconsList(QHBoxLayout):
    tool = """
        QToolButton {
            color: transparent;
            background-color: transparent;
            border-color: transparent;
            max-width: 3em;
            min-width: 3em;
            font: 25px;
            padding: 5px;
            font-family: "Times New Roman", Times, serif;
        }
        """

    def __init__(self):
        super().__init__()

        arrow_up = DragButton("button-arrow-up")
        arrow_up.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-arrow-up.svg")))
        arrow_up.setStyleSheet(self.tool)
        arrow_up.setIconSize(QSize(60, 60))
        self.addWidget(arrow_up)

        # The down arrow and left arrow have been commented out because
        # up and down cannot be pressed at the same time and left and
        # right cannot be played at the same time either so we decided
        # to remove them so the user cannot account this problem
        ## arrow_down = DragButton("button-arrow-down")
        ## arrow_down.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-arrow-down.svg")))
        ## arrow_down.setStyleSheet(tool)
        ## arrow_down.setIconSize(QSize(60, 60))
        ## iconsList.addWidget(arrow_down)

        ## arrow_left = DragButton("button-arrow-left")
        ## arrow_left.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-arrow-left.svg")))
        ## arrow_left.setStyleSheet(tool)
        ## arrow_left.setIconSize(QSize(60, 50))
        ## iconsList.addWidget(arrow_left)

        arrow_right = DragButton("button-arrow-right")
        arrow_right.setIcon(QIcon(
            os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-arrow-right.svg")))
        arrow_right.setStyleSheet(self.tool)
        arrow_right.setIconSize(QSize(60, 50))
        self.addWidget(arrow_right)

        A = DragButton("button-A")
        A.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-A.svg")))
        A.setStyleSheet(self.tool)
        A.setIconSize(QSize(60, 50))
        self.addWidget(A)

        B = DragButton("button-B")
        B.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-B.svg")))
        B.setStyleSheet(self.tool)
        B.setIconSize(QSize(60, 50))
        self.addWidget(B)

        X = DragButton("button-X")
        X.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-X.svg")))
        X.setStyleSheet(self.tool)
        X.setIconSize(QSize(60, 50))
        self.addWidget(X)

        Y = DragButton("button-Y")
        Y.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-Y.svg")))
        Y.setStyleSheet(self.tool)
        Y.setIconSize(QSize(60, 50))
        self.addWidget(Y)

        RB = DragButton("button-RB")
        RB.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-RB.svg")))
        RB.setStyleSheet(self.tool)
        RB.setIconSize(QSize(60, 50))
        self.addWidget(RB)

        LB = DragButton("button-LB")
        LB.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-LB.svg")))
        LB.setStyleSheet(self.tool)
        LB.setIconSize(QSize(60, 50))
        self.addWidget(LB)

        RT = DragButton("button-RT")
        RT.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-RT.svg")))
        RT.setStyleSheet(self.tool)
        RT.setIconSize(QSize(60, 50))
        self.addWidget(RT)

        LT = DragButton("button-LT")
        LT.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-LT.svg")))
        LT.setStyleSheet(self.tool)
        LT.setIconSize(QSize(60, 50))
        self.addWidget(LT)

        LS = DragButton("button-LS")
        LS.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-LS.svg")))
        LS.setStyleSheet(self.tool)
        LS.setIconSize(QSize(60, 50))
        self.addWidget(LS)

        RS = DragButton("button-RS")
        RS.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-RS.svg")))
        RS.setStyleSheet(self.tool)
        RS.setIconSize(QSize(60, 50))
        self.addWidget(RS)

        select = DragButton("button-Select")
        select.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-select.svg")))
        select.setStyleSheet(self.tool)
        select.setIconSize(QSize(60, 50))
        self.addWidget(select)

        start = DragButton("button-start")
        start.setIcon(
            QIcon(os.path.join(os.path.dirname(__file__), "..", "..", "UI_Images", "settings", "button-start.svg")))
        start.setStyleSheet(self.tool)
        start.setIconSize(QSize(60, 50))
        self.addWidget(start)
