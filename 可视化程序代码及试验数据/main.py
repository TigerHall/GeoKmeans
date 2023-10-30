# 导入pyqt6模块
import os
import sys
import time
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton, QGraphicsView, QInputDialog, QGraphicsScene, QLabel, QFileDialog, QTextEdit, QTableWidget, QTableWidgetItem, QVBoxLayout, QMessageBox)
from PyQt6.QtGui import QPixmap, QIcon,QGuiApplication
from PyQt6.QtCore import Qt
from KmeansCSV import kmeanscsv ,lkxscsv

# 创建一个窗口类
class Window(QWidget):
    def __init__(self):
        super().__init__()
        # 设置窗口标题和大小
        self.setWindowTitle("GeoKmeans-地化数据聚类分析小软件")
        self.setWindowIcon(QIcon('../pic/jl.ico'))
        # 创建两个按钮
        self.button1 = QPushButton("读取csv", self)
        self.button2 = QPushButton("聚类计算", self)
        self.button3 = QPushButton("轮廓系数", self)
        # 按钮提示
        self.button1.setToolTip('请添加除了表头外其余为 <b>纯数据的CSV</b> 文件')
        self.button2.setToolTip('将会输出聚类结果在<b>CSV</b>文件旁, 请注意查看!')
        self.button3.setToolTip('将会输出轮廓系数和SSE在<b>CSV</b>文件旁, 请注意查看!')
        # 设置按钮的位置和大小
        btnw=100
        btnh=40
        self.button1.setGeometry(20, 20, btnw, btnh)
        self.button2.setGeometry(20, 70, btnw, btnh)
        self.button3.setGeometry(20, 120, btnw, btnh)
        # 绑定按钮的点击事件
        self.button1.clicked.connect(self.select_csv)
        self.button2.clicked.connect(self.jlsf)
        self.button3.clicked.connect(self.lkss)
        # 创建一个标签，用于存储文件名
        self.label = QLabel("0", self)
        # 设置标签的位置和大小
        self.label.setGeometry(0, 0, 0, 0)
        # 隐藏标签
        self.label.hide()
        # 创建一个文本编辑框，用来显示文件信息
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.move(140, 20)
        self.text_edit.resize(400, 200)
        # 一个图形框来显示成图
        self.scene = QGraphicsScene()
        self.scene.addText('图形界面')

    # 定义一个选择csv文件的方法
    def select_csv(self):
        # 弹出一个文件对话框，让用户选择csv文件，返回文件名和过滤器
        filename, filter = QFileDialog.getOpenFileName(self, "选择csv文件", "", "CSV files (*.csv)")
        # 如果文件名不为空，则尝试读取csv文件，如果成功则弹出一个消息框提示成功，否则弹出一个消息框提示失败，并返回上一个窗口
        if filename:
            try:
                # 读取csv文件
                df = pd.read_csv(filename)
                # 判断数据中是否存在非数字存在(找出对应列)
                if 'object' in str(df.dtypes.value_counts()):
                    baddata = df.select_dtypes(include=object)
                    baddata.index.name='IndexID'
                    baddata.to_csv(f'{filename}_存在字符串(空格)的数据列.csv', index=True, header=True)
                    os.startfile(f'{filename}_存在字符串(空格)的数据列.csv')
                    self.text_edit.setText(f'{filename}数据中\n\n有字符数据存在,请检查生成的字符串数据列文件!!!')
                    self.label.setText('0')
                # 判断数据中是否含空值并输出含空值的数据行
                elif 'True' in str(df.isnull().any()):
                    emp = df[df.isnull().values==True]
                    emp.index.name='IndexID'
                    emp.fillna(value='NaN').to_csv(f'{filename}_空值数据行情况.csv',index=True,header=True)
                    os.startfile(f'{filename}_空值数据行情况.csv')
                    self.text_edit.setText(f'{filename}数据中\n\n有空值数据行存在,请检查生成的空值数据行文件!!!')
                    self.label.setText('0')
                else:
                    self.text_edit.setText(f"已成功读取{filename}文件:\n\n聚类维度包含:\n{str(list(df.columns))}\n")
                    # 将文件名存储在标签上，并显示标签
                    self.label.setText(filename)
                    self.label.show()
            except Exception as e:
                # 弹出一个消息框提示失败，并显示错误信息
                QMessageBox.critical(self, "文件载入失败！","请查看文件是否正确，是否有损坏")
                # 返回上一个窗口
                self.show()

    # 定义聚类算法
    def jlsf(self):
        # 获取标签上的文件名，如果为空，则弹出一个消息框提示用户先选择csv文件，否则尝试读取csv文件，并计算行列数，然后弹出一个消息框显示结果
        filename = self.label.text()
        if filename == '0':
            QMessageBox.warning(self, "警告", "请先载入csv文件")
        else:
            num=2
            maxk = len(pd.read_csv(filename).index)
            num, ok = QInputDialog.getInt(window, "聚类数输入框", f"请输入一个聚类数（整数）\n最大值为文件总行数{maxk}", 0, 2, maxk, 1)
            if ok:
                self.text_edit.append(f'正在进行聚类中心 <b> K={num} </b> 的计算，请勿进行其他操作\n')
                time.sleep(1)
                kmeanscsv(filename,num)
                self.text_edit.append('聚类文件计算完成!请在数据文件目录中查看结果.\n')
                # 弹出一个消息框提示计算完成
                QMessageBox.information(self,"聚类文件计算完成！", "已尝试为你打开数据所在文件夹,\n您可以进行其他操作.")
                os.startfile(os.path.dirname(filename))
            else :
                QMessageBox.information(self,"未进行聚类计算", "未获得聚类数以进行聚类计算，\n请重试!!")
            self.show()

    # 定义轮廓算法
    def lkss(self):
        # 获取标签上的文件名，如果为空，则弹出一个消息框提示用户先选择csv文件，否则尝试读取csv文件，并计算行列数，然后弹出一个消息框显示结果
        filename = self.label.text()
        if filename == '0':
            QMessageBox.warning(self, "警告", "请先载入csv文件")
        else:
            self.text_edit.append('正在进行聚类轮廓系数的计算,请勿进行其他操作!\n')
            time.sleep(1)
            lkxscsv(filename)
            self.text_edit.append('轮廓计算完成!请在数据文件目录中查看结果.\n')
            # 弹出一个消息框显示结果
            QMessageBox.information(self, "轮廓计算完成！", "已尝试为你打开数据所在文件夹,\n您可以进行其他操作.")
            os.startfile(os.path.dirname(filename))
            self.show()

    # 定义关闭按钮的作用
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出提示',
                    "确定要退出么?", QMessageBox.StandardButton.Yes |
                    QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

# 创建一个应用对象
app = QApplication([])
# 创建一个窗口对象
window = Window()
# 显示窗口
window.show()
# 运行应用程序
sys.exit(app.exec())