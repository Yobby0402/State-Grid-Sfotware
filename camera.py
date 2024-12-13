# -*- coding: utf-8 -*-
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        layout = QVBoxLayout(self)
        self.axWidget = QAxWidget('Word.Applicatio', self)
        layout.addWidget(self.axWidget)
        layout.addWidget(QPushButton('打开word', self, clicked=self.onOpenWord))

    def onOpenWord(self):
        path, _ = QFileDialog.getOpenFileName(
            self, '请选择Word文件', '', 'word(*.docx *.doc)')
        if not path:
            return
        # 不显示窗体
        self.axWidget.dynamicCall('SetVisible (bool Visible)', 'false')
        self.axWidget.setProperty('DisplayAlerts', False)
        self.axWidget.setControl(path)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())