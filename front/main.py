from PyQt5 import QtWidgets

from front.main_window import Ui_MainWindow
from analyzer.states import Start, F
from analyzer.exceptions import SyntaxAnalyzeError, SemanticAnalyzeError


class SyntaxAnalyzerApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.analyzeButton.clicked.connect(self.syntax_analyze)
        self.semanticButton.clicked.connect(self.output_semantic)

    def _mark_err_literal(self, position):
        self.textEdit.setFocus()
        cursor = self.textEdit.textCursor()
        print(position)
        cursor.movePosition(cursor.Start, cursor.KeepAnchor)
        cursor.movePosition(cursor.Right, cursor.KeepAnchor, position)
        cursor.clearSelection()
        self.textEdit.setTextCursor(cursor)

    def syntax_analyze(self):
        input_str = self.textEdit.toPlainText()
        try:
            Start(input_str).analyze()
        except SyntaxAnalyzeError as ex:
            self.errorsLabel.setText(f'Синтаксическая ошибка в {ex.position} символе. {ex}')
            self.errorsLabel.setStyleSheet("color: red")
            self._mark_err_literal(ex.position)
        except SemanticAnalyzeError as ex:
            self.errorsLabel.setText(f'Семантическая ошибка в {ex.position} символе. {ex}')
            self.errorsLabel.setStyleSheet("color: red")
            self._mark_err_literal(ex.position)
        else:
            self.errorsLabel.setText('Строка корректна!')
            self.errorsLabel.setStyleSheet("color: green")

    def output_semantic(self):
        self.identifiersList.clear()
        self.constantsList.clear()
        input_str = self.textEdit.toPlainText()
        try:
            final_state: F = Start(input_str).analyze()
        except (SyntaxAnalyzeError, SemanticAnalyzeError):
            pass
        else:
            semantic_data = final_state.semantic_data
            for identifier in semantic_data.identifiers:
                self.identifiersList.addItem(identifier)
            for const in semantic_data.constants:
                self.constantsList.addItem(str(const))
