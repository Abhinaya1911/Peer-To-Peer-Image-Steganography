# import modules
from tkinter import *
import tkinter.filedialog
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
from io import BytesIO
import os
import socket
import tqdm


class Img_steganography:
    output_image_size = 0

    # Main frame or start page
    def start_page(self, window):
        window.title('ImageSteganography')
        window.geometry('550x600')
        window.resizable(width=False, height=False)
        window.config(bg='#ebedf0') #f7f0f0
        frame = Frame(window, relief='sunken')
        frame.grid(sticky="we")
        frame.grid_rowconfigure(0, weight=0)
        frame.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)
        image = Image.open("sastra.png")
        resize_image = image.resize((250,200))
        img = ImageTk.PhotoImage(resize_image)
        label1 = Label(frame,image=img)
        label1.image = img
        label1.grid(pady=10)   
        label = Label(frame, text="Welcome to \nImage Steganography",
                      font=('Times', 25, 'bold italic'),
                      fg='#0F3460',
                      bg='#A5F1E9')
        label.grid(row=2, column=0)
        label.grid_rowconfigure(1, weight=1)
        label.grid_columnconfigure(1, weight=1)
        button = Button(frame, text="Start",
                        font=('Times', 25, 'bold italic'),
                        command=lambda: self.main_page(frame),
                        fg='#A5F1E9',
                        bg='#0F3460',
                        activeforeground='#A5F1E9',
                        activebackground='black')
        button.grid(row=3, column=0, pady=5)
        label1 = Label(frame, text="By \n Abhinaya.S.S",
                        font=('Times', 25, 'bold italic'),
                        fg='#0F3460',
                        bg='#A5F1E9')
        label1.grid(sticky='SE', padx=50, pady=100)
        button.grid_rowconfigure(1, weight=1)
        button.grid_columnconfigure(1, weight=1)

    #Main Page
    def main_page(self, frame):
        frame.destroy()
        fm = Frame(window)
        label1 = Label(fm, text="Select the Option!!",
                       fg="#0F3460",
                       font=('Times', 25, 'bold italic'),
                       bg='#A5F1E9')
        label1.grid(row=2, pady=10)
        encode_button = Button(fm, text="Encode",
                               font=('Times', 20, 'bold italic'),
                               command=lambda: self.encode_page(fm),
                               fg='#A5F1E9',
                               bg='#0F3460',
                               activeforeground='#A5F1E9',
                               activebackground='#0F3460')
        encode_button.grid(row=3)
        decode_button = Button(fm, text="Decode",
                               font=('Times', 20, 'bold italic'),
                               command=lambda: self.decode_page(fm),
                               fg='#A5F1E9',
                               bg='#0F3460',
                               activeforeground='#A5F1E9',
                               activebackground='#0F3460')
        decode_button.grid(row=4, pady=5)
        send_button = Button(fm, text="Send",
                               command=lambda: self.send_image(fm),
                               font=('Times', 20, 'bold italic'),
                               fg='#A5F1E9',
                               bg='#0F3460',
                               activeforeground='#A5F1E9',
                               activebackground='#0F3460')
        send_button.grid(row=5)
        receive_button = Button(fm, text="Receive",
                               command=lambda: self.rcv_image(fm),
                               font=('Times', 20, 'bold italic'),
                               fg='#A5F1E9',
                               bg='#0F3460',
                               activeforeground='#A5F1E9',
                               activebackground='#0F3460')
        receive_button.grid(row=6,pady=5)
        window.grid_rowconfigure(1, weight=3)
        window.grid_columnconfigure(0, weight=1)
        fm.grid()

    #Send page
    def send_image(self,frame):
        frame.destroy()
        send_frame = Frame(window)
        label6 = Label(send_frame, text="Enter details",
                       fg="#0F3460",
                       font=('Times', 25, 'bold italic'),
                       bg='#A5F1E9')
        label6.grid(row=2)
        label7 = Label(send_frame, text="Enter image name",
                       fg="#0F3460",
                       font=('Times', 20, 'italic'),
                       bg='#A5F1E9')
        label7.grid(row=3,pady=7)
        e1=Entry(send_frame)
        e1.grid(pady=5)
        label8 = Label(send_frame, text="Enter Receiver IP address",
                       fg="#0F3460",
                       font=('Times', 20, 'italic'),
                       bg='#A5F1E9')
        label8.grid(row=5,pady=7)
        e2=Entry(send_frame)
        e2.grid(pady=5)
        send_btn = Button(send_frame, text="Send",
                               command=lambda: self.send_file(e1.get(), e2.get()),
                               font=('Times', 20, 'bold italic'),
                               fg='#A5F1E9',
                               bg='#0F3460',
                               activeforeground='#A5F1E9',
                               activebackground='#0F3460')
        send_btn.grid(row=7)
        cancel_button = Button(send_frame, text="Cancel",
                               font=('Times', 20, 'bold italic'),
                               command=lambda: Img_steganography.go_back(self, send_frame),
                               fg='#A5F1E9',
                               bg='#0F3460',
                               activeforeground='#A5F1E9',
                               activebackground='#0F3460')
        cancel_button.grid(row=8, pady=5)
        send_frame.grid()

    #Sending Process
    def send_file(self, f_name, host):
        SEPARATOR = "<SEPARATOR>"
        f_size = os.path.getsize(f_name)
        port=5001
        soc = socket.socket()
        print(f"[+] Connecting to {host}:{port}")
        soc.connect((host, port))
        print("[+] Connected.")
        soc.send(f"{f_name}{SEPARATOR}{f_size}".encode())
        progress = tqdm.tqdm(range(f_size), f"Sending {f_name}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(f_name, "rb") as f:
            while True:
                byteReader = f.read(1024*4)
                if not byteReader:
                    break
                soc.sendall(byteReader)
                progress.update(len(byteReader))
        soc.close()

    #Receiver Page
    def rcv_image(self,frame):
        frame.destroy()
        rcv_frame = Frame(window)
        label8 = Label(rcv_frame, text="Image received Successfully!!",
                       fg="#0F3460",
                       font=('Times', 25, 'bold italic'),
                       bg='#A5F1E9')
        label8.grid(row=2)
        cancel_button = Button(rcv_frame, text="Cancel",
                               font=('Times', 20, 'bold italic'),
                               command=lambda: Img_steganography.go_back(self, rcv_frame),
                               fg='#A5F1E9',
                               bg='#0F3460',
                               activeforeground='#A5F1E9',
                               activebackground='#0F3460')
        cancel_button.grid(row=8, pady=5)
        SERVER_HOST = "0.0.0.0"
        SERVER_PORT = 5001
        BUFFER_SIZE = 4096
        SEPARATOR = "<SEPARATOR>"
        soc = socket.socket()
        soc.bind((SERVER_HOST, SERVER_PORT))
        soc.listen(5)
        print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
        c_socket, add = soc.accept() 
        print(f"[+] {add} is connected.")
        rcv = c_socket.recv(BUFFER_SIZE).decode()
        f_name, f_size = rcv.split(SEPARATOR)
        f_name = os.path.basename(f_name)
        f_size = int(f_size)
        progress = tqdm.tqdm(range(f_size), f"Receiving {f_name}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(f_name, "wb") as f:
            while True:
                byteReader = c_socket.recv(BUFFER_SIZE)
                if not byteReader:    
                    break
                f.write(byteReader)
                progress.update(len(byteReader))
        c_socket.close()
        soc.close()
        rcv_frame.grid()

    # Back function to loop back to main screen
    def go_back(self, frame):
        frame.destroy()
        self.start_page(window)

    # Frame for encode page
    def encode_page(self, frame1):
        frame1.destroy()
        enc_frame = Frame(window)
        label2 = Label(enc_frame, text=" Pick a Pic!!",
                       fg="#0F3460",
                       font=('Times', 25, 'bold italic'),
                       bg='#A5F1E9')
        label2.grid(row=2, pady=10)
        select_button = Button(enc_frame, text=" Select ",
                               font=('Times', 20, 'bold italic'),
                               command=lambda: self.encode_frame2(enc_frame),
                               fg='#A5F1E9',
                               bg='#0F3460',
                               activeforeground='#A5F1E9',
                               activebackground='#0F3460')
        select_button.grid(row=3)
        cancel_button = Button(enc_frame, text="Cancel",
                               font=('Times', 20, 'bold italic'),
                               command=lambda: Img_steganography.go_back(self, enc_frame),
                               fg='#A5F1E9',
                               bg='#0F3460',
                               activeforeground='#A5F1E9',
                               activebackground='#0F3460')
        cancel_button.grid(row=5, pady=5)
        window.grid_rowconfigure(1, weight=3)
        window.grid_columnconfigure(0, weight=1)
        enc_frame.grid()

    # Frame for decode page
    def decode_page(self, frame2):
        frame2.destroy()
        dec_frame = Frame(window)
        label2 = Label(dec_frame, text=" Pick a Pic!!",
                       fg="#0F3460",
                       font=('Times', 25, 'bold italic'),
                       bg='#A5F1E9')
        label2.grid(row=2, pady=10)
        select_button = Button(dec_frame, text=" Select ",
                               font=('Times', 20, 'bold italic'),
                               command=lambda: self.decode_frame2(dec_frame),
                               fg='#A5F1E9',
                               bg='#0F3460',
                               activeforeground='#A5F1E9',
                               activebackground='#0F3460')
        select_button.grid(row=3)
        cancel_button = Button(dec_frame, text="Cancel",
                               font=('Times', 20, 'bold italic'),
                               command=lambda: Img_steganography.go_back(self, dec_frame),
                               fg='#A5F1E9',
                               bg='#0F3460',
                               activeforeground='#A5F1E9',
                               activebackground='#0F3460')
        cancel_button.grid(row=5, pady=5)
        window.grid_rowconfigure(1, weight=3)
        window.grid_columnconfigure(0, weight=1)
        dec_frame.grid()

    # Function to encode image
    def encode_frame2(self, frame3):
        enc_frame2 = Frame(window)
        myfile = tkinter.filedialog.askopenfilename(
            filetypes=(('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')))
        if not myfile:
            messagebox.showerror("Error", "You haven't selected anything !!")
        else:
            my_img = Image.open(myfile)
            new_image = my_img.resize((250, 200))
            img = ImageTk.PhotoImage(new_image)
            label2 = Label(enc_frame2, text="Selected Image",
                           fg="#0F3460",
                           font=('Times', 25, 'bold italic'),
                           bg='#A5F1E9')
            label2.grid()
            board = Label(enc_frame2, image=img)
            board.image = img
            self.output_image_size = os.stat(myfile)
            self.o_image_w, self.o_image_h = my_img.size
            board.grid(pady=5)
            label3 = Label(enc_frame2, text="Enter the message",
                           fg="#0F3460",
                           font=('Times', 25, 'bold italic'),
                           bg='#A5F1E9')
            label3.grid(pady=5)
            text_a = Text(enc_frame2, width=50, height=10)
            text_a.grid()
            encode_button = Button(enc_frame2, text="Encode",
                                   font=('Times', 20, 'bold italic'),
                                   command=lambda: [self.enc_fun(text_a, my_img), Img_steganography.go_back(self, enc_frame2)],
                                   fg='#A5F1E9',
                                   bg='#0F3460',
                                   activeforeground='#A5F1E9',
                                   activebackground='#0F3460')
            encode_button.grid(pady=5)
            cancel_button = Button(enc_frame2, text="Cancel",
                                   font=('Times', 20, 'bold italic'),
                                   command=lambda: Img_steganography.go_back(self, enc_frame2),
                                   fg='#A5F1E9',
                                   bg='#0F3460',
                                   activeforeground='#A5F1E9',
                                   activebackground='#0F3460')
            cancel_button.grid()
            enc_frame2.grid(row=1)
            frame3.destroy()

    # Function to decode image
    def decode_frame2(self, frame4):
        dec_frame2 = Frame(window)
        myfiles = tkinter.filedialog.askopenfilename(
            filetypes=(('png', '*.png'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('All Files', '*.*')))
        if not myfiles:
            messagebox.showerror("Error", "You have selected nothing! ")
        else:
            my_img = Image.open(myfiles, 'r')
            my_image = my_img.resize((250, 200))
            img = ImageTk.PhotoImage(my_image)
            label4 = Label(dec_frame2, text="Selected Image",
                           fg="#0F3460",
                           font=('Times', 25, 'bold italic'),
                           bg='#A5F1E9')
            label4.grid()
            board = Label(dec_frame2, image=img)
            board.image = img
            board.grid()
            hidden_data = self.decode(my_img)
            label5 = Label(dec_frame2, text="Hidden Message is: ",
                           fg="#0F3460",
                           font=('Times', 25, 'bold italic'),
                           bg='#A5F1E9')
            label5.grid(pady=10)
            text_a = Text(dec_frame2, width=50, height=10)
            text_a.insert(INSERT, hidden_data)
            text_a.configure(state='disabled')
            text_a.grid()
            cancel_button = Button(dec_frame2, text="Cancel",
                                   font=('Times', 20, 'bold italic'),
                                   command=lambda: self.frame_3(dec_frame2),
                                   fg='#A5F1E9',
                                   bg='#0F3460',
                                   activeforeground='#A5F1E9',
                                   activebackground='#0F3460')
            cancel_button.grid(pady=15)
            dec_frame2.grid(row=1)
            frame4.destroy()

    # Function to decode data
    def decode(self, image):
        image_data = iter(image.getdata())
        data = ''

        while (True):
            pixels = [value for value in image_data.__next__()[:3] +
                      image_data.__next__()[:3] +
                      image_data.__next__()[:3]]
            binary_str = ''
            for i in pixels[:8]:
                if i % 2 == 0:
                    binary_str += '0'
                else:
                    binary_str += '1'

            data += chr(int(binary_str, 2))
            if pixels[-1] % 2 != 0:
                return data

    # Function to generate data
    def generate_Data(self, data):
        new_data = []

        for i in data:
            new_data.append(format(ord(i), '08b'))
        return new_data

    # Function to modify the pixels of image
    def modify_Pix(self, pix, data):
        dataList = self.generate_Data(data)
        dataLen = len(dataList)
        imgData = iter(pix)
        for i in range(dataLen):
            # Extracting 3 pixels at a time
            pix = [value for value in imgData.__next__()[:3] +
                   imgData.__next__()[:3] +
                   imgData.__next__()[:3]]

            for j in range(0, 8):
                if (dataList[i][j] == '0') and (pix[j] % 2 != 0):
                    if (pix[j] % 2 != 0):
                        pix[j] -= 1

                elif (dataList[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1

            if (i == dataLen - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1

            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    # Function to enter the data pixels in image
    def encode_enc(self, newImg, data):
        w = newImg.size[0]
        (x, y) = (0, 0)

        for pixel in self.modify_Pix(newImg.getdata(), data):

            # Putting modified pixels in the new image
            newImg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1

    # Function to enter hidden text
    def enc_fun(self, text_a, myImg):
        data = text_a.get("1.0", "end-1c")
        if len(data) == 0:
            messagebox.showinfo("Alert", "Kindly enter text in TextBox")
        else:
            newImg = myImg.copy()
            self.encode_enc(newImg, data)
            my_file = BytesIO()
            temp = os.path.splitext(os.path.basename(myImg.filename))[0]
            newImg.save(tkinter.filedialog.asksaveasfilename(initialfile=temp, filetypes=([('png', '*.png')]),
                                                             defaultextension=".png"))
            self.d_image_size = my_file.tell()
            self.d_image_w, self.d_image_h = newImg.size
            messagebox.showinfo("Success",
                                "Successfully Encoded\nFile is saved as an Image with hiddentext.png in the selected directory")

    def frame_3(self, frame):
        frame.destroy()
        self.start_page(window)


# GUI loop
window = Tk()
o = Img_steganography()
o.start_page(window)
window.mainloop()
