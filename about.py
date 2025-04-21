from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
)
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import Qt, QSize


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("关于")
        self.setWindowIcon(QIcon(":/icons/app_icon.png"))  # 替换为你的应用图标
        self.setFixedSize(500, 400)
        
        self.setup_ui()
    
    def setup_ui(self):
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(20, 20, 20, 20)
        mainLayout.setSpacing(15)
        
        # 头像和基本信息区域
        infoLayout = QHBoxLayout()
        infoLayout.setSpacing(20)
        
        # 头像
        avatarLabel = QLabel()
        avatarPixmap = QPixmap("1709210261156.png")  # 替换为你的头像路径
        avatarLabel.setPixmap(avatarPixmap.scaled(
            100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        ))
        avatarLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        infoLayout.addWidget(avatarLabel)
        
        # 基本信息
        infoWidget = QWidget()
        infoInnerLayout = QVBoxLayout()
        infoInnerLayout.setSpacing(8)
        
        # 用户名
        usernameLabel = QLabel("GitHub: @lyy1119")  # 替换为你的用户名
        usernameFont = QFont()
        usernameFont.setBold(True)
        usernameFont.setPointSize(14)
        usernameLabel.setFont(usernameFont)
        infoInnerLayout.addWidget(usernameLabel)
        
        # 应用名称
        appNameLabel = QLabel("凸优化程序")  # 替换为你的应用名称
        appNameFont = QFont()
        appNameFont.setPointSize(12)
        appNameLabel.setFont(appNameFont)
        infoInnerLayout.addWidget(appNameLabel)
        
        # 版本
        versionLabel = QLabel("版本: 1.0.2")  # 替换为你的版本号
        versionLabel.setFont(appNameFont)
        infoInnerLayout.addWidget(versionLabel)
        
        infoWidget.setLayout(infoInnerLayout)
        infoLayout.addWidget(infoWidget)
        
        mainLayout.addLayout(infoLayout)
        
        # 分隔线
        separator = QWidget()
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: #ddd;")
        mainLayout.addWidget(separator)
        
        # GitHub信息
        githubLayout = QHBoxLayout()
        githubLayout.setSpacing(10)
        
        # GitHub图标
        githubIcon = QLabel()
        githubPixmap = QPixmap("github-mark.png")  # 替换为GitHub图标路径
        githubIcon.setPixmap(githubPixmap.scaled(
            24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        ))
        githubLayout.addWidget(githubIcon)
        
        # GitHub链接
        githubLink = QLabel(
            '<a href="https://github.com/lyy1119/ConvexOptimizationGUI" style="color: #0066cc; text-decoration: none;">'
            'https://github.com/lyy1119/ConvexOptimizationGUI</a>'  # 替换为你的仓库链接
        )
        githubLink.setOpenExternalLinks(True)
        githubLayout.addWidget(githubLink)
        githubLayout.addStretch()
        
        mainLayout.addLayout(githubLayout)
        
        # 开源协议
        licenseLayout = QVBoxLayout()
        licenseLayout.setSpacing(5)
        
        licenseTitle = QLabel("开源协议")
        licenseTitleFont = QFont()
        licenseTitleFont.setBold(True)
        licenseTitle.setFont(licenseTitleFont)
        licenseLayout.addWidget(licenseTitle)
        
        # 从LICENSE文件读取内容
        licensePreview = "MIT License"  # 默认显示
        
        licenseContent = QLabel(licensePreview)
        licenseContent.setWordWrap(True)
        licenseContent.setStyleSheet("color: #555;")
        licenseLayout.addWidget(licenseContent)
        
        
        mainLayout.addLayout(licenseLayout)
        
        # 底部按钮
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        
        closeBtn = QPushButton("关闭")
        closeBtn.setFixedSize(80, 30)
        closeBtn.clicked.connect(self.close)
        buttonLayout.addWidget(closeBtn)
        
        mainLayout.addLayout(buttonLayout)
        
        self.setLayout(mainLayout)