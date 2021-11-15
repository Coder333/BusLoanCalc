#!/usr/bin/python
import sys
from PyQt5.QtWidgets import QLabel, QToolTip, QPushButton, QApplication, QHBoxLayout, QVBoxLayout, QMainWindow, QPushButton, QWidget, QTextEdit, QComboBox, QLineEdit
from PyQt5.QtGui import QIcon, QFont, QTextCursor




class HouseLoanCalc:
    def __init__(self, bus_loan, bus_years, bus_rate, mode):
        # 商贷配置
        self.bus_loan = bus_loan
        self.bus_years = bus_years
        self.bus_rate = bus_rate
        self.mode = mode


    def bus_repay_per_month(self):
        if self.mode == '等额本息':
            beta = self.bus_rate / 100 / 12
            n = self.bus_years * 12
            repayment_per_month = self.bus_loan * beta * (1 + beta) ** n / ((1 + beta) ** n - 1)
            return (repayment_per_month / 100) * 1000000
        else:
            beta = self.bus_rate / 100 / 12
            n = self.bus_years * 12
            repayment_per_month = ""
            for i in range(1,241):
                repayment_per_month += ("第%d个月还款：%.2f \n" %(i,(self.bus_loan / n + self.bus_loan * (1-(i-1) / n) *beta) * 10000))
            return repayment_per_month


    def final_repayment(self):
        if self.mode == '等额本息':
            return self.bus_repay_per_month() * 12 * self.bus_years
        else:
            beta = self.bus_rate / 100 / 12
            n = self.bus_years * 12
            return (self.bus_loan + self.bus_loan * beta * (n+1) / 2 ) * 10000

    def print_details(self):
        if self.mode == '等额本息':
            return ("每月还款：{:.2f} "
                "\n\n还款总额：{:.2f}".format(self.bus_repay_per_month(),self.final_repayment()))
        else:
            return ("还款总额：{:.2f}\n\n".format(self.final_repayment()) + self.bus_repay_per_month())




class MyComboBox(QComboBox):
    def __init__(self):
        super(MyComboBox, self).__init__()

    def showPopup(self):                    #重写showPopup函数
        QComboBox.showPopup(self)




class TooltipForm(QMainWindow):
    def __init__(self):
        super(TooltipForm,self).__init__()
        self.initUI()

        self.cb1.currentIndexChanged[str].connect(self.select_mode)
        self.button_calc.clicked.connect(self.onClick_Button_calc)


    def initUI(self):
        self.setWindowTitle("商贷计算器")
        self.setGeometry(500,500,500,500)
        # 状态栏
        self.status = self.statusBar()


        #商业贷款标签
        self.bus_loan_label = QLabel(self)
        self.bus_loan_label.setText("商业贷款（万元）：")
        #输入文本框
        self.bus_loan_line = QLineEdit(self)
        self.bus_loan_line.setText("100")
        self.bus_loan = int(self.bus_loan_line.text())

        
        #贷款期限标签
        self.bus_years_label = QLabel(self)
        self.bus_years_label.setText("贷款期限（年）：")
        #输入文本框
        self.bus_years_line = QLineEdit(self)
        self.bus_years_line.setText("20")
        self.bus_years = int(self.bus_years_line.text())
        
        
        #商贷利率标签
        self.bus_rate_label = QLabel(self)
        self.bus_rate_label.setText("商贷利率（%）：")
        #输入文本框
        self.bus_rate_line = QLineEdit(self)
        self.bus_rate_line.setText("6.55")
        self.bus_rate = float(self.bus_rate_line.text())

        
        #还款方式标签
        self.mode_label = QLabel(self)
        self.mode_label.setText("还款方式：")
        #下拉框
        self.cb1 = MyComboBox()
        mode = ['等额本息','等额本金']
        self.cb1.addItems(mode)
        self.cb1.setCurrentIndex(0)
        self.mode = self.cb1.currentText()

        
        # 设置计算按钮   
        self.button_calc = QPushButton() 
        self.button_calc.setText("计算")
        
        
        #计算结果
        self.info = QTextEdit()
        self.info.setReadOnly(True)
        
        
        #实例化水平布局
        layout1 = QHBoxLayout()
        #相关控件添加到水平布局中
        layout1.addWidget(self.bus_loan_label)
        layout1.addWidget(self.bus_loan_line)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.bus_years_label)
        layout2.addWidget(self.bus_years_line)
        
        layout3 = QHBoxLayout()
        layout3.addWidget(self.bus_rate_label)
        layout3.addWidget(self.bus_rate_line)

        layout4 = QHBoxLayout()
        layout4.addWidget(self.mode_label)
        layout4.addWidget(self.cb1)

        layout_bnt = QHBoxLayout()
        layout_bnt.addWidget(self.button_calc)
        
        layout_info = QHBoxLayout()
        layout_info.addWidget(self.info)


        # 主框架，所有控件的放置位置
        mainFrame = QWidget()

        #全局布局
        mainLayout = QVBoxLayout(mainFrame)

        #全局布局中添加小布局
        mainLayout.addLayout(layout1)
        mainLayout.addLayout(layout2)
        mainLayout.addLayout(layout3)
        mainLayout.addLayout(layout4)
        mainLayout.addLayout(layout_bnt)
        mainLayout.addLayout(layout_info)

        mainFrame.setLayout(mainLayout)
        # 使充满屏幕
        self.setCentralWidget(mainFrame)

    
    def onClick_Button_calc(self):
        calc = HouseLoanCalc(self.bus_loan, self.bus_years, self.bus_rate, self.mode)
        self.info.setText(calc.print_details())


    def select_mode(self, i):
        self.mode = i




if __name__ == "__main__":

    app = QApplication(sys.argv)
    main = TooltipForm()
    # 显示窗口
    main.show() 
    # 建立循环
    sys.exit(app.exec_())