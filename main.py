import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class EcuatieGradul3(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Rezolvator de ecuații de gradul al treilea')
        self.setGeometry(100, 100, 1000, 800)

        self.label_a = QLabel('a:')
        self.label_b = QLabel('b:')
        self.label_c = QLabel('c:')
        self.label_d = QLabel('d:')

        self.input_a = QLineEdit()
        self.input_b = QLineEdit()
        self.input_c = QLineEdit()
        self.input_d = QLineEdit()

        self.solve_button = QPushButton('Rezolvă')
        self.solve_button.clicked.connect(self.solve)

        self.result_label = QLabel('')
        self.result_label.setAlignment(Qt.AlignCenter)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        self.axes.set_facecolor('#F0F0F0')

        layout = QVBoxLayout()
        layout.addWidget(self.label_a)
        layout.addWidget(self.input_a)
        layout.addWidget(self.label_b)
        layout.addWidget(self.input_b)
        layout.addWidget(self.label_c)
        layout.addWidget(self.input_c)
        layout.addWidget(self.label_d)
        layout.addWidget(self.input_d)
        layout.addWidget(self.solve_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def solve(self):
        try:
            a = np.complex128(self.input_a.text())
            b = np.complex128(self.input_b.text())
            c = np.complex128(self.input_c.text())
            d = np.complex128(self.input_d.text())

            b_redus = np.real(b / a)
            c_redus = np.real(c / a)
            d_redus = np.real(d / a)

            coeficients = [a, b, c, d]
            roots = np.roots(coeficients)

            solutii_reale = []
            solutii_complexe = []
            for root in roots:
                if np.isclose(root.imag, 0):
                    solutii_reale.append(root.real)
                else:
                    solutii_complexe.append(root)

            rezultat = f'Forma redusă: x^3 + {b_redus:.2f}x^2 + {c_redus:.2f}x + {d_redus:.2f} = 0\n'

            if len(solutii_reale) > 0:
                rezultat += f'Soluțiile reale sunt: {", ".join([f"{sol:.2f}" for sol in solutii_reale])}\n'

            if len(solutii_complexe) > 0:
                rezultat += f'Soluțiile complexe conjugate sunt: '
                for sol in solutii_complexe:
                    rezultat += f'{sol.real:.2f} + {sol.imag:.2f}i, '

            self.result_label.setText(rezultat)

            x = np.linspace(-10, 10, 400)
            y = np.polyval([np.real(a), np.real(b), np.real(c), np.real(d)], x)
            self.axes.clear()
            self.axes.plot(x, y)
            self.axes.set_title('Graficul ecuației')
            self.axes.grid(True)

            self.canvas.draw()
        except ValueError:
            QMessageBox.warning(self, 'Eroare', 'Introduceți coeficienți valizi!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EcuatieGradul3()
    style = """
            QWidget {
                background: #262D37;
            }
            QLabel {
                color: #fff;
            } 
            QLineEdit {
                padding: 1px;
                color: #fff;
                border-style: solid;
                border: 2px solid #fff;
                border-radius: 8px;
            }
            QPushButton {
                color: white;
                background: #0577a8;
                border: 1px #DADADA solid;
                padding: 5px 10px;
                border-radius: 2px;
                font-weight: bold;
                font-size: 9pt;
                outline: none;
            }
            QPushButton:hover {
                border: 1px #C6C6C6 solid;
                background: #0892D0;
            }
        """
    window.setStyleSheet(style)
    window.show()
    sys.exit(app.exec_())
