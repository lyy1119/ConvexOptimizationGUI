from lyy19Lib.convexOptimization import MethodType , OnedimensionOptimization , MultidimensionOptimization, ConstraintOptimization
from lyy19Lib.mathFunction import FractionFunction
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout , QLabel, QPushButton, QLineEdit, QMessageBox , QDialog , QRadioButton , QGridLayout , QTextEdit , QButtonGroup, QMainWindow, QMenuBar, QGroupBox, QSizePolicy, QScrollArea
from PyQt6.QtGui import QAction
from enum import Enum
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from customWidget import *

class ProblemType(Enum):
    oneDimension = 0
    multiDimension = 1
    constrainted = 2
    multiTarget = 4

class InputParameterPrototype(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 获取当前所在屏幕的几何尺寸
        screen = QApplication.screenAt(self.pos())
        if screen is None:
            screen = QApplication.primaryScreen()
        screenGeometry = screen.availableGeometry()
        # 获取主屏幕的可用几何尺寸（排除任务栏等）
        screen = QApplication.primaryScreen()
        screenGeometry = screen.availableGeometry()
        
        # 计算90%的宽度和高度
        maxWidth = int(screenGeometry.width()*0.8)
        maxHeight = int(screenGeometry.height()*0.8)
        
        # 设置对话框的最大尺寸
        self.setMaximumSize(QSize(maxWidth, maxHeight))
        # 创建主布局
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        # 创建滚动区域
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)  # 允许内部widget调整大小
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        # 创建内容widget
        self.contentWidget = QWidget()
        # self.contentLayout = QVBoxLayout(self.contentWidget)
        # self.contentLayout.setContentsMargins(10, 10, 10, 10)  # 设置内容边距
        # 设置滚动区域的内容widget
        scrollArea.setWidget(self.contentWidget)
        # 将滚动区域添加到主布局
        mainLayout.addWidget(scrollArea)

class oneDimensionDialog(InputParameterPrototype):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_layout()
        self.result = None

    def create_layout(self):
        # 填写一维优化所需参数
        layout = QVBoxLayout(self.contentWidget)

        # 输入参数
        parameter = QGroupBox("输入参数")
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

        # epsilonx
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
            epsilonf = float(self.epsilonf.text())
            if epsilonf < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self,  "输入错误", "输入的epsilonx不是正实数")
            return
        self.result["epsilonf"] = epsilonf
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

class multiDimensionDialog(InputParameterPrototype):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_layout()
        self.result = None

    def create_layout(self):
        # 填写多维无约束优化所需参数
        layout = QVBoxLayout(self.contentWidget)

        # 输入参数
        parameter = QGroupBox("输入参数")
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

        # epsilonx
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
            epsilonf = float(self.epsilonf.text())
            if epsilonf < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self,  "输入错误", "输入的epsilonx不是正实数")
            return
        self.result["epsilonf"] = epsilonf
        # 优化方法
        for i, j in self.multiDimensionButton.items():
            if i.isChecked():
                self.result["method"] = j
        return super().accept()

class constraintedDialog(InputParameterPrototype):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_layout()
        self.result = None

    def create_layout(self):
        nowLine = 0
        # 填写多维无约束优化所需参数
        layout = QVBoxLayout(self.contentWidget)

        # 输入参数
        parameter = QGroupBox("输入参数")
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

        # hv
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

        # epsilonx
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

        # upLimit
        upLable = QLabel("初始点上限")
        parameterLayout.addWidget(upLable, nowLine, 0)
        self.upLimit = QLineEdit(self)
        self.upLimit.setPlaceholderText("空格分隔")
        parameterLayout.addWidget(self.upLimit, nowLine, 1)

        nowLine += 1

        # lowLimit
        lowLabel = QLabel("初始点下限")
        parameterLayout.addWidget(lowLabel, nowLine, 0)
        self.lowLimit = QLineEdit(self)
        self.lowLimit.setPlaceholderText("空格分隔")
        parameterLayout.addWidget(self.lowLimit, nowLine, 1)

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
        methodLayout = QHBoxLayout(method)
        # 多维优化方法
        multiDimensionMethodGroup = QButtonGroup(self)
        self.stochasticDirectionMethod = QRadioButton("随机方向法")
        multiDimensionMethodGroup.addButton(self.stochasticDirectionMethod)
        self.compositeMethod = QRadioButton("复合形法")
        multiDimensionMethodGroup.addButton(self.compositeMethod)
        self.penaltyMethodInterior = QRadioButton("内点罚函数法")
        multiDimensionMethodGroup.addButton(self.penaltyMethodInterior)
        self.methodButton = {
            self.stochasticDirectionMethod  : MethodType.stochasticDirectionMethod,
            self.compositeMethod            : MethodType.compositeMethod,
            self.penaltyMethodInterior      : MethodType.penaltyMethodInterior
            }
        for i in self.methodButton.keys():
            methodLayout.addWidget(i)
        self.stochasticDirectionMethod.setChecked(True)
        layout.addWidget(method)

        # 优化参数 主要是内点罚函数的r和c
        optimizationPara = QGroupBox("优化参数")
        layout.addWidget(optimizationPara)

        optimizationParaLayout = QGridLayout(optimizationPara)
        nowLine = 0
        # 惩罚因子r
        rLable = QLabel("惩罚因子r")
        optimizationParaLayout.addWidget(rLable , nowLine, 0)
        self.r = QLineEdit(self)
        self.r.setPlaceholderText("实数")
        optimizationParaLayout.addWidget(self.r , nowLine, 1)

        nowLine += 1

        # 递增/递减系数
        cLable = QLabel("递增/递减系数")
        optimizationParaLayout.addWidget(cLable , nowLine, 0)
        self.c = QLineEdit(self)
        self.c.setPlaceholderText("实数")
        optimizationParaLayout.addWidget(self.c , nowLine, 1)

        nowLine += 1

        # x0
        x0Lable = QLabel("初始点")
        optimizationParaLayout.addWidget(x0Lable, nowLine, 0)
        self.x0 = QLineEdit(self)
        self.x0.setPlaceholderText("空格分隔  1.0 1.0 不指定时自动生成")
        optimizationParaLayout.addWidget(self.x0, nowLine, 1)

        nowLine += 1

        # 指定无约束优化方法
        method = QGroupBox("优化方法")
        methodLayout = QHBoxLayout(method)
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
        # 验证函数
        try:
            f = FractionFunction(self.function.text())
        except:
            QMessageBox.warning(self, "输入错误", "输入的函数无法解析，请检查函数")
            return
        self.result["function"] = f
        # 验证gu
        gu = self.gu.get_values()
        if gu != [""]:
            gu = [FractionFunction(i) for i in gu]
        else:
            gu = []
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
        if hv != [""]:
            hv = [FractionFunction(i) for i in hv]
        else:
            hv = []
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
        # 上下限
        try:
            upLimit = list(map(int, self.upLimit.text().split()))
            if len(upLimit) != f.dimension:
                QMessageBox.warning(self, "错误", "输入的初始点上限与函数维度不符")
                return
            else:
                self.result["upLimit"] = upLimit
        except:
            QMessageBox.warning(self, "错误", "输入的初始点上限格式有误")
        try:
            lowLimit = list(map(int, self.lowLimit.text().split()))
            if len(lowLimit) != f.dimension:
                QMessageBox.warning(self, "错误", "输入的初始点下限与函数维度不符")
                return
            else:
                self.result["lowLimit"] = lowLimit
        except:
            QMessageBox.warning(self, "错误", "输入的初始点下限格式有误")

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
            epsilonf = float(self.epsilonf.text())
            if epsilonf < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self,  "输入错误", "输入的epsilonx不是正实数")
            return
        self.result["epsilonf"] = epsilonf
        # 优化方法
        for i, j in self.methodButton.items():
            if i.isChecked():
                self.result["method"] = j


        self.result["optimizationParameter"] = []
        # 优化方法参数载入
        if self.result["method"] == MethodType.penaltyMethodInterior or self.result["method"] == MethodType.penaltyMethodExterior or self.result["method"] == MethodType.penaltyMethodMixed:
            # 载入 r,c
            if self.r.text():
                try:
                    r = float(self.r.text())
                except:
                    QMessageBox.warning(self, "错误", "惩罚因子r输入格式错误")
                    return
            else:
                if self.result["method"] == MethodType.penaltyMethodInterior:
                    r = 1
                elif self.result["method"] == MethodType.penaltyMethodExterior:
                    r = 10
                else:
                    QMessageBox.warning(self, "warning", "程序错误 -1")
                    raise ValueError("wrong way")
            self.result["optimizationParameter"].append(r)
            if self.c.text():
                try:
                    c = float(self.c.text())
                except:
                    QMessageBox.warning(self, "错误", "递增递减系数输入错误")
                    return
            else:
                if self.result["method"] == MethodType.penaltyMethodInterior:
                    c = 0.6
                elif self.result["method"] == MethodType.penaltyMethodExterior:
                    c = 8
                else:
                    QMessageBox.warning(self, "warning", "程序错误 -1")
                    raise ValueError("wrong way")
            self.result["optimizationParameter"].append(c)
        # 指定多维无约束优化方法
        for i, j in self.multiDimensionButton.items():
            if i.isChecked():
                unconsitraintMethod = j
                break
        self.result["optimizationParameter"].append(unconsitraintMethod)
        # 载入初始点，可能有，也可能没有
        if self.x0.text():
            # 如果有
            try:
                x0 = list(map(int , self.x0.text().split()))
            except:
                QMessageBox.warning(self, "错误", "输出的初始点格式错误")
                return
            self.result["optimizationParameter"].append(x0)
        return super().accept()

class multiTargetDialog(InputParameterPrototype):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_layout()
        self.result = None

    def create_layout(self):
        nowLine = 0
        # 填写多维无约束优化所需参数
        layout = QVBoxLayout(self.contentWidget)

        # 输入参数
        parameter = QGroupBox("输入参数")
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

        # hv
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

        # epsilonx
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

        # upLimit
        upLable = QLabel("初始点上限")
        parameterLayout.addWidget(upLable, nowLine, 0)
        self.upLimit = QLineEdit(self)
        self.upLimit.setPlaceholderText("空格分隔")
        parameterLayout.addWidget(self.upLimit, nowLine, 1)

        nowLine += 1

        # lowLimit
        lowLabel = QLabel("初始点下限")
        parameterLayout.addWidget(lowLabel, nowLine, 0)
        self.lowLimit = QLineEdit(self)
        self.lowLimit.setPlaceholderText("空格分隔")
        parameterLayout.addWidget(self.lowLimit, nowLine, 1)

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
        methodLayout = QHBoxLayout(method)
        # 多维优化方法
        multiDimensionMethodGroup = QButtonGroup(self)
        self.stochasticDirectionMethod = QRadioButton("随机方向法")
        multiDimensionMethodGroup.addButton(self.stochasticDirectionMethod)
        self.compositeMethod = QRadioButton("复合形法")
        multiDimensionMethodGroup.addButton(self.compositeMethod)
        self.penaltyMethodInterior = QRadioButton("内点罚函数法")
        multiDimensionMethodGroup.addButton(self.penaltyMethodInterior)
        self.methodButton = {
            self.stochasticDirectionMethod  : MethodType.stochasticDirectionMethod,
            self.compositeMethod            : MethodType.compositeMethod,
            self.penaltyMethodInterior      : MethodType.penaltyMethodInterior
            }
        for i in self.methodButton.keys():
            methodLayout.addWidget(i)
        self.stochasticDirectionMethod.setChecked(True)
        layout.addWidget(method)

        # 优化参数 主要是内点罚函数的r和c
        optimizationPara = QGroupBox("优化参数")
        layout.addWidget(optimizationPara)

        optimizationParaLayout = QGridLayout(optimizationPara)
        nowLine = 0
        # 惩罚因子r
        rLable = QLabel("惩罚因子r")
        optimizationParaLayout.addWidget(rLable , nowLine, 0)
        self.r = QLineEdit(self)
        self.r.setPlaceholderText("实数")
        optimizationParaLayout.addWidget(self.r , nowLine, 1)

        nowLine += 1

        # 递增/递减系数
        cLable = QLabel("递增/递减系数")
        optimizationParaLayout.addWidget(cLable , nowLine, 0)
        self.c = QLineEdit(self)
        self.c.setPlaceholderText("实数")
        optimizationParaLayout.addWidget(self.c , nowLine, 1)

        nowLine += 1

        # x0
        x0Lable = QLabel("初始点")
        optimizationParaLayout.addWidget(x0Lable, nowLine, 0)
        self.x0 = QLineEdit(self)
        self.x0.setPlaceholderText("空格分隔  1.0 1.0 不指定时自动生成")
        optimizationParaLayout.addWidget(self.x0, nowLine, 1)

        nowLine += 1

        # 指定无约束优化方法
        method = QGroupBox("优化方法")
        methodLayout = QHBoxLayout(method)
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
        if gu != [""]:
            gu = [FractionFunction(i) for i in gu]
        else:
            gu = []
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
        if hv != [""]:
            hv = [FractionFunction(i) for i in hv]
        else:
            hv = []
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
        # 上下限
        try:
            upLimit = list(map(int, self.upLimit.text().split()))
            if len(upLimit) != dimension:
                QMessageBox.warning(self, "错误", "输入的初始点上限与函数维度不符")
                return
            else:
                self.result["upLimit"] = upLimit
        except:
            QMessageBox.warning(self, "错误", "输入的初始点上限格式有误")
        try:
            lowLimit = list(map(int, self.lowLimit.text().split()))
            if len(lowLimit) != dimension:
                QMessageBox.warning(self, "错误", "输入的初始点下限与函数维度不符")
                return
            else:
                self.result["lowLimit"] = lowLimit
        except:
            QMessageBox.warning(self, "错误", "输入的初始点下限格式有误")

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
            epsilonf = float(self.epsilonf.text())
            if epsilonf < 0:
                raise ValueError()
        except:
            QMessageBox.warning(self,  "输入错误", "输入的epsilonx不是正实数")
            return
        self.result["epsilonf"] = epsilonf
        # 优化方法
        for i, j in self.methodButton.items():
            if i.isChecked():
                self.result["method"] = j


        self.result["optimizationParameter"] = []
        # 优化方法参数载入
        if self.result["method"] == MethodType.penaltyMethodInterior or self.result["method"] == MethodType.penaltyMethodExterior or self.result["method"] == MethodType.penaltyMethodMixed:
            # 载入 r,c
            if self.r.text():
                try:
                    r = float(self.r.text())
                except:
                    QMessageBox.warning(self, "错误", "惩罚因子r输入格式错误")
                    return
            else:
                if self.result["method"] == MethodType.penaltyMethodInterior:
                    r = 1
                elif self.result["method"] == MethodType.penaltyMethodExterior:
                    r = 10
                else:
                    QMessageBox.warning(self, "warning", "程序错误 -1")
                    raise ValueError("wrong way")
            self.result["optimizationParameter"].append(r)
            if self.c.text():
                try:
                    c = float(self.c.text())
                except:
                    QMessageBox.warning(self, "错误", "递增递减系数输入错误")
                    return
            else:
                if self.result["method"] == MethodType.penaltyMethodInterior:
                    c = 0.6
                elif self.result["method"] == MethodType.penaltyMethodExterior:
                    c = 8
                else:
                    QMessageBox.warning(self, "warning", "程序错误 -1")
                    raise ValueError("wrong way")
            self.result["optimizationParameter"].append(c)
        # 指定多维无约束优化方法
        for i, j in self.multiDimensionButton.items():
            if i.isChecked():
                unconsitraintMethod = j
                break
        self.result["optimizationParameter"].append(unconsitraintMethod)
        # 载入初始点，可能有，也可能没有
        if self.x0.text():
            # 如果有
            try:
                x0 = list(map(int , self.x0.text().split()))
            except:
                QMessageBox.warning(self, "错误", "输出的初始点格式错误")
                return
            self.result["optimizationParameter"].append(x0)
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
