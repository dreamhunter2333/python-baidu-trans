# -*- coding: utf-8 -*-

__author__ = 'jinmu333'

from tkinter import *
from multiprocessing import Process
import tkinter.messagebox as messagebox
import socket
import threading,time
import urllib,hashlib
import random
import requests,sys

def getTransText(in_text):
	q = in_text
	fromLang = 'auto'  #翻译源语言=自动检测
	toLang1 = 'auto'    #译文语言 = 自动检测

	appid = '20171015000088315' #APP ID
	salt = random.randint(32768, 65536)
	secretKey = 'mjnCecEKmR4iDwimJINc' #密钥

    #生成sign
	sign = appid+q+str(salt)+secretKey
	#计算签名sign(对字符串1做md5加密，注意计算md5之前，串1必须为UTF-8编码)
	m1 = hashlib.md5(sign.encode('utf-8'))
	sign = m1.hexdigest()
     
    #计算完整请求
	myurl = '/api/trans/vip/translate'
	myurl = myurl+'?appid='+appid+'&q='+q+'&from='+fromLang+'&to='+toLang1+'&salt='+str(salt)+'&sign='+sign
	url = "http://api.fanyi.baidu.com"+myurl

    # 发送请求
	url = url.encode('utf-8')
	res = requests.get(url)

	#转换为字典类型
	res = eval(res.text)
	return (res["trans_result"][0]['dst'])

root = Tk()
root.title("翻译 by jinmu333")
root.geometry('400x500')                 #是x 不是*
root.resizable(width=True, height=True) #宽不可变, 高可变,默认为True
l = Label(root, text="更多软件加qq2544236134", font=("Arial", 9), width=20)
l.pack(side=BOTTOM)    
t = Text()
t.pack()
t.insert('1.0', "此处显示历史翻译内容\n")
var = StringVar()
e = Entry(root, textvariable = var)
var.set('此处显示最新翻译内容')
e.pack()
class Application(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		self.nameInput = Entry(self)
		self.nameInput.bind('<Key-Return>',self. hello)
		self.nameInput.pack()
		self.alertButton = Button(self, text='一键翻译', command=self.hello,width = 20,height = 2,bd = 2)
		self.alertButton.pack()
    
	def hello(self,event):
		in_text = self.nameInput.get() or '请输入需要翻译的内容'
		data=getTransText(in_text)
		print (in_text+'  =  '+data)
		var.set(data)
		t.insert('1.0', "-------------------------------------------------------\n")
		t.insert('1.0', "翻译: %s\n" %data)
		t.insert('1.0', "原文: %s\n" %in_text)
app = Application()
    
# 主消息循环:
app.mainloop()