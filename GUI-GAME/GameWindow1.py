import sys
from enum import IntEnum
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from AIshow import AIshow
import copy
import Astar
import GameWindowChoose
import MainWindow


# 方向
class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

# 简单游戏3X3游戏
class GameWindow1(QMainWindow):

    def __init__(self):
        super().__init__()
        # 设置背景图片
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('bg.JPG')))
        self.setPalette(palette)
        # 状态数组
        self.blocks = []
        # 空白格位置
        self.zero_row = 0
        self.zero_column = 0
        # 数字块网格布局
        self.gltMain = QGridLayout()
        self.initUI()
        # self.button1 = QPushButton('AI演示')
        # self.button2 = QPushButton('重开本局')
        # self.button2.clicked.connect(self.onInit)

    def initUI(self):
        # 设置方块间隔
        self.gltMain.setSpacing(10)
        self.onInit()
        # 设置布局
        mainframe = QWidget()
        mainframe.setLayout(self.gltMain)
        self.setCentralWidget(mainframe)
        # self.setLayout(self.gltMain)

        # 设置宽和高
        self.setFixedSize(600, 600)
        self.setWindowTitle('简单模式-3X3')
        self.setWindowModality(Qt.ApplicationModal)
        # 设置背景颜色
        # self.setStyleSheet("background-color:gray;")
        # self.show()

        # 工具栏
        toolbar1 = self.addToolBar('更换题目')
        new = QAction(QIcon('exchangerate.png'), '更换题目', self)
        toolbar1.addAction(new)
        toolbar1.actionTriggered.connect(self.restart)
        toolbar1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        toolbar2 = self.addToolBar('AI演示')
        new = QAction(QIcon('quick.png'), 'AI演示', self)
        toolbar2.addAction(new)
        toolbar2.actionTriggered.connect(self.AIshow)
        toolbar2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        toolbar3 = self.addToolBar('返回')
        new = QAction(QIcon('home.png'), '返回', self)
        toolbar3.addAction(new)
        toolbar3.actionTriggered.connect(self.back)
        toolbar3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    # 返回功能
    def back(self):
        self.hide()
        self.father = MainWindow.MainWindow()
        self.father.show()

    # 重新开始功能
    def restart(self):
        self.blocks = []
        self.zero_row = 0
        self.zero_column = 0
        self.onInit()

    # AI演示功能
    def AIshow(self):
        # 将状态数组、空白快位置拷贝到temp变量
        temp1 = copy.deepcopy(self.blocks)
        temp2 = copy.deepcopy(self.zero_row)
        temp3 = copy.deepcopy(self.zero_column)
        list = []
        for i in range(3):
            for j in range(3):
                list.append(temp1[i][j])
        print(temp1)
        print(temp2)
        print(temp3)
        # 调用A*算法
        walklist = Astar.bfsHash(list, temp2, temp3, 3)
        print('walklist:', walklist)
        temp4 = copy.deepcopy(walklist)
        self.ai_show = AIshow(temp1, temp2, temp3, 3, temp4)
        self.ai_show.show()
        # print(self.blocks)
        # print(self.zero_row)
        # print(self.zero_column)

    # 初始化布局
    def onInit(self):
        # 产生顺序数组
        self.numbers = list(range(1, 9))
        self.numbers.append(0)
        # 将数字添加到二维数组
        for row in range(3):
            self.blocks.append([])
            for column in range(3):
                temp = self.numbers[row * 3 + column]
                if temp == 0:
                    self.zero_row = row
                    self.zero_column = column
                self.blocks[row].append(temp)
        # 打乱数组
        for i in range(500):
            random_num = random.randint(0, 3)
            self.move(Direction(random_num))
        self.updatePanel()

    # 检测按键
    def keyPressEvent(self, event):
        # print(self.blocks)
        # print(self.zero_row)
        # print(self.zero_column)
        key = event.key()
        if (key == Qt.Key_Up or key == Qt.Key_W):
            self.move(Direction.UP)
        if (key == Qt.Key_Down or key == Qt.Key_S):
            self.move(Direction.DOWN)
        if (key == Qt.Key_Left or key == Qt.Key_A):
            self.move(Direction.LEFT)
        if (key == Qt.Key_Right or key == Qt.Key_D):
            self.move(Direction.RIGHT)
        self.updatePanel()
        # print(self.blocks)
        # print(self.zero_column)
        # print(self.zero_row)
        if self.checkResult():
            if QMessageBox.Ok == QMessageBox.information(self, '挑战结果', '恭喜您完成挑战！'):
                self.onInit()

    # 方块移动算法
    def move(self, direction):
        if (direction == Direction.UP):  # 上
            if self.zero_row != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row + 1][self.zero_column]
                self.blocks[self.zero_row + 1][self.zero_column] = 0
                self.zero_row += 1
        if (direction == Direction.DOWN):  # 下
            if self.zero_row != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row - 1][self.zero_column]
                self.blocks[self.zero_row - 1][self.zero_column] = 0
                self.zero_row -= 1
        if (direction == Direction.LEFT):  # 左
            if self.zero_column != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column + 1]
                self.blocks[self.zero_row][self.zero_column + 1] = 0
                self.zero_column += 1
        if (direction == Direction.RIGHT):  # 右
            if self.zero_column != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column - 1]
                self.blocks[self.zero_row][self.zero_column - 1] = 0
                self.zero_column -= 1

    # 刷新面板
    def updatePanel(self):
        for row in range(3):
            for column in range(3):
                self.gltMain.addWidget(Block(self.blocks[row][column]), row, column)
        self.setLayout(self.gltMain)

    # 检测是否完成
    def checkResult(self):
        # 先检测最右下角是否为0
        if self.blocks[2][2] != 0:
            return False

        for row in range(3):
            for column in range(3):
                # 运行到此处说明最右下角已经为0，pass即可
                if row == 2 and column == 2:
                    pass
                # 值是否对应
                elif self.blocks[row][column] != row * 3 + column + 1:
                    return False

        return True

    # 监听关闭事件
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出游戏', '你确定退出游戏吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class Block(QLabel):
    """ 数字方块 """

    def __init__(self, number):
        super().__init__()

        self.number = number
        self.setFixedSize(80, 80)

        # 设置字体
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.setFont(font)

        # 设置字体颜色
        pa = QPalette()
        pa.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(pa)

        # 设置文字位置
        self.setAlignment(Qt.AlignCenter)

        # 设置背景颜色\圆角和文本内容
        if self.number == 0:
            self.setStyleSheet("background-color:white;border-radius:10px;")
        else:
            self.setStyleSheet("background-color:#000000;border-radius:10px;")
            self.setText(str(self.number))
