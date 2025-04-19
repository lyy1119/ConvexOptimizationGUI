from lyy19Lib.convexOptimization import MethodType , OnedimensionOptimization , MultidimensionOptimization, ConstraintOptimization, MultiTargetConstraintOptimization
from lyy19Lib.mathFunction import FractionFunction
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout , QLabel, QPushButton, QLineEdit, QMessageBox , QDialog , QRadioButton , QGridLayout , QTextEdit , QButtonGroup, QMainWindow, QMenuBar, QGroupBox, QSizePolicy, QFileDialog
from PyQt6.QtGui import QAction
from enum import Enum
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from dialog import *

defaultInputText = """函数：
初始点： 
epsilon x: 
epsilon f: 
maxStep: 
S: 
"""
defaultOutPutText = """=============================
优化结果
迭代次数：
X=


函数值F=
=============================
"""

# 求解器、dialog、枚举类型映射表
project = [
    [ProblemType.oneDimension   , oneDimensionDialog    , OnedimensionOptimization      ],
    [ProblemType.multiDimension , multiDimensionDialog  , MultidimensionOptimization    ],
    [ProblemType.constrainted   , constraintedDialog    , ConstraintOptimization        ],
    [ProblemType.multiTarget    , multiTargetDialog     , MultiTargetConstraintOptimization]
]

class Worker(QThread):
    log_signal = pyqtSignal(str)  # 用于实时更新log
    result_signal = pyqtSignal(str)  # 用于传递最终结果

    def __init__(self, my_class, *args):
        super().__init__()
        self.my_class = my_class
        self.args = args

    def run(self):
        # 执行solve方法，模拟优化过程
        self.my_class.solve(self.args)
        self.log_signal.emit(self.my_class.logs)  # 发射log
        self.result_signal.emit("")  # 发射最终结果

class LogWindow(QDialog):
    def __init__(self):
        super().__init__()

        # 设置UI组件
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)  # 让文本框只读

        # 布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)

        self.setLayout(layout)
        self.setWindowTitle("Log Viewer")
        # self.setGeometry(100, 100, 400, 300)

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() # 布局设计
        self.problem = None

    def initUI(self):
        '''
        布局设计
        '''
        layout = QVBoxLayout() # 总布局为垂直布局

        self.inpuLable = QLabel("输入模型:")
        layout.addWidget(self.inpuLable)

        self.inputInfo = QTextEdit(self)
        self.inputInfo.setReadOnly(True)
        self.inputInfo.setText(defaultInputText)
        layout.addWidget(self.inputInfo)

        # 结果
        label = QLabel("结果:")
        layout.addWidget(label)
        self.outputInfo = QTextEdit(self)
        self.outputInfo.setReadOnly(True)
        self.outputInfo.setText(defaultOutPutText)
        layout.addWidget(self.outputInfo)

        self.setLayout(layout)
        self.setWindowTitle("无约束凸优化")

    def save_log(self):
        with open("out.txt" , "w" , encoding="utf-8") as f:
            f.write(self.problem.read_logs())
        import os
        path = os.getcwd() + '\out.txt'
        QMessageBox.information(self , "info" , f"已保存log到{path}")

    def run_optimization(self):
        self.problem.solve(self.method)
        # 展示
        self.outputInfo.setText(f"{self.problem.res}")
    def start_optimization(self):
        # 创建并显示LogWindow窗口
        self.log_window = LogWindow()
        self.log_window.show()

        # 创建并启动后台线程执行优化过程
        self.worker = Worker(self.problem, method=self.method)
        self.worker.log_signal.connect(self.update_log)  # 连接log更新槽
        self.worker.result_signal.connect(self.display_result)  # 连接结果显示槽
        self.worker.start()  # 启动线程

    def update_log(self, log):
        # 更新LogWindow中的内容
        self.log_window.text_edit.setText(log)

    def display_result(self, result):
        # 显示最终结果
        self.outputInfo.setText(result)

    def call_method(self, method_name):
        if self.my_instance:
            result = getattr(self.my_instance, method_name)()
            self.result_label.setText(f"结果: {result}")

    def set_output(self, str=defaultOutPutText):
        self.outputInfo.setText(str)
    
    def set_input(self, str=defaultInputText):
        self.inputInfo.setText(str)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initWidth = 600
        self.initHeight = 450
        self.setMinimumWidth(self.initWidth)
        self.setMinimumHeight(self.initHeight)
        self.resize(self.initWidth, self.initHeight)  # 初始大小
        self.setWindowTitle("凸优化程序")

        # 创建菜单栏
        self.create_menu_bar()
        self.widget = MainWidget()
        self.setCentralWidget(self.widget)

        # 存储优化程序
        self.problem = None
        self.method = None
        self.optimizationPara = None

    def create_menu_bar(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("文件(&F)")

        newAction = QAction("创建优化实例", self)
        newAction.setShortcut("Ctrl+N")
        newAction.triggered.connect(self.create_optimization_entity)
        fileMenu.addAction(newAction)

        exitAction = QAction("退出", self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        runMenu = menuBar.addMenu("运行(&R)")

        runAction = QAction("求解优化模型", self)
        runAction.setShortcut("Ctrl+R")
        runAction.triggered.connect(self.solve)
        runMenu.addAction(runAction)

        dataMenu = menuBar.addMenu("数据(&O)")

        logAction = QAction("查看运行日志", self)
        logAction.setShortcut("Ctrl+L")
        logAction.triggered.connect(self.show_log_window)
        dataMenu.addAction(logAction)

        saveLogAction = QAction("保存日志", self)
        saveLogAction.setShortcut("Ctrl+O")
        saveLogAction.triggered.connect(self.save_logs)
        dataMenu.addAction(saveLogAction)

    def create_optimization_entity(self):
        # 选则创建哪种优化问题
        dialog = ProblemSwitch(self)
        while True:
            if dialog.exec() == QDialog.DialogCode.Accepted:
                for i in project:
                    if dialog.result in i:
                        inputDialog = i[1]()
                        optimization = i[2]

                if inputDialog.exec() == QDialog.DialogCode.Rejected:
                    continue
                else:
                    # 输入成功，初始化求解器
                    # 初始化
                    parameter = inputDialog.result
                    self.problem = optimization(parameter)
                    self.method = parameter["method"]
                    # print(parameter)
                    self.optimizationPara = parameter.get("optimizationParameter", None)
                    if self.optimizationPara == []:
                        self.optimizationPara = None
                    # 写初始化结果
                    # print(self.optimizationPara)
                    self.widget.set_input(self.problem.logs)
                    break
            else:
                break

    def update_log(self, log):
        # 更新LogWindow中的内容
        self.logDialog.text_edit.setText(log)

    def display_result(self, res):
        # 显示最终结果
        self.widget.set_output(f"{self.problem.res}")

    def solve(self):
        method = self.method
        if self.optimizationPara:
            self.problem.solve(method, *self.optimizationPara)
        else:
            self.problem.solve(method)

        self.logDialog = LogWindow()
        self.logDialog.show()

        # 创建并启动后台线程执行优化过程
        self.worker = Worker(self.problem, self.method)
        self.worker.log_signal.connect(self.update_log)  # 连接log更新槽
        self.worker.result_signal.connect(self.display_result)  # 连接结果显示槽
        self.worker.start()  # 启动线程

    def show_log_window(self):
        LogDialog = LogWindow()
        LogDialog.text_edit.setText(f"{self.problem.logs}")

        if LogDialog.exec():
            pass
    
    def save_logs(self):
        # 打开文件选择对话框
        filePath, _ = QFileDialog.getSaveFileName(
            self,  # 父窗口
            "选择保存位置",  # 标题
            "",  # 起始目录
            "文本文件 (*.txt);;"  # 文件过滤器
        )
        if filePath:
            try:
                with open(filePath , "w" , encoding="utf-8") as f:
                    f.write(self.problem.read_logs())
                QMessageBox.information(self , "info" , f"已保存log到{filePath}")
            except:
                QMessageBox.warning(self, "错误", f"无法打开路径{filePath}，或存在其他错误")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()