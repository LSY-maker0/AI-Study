"""
example12(工资月薪结算系统) -

三类员工：
～ 部门经理：固定月薪，15000元
～ 程序员：计时结算月薪，每小时200元
～ 销售员：底薪+提成，底薪1800元，销售额提成5%左右

录入员工信息，自动结算信息

子类对父类已有的方法，重新给出自己的实现版本，这个过程叫做方法重写

Author: lsy
Date: 2025/12/10
"""
class Employee:
    def __init__(self,no,name):
        self.no = no
        self.name = name

    def get_salary(self):
        pass

class Manager(Employee):

    def get_salary(self):
        return 15000

class Programmer(Employee):

    def __init__(self,no,name):
        super().__init__(no,name)
        self.working_hour=0

    def get_salary(self):
        return 200*self.working_hour

class Salesman(Employee):

    def __init__(self, no, name):
        super().__init__(no, name)
        self.sales = 0

    def get_salary(self):
        return 1800*0.05*self.sales