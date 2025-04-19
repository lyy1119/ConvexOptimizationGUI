from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QPushButton, QVBoxLayout, QGridLayout
)
from PyQt6.QtCore import pyqtSignal


class StackedInputWidget(QWidget):
    """栈式可增减输入框组件"""
    inputsChanged = pyqtSignal(list)  # 当输入变化时发射信号

    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_rows = []  # 保存所有输入行
        self.init_ui()
        self.add_row()  # 初始添加一行

    def init_ui(self):
        """初始化布局"""
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)

    def add_row(self, text=""):
        """添加一个新行"""
        row_index = len(self.input_rows)
        
        # 创建行部件
        line_edit = QLineEdit()
        line_edit.setText(text)
        add_btn = QPushButton("+")
        remove_btn = QPushButton("-")
        
        # 设置按钮大小
        add_btn.setFixedSize(30, 30)
        remove_btn.setFixedSize(30, 30)
        
        # 连接信号
        line_edit.textChanged.connect(self.emit_inputs_changed)
        add_btn.clicked.connect(lambda: self.add_row())
        remove_btn.clicked.connect(lambda: self.remove_row(row_index))
        
        # 如果是第一行且唯一一行，禁用减号
        if row_index == 0 and len(self.input_rows) == 0:
            remove_btn.setEnabled(False)
        
        # 添加到布局
        self.layout.addWidget(line_edit, row_index, 0)
        self.layout.addWidget(add_btn, row_index, 1)
        self.layout.addWidget(remove_btn, row_index, 2)
        
        # 保存行数据
        self.input_rows.append({
            "line_edit": line_edit,
            "add_btn": add_btn,
            "remove_btn": remove_btn
        })
        
        # 隐藏旧行的加号和减号（如果有）
        if row_index > 0:
            prev_row = self.input_rows[row_index - 1]
            prev_row["add_btn"].setVisible(False)
            prev_row["remove_btn"].setVisible(False)
        
        self.emit_inputs_changed()

    def remove_row(self, row_index):
        """移除指定行"""
        if len(self.input_rows) <= 1:
            return  # 至少保留一行
        
        # 获取要移除的行部件
        row = self.input_rows.pop(row_index)
        
        # 从布局中移除并删除
        self.layout.removeWidget(row["line_edit"])
        self.layout.removeWidget(row["add_btn"])
        self.layout.removeWidget(row["remove_btn"])
        row["line_edit"].deleteLater()
        row["add_btn"].deleteLater()
        row["remove_btn"].deleteLater()
        
        # 更新剩余行的位置
        for i, row_data in enumerate(self.input_rows):
            self.layout.addWidget(row_data["line_edit"], i, 0)
            self.layout.addWidget(row_data["add_btn"], i, 1)
            self.layout.addWidget(row_data["remove_btn"], i, 2)
            
            # 只有最后一行显示按钮
            is_last_row = (i == len(self.input_rows) - 1)
            row_data["add_btn"].setVisible(is_last_row)
            row_data["remove_btn"].setVisible(is_last_row)
        
        # 如果只剩一行，禁用减号
        if len(self.input_rows) == 1:
            self.input_rows[0]["remove_btn"].setEnabled(False)
        
        self.emit_inputs_changed()

    def get_values(self):
        """获取所有输入框的值"""
        return [row["line_edit"].text() for row in self.input_rows]

    def set_values(self, values):
        """设置输入框的值"""
        # 清空现有行
        while self.input_rows:
            self.remove_row(0)
        
        # 添加新行
        for value in values:
            self.add_row(value)
        
        # 确保至少有一行
        if not self.input_rows:
            self.add_row()

    def emit_inputs_changed(self):
        """发射输入变化信号"""
        self.inputsChanged.emit(self.get_values())


# 示例使用
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    
    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("栈式可增减输入框")
            self.setGeometry(100, 100, 400, 300)
            
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            layout = QVBoxLayout(central_widget)
            
            # 创建组件
            self.input_widget = StackedInputWidget()
            self.input_widget.inputsChanged.connect(self.on_inputs_changed)
            
            layout.addWidget(self.input_widget)
        
        def on_inputs_changed(self, values):
            print("当前输入:", values)
    
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()