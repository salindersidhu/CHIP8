from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont, QColor


class DebugWindow(QtWidgets.QDialog):
    def __init__(self, parent, chip8, step_callback, run_callback, stop_callback, close_callback):
        super().__init__(parent)

        self.setWindowFlags(
            self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint
        )

        self.__chip8 = chip8
        self.__step_callback = step_callback
        self.__run_callback = run_callback
        self.__stop_callback = stop_callback
        self.__close_callback = close_callback

        self.setWindowTitle("CHIP-8 Debugger")
        self.resize(1200, 700)

        self.__fields = {}
        self.__registerFields = []
        self.__memoryTable = None

        self.__stepButton = None
        self.__runButton = None
        self.__stopButton = None

        self.__refreshTimer = QtCore.QTimer(self)
        self.__refreshTimer.timeout.connect(self.refresh)

        self.__buildUi()
        self.refresh()
        self.__setStoppedMode()

    def __buildUi(self):
        mainLayout = QtWidgets.QVBoxLayout()

        topLayout = QtWidgets.QHBoxLayout()

        leftLayout = QtWidgets.QVBoxLayout()
        leftLayout.addWidget(self.__buildCpuSection())
        leftLayout.addWidget(self.__buildTimerKeySection())

        topLayout.addLayout(leftLayout, 1)
        topLayout.addWidget(self.__buildRegisterSection(), 2)

        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.__buildMemorySection(), 1)

        buttonLayout = QtWidgets.QHBoxLayout()

        self.__stepButton = QtWidgets.QPushButton("Step")
        self.__stepButton.clicked.connect(self.__step)

        self.__runButton = QtWidgets.QPushButton("Run")
        self.__runButton.clicked.connect(self.__run)

        self.__stopButton = QtWidgets.QPushButton("Stop")
        self.__stopButton.clicked.connect(self.__stop)

        buttonLayout.addWidget(self.__stepButton)
        buttonLayout.addWidget(self.__runButton)
        buttonLayout.addWidget(self.__stopButton)

        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)

    def __buildCpuSection(self):
        group = QtWidgets.QGroupBox("CPU")
        form = QtWidgets.QFormLayout()

        for name in ["PC", "I", "OP"]:
            field = self.__readOnlyField()
            self.__fields[name] = field
            form.addRow(name, field)

        group.setLayout(form)
        return group

    def __buildRegisterSection(self):
        group = QtWidgets.QGroupBox("Registers")
        grid = QtWidgets.QGridLayout()

        for index in range(16):
            label = QtWidgets.QLabel(f"V{index:X}")
            field = self.__readOnlyField()
            self.__registerFields.append(field)

            row = index // 4
            col = (index % 4) * 2

            grid.addWidget(label, row, col)
            grid.addWidget(field, row, col + 1)

        group.setLayout(grid)
        return group

    def __buildTimerKeySection(self):
        group = QtWidgets.QGroupBox("Timers / Keys")
        form = QtWidgets.QFormLayout()

        for name in ["Delay Timer", "Sound Timer", "Keys", "Stack"]:
            field = self.__readOnlyField()
            self.__fields[name] = field
            form.addRow(name, field)

        group.setLayout(form)
        return group

    def __buildMemorySection(self):
        group = QtWidgets.QGroupBox("Memory")
        layout = QtWidgets.QVBoxLayout()

        self.__memoryTable = QtWidgets.QTableWidget()
        self.__memoryTable.setColumnCount(17)
        self.__memoryTable.setRowCount(256)

        headers = ["Addr"] + [f"+{i:X}" for i in range(16)]
        self.__memoryTable.setHorizontalHeaderLabels(headers)

        self.__memoryTable.verticalHeader().setVisible(False)
        self.__memoryTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.__memoryTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.__memoryTable.setFont(QFont("Courier New", 9))

        header = self.__memoryTable.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

        for row in range(256):
            baseAddress = row * 16

            self.__memoryTable.setItem(
                row,
                0,
                QtWidgets.QTableWidgetItem(f"0x{baseAddress:03X}")
            )

            for col in range(16):
                self.__memoryTable.setItem(
                    row,
                    col + 1,
                    QtWidgets.QTableWidgetItem("00")
                )

        layout.addWidget(self.__memoryTable)
        group.setLayout(layout)
        return group

    def __readOnlyField(self):
        field = QtWidgets.QLineEdit()
        field.setReadOnly(True)
        field.setFont(QFont("Courier New", 10))
        return field

    def __step(self):
        self.__step_callback()
        self.refresh()

    def __run(self):
        self.__run_callback()
        self.__refreshTimer.start(100)
        self.__setRunningMode()

    def __stop(self):
        self.__stop_callback()
        self.__refreshTimer.stop()
        self.refresh()
        self.__setStoppedMode()

    def __setRunningMode(self):
        self.__stepButton.setEnabled(False)
        self.__runButton.setEnabled(False)
        self.__stopButton.setEnabled(True)

    def __setStoppedMode(self):
        self.__stepButton.setEnabled(True)
        self.__runButton.setEnabled(True)
        self.__stopButton.setEnabled(False)

    def refresh(self):
        state = self.__chip8.getState()

        self.__fields["PC"].setText(f"0x{state['PRC']:03X}")
        self.__fields["I"].setText(f"0x{state['ADR']:03X}")

        pc = state["PRC"]
        ram = state["RAM"]

        if pc + 1 < len(ram):
            byte1 = str(ram[pc]).replace("0x", "").upper()
            byte2 = str(ram[pc + 1]).replace("0x", "").upper()

            self.__fields["OP"].setText(f"0x{byte1}{byte2}")
        else:
            self.__fields["OP"].setText("----")

        self.__fields["Delay Timer"].setText(str(state["TIM"][0]))
        self.__fields["Sound Timer"].setText(str(state["TIM"][1]))
        self.__fields["Keys"].setText(str(state["KEY"]))

        stack = state["STK"].toList() if hasattr(state["STK"], "toList") else state["STK"]
        self.__fields["Stack"].setText(str(stack))

        for index, value in enumerate(state["REG"]):
            self.__registerFields[index].setText(f"0x{value:02X} ({value})")

        self.__refreshMemory(state["RAM"], state["PRC"])

    def __refreshMemory(self, ram, pc):
        self.__memoryTable.setUpdatesEnabled(False)

        normalBackground = QColor(255, 255, 255)
        pcBackground = QColor(255, 230, 120)
        nextByteBackground = QColor(255, 245, 190)

        for row in range(256):
            baseAddress = row * 16

            for col in range(16):
                address = baseAddress + col
                item = self.__memoryTable.item(row, col + 1)

                if address < len(ram):
                    value = ram[address]
                    text = f"{value:02X}" if isinstance(value, int) else str(value)
                else:
                    text = ""

                item.setText(text)

                font = item.font()
                font.setBold(address == pc or address == pc + 1)
                item.setFont(font)

                if address == pc:
                    item.setBackground(pcBackground)
                elif address == pc + 1:
                    item.setBackground(nextByteBackground)
                else:
                    item.setBackground(normalBackground)

        self.__memoryTable.setUpdatesEnabled(True)

    def closeEvent(self, event):
        self.__refreshTimer.stop()
        self.__close_callback()
        event.accept()

    def resetControls(self):
        self.__refreshTimer.stop()
        self.__setStoppedMode()
        self.refresh()
