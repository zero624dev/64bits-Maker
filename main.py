from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence, QPalette, QColor
from PyQt5.QtCore import Qt
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from PIL import Image
import os, sys, requests

if not os.path.isdir('./resource'):
    os.mkdir('./resource')

if not os.path.exists('./resource/audio.mp3'):
    url = 'https://github.com/Z640/64bits-Maker/raw/main/audio.mp3'
    r = requests.get(url, allow_redirects=True)
    open('./resource/audio.mp3', 'wb').write(r.content)

if len(sys.argv) > 1:
    if sys.argv[1].lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
	    img1 = sys.argv[1]
else:
	img1 = None


if len(sys.argv) > 2:
    if sys.argv[2].lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
	    img2 = sys.argv[2]
else:
	img2 = None

pixelized = False

app = QApplication([])

# Force the style to be the same on all OSs:
app.setStyle("Fusion")

# Now use a palette to switch to dark colors:
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.white)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)

# The rest of the code is the same as for the "normal" text editor.

app.setApplicationName("64bits Maker")

# text = QPlainTextEdit()
widget = QWidget()

btn2 = QPushButton(widget)
if img2 is None:
    btn2.setText("128비트 이미지")
else:
    btn2.setText(os.path.basename(img2))
btn2.move(10,70)
btn2.resize(150, 50)
def btn2_clicked():
    global img2
    path = QFileDialog.getOpenFileName(window, "Open")[0]
    if path:
        if path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            img2 = path
            btn2.setText(os.path.basename(path))
        else:
            alert = QMessageBox()
            alert.setText('지원하는 파일 포맷이 아닙니다.')
            alert.exec_()
btn2.clicked.connect(btn2_clicked)

btn3 = QPushButton(widget)
btn3.setText("픽셀화")
btn3.move(170,10)
btn3.resize(150, 50)
def resize(image, w=1920, h=1080):
    background = Image.new('RGBA', (w, h), (255, 255, 255, 255))
    offset=((background.size[0] - image.size[0]) // 2, (background.size[1] - image.size[1]) // 2)
    background.paste(image, offset)
    return background

def pixelize():
    global pixelized
    if img1 is None:
        alert = QMessageBox()
        alert.setText('64비트 이미지를 선택해주세요.')
        alert.exec_()
        return
    
    image = Image.open(img1)
    resize(image).save('./resource/64bit.png')

    for i in range(1, 5):
        downscaled_image = image.resize((int(image.size[0]/(8*i)), int(image.size[1]/(8*i))), Image.NEAREST)
        upscaled_image = downscaled_image.resize((downscaled_image.size[0]*(8*i), downscaled_image.size[1]*(8*i)), Image.NEAREST)
        resize(upscaled_image).save(f'./resource/{["32bit","16bit","8bit","4bit"][i-1]}.png')
    
    for i in range(1,3):
        downscaled_image = image.resize((1, i), Image.NEAREST)
        upscaled_image = downscaled_image.resize((150, 150*i), Image.NEAREST)
        resize(upscaled_image).save(f'./resource/{i}bit.png')

    pixelized = True
    btn3.setText("픽셀화 완료")
btn3.clicked.connect(pixelize)

btn1 = QPushButton(widget)
if img1 is None:
    btn1.setText("64비트 이미지")
else:
    btn1.setText(os.path.basename(img1))
btn1.move(10,10)
btn1.resize(150, 50) 
def btn1_clicked():
    global img1
    global pixelized
    path = QFileDialog.getOpenFileName(window, "Open")[0]
    if path:
        if path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            img1 = path
            btn1.setText(os.path.basename(path))
            pixelized = False
            btn3.setText("픽셀화")
        else:
            alert = QMessageBox()
            alert.setText('지원하는 파일 포맷이 아닙니다.')
            alert.exec_()
btn1.clicked.connect(btn1_clicked)

btn4 = QPushButton(widget)
btn4.setText("렌더링")
btn4.move(170,70)
btn4.resize(150, 50)
def render():
    if img1 is None:
        alert = QMessageBox()
        alert.setText('64비트 이미지를 선택해주세요.')
        alert.exec_()
        return

    if not pixelized:
        alert = QMessageBox()
        alert.setText('픽셀화를 해주세요.')
        alert.exec_()
        return

    if img2 is None:
        alert = QMessageBox()
        alert.setText('128비트 이미지를 선택해주세요.')
        alert.exec_()
        return

    image = Image.open(img2)
    resize(image).save('./resource/128bit.png')
    clips = [ImageClip(f'./resource/{m}').set_duration(1) for m in ['1bit.png', '2bit.png', '4bit.png', '8bit.png']]
    clips.append(ImageClip('./resource/16bit.png').set_duration(1.5))
    clips.append(ImageClip('./resource/32bit.png').set_duration(1.7))
    clips.append(ImageClip('./resource/64bit.png').set_duration(1.6))
    clips.append(ImageClip('./resource/128bit.png').set_duration(1))
    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.audio = AudioFileClip(r"./resource/audio.mp3")
    concat_clip.write_videofile("result.mp4", fps=24)
    
    alert = QMessageBox()
    alert.setText('렌더링 완료 result.mp4가 생성되었습니다.')
    alert.exec_()
btn4.clicked.connect(render)

class MainWindow(QMainWindow):
    def closeEvent(self, e):
        # if not text.document().isModified():
        return
        answer = QMessageBox.question(
            window, None,
            "You have unsaved changes. Save before closing?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )
        if answer & QMessageBox.Save:
            save()
        elif answer & QMessageBox.Cancel:
            e.ignore()

window = MainWindow()
# window.setCentralWidget(text)
window.setCentralWidget(widget)
window.setFixedSize(330, 150)

menu = window.menuBar().addMenu("&파일")
open_action = QAction("&열기")
def open_file():
    alert = QMessageBox()
    alert.setText('그냥 허전해서 넣은 거')
    alert.exec_()
    # global img1
    # path = QFileDialog.getOpenFileName(window, "열기")[0]
    # if path:
    #     text.setPlainText(open(path).read())
    #     img1 = path
open_action.triggered.connect(open_file)
open_action.setShortcut(QKeySequence.Open)
menu.addAction(open_action)

save_action = QAction("&저장")
def save():
    alert = QMessageBox()
    alert.setText('아무 기능 없음')
    alert.exec_()
    # if img1 is None:
    #     save_as()
    # else:
    #     with open(img1, "w") as f:
    #         f.write(text.toPlainText())
    #     text.document().setModified(False)
save_action.triggered.connect(save)
save_action.setShortcut(QKeySequence.Save)
menu.addAction(save_action)

save_as_action = QAction("다른 이름으로 저장") #Save &As...
def save_as():
    alert = QMessageBox()
    alert.setText('아무 기능 없다니까?')
    alert.exec_()
    # global img1
    # path = QFileDialog.getSaveFileName(window, "Save As")[0]
    # if path:
    #     img1 = path
    #     save()
save_as_action.triggered.connect(save_as)
menu.addAction(save_as_action)

close = QAction("&닫기")
close.triggered.connect(window.close)
menu.addAction(close)

help_menu = window.menuBar().addMenu("&도움")
about_action = QAction("&정보")
help_menu.addAction(about_action)
def show_about_dialog():
    text = "<center>" \
           "<h1>64bits Maker</h1>" \
           "&#8291;" \
           "<img src=icon.svg>" \
           "</center>" \
           "<p>Version 1.0.0<br/>" \
           "Copyright &copy; ZERO#5459.</p>"
    QMessageBox.about(window, "About 64bits Maker", text)
about_action.triggered.connect(show_about_dialog)

window.show()
app.exec_()