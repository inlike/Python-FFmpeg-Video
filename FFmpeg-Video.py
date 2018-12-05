# coding=utf-8
import os
import subprocess
import datetime
import json, pprint
import re, time
import threading
import random
import shutil


class FFmpeg:

    def __init__(self, editvdo, addlogo=None, addmusic=None,
                 addvdohead=None, addvdotail=None):
        self.editvdo = editvdo
        self.addlogo = addlogo
        self.addmusic = addmusic
        self.addvdohead = addvdohead
        self.addvdotail = addvdotail
        self.vdo_time, self.vdo_width, self.vdo_height = self.get_attr()
        self.editvdo_path = os.path.dirname(editvdo)
        self.editvdo_name = os.path.basename(editvdo)

    def get_attr(self):
        """
        获取视频属性参数
        :return:
        """
        strcmd = r'ffmpeg -print_format json -show_streams -i "{}"'.format(
                self.editvdo)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        vdo_time = int(re.findall('"duration": "\d{0,5}', str(
            result))[0][13:])  # 获取视频长度
        vdo_width = int(
            re.findall('"width": \d{0,5}', str(result))[0][9:])  # 获取视频宽度
        vdo_height = int(
            re.findall('"height": \d{0,5}', str(result))[0][10:])  # 获取视频高度
        attr = (vdo_time, vdo_width, vdo_height)
        return attr

    def edit_head(self, second, deposit=None):
        """
        去除头部视频
        :param second: 去除开始的多少秒
        :param deposit: 另存为文件
        :return: True/Flase
        """
        if None == deposit:
            deposit = self.editvdo_path+'/'+'edit_head'+self.editvdo_name
        strcmd = 'ffmpeg -i "{}" -ss  10 -t {}  -codec copy "{}"'.format(
            self.editvdo, second, deposit)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE,
                                shell=True)
        if os.path.exists(deposit):
            os.remove(self.editvdo)
            os.rename(deposit, self.editvdo)
            return True
        else:
            return False

    def edit_logo(self, deposit=None):
        """
        添加水印
        :param deposit:添加水印后另存为路径，为空则覆盖
        :return: True/False
        """
        if None == deposit:
            deposit = self.editvdo_path+'/'+'edit_logo'+self.editvdo_name
        strcmd = r'ffmpeg -i "{}" -vf "movie=\'{}\' [watermark];[in] ' \
                 r'[watermark] overlay=main_w-overlay_w-10:10 [out]"  "{}"'.format(
                    self.editvdo, self.addlogo, deposit)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        if os.path.exists(deposit):
            os.remove(self.editvdo)
            os.rename(deposit, self.editvdo)
            return True
        else:
            return False

    def edit_music(self, deposit=None):
        if None == deposit:
            deposit = self.editvdo_path+'/'+'edit_music'+self.editvdo_name
        strcmd = r'ffmpeg -y -i "{}" -i "{}" -filter_complex "[0:a] ' \
                 r'pan=stereo|c0=1*c0|c1=1*c1 [a1], [1:a] ' \
                 r'pan=stereo|c0=1*c0|c1=1*c1 [a2],[a1][a2]amix=duration=first,' \
                 r'pan=stereo|c0<c0+c1|c1<c2+c3,pan=mono|c0=c0+c1[a]" ' \
                 r'-map "[a]" -map 0:v -c:v libx264 -c:a aac ' \
                 r'-strict -2 -ac 2 "{}"'.format(self.editvdo, self.addmusic, deposit)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        if os.path.exists(deposit):
            os.remove(self.editvdo)
            os.rename(deposit, self.editvdo)
            return True
        else:
            return False

    def edit_rate(self, rete=30, deposit=None):
        """
        改变帧率
        :param rete: 修改大小帧率
        :param deposit: 修改后保存路径
        :return:
        """
        if None == deposit:
            deposit = self.editvdo_path+'/'+'edit_music'+self.editvdo_name
        strcmd = r'ffmpeg -i "{}" -r {} "{}"' % (self.editvdo, rete, deposit)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        if os.path.exists(deposit):
            os.remove(self.editvdo)
            os.rename(deposit, self.editvdo)
            return True
        else:
            return False

    def edit_power(self, power='1280x720', deposit=None):
        """
        修改分辨率
        :param power: 分辨率
        :param deposit: 修改后保存路径，为空则覆盖
        :return:
        """
        if None == deposit:
            deposit = self.editvdo_path+'/'+'edit_power'+self.editvdo_name
        strcmd = r'ffmpeg -i "{}" -s {} "{}"'.format(self.editvdo, power, deposit)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        if os.path.exists(deposit):
            os.remove(self.editvdo)
            os.rename(deposit, self.editvdo)
            return True
        else:
            return False

    def rdit_marge(self, vdo_head, vdo_tail, deposit=None):
        if None == deposit:
            deposit = self.editvdo_path+'/'+'rdit_marge'+self.editvdo_name
        with open(self.editvdo_path+'/'+'rdit_marge.txt', 'w', encoding='utf-8') as f:
            f.write("file '{}' \nfile '{}' \nfile '{}'" .format(
                vdo_head, self.editvdo, vdo_tail))
        strcmd = r'ffmpeg -f concat -safe 0 -i "{}" -c copy "{}"'.format(
            self.editvdo_path + '/' + 'rdit_marge.txt', deposit)
        result = subprocess.run(args=strcmd, stdout=subprocess.PIPE, shell=True)
        if os.path.exists(deposit):
            os.remove(self.editvdo)
            os.rename(deposit, self.editvdo)
            return True
        else:
            return False



    # ffmpeg - i input.mkv - filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" - map"[v]" - map"[a]"  output.mkv



test = FFmpeg(r"C:\Users\billl\1.mp4")
pass

