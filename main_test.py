import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QDesktopWidget,
    QPushButton,
    QGridLayout,
    QMessageBox
)


class MainWindow(QWidget):
    # 初始化类
    def __init__(self, winOption):
        super().__init__()
        self.initGUI(winOption)

    # 初始化显示
    def initGUI(self, winOption):
        self.resize(*winOption['size'])
        self.setWindowTitle(winOption['title'])
        self.center()

        grid = QGridLayout()
        grid.setSpacing(2)
        btnOne = self.addButton({
            'name': 'btn1',
            'size': (200, 100),
            'position': (0, 0)
        }, grid)
        btnTwo = self.addButton({
            'name': 'btn2',
            'size': (200, 100),
            'position': (1, 0)
        }, grid)
        self.setLayout(grid)
        self.show()

    # 窗口显示在屏幕中心
    def center(self):
        qr = self.frameGeometry()  # 获得窗口
        cp = QDesktopWidget().availableGeometry().center()  # 获得屏幕中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # 添加按钮
    def addButton(self, btnOption, grid):
        btn = QPushButton(btnOption['name'], self)
        btn.resize(*btnOption['size'])
        grid.addWidget(btn, *btnOption['position'])
        return btn

    # 关闭窗口
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            '提醒',
            "确认退出?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    winOption = {
        'size': (400, 300),
        'title': '主窗口',
    }
    win = MainWindow(winOption)
    sys.exit(app.exec_())
