#!/usr/bin/python3.6
# -*- coding:UTF-8 -*-

import ftplib
import os
import socket

def download_file_by_ftp(remote_host,remote_dir,remote_file,local_dir = ""):
    try:
        ftp = ftplib.FTP(remote_host)
    except (socket.error, socket.gaierror):
        print("ERROR cannot reach '%s'" % remote_host)
        return
    print("..Connected to remote_host '%s'.." % remote_host)

    try:
        ftp.login()  # 使用匿名账号登陆也就是anonymous
    except ftplib.error_perm:
        print("ERROR cannot login anonymously")
        ftp.quit()
        return
    print("...logged in as 'anonymously'...")

    try:
        ftp.cwd(remote_dir)  # 切换当前工作目录
    except ftplib.error_perm:
        print("ERROR cannot cd to '%s'" % remote_dir)
        ftp.quit()
        return
    print("....Changed to '%s' folder...." % remote_dir)
    local_file = local_dir + remote_file
    try:  # 传一个回调函数给retrbinary() 它在每接收一个二进制数据时都会被调用
        ftp.retrbinary("RETR %s" % remote_file, open(local_file, "wb").write)
    except ftplib.error_perm:
        print("ERROR cannot remote_file '%s'" % remote_file)
        #os.remove(local_file)
        os.unlink(remote_file)
    else:
        print(".....Download '%s' to cwd....." % remote_file)
    finally:
        ftp.quit()
        return
