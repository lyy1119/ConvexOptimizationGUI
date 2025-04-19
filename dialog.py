from lyy19Lib.convexOptimization import MethodType , OnedimensionOptimization , MultidimensionOptimization, ConstraintOptimization
from lyy19Lib.mathFunction import FractionFunction
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout , QLabel, QPushButton, QLineEdit, QMessageBox , QDialog , QRadioButton , QGridLayout , QTextEdit , QButtonGroup, QMainWindow, QMenuBar, QGroupBox, QSizePolicy
from PyQt6.QtGui import QAction
from enum import Enum
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from customWidget import *

class ProblemType(Enum):
    oneDimension = 0
    multiDimension = 1
    constrainted = 2
    multiTarget = 4

class oneDimensionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_layout()
        self.result = None

    def create_layout(self):
        # 填写一维优化所需参数
        layout = QVBoxLayout(self)

        # 输入参数
        parameter = QGroupBox("输出参数")
        parameterLayout = QGridLayout(parameter)

        # 函数
        functionLable = QLabel("函数")
        parameterLayout.addWidget(functionLable , 0 , 0)
        self.function = QLineEdit(self)
        self.function.setPlaceholderText("字符串")
        parameterLayout.addWidget(self.function , 0 , 1)

        # x0
        x0Lable = QLabel("起始点X0")
        parameterLayout.addWidget(x0Lable , 1 , 0)
        self.x0 = QLineEdit(self)
        self.x0.setPlaceholderText("空格分隔  1.0 1.0")
        parameterLayout.addWidget(self.x0 , 1 , 1)

        # epslionx
        epXLable = QLabel("epsilon x")
        parameterLayout.addWidget(epXLable , 2 , 0)
        self.epsilonx = QLineEdit(self)
        self.epsilonx.setPlaceholderText("0.01")
        parameterLayout.addWidget(self.epsilonx , 2 , 1)

        # epsilonf
        epFLable = QLabel("epsilon f")
        parameterLayout.addWidget(epFLable , 3 , 0)
        self.epsilonf = QLineEdit(self)
        self.epsilonf.setPlaceholderText("0.01")
        parameterLayout.addWidget(self.epsilonf , 3 , 1)

        # 搜索方向
        sLable = QLabel("搜索方向S")
        parameterLayout.addWidget(sLable , 4 , 0)
        self.sInputTextbox = QLineEdit(self)
        self.sInputTextbox.setPlaceholderText("空格分隔 1.2 1.2")
        parameterLayout.addWidget(self.sInputTextbox , 4 , 1)

        # 最大步长
        maxStepLable = QLabel("最大迭代次数")
        parameterLayout.addWidget(maxStepLable , 5 , 0)
        self.maxStep = QLineEdit(self)
        self.maxStep.setPlaceholderText("默认1000")
        self.maxStep.setText("1000")
        parameterLayout.addWidget(self.maxStep , 5 , 1)

        layout.addWidget(parameter)

        # 方法选择
        method = QGroupBox("优化方法")
        methodLayout = QVBoxLayout(method)
        # 一维优化方法
        onedimensonMethodGroup = QButtonGroup(self)
        self.goldenSection = QRadioButton("黄金分割法")
        onedimensonMethodGroup.addButton(self.goldenSection)
        self.quadraticInterpolation = QRadioButton("二次插值法")
        onedimensonMethodGroup.addButton(self.quadraticInterpolation)
        self.oneDimensionButton = {
            self.goldenSection:MethodType.goldenSection,
            self.quadraticInterpolation:MethodType.quadraticInterpolation
            }
        for i in self.oneDimensionButton.keys():
            methodLayout.addWidget(i)
        self.goldenSection.setChecked(True)
        layout.addWidget(method)

        # 确定与取消
        buttonLayout = QHBoxLayout()
        ok = QPushButton("确认")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("取消")
        cancel.clicked.connect(self.reject)
        buttonLayout.addWidget(ok)
        buttonLayout.addWidget(cancel)
        layout.addLayout(buttonLayout)

    def accept(self):
        self.result = {}
        # 验证函数
        try:
            f = FractionFunction(self.function.text())
        except:
            QMessageBox.warning(self, "输入错误", "输入的函数无法解析，请检查函数")
            return
        self.result["function"] = f
        # 验证初始点
        dimension = f.dimension
        if len(self.x0.text().split()) != dimension:
            QMessageBox.warning(self,  "输入错误", "输入的初始点和函数维度不符")
            return
        self.result["x0"] = list(self.x0.text().split())
        # 验证epsilonx
        try:
            epsilonx = float(self.epsilonx.text())
            if epsilonx < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self,  "输入错误", "输入的epsilonx不是正实数")
            return
        self.result["epsilonx"] = epsilonx
        # 验证epsilonf
        try:
            epsilonx = float(self.epsilonx.text())
            if epsilonx < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self,  "输入错误", "输入的epsilonx不是正实数")
            return
        self.result["epsilonx"] = epsilonx
        # 验证S
        dimension = f.dimension
        if len(self.sInputTextbox.text().split()) != dimension:
            QMessageBox.warning(self,  "输入错误", "输入的搜索方向S和函数维度不符")
            return
        self.result["s"] = list(self.sInputTextbox.text().split())
        # 优化方法
        for i, j in self.oneDimensionButton.items():
            if i.isChecked():
                self.result["method"] = j
        return super().accept()

class multiDimensionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_layout()
        self.result = None

    def create_layout(self):
        # 填写多维无约束优化所需参数
        layout = QVBoxLayout(self)

        # 输入参数
        parameter = QGroupBox("输出参数")
        parameterLayout = QGridLayout(parameter)

        # 函数
        functionLable = QLabel("函数")
        parameterLayout.addWidget(functionLable , 0 , 0)
        self.function = QLineEdit(self)
        self.function.setPlaceholderText("字符串")
        parameterLayout.addWidget(self.function , 0 , 1)

        # x0
        x0Lable = QLabel("起始点X0")
        parameterLayout.addWidget(x0Lable , 1 , 0)
        self.x0 = QLineEdit(self)
        self.x0.setPlaceholderText("空格分隔  1.0 1.0")
        parameterLayout.addWidget(self.x0 , 1 , 1)

        # epslionx
        epXLable = QLabel("epsilon x")
        parameterLayout.addWidget(epXLable , 2 , 0)
        self.epsilonx = QLineEdit(self)
        self.epsilonx.setPlaceholderText("0.01")
        parameterLayout.addWidget(self.epsilonx , 2 , 1)

        # epsilonf
        epFLable = QLabel("epsilon f")
        parameterLayout.addWidget(epFLable , 3 , 0)
        self.epsilonf = QLineEdit(self)
        self.epsilonf.setPlaceholderText("0.01")
        parameterLayout.addWidget(self.epsilonf , 3 , 1)

        # 最大步长
        maxStepLable = QLabel("最大迭代次数")
        parameterLayout.addWidget(maxStepLable , 5 , 0)
        self.maxStep = QLineEdit(self)
        self.maxStep.setPlaceholderText("默认1000")
        self.maxStep.setText("1000")
        parameterLayout.addWidget(self.maxStep , 5 , 1)

        layout.addWidget(parameter)

        # 方法选择
        method = QGroupBox("优化方法")
        methodLayout = QVBoxLayout(method)
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
        self.multiDimensionButton = {
            self.coordinateDescent: MethodType.coordinateDescent,
            self.gradientDescent: MethodType.gradientDescent ,
            self.dampedNewton: MethodType.dampedNewton ,
            self.conjugateDirection: MethodType.conjugateDirection ,
            self.powell: MethodType.powell ,
            self.dfp: MethodType.dfp ,
            self.bfgs: MethodType.bfgs
            }
        for i in self.multiDimensionButton.keys():
            methodLayout.addWidget(i)
        self.coordinateDescent.setChecked(True)
        layout.addWidget(method)

        # 确定与取消
        buttonLayout = QHBoxLayout()
        ok = QPushButton("确认")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("取消")
        cancel.clicked.connect(self.reject)
        buttonLayout.addWidget(ok)
        buttonLayout.addWidget(cancel)
        layout.addLayout(buttonLayout)

    def accept(self):
        self.result = {}
        # 验证函数
        try:
            f = FractionFunction(self.function.text())
        except:
            QMessageBox.warning(self, "输入错误", "输入的函数无法解析，请检查函数")
            return
        self.result["function"] = f
        # 验证初始点
        dimension = f.dimension
        if len(self.x0.text().split()) != dimension:
            QMessageBox.warning(self,  "输入错误", "输入的初始点和函数维度不符")
            return
        self.result["x0"] = list(self.x0.text().split())
        # 验证epsilonx
        try:
            epsilonx = float(self.epsilonx.text())
            if epsilonx < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self,  "输入错误", "输入的epsilonx不是正实数")
            return
        self.result["epsilonx"] = epsilonx
        # 验证epsilonf
        try:
            epsilonx = float(self.epsilonx.text())
            if epsilonx < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self,  "输入错误", "输入的epsilonx不是正实数")
            return
        self.result["epsilonx"] = epsilonx
        # 优化方法
        for i, j in self.multiDimensionButton.items():
            if i.isChecked():
                self.result["method"] = j
        return super().accept()

class constraintedDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_layout()
        self.result = None

    def create_layout(self):
        nowLine = 0
        # 填写多维无约束优化所需参数
        layout = QVBoxLayout(self)

        # 输入参数
        parameter = QGroupBox("输出参数")
        parameterLayout = QGridLayout(parameter)

        # 函数
        functionLable = QLabel("函数")
        parameterLayout.addWidget(functionLable , nowLine, 0)
        self.function = QLineEdit(self)
        self.function.setPlaceholderText("字符串")
        parameterLayout.addWidget(self.function , nowLine, 1)
        
        nowLine += 1

        # gu
        guLable = QLabel("gu(X)")
        guLable.setAlignment(Qt.AlignmentFlag.AlignTop)
        guLable.setStyleSheet("""
    QLabel {
        padding-top: 5px 0 0 0;
    }
""")
        parameterLayout.addWidget(guLable, nowLine, 0)
        self.gu = StackedInputWidget()
        parameterLayout.addWidget(self.gu, nowLine, 1)

        nowLine += 1

        # gu
        hvLable = QLabel("hv(X)")
        hvLable.setAlignment(Qt.AlignmentFlag.AlignTop)
        hvLable.setStyleSheet("""
    QLabel {
        padding-top: 5px 0 0 0;
    }
""")
        parameterLayout.addWidget(hvLable, nowLine, 0)
        self.hv = StackedInputWidget()
        parameterLayout.addWidget(self.hv, nowLine, 1)

        nowLine += 1

        # x0
        x0Lable = QLabel("起始点X0")
        parameterLayout.addWidget(x0Lable , nowLine, 0)
        self.x0 = QLineEdit(self)
        self.x0.setPlaceholderText("空格分隔  1.0 1.0")
        parameterLayout.addWidget(self.x0 , nowLine, 1)

        nowLine += 1

        # epslionx
        epXLable = QLabel("epsilon x")
        parameterLayout.addWidget(epXLable , nowLine, 0)
        self.epsilonx = QLineEdit(self)
        self.epsilonx.setPlaceholderText("0.01")
        parameterLayout.addWidget(self.epsilonx , nowLine, 1)

        nowLine += 1

        # epsilonf
        epFLable = QLabel("epsilon f")
        parameterLayout.addWidget(epFLable , nowLine, 0)
        self.epsilonf = QLineEdit(self)
        self.epsilonf.setPlaceholderText("0.01")
        parameterLayout.addWidget(self.epsilonf , nowLine, 1)

        nowLine += 1

        # 最大步长
        maxStepLable = QLabel("最大迭代次数")
        parameterLayout.addWidget(maxStepLable , nowLine, 0)
        self.maxStep = QLineEdit(self)
        self.maxStep.setPlaceholderText("默认1000")
        self.maxStep.setText("1000")
        parameterLayout.addWidget(self.maxStep , nowLine, 1)

        layout.addWidget(parameter)

        # 方法选择
        method = QGroupBox("优化方法")
        methodLayout = QVBoxLayout(method)
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
        self.multiDimensionButton = {
            self.coordinateDescent: MethodType.coordinateDescent,
            self.gradientDescent: MethodType.gradientDescent ,
            self.dampedNewton: MethodType.dampedNewton ,
            self.conjugateDirection: MethodType.conjugateDirection ,
            self.powell: MethodType.powell ,
            self.dfp: MethodType.dfp ,
            self.bfgs: MethodType.bfgs
            }
        for i in self.multiDimensionButton.keys():
            methodLayout.addWidget(i)
        self.coordinateDescent.setChecked(True)
        layout.addWidget(method)

        # 确定与取消
        buttonLayout = QHBoxLayout()
        ok = QPushButton("确认")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("取消")
        cancel.clicked.connect(self.reject)
        buttonLayout.addWidget(ok)
        buttonLayout.addWidget(cancel)
        layout.addLayout(buttonLayout)

    def accept(self):
        self.result = {}
        # 验证函数
        try:
            f = FractionFunction(self.function.text())
        except:
            QMessageBox.warning(self, "输入错误", "输入的函数无法解析，请检查函数")
            return
        self.result["function"] = f
        # 验证gu
        gu = self.gu.get_values()
        gu = [FractionFunction(i) for i in gu]
        maxDimension = 0
        for index, i in enumerate(gu):
            try:
                maxDimension = max(maxDimension, i.dimension)
            except:
                QMessageBox.warning(self, "输入错误", f"不等式约束{index+1}不合法")
                return
        if maxDimension > f.dimension:
            QMessageBox.warning(self, "输入错误", "不等式约束的最大维度大于函数维度")
            return
        else:
            self.result["gu"] = gu
        # 验证hv
        hv = self.hv.get_values()
        hv = [FractionFunction(i) for i in hv]
        maxDimension = 0
        for index, i in enumerate(hv):
            try:
                maxDimension = max(maxDimension, i.dimension)
            except:
                QMessageBox.warning(self, "输入错误", f"等式约束{index+1}不合法")
                return
        if maxDimension > f.dimension:
            QMessageBox.warning(self, "输入错误", "等式约束的最大维度大于函数维度")
            return
        else:
            self.result["hv"] = hv
        # 验证初始点
        dimension = f.dimension
        if len(self.x0.text().split()) != dimension:
            QMessageBox.warning(self,  "输入错误", "输入的初始点和函数维度不符")
            return
        self.result["x0"] = list(self.x0.text().split())
        # 验证epsilonx
        try:
            epsilonx = float(self.epsilonx.text())
            if epsilonx < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self,  "输入错误", "输入的epsilonx不是正实数")
            return
        self.result["epsilonx"] = epsilonx
        # 验证epsilonf
        try:
            epsilonx = float(self.epsilonx.text())
            if epsilonx < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self,  "输入错误", "输入的epsilonx不是正实数")
            return
        self.result["epsilonx"] = epsilonx
        # 优化方法
        for i, j in self.multiDimensionButton.items():
            if i.isChecked():
                self.result["method"] = j
        return super().accept()

class multiTargetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_layout()
        self.result = None

    def create_layout(self):
        nowLine = 0
        # 填写多维无约束优化所需参数
        layout = QVBoxLayout(self)

        # 输入参数
        parameter = QGroupBox("输出参数")
        parameterLayout = QGridLayout(parameter)

        # 函数
        functionLable = QLabel("函数")
        functionLable.setAlignment(Qt.AlignmentFlag.AlignTop)
        functionLable.setStyleSheet("""
    QLabel {
        padding-top: 5px 0 0 0;
    }
""")
        parameterLayout.addWidget(functionLable , nowLine, 0)
        self.function = StackedInputWidget()
        parameterLayout.addWidget(self.function , nowLine, 1)
        
        nowLine += 1

        # 权重
        wLabel = QLabel("权重")
        parameterLayout.addWidget(wLabel , nowLine, 0)
        self.w = QLineEdit(self)
        self.w.setPlaceholderText("空格分隔  1.0 1.0")
        parameterLayout.addWidget(self.w , nowLine, 1)

        nowLine += 1

        # gu
        guLable = QLabel("gu(X)")
        guLable.setAlignment(Qt.AlignmentFlag.AlignTop)
        guLable.setStyleSheet("""
    QLabel {
        padding-top: 5px 0 0 0;
    }
""")
        parameterLayout.addWidget(guLable, nowLine, 0)
        self.gu = StackedInputWidget()
        parameterLayout.addWidget(self.gu, nowLine, 1)

        nowLine += 1

        # gu
        hvLable = QLabel("hv(X)")
        hvLable.setAlignment(Qt.AlignmentFlag.AlignTop)
        hvLable.setStyleSheet("""
    QLabel {
        padding-top: 5px 0 0 0;
    }
""")
        parameterLayout.addWidget(hvLable, nowLine, 0)
        self.hv = StackedInputWidget()
        parameterLayout.addWidget(self.hv, nowLine, 1)

        nowLine += 1

        # x0
        x0Lable = QLabel("起始点X0")
        parameterLayout.addWidget(x0Lable , nowLine, 0)
        self.x0 = QLineEdit(self)
        self.x0.setPlaceholderText("空格分隔  1.0 1.0")
        parameterLayout.addWidget(self.x0 , nowLine, 1)

        nowLine += 1

        # epslionx
        epXLable = QLabel("epsilon x")
        parameterLayout.addWidget(epXLable , nowLine, 0)
        self.epsilonx = QLineEdit(self)
        self.epsilonx.setPlaceholderText("0.01")
        parameterLayout.addWidget(self.epsilonx , nowLine, 1)

        nowLine += 1

        # epsilonf
        epFLable = QLabel("epsilon f")
        parameterLayout.addWidget(epFLable , nowLine, 0)
        self.epsilonf = QLineEdit(self)
        self.epsilonf.setPlaceholderText("0.01")
        parameterLayout.addWidget(self.epsilonf , nowLine, 1)

        nowLine += 1

        # 最大步长
        maxStepLable = QLabel("最大迭代次数")
        parameterLayout.addWidget(maxStepLable , nowLine, 0)
        self.maxStep = QLineEdit(self)
        self.maxStep.setPlaceholderText("默认1000")
        self.maxStep.setText("1000")
        parameterLayout.addWidget(self.maxStep , nowLine, 1)

        layout.addWidget(parameter)

        # 方法选择
        method = QGroupBox("优化方法")
        methodLayout = QVBoxLayout(method)
        # 多维优化方法
        multiDimensionMethodGroup = QButtonGroup(self)
        self.powell = QRadioButton("powell法")
        multiDimensionMethodGroup.addButton(self.powell)
        self.dfp = QRadioButton("dfp")
        multiDimensionMethodGroup.addButton(self.dfp)
        self.bfgs = QRadioButton("bfgs")
        multiDimensionMethodGroup.addButton(self.bfgs)
        self.multiDimensionButton = {
            self.powell: MethodType.powell ,
            self.dfp: MethodType.dfp ,
            self.bfgs: MethodType.bfgs
            }
        for i in self.multiDimensionButton.keys():
            methodLayout.addWidget(i)
        self.powell.setChecked(True)
        layout.addWidget(method)

        # 确定与取消
        buttonLayout = QHBoxLayout()
        ok = QPushButton("确认")
        ok.clicked.connect(self.accept)
        cancel = QPushButton("取消")
        cancel.clicked.connect(self.reject)
        buttonLayout.addWidget(ok)
        buttonLayout.addWidget(cancel)
        layout.addLayout(buttonLayout)

    def accept(self):
        self.result = {}
        # 验证函数,多个
        functions = self.function.get_values()
        try:
            functions = [FractionFunction(i) for i in functions]
        except:
            QMessageBox.warning(self, "输入错误", f"输入函数不合法")
            return
        dimension = 0
        for i in functions:
            dimension = max(dimension, i.dimension)
        # 验证权重
        w = self.w.text().split()
        if len(w) != len(functions):
            QMessageBox.warning(self, "输入错误", "输入的权重数量小于输入的函数数量")
            return
        self.result["function"] = [[functions[i], float(w[i])] for i in range(len(w))]
        # 验证gu
        gu = self.gu.get_values()
        gu = [FractionFunction(i) for i in gu]
        maxDimension = 0
        for index, i in enumerate(gu):
            try:
                maxDimension = max(maxDimension, i.dimension)
            except:
                QMessageBox.warning(self, "输入错误", f"不等式约束{index+1}不合法")
                return
        if maxDimension > dimension:
            QMessageBox.warning(self, "输入错误", "不等式约束的最大维度大于函数维度")
            return
        else:
            self.result["gu"] = gu
        # 验证hv
        hv = self.hv.get_values()
        hv = [FractionFunction(i) for i in hv]
        maxDimension = 0
        for index, i in enumerate(hv):
            try:
                maxDimension = max(maxDimension, i.dimension)
            except:
                QMessageBox.warning(self, "输入错误", f"等式约束{index+1}不合法")
                return
        if maxDimension > dimension:
            QMessageBox.warning(self, "输入错误", "等式约束的最大维度大于函数维度")
            return
        else:
            self.result["hv"] = hv
        # 验证初始点
        if len(self.x0.text().split()) != dimension:
            QMessageBox.warning(self,  "输入错误", "输入的初始点和函数维度不符")
            return
        self.result["x0"] = list(self.x0.text().split())
        # 验证epsilonx
        try:
            epsilonx = float(self.epsilonx.text())
            if epsilonx < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self,  "输入错误", "输入的epsilonx不是正实数")
            return
        self.result["epsilonx"] = epsilonx
        # 验证epsilonf
        try:
            epsilonx = float(self.epsilonx.text())
            if epsilonx < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self,  "输入错误", "输入的epsilonx不是正实数")
            return
        self.result["epsilonx"] = epsilonx
        # 优化方法
        for i, j in self.multiDimensionButton.items():
            if i.isChecked():
                self.result["method"] = j
        return super().accept()


class ProblemSwitch(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_layout()
        self.result = ProblemType.oneDimension

    def create_layout(self):
        self.setWindowTitle('选择优化模型类型')
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # 创建布局
        layout = QVBoxLayout(self)
        # 一个单选框加按钮
        group_box = QGroupBox("优化模型类型")
        group_layout = QVBoxLayout()
        # 创建单选框
        radio1 = QRadioButton("一维无约束凸优化（指定方向的优化）")
        radio2 = QRadioButton("多维无约束凸优化")
        radio3 = QRadioButton("多维约束优化")
        radio4 = QRadioButton("多目标多维约束优化（线性加权）")
        # 默认选项
        self.radios = {
            radio1:ProblemType.oneDimension,
            radio2:ProblemType.multiDimension,
            radio3:ProblemType.constrainted, 
            radio4:ProblemType.multiTarget
            }
        radio1.setChecked(True)
        group_layout.addWidget(radio1)
        group_layout.addWidget(radio2)
        group_layout.addWidget(radio3)
        group_layout.addWidget(radio4)

        group_box.setLayout(group_layout)
        layout.addWidget(group_box)
        # 确认与取消按钮
        buttonLayout = QHBoxLayout()
        layout.addLayout(buttonLayout)
        ok = QPushButton("确认")
        cancel = QPushButton("取消")
        buttonLayout.addWidget(ok)
        buttonLayout.addWidget(cancel)
        ok.clicked.connect(self.accept)
        cancel.clicked.connect(self.reject)

    def accept(self):
        for key, value in self.radios.items():
            if key.isChecked():
                self.result = value
        return super().accept()
