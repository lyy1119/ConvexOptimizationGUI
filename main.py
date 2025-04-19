from lyy19Lib.convexOptimization import MethodType , OnedimensionOptimization , MultidimensionOptimization, ConstraintOptimization
from lyy19Lib.mathFunction import FractionFunction
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout , QLabel, QPushButton, QLineEdit, QMessageBox , QDialog , QRadioButton , QGridLayout , QTextEdit , QButtonGroup, QMainWindow, QMenuBar, QGroupBox, QSizePolicy
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

class Worker(QThread):
    log_signal = pyqtSignal(str)  # 用于实时更新log
    result_signal = pyqtSignal(str)  # 用于传递最终结果

    def __init__(self, my_class, method):
        super().__init__()
        self.my_class = my_class
        self.method = method

    def run(self):
        # 执行solve方法，模拟优化过程
        self.my_class.solve(self.method)
        self.log_signal.emit(self.my_class.logs)  # 发射log
        self.result_signal.emit(str(self.my_class.res))  # 发射最终结果

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
        self.setGeometry(100, 100, 400, 300)

class InputFunction(QDialog):
    """ 优化问题输入窗口 """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("输入窗口")
        self.setGeometry(100, 100, 300, 150)

        # 一维优化方法
        onedimensonMethodGroup = QButtonGroup(self)
        self.goldenSection = QRadioButton("黄金分割法")
        onedimensonMethodGroup.addButton(self.goldenSection)
        self.quadraticInterpolation = QRadioButton("二次插值法")
        onedimensonMethodGroup.addButton(self.quadraticInterpolation)
        self.oneDimensionButton = [self.goldenSection , self.quadraticInterpolation]
        # 多维优化方法
        multiDimensionMethodGroup = QButtonGroup(self)
        self.coordinateDescent = QRadioButton("坐标轮换法")
        multiDimensionMethodGroup.addButton(self.coordinateDescent)
        self.gradientDescent = QRadioButton("梯度法")
        multiDimensionMethodGroup.addButton(self.gradientDescent)
        self.dampedNewton = QRadioButton("阻尼牛顿法")
        multiDimensionMethodGroup.addButton(self.dampedNewton)
        self.conjugateDirection = QRadioButton("共轭方向法")
        multiDimensionMethodGroup.addButton(self.conjugateDirection)
        self.powell = QRadioButton("powell法")
        multiDimensionMethodGroup.addButton(self.powell)
        self.dfp = QRadioButton("dfp")
        multiDimensionMethodGroup.addButton(self.dfp)
        self.bfgs = QRadioButton("bfgs")
        multiDimensionMethodGroup.addButton(self.bfgs)
        self.mutiDimensionButton = [self.coordinateDescent , self.gradientDescent , self.dampedNewton , self.conjugateDirection , self.powell , self.dfp , self.bfgs]



        # 设置主窗口的布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 标签
        self.lable1 = QLabel("优化类型:")
        layout.addWidget(self.lable1)

        # 创建单选框
        self.typeGroup = QButtonGroup()
        buttonLayout = QHBoxLayout()
        self.radio_enable = QRadioButton("一维优化", self)
        self.radio_enable.toggled.connect(self.change_layout)
        self.radio_disable = QRadioButton("多维优化", self)
        self.radio_disable.toggled.connect(self.change_layout)
        self.typeGroup.addButton(self.radio_disable)
        self.typeGroup.addButton(self.radio_enable)
        # 连接单选框的点击事件到相应的槽函数
        self.radio_enable.clicked.connect(self.enable_s_input)
        self.radio_disable.clicked.connect(self.disable_s_input)
        # 添加到布局
        buttonLayout.addWidget(self.radio_enable)
        buttonLayout.addWidget(self.radio_disable)
        layout.addLayout(buttonLayout)

        # 用于创建优化问题对象的参数
        self.lable2 = QLabel("输入参数:")
        layout.addWidget(self.lable2)

        gridLayout = QGridLayout(self)
        layout.addLayout(gridLayout)

        # 函数
        functionLable = QLabel("函数")
        gridLayout.addWidget(functionLable , 0 , 0)
        self.function = QLineEdit(self)
        self.function.setPlaceholderText("字符串")
        gridLayout.addWidget(self.function , 0 , 1)

        # x0
        x0Lable = QLabel("起始点X0")
        gridLayout.addWidget(x0Lable , 1 , 0)
        self.x0 = QLineEdit(self)
        self.x0.setPlaceholderText("空格分隔  1.0 1.0")
        gridLayout.addWidget(self.x0 , 1 , 1)

        # epslionx
        epXLable = QLabel("epsilon x")
        gridLayout.addWidget(epXLable , 2 , 0)
        self.epsilonx = QLineEdit(self)
        self.epsilonx.setPlaceholderText("0.01")
        gridLayout.addWidget(self.epsilonx , 2 , 1)

        # epsilonf
        epFLable = QLabel("epsilon f")
        gridLayout.addWidget(epFLable , 3 , 0)
        self.epsilonf = QLineEdit(self)
        self.epsilonf.setPlaceholderText("0.01")
        gridLayout.addWidget(self.epsilonf , 3 , 1)

        # 搜索方向
        sLable = QLabel("搜索方向S")
        gridLayout.addWidget(sLable , 4 , 0)
        self.sInputTextbox = QLineEdit(self)
        self.sInputTextbox.setPlaceholderText("空格分隔 1.2 1.2")
        gridLayout.addWidget(self.sInputTextbox , 4 , 1)

        # 最大步长
        maxStepLable = QLabel("最大迭代次数")
        gridLayout.addWidget(maxStepLable , 5 , 0)
        self.maxStep = QLineEdit(self)
        self.maxStep.setPlaceholderText("默认1000")
        self.maxStep.setText("1000")
        gridLayout.addWidget(self.maxStep , 5 , 1)

        # 默认情况下启用文本框，设置单选框状态
        self.sInputTextbox.setEnabled(True)
        self.radio_enable.setChecked(True)
        # 方法选择框
        methodLable = QLabel("优化方法")
        layout.addWidget(methodLable)
        # 放入布局
        for i in self.oneDimensionButton:
            layout.addWidget(i)
        for i in self.mutiDimensionButton:
            layout.addWidget(i)
        # 添加按钮
        self.change_layout()
        # 确定按钮
        self.ok = QPushButton("确认" , self)
        self.ok.clicked.connect(self.check_input)
        layout.addWidget(self.ok)

    def change_layout(self):
        if self.radio_enable.isChecked():
            # 显示一维
            for i in self.oneDimensionButton:
                i.setVisible(True)
            for i in self.mutiDimensionButton:
                i.setVisible(False)
        else:
            # 显示二维
            for i in self.oneDimensionButton:
                i.setVisible(False)
            for i in self.mutiDimensionButton:
                i.setVisible(True)

    def get_input(self):
        method = None
        if self.radio_enable.isChecked():
            # 代表是一维优化
            pType = ProblemType.oneDimension
            s = list(map(float , self.sInputTextbox.text().split()))
            if self.goldenSection.isChecked():
                method = MethodType.goldenSection
            else:
                method = MethodType.quadraticInterpolation
        else:
            pType = ProblemType.multiDimension
            s = None
            if self.coordinateDescent.isChecked():
                method = MethodType.coordinateDescent
            elif self.gradientDescent.isChecked():
                method = MethodType.gradientDescent
            elif self.dampedNewton.isChecked():
                method = MethodType.dampedNewton
            elif self.conjugateDirection.isChecked():
                method = MethodType.conjugateDirection
            elif self.powell.isChecked():
                method = MethodType.powell
            elif self.dfp.isChecked():
                method = MethodType.dfp
            elif self.bfgs.isChecked():
                method = MethodType.bfgs
        return {
            "type" : pType,
            "function" : self.function.text(),
            "x0" : list(map(float , self.x0.text().split())),
            "epsilonx" : float(self.epsilonx.text().strip()),
            "epsilonf" : float(self.epsilonf.text().strip()),
            "s" :s,
            "maxStep": int(self.maxStep.text()),
            "method" : method
        }

    def check_input(self):
        if not self.function.text().strip():
            QMessageBox.warning(self , "输入错误" , "输入函数为空!")
        elif not self.x0.text().strip():
            QMessageBox.warning(self , "输入错误" , "输入初始点为空!")
        elif not self.epsilonx.text().strip():
            QMessageBox.warning(self , "输入错误" , "输入epsilon x为空!")
        elif not self.epsilonf.text().strip():
            QMessageBox.warning(self , "输入错误" , "输入epsilon f为空!")
        elif self.radio_enable.isChecked() and (not self.sInputTextbox.text().strip()):
            QMessageBox.warning(self , "输入错误" , "已选择一维优化模型，但是输入搜索方向为空!")
        elif not self.maxStep.text().strip():
            QMessageBox.warning(self , "输入错误" , "输入最大迭代次数为空!")
        else:
            self.accept()


    def enable_s_input(self):
        self.sInputTextbox.setEnabled(True)

    def disable_s_input(self):
        self.sInputTextbox.setDisabled(True)

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        # self.resize(600, 450)  # 初始大小
        # self.aspect_ratio = 4 / 3  # 设定固定比例 (4:3)
        self.initUI() # 布局设计
        self.problem = None

    def initUI(self):
        '''
        布局设计
        '''
        layout = QVBoxLayout() # 总布局为垂直布局

        self.InputButton = QPushButton("输入优化问题", self)
        self.InputButton.clicked.connect(self.get_input_function_dialog)  # 绑定点击事件
        layout.addWidget(self.InputButton)

        self.inpuLable = QLabel("输入模型:")
        layout.addWidget(self.inpuLable)

        self.inputInfo = QTextEdit(self)
        self.inputInfo.setReadOnly(True)
        self.inputInfo.setText(defaultInputText)
        layout.addWidget(self.inputInfo)

        # 结果
        self.outputInfo = QTextEdit(self)
        self.outputInfo.setReadOnly(True)
        self.outputInfo.setText(defaultOutPutText)
        layout.addWidget(self.outputInfo)

        # 优化按钮与log按钮
        buttonLayout = QHBoxLayout()
        self.optimizeButton = QPushButton("优化")
        self.optimizeButton.clicked.connect(self.start_optimization)
        buttonLayout.addWidget(self.optimizeButton)
        self.saveLogButton = QPushButton("导出log")
        self.saveLogButton.clicked.connect(self.save_log)
        buttonLayout.addWidget(self.saveLogButton)
        layout.addLayout(buttonLayout)

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
    
    def get_input_function_dialog(self):
        '''
        调用窗口，输入函数
        '''
        dialog = InputFunction(self)
        if dialog.exec():
            input = dialog.get_input()
            # 初始化self.problem
            t = input["type"]
            function = input["function"]
            x0 = input["x0"]
            epsilonx = input["epsilonx"]
            epsilonf = input["epsilonf"]
            s = input["s"]
            self.method = input["method"]
            maxStep = input["maxStep"]
            if t == ProblemType.oneDimension:
                self.problem = OnedimensionOptimization(function , x0 , s , epsilonx , epsilonf , maxStep)
            else:
                self.problem = MultidimensionOptimization(function , x0 , epsilonx , epsilonf , maxStep)
            # 合成信息
            inputInfo = f"函数：{self.problem.function}\n初始点：\n{self.problem.x0}\nepsilon x：{epsilonx}\nepsilon f：{epsilonf}\nmaxStep：{maxStep}"
            if t == ProblemType.oneDimension:
                inputInfo += f"\nS：\n{self.problem.s}"
            # 写入
            #inputInfo += f"\nmethod："
            #inputInfo += f"{}"
            self.inputInfo.setText(inputInfo)

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
        self.setCentralWidget(MainWidget())

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

    def create_optimization_entity(self):
        # 选则创建哪种优化问题
        dialog = ProblemSwitch(self)
        while True:
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # print(dialog.result)
                if dialog.result == ProblemType.oneDimension:
                    inputDialog = oneDimensionDialog(self)
                elif dialog.result == ProblemType.multiDimension:
                    inputDialog = multiDimensionDialog(self)
                if inputDialog.exec() == QDialog.DialogCode.Rejected:
                    continue
                else: # 初始化
                    print(inputDialog.result)
                    break
            else:
                break

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()