import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract
import os
from reportlab.pdfgen import canvas
from translate import Translator

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class OCRApp : 
    def __init__(self, root) :
        self.root = root
        self.root.title("OCR 일본어 이미지 번역기")

        # 이미지 불러오기 프레임
        self.image_frame = tk.Frame(root, padx=10, pady=10)
        self.image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.image_frame, text="이미지를 업로드하세요")
        self.label.pack()

        self.upload_button = tk.Button(self.image_frame, text="이미지 업로드", command=self.upload_image)
        self.upload_button.pack()

        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack()

        # 텍스트 변환 프레임
        self.text_frame = tk.Frame(root, padx=10, pady=10)
        self.text_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text_label = tk.Label(self.text_frame, text="번역된 텍스트")
        self.text_label.pack()

        self.text_area = tk.Text(self.text_frame, wrap='word', width=50, height=15)
        self.text_area.pack()

        self.save_button = tk.Button(self.text_frame, text="저장", command=self.save_text)
        self.save_button.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.image.thumbnail((400, 400))
            self.img = ImageTk.PhotoImage(self.image)
            self.image_label.config(image=self.img)
            self.extract_text(file_path)

    def extract_text(self, image_path):
        try:
            text = pytesseract.image_to_string(Image.open(image_path), lang='jpn')
            translator = Translator(from_lang='ja', to_lang='ko')
            translation = translator.translate(text.replace(" ", ""))
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, translation)
        except pytesseract.TesseractError as e:
            messagebox.showerror("OCR 오류", f"OCR 처리 중 오류가 발생했습니다 : {e}")

    def save_text(self):
        file_types = [("Text file", "*.txt"), ("PDF file", "*.pdf")]
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=file_types)
        if file_path:
            text = self.text_area.get(1.0, tk.END)
            if file_path.endswith('.txt'):
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(text)
            elif file_path.endswith('.pdf'):
                pdf = canvas.Canvas(file_path)
                pdf.drawString(100, 750, text)
                pdf.save()
            messagebox.showinfo("저장 완료", "파일이 성공적으로 저장되었습니다.")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
