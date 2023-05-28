# -*- coding: utf-8 -*-
"""
    @author : liuxiaobo
    @time   : 2023-5-29
    @desc   : utools入口文件
"""

import json
import re
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTextEdit, QMessageBox

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('golang struct to json')
        self.setGeometry(0, 0, 800, 600)
        hbox = QHBoxLayout(self)

        # 左侧文本域
        self.left_textarea = QTextEdit(self)
        self.left_textarea.textChanged.connect(self.onTextChanged)
        hbox.addWidget(self.left_textarea)

        # 右侧文本域
        self.right_textarea = QTextEdit(self)
        self.right_textarea.setReadOnly(True)
        hbox.addWidget(self.right_textarea)

        self.setLayout(hbox)
        self.show()

    def onTextChanged(self):
        # 左侧文本域内容改变时，同步到右侧文本域
        text = self.left_textarea.toPlainText()
        try:
            # 尝试将文本解析为golang结构体
            struct_pattern = r'type\s+\w+\s+struct\s*{[\s\S]*?}'
            struct_match = re.search(struct_pattern, text)
            if struct_match:
                struct_text = struct_match.group()
                struct_name = re.search(r'type\s+(\w+)\s+struct', struct_text).group(1)
                struct_dict = {}
                for field_match in re.finditer(r'(\w+)\s+(\w+)(\s+`.*`)?', struct_text):
                    field_name, field_type = field_match.group(1), field_match.group(2)
                    # Ignore tag content
                    field_type = re.sub(r'`.*`', '', field_type).strip()
                    struct_dict[field_name] = field_type
                json_text = json.dumps(struct_dict, indent=4)
                self.right_textarea.setText(json_text)
            else:
                self.right_textarea.setText('')
                raise ValueError('Not a valid golang struct')
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))

def main():
    app = QApplication([])
    window = MainWindow()
    app.exec_()

if __name__ == '__main__':
    main()
