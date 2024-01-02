# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 15:33:03 2024

@author: Ahsan
"""


"""
Media player to play media content, with an additional option to download the content 
from social media i.e. Youtube
Added functinons:
    i.      load source media from folder      [btn --> load content] 
    ii.     input url of media                 [btn --> Enter url]
    iii.    download media from the proved url     [btn --> Download]
    iv.     Created source video display widget
"""

from PyQt5.QtWidgets import (QInputDialog, QApplication, QPushButton, QLabel, 
                             QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, 
                             QStyle, QSlider)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtCore
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
import os


# label = ""
f_name = [0]
f_nm_targ = [0]

# flag to obtain the downloading file size
url_lnk_size = 0 
tot_size = 0
vid_addrs = ''
# list for store the title od downloaded contents
lst = []


# # object for downloading stream from youtube
# class vid_dwnld(QtCore.QObject):
#     # dwnld_status_flg = QtCore.pyqtSignal(int)
#     def __init__(self, parent = None):
#         super().__init__(parent)
#         # self.dwnld_status_flg = dwnld_status_flg
#         # self.dwnld(self.dwnld_status_flg)

#     # function to for downloading the stream
#     def dwnld(self):
#         global url_lnk_size, vid_addrs, lst
#         # url = YouTube('https://www.youtube.com/watch?v=p3tSLatmGvU',
#         #               on_progress_callback = progress_func,
#         #               on_complete_callback = complete_func,
#         #               proxies = my_proxies,
#         #               use_oauth = False,
#         #               allow_oauth_cache = True
#         #               )
        
#         try:
#             url_lnk_size = 0
            
#             # url = YouTube('https://www.youtube.com/watch?v=p3tSLatmGvU')
            
#             # set the url for Youtube object (i.e. from pytube module)
#             url = YouTube(vid_addrs)
#             # register the progress status of youtube object for downloaded stream
#             # by calling the prog function
#             url.register_on_progress_callback(self.prog_func)    
            
#             print('Title: ', url.title)
#             print('Views: ', url.views)
            
#             # get title from url 
#             Title = url.title
            
#             # -----------------------------------------------------------------
#             # Removing the special character from the title of stream 
            
#             new_title = []
#             # loop for getting characters of the title and check if the character
#             # acquired is special case or not, by function [isalnum] 'is alpha-numeric'
#             for ch in Title:
#                 if ch.isalnum():
#                     new_title.append(ch)
#             # remove the space between words of the title and appending the ".mp4" file format
#             New_title = "".join(new_title) + str(".mp4")
            
#             # array for storing the titles of all the downloaded streams
#             lst.append(str(New_title))
#             print("LIST:", lst)
            
#             # -----------------------------------------------------------------

#         # if the sream from url is unavailable then raise the exception error            
#         except VideoUnavailable:
#             print(f'Error while downloading content from {url}')
#         # if no error then download the stream
#         else:
#             vid = url.streams.get_highest_resolution()
      
#             vid.download(filename = New_title)
#             print("Downloaded Successfully")
#             # dwnld_status_flg.emit(1)
    
#     # function for manipulating the received bytes of the stream and calculate percentge
#     def prog_func(self, stream, chunk, bytes_remaining):
#         global url_lnk_size, tot_size
#         print("Bytes remain",bytes_remaining)
#         if url_lnk_size == 0:
#             tot_size = stream.filesize
#             print("Tot_size",tot_size)
#             url_lnk_size = 1
    
#         dwnld_per = int((tot_size - bytes_remaining)/tot_size * 100)
#         print("Download percentage: ", dwnld_per)
        

# label = QLabel("Please load content!!!")    

# main widget for PyQt GUI
class GUI_disp(QWidget):
    # global label

    def __init__(self, parent = None):
        super().__init__(parent)
        # initilizing label for displaying the message for the uploaded content
        # and the downloaded stream
        self.label = QLabel("Please load content!!!")

        label1 = QLabel("ADD the video display here...")
        
        self.setWindowTitle("Media Box")
        
        # *********************************************************************
        # --------------------- Source Media Stream Widget --------------------
        self.mediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        video_widget = QVideoWidget()
        
        self.play_btn = QPushButton()
        self.play_btn.setEnabled(False)
        self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_btn.clicked.connect(self.play_vid)
        
        
        self.slider = QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.setposition)
        # vid_widgt = QVBoxLayout()
        # vid_widgt.addWidget(video_widget)
        # vid_widgt.addWidget(self.play_btn)
        
        hor = QHBoxLayout()
        hor.addWidget(self.play_btn)
        hor.addWidget(self.slider)
        
        vert = QVBoxLayout()
        vert.addWidget(video_widget)
        # vert.addWidget(label1)
        vert.addLayout(hor)

        self.mediaplayer.setVideoOutput(video_widget)        

        self.mediaplayer.stateChanged.connect(self.med_state_changed)
        self.mediaplayer.positionChanged.connect(self.s_position)
        self.mediaplayer.durationChanged.connect(self.duration)
        # *********************************************************************
        

        
        self.button1 = QPushButton("Load content...")
        # button1.clicked.connect(pressed)
        self.button1.clicked.connect(self.get_file)
        label2 = QLabel("Show the Edited video here...")
        self.button2 = QPushButton("Exit Player")
        # button2.clicked.connect(released)
        self.button2.clicked.connect(self.exit_player)



        self.button3 = QPushButton("Download")
        self.button3.clicked.connect(self.vid_dld)

        # ______________________________________________________

        # button to enter url
        self.btn1 = QPushButton("Enter URL")
        self.btn1.clicked.connect(self.gettext)

        layout = QHBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.btn1)
        layout.addWidget(self.button3)
        layout.addWidget(self.button2)
        
        # Creating vertical layout
        f_layout = QVBoxLayout()
        # Add widgets to the defined layout
        f_layout.addWidget(label1)
        f_layout.addLayout(vert)
        f_layout.addLayout(layout)
        f_layout.addWidget(self.label)

    
        self.setLayout(f_layout)


    def vid_dld(self):
        # self.video = vid_dwnld()
        # self.video = vid_dwnld()
        # self.video.dwnld.connect(self.stat)
        
        global url_lnk_size, vid_addrs, lst
        # url = YouTube('https://www.youtube.com/watch?v=p3tSLatmGvU',
        #               on_progress_callback = progress_func,
        #               on_complete_callback = complete_func,
        #               proxies = my_proxies,
        #               use_oauth = False,
        #               allow_oauth_cache = True
        #               )
        
        try:
            url_lnk_size = 0
            
            # url = YouTube('https://www.youtube.com/watch?v=p3tSLatmGvU')
            
            # set the url for Youtube object (i.e. from pytube module)
            url = YouTube(vid_addrs)
            # register the progress status of youtube object for downloaded stream
            # by calling the prog function
            url.register_on_progress_callback(self.prog_func)    
            
            print('Title: ', url.title)
            print('Views: ', url.views)
            
            # get title from url 
            Title = url.title
            
            # -----------------------------------------------------------------
            # Removing the special character from the title of stream 
            
            new_title = []
            # loop for getting characters of the title and check if the character
            # acquired is special case or not, by function [isalnum] 'is alpha-numeric'
            for ch in Title:
                if ch.isalnum():
                    new_title.append(ch)
            # remove the space between words of the title and appending the ".mp4" file format
            New_title = "".join(new_title) + str(".mp4")
            
            # array for storing the titles of all the downloaded streams
            lst.append(str(New_title))
            print("LIST:", lst)
            
            # -----------------------------------------------------------------

        # if the sream from url is unavailable then raise the exception error            
        except VideoUnavailable:
            print(f'Error while downloading content from {url}')
        # if no error then download the stream
        else:
            vid = url.streams.get_highest_resolution()
      
            vid.download(filename = New_title)
            print("Downloaded Successfully")
            # dwnld_status_flg.emit(1)
            
            self.mediaplayer.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(New_title)))
            self.play_btn.setEnabled(True)
    
    # function for manipulating the received bytes of the stream and calculate percentge
    def prog_func(self, stream, chunk, bytes_remaining):
        global url_lnk_size, tot_size
        print("Bytes remain",bytes_remaining)
        if url_lnk_size == 0:
            tot_size = stream.filesize
            print("Tot_size",tot_size)
            url_lnk_size = 1
    
        dwnld_per = int((tot_size - bytes_remaining)/tot_size * 100)
        print("Download percentage: ", dwnld_per)
    
    def stat(self):
        self.label.setText("downloaded")


    # *************************************************************************
    # ------------------ Source Media Stream Widget Function ------------------
    # function for selecting the source file you want to open from the pc
    def get_file(self):
        global f_name
        f_name,_ = QFileDialog.getOpenFileName(self, 'Open Video')
        self.label.setText("Content uploaded successfully...")
        print("file opened.........")
        print("file name: ", f_name)
        
        # *********************************************************************
        if f_name != '':
            self.mediaplayer.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(f_name)))
            self.play_btn.setEnabled(True)
        # *********************************************************************
        
    def play_vid(self):
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.mediaplayer.pause()
        else:
            self.mediaplayer.play()
    
    def s_position(self, position):
        self.slider.setValue(position)
    
    def setposition(self, position):
        self.mediaplayer.setPosition(position)
    
    def med_state_changed(self, state):
        if self.mediaplayer.state() == QMediaPlayer.PlayingState:
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_btn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
    
    def duration(self, duration):
        self.slider.setRange(0, duration)
    # *************************************************************************

    # getting url of the content from user
    def gettext(self):
        global vid_addrs
        vid_addrs, done = QInputDialog.getText(self, 'Content URl', 'Enter url:') 
        if done:
            self.label.setText("url added: " + str(vid_addrs))
            print("url_string: ", vid_addrs)

    def exit_player(self):
        os._exit(0)

def main():
    # initiate GUI instance
    app = QApplication([])

    display = GUI_disp()
    display.resize(680,480)
    display.show()

    app.exec_()


if __name__ == "__main__":
    main()