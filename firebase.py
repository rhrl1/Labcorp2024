import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QStackedWidget, QLabel
import firebase_admin
from firebase_admin import credentials, db

# Firebase 초기화
cred = credentials.Certificate(r"C:\Users\ilove\OneDrive\바탕 화면\Lapcorps\labc-d8979-firebase-adminsdk-1kvwa-7f41e0808b.json")  # 다운로드 받은 서비스 계정 키 파일의 경로로 변경하세요
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://labc-d8979-default-rtdb.firebaseio.com//'  # 자신의 데이터베이스 URL로 변경하세요
})

class ButtonApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.button_sequence = []

    def initUI(self):
        # QStackedWidget을 사용해 두 개의 페이지를 만듭니다.
        self.stackedWidget = QStackedWidget(self)

        # 첫 번째 페이지 (버튼 클릭 페이지)
        page1 = QWidget()
        layout1 = QVBoxLayout()

        self.bananaButton = QPushButton('바나나', self)
        self.appleButton = QPushButton('사과', self)
        self.pearButton = QPushButton('배', self)
        self.historyButton = QPushButton('과거기록', self)

        # 버튼 클릭 이벤트 연결
        self.bananaButton.clicked.connect(lambda: self.record_button_click('바나나'))
        self.appleButton.clicked.connect(lambda: self.record_button_click('사과'))
        self.pearButton.clicked.connect(lambda: self.record_button_click('배'))
        self.historyButton.clicked.connect(self.show_history_page)

        layout1.addWidget(self.bananaButton)
        layout1.addWidget(self.appleButton)
        layout1.addWidget(self.pearButton)
        layout1.addWidget(self.historyButton)

        page1.setLayout(layout1)

        # 두 번째 페이지 (과거 기록 페이지)
        self.page2 = QWidget()
        layout2 = QVBoxLayout()

        self.historyLabel = QLabel("과거 기록이 여기에 표시됩니다.", self)
        self.backButton = QPushButton('뒤로가기', self)
        self.clearHistoryButton = QPushButton('기록 삭제하기', self)

        # 이벤트 연결
        self.backButton.clicked.connect(self.show_main_page)
        self.clearHistoryButton.clicked.connect(self.clear_history)

        layout2.addWidget(self.historyLabel)
        layout2.addWidget(self.backButton)
        layout2.addWidget(self.clearHistoryButton)

        self.page2.setLayout(layout2)

        # QStackedWidget에 두 페이지를 추가
        self.stackedWidget.addWidget(page1)
        self.stackedWidget.addWidget(self.page2)

        # 첫 번째 페이지를 기본으로 설정
        self.stackedWidget.setCurrentIndex(0)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.stackedWidget)
        self.setLayout(mainLayout)
        self.setWindowTitle('Button Click Recorder')

    def record_button_click(self, button_name):
        # 버튼 클릭 기록
        self.button_sequence.append(button_name)

        # Firebase에 버튼 클릭 순서 저장 (누를 때마다 저장)
        ref = db.reference('button_history')
        ref.push(self.button_sequence)
        self.button_sequence = []  # 저장 후 순서 초기화

    def show_history_page(self):
        # Firebase에서 과거 클릭 기록 가져오기 (최신 순으로 정렬)
        ref = db.reference('button_history')
        sequences = ref.get()

        history_text = ""
        if sequences:
            sorted_keys = sorted(sequences.keys(), reverse=True)  # 최신 순으로 정렬
            for key in sorted_keys:
                sequence = sequences[key]
                for button in sequence[::-1]:  # 클릭한 순서를 거꾸로 표시
                    history_text += f'{button}\n'
                history_text += '---\n'  # 기록 간 구분선
        else:
            history_text = '저장된 기록이 없습니다.'

        self.historyLabel.setText(history_text)
        self.stackedWidget.setCurrentIndex(1)  # 두 번째 페이지로 이동

    def clear_history(self):
        # Firebase에서 과거 기록 모두 삭제
        ref = db.reference('button_history')
        ref.delete()  # 전체 기록 삭제
        self.historyLabel.setText('기록이 삭제되었습니다.')

    def show_main_page(self):
        # 첫 번째 페이지로 돌아가기
        self.stackedWidget.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ButtonApp()
    ex.show()
    sys.exit(app.exec_())