from convexOptimization import *
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout , QLabel, QPushButton, QLineEdit, QMessageBox , QDialog , QRadioButton , QGridLayout

class InputFunction(QDialog):
    """ 优化问题输入窗口 """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("输入窗口")
        self.setGeometry(100, 100, 300, 150)


        # 设置主窗口的布局
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 标签
        self.lable1 = QLabel("优化类型:")
        layout.addWidget(self.lable1)

        # 创建单选框
        buttonLayout = QHBoxLayout()
        self.radio_enable = QRadioButton("一维优化", self)
        self.radio_disable = QRadioButton("多维优化", self)
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

        gridLayout = QGridLayout()
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

        # 确定按钮
        self.ok = QPushButton("确认" , self)
        self.ok.clicked.connect(self.check_input)
        layout.addWidget(self.ok)

    def return_input(self):
        pass

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


    def get_text(self):
        """ 返回输入的文本 """
        return self.input_field.text()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("固定比例窗口")
        self.resize(400, 300)  # 初始大小
        self.aspect_ratio = 4 / 3  # 设定固定比例 (4:3)

        self.initUI()
        self.problem = None

    def initUI(self):
        '''
        布局设计
        '''
        layout = QVBoxLayout()
        self.oneDimensionInputButton = QPushButton("输入优化问题", self)
        self.oneDimensionInputButton.clicked.connect(self.show_input_function_dialog)  # 绑定点击事件
        layout.addWidget(self.oneDimensionInputButton)
        # 显示函数
        self.function_label = QLabel("F(X)=")
        layout.addWidget(self.function_label)

        self.label = QLabel("输入参数:")
        layout.addWidget(self.label)

        self.input_text = QLineEdit(self)
        self.input_text.setPlaceholderText("字符串")
        layout.addWidget(self.input_text)

        self.input_list = QLineEdit(self)
        self.input_list.setPlaceholderText("列表(逗号分隔)")
        layout.addWidget(self.input_list)

        self.input_num1 = QLineEdit(self)
        self.input_num1.setPlaceholderText("浮点数1")
        layout.addWidget(self.input_num1)

        self.input_num2 = QLineEdit(self)
        self.input_num2.setPlaceholderText("浮点数2")
        layout.addWidget(self.input_num2)



        self.result_label = QLabel("结果:")
        layout.addWidget(self.result_label)





        self.setLayout(layout)
        self.setWindowTitle("MyClass GUI")

    def create_instance(self):
        try:
            text = self.input_text.text()
            values = list(map(float, self.input_list.text().split(',')))
            num1 = float(self.input_num1.text())
            num2 = float(self.input_num2.text())
            self.my_instance = MultidimensionOptimization(text, values, num1, num2)
            QMessageBox.information(self, "Success", "实例创建成功！")
        except ValueError:
            QMessageBox.critical(self, "Error", "请输入正确格式的数据！")

    def call_method(self, method_name):
        if self.my_instance:
            result = getattr(self.my_instance, method_name)()
            self.result_label.setText(f"结果: {result}")
    
    def show_input_function_dialog(self):
        '''
        调用窗口，输入函数
        '''
        dialog = InputFunction(self)
        if dialog.exec():
            text = dialog.get_text()
            self.function_label.setText(f"{text}")  # 更新主窗口的文本

    def resizeEvent(self, event):
        """ 监听窗口调整事件，并强制窗口保持固定比例 """
        width = event.size().width()
        height = int(width / self.aspect_ratio)
        self.resize(width, height)  # 重新设置窗口大小，使其符合比例


app = QApplication([])
window = MyApp()
window.show()
app.exec()
