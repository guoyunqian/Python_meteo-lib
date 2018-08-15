from PIL import Image
import os
def get_gif(filenames,gif_file_path):
    im = Image.open(filenames[0])
    im.thumbnail((800, 600), Image.ANTIALIAS)
    images = []
    for i in range(len(filenames)-1):
        im1 = Image.open(filenames[i+1])
        im1.thumbnail((800, 600), Image.ANTIALIAS)
        images.append(im1)
    im.save(gif_file_path, save_all=True, append_images=images, loop=10, duration=0.5, comment=b"aaabb")

files = os.listdir(r"H:\task\project\colleague\201804-baohongjun-qpe\包红军-多源观测实时雨量场构建技术\pic")
filenames = []
for file in files:
    filenames.append(r"H:\task\project\colleague\201804-baohongjun-qpe\包红军-多源观测实时雨量场构建技术\pic\\" + file)
gif_file_path = r"H:\task\project\colleague\201804-baohongjun-qpe\包红军-多源观测实时雨量场构建技术\1小时雨量动画.gif"
get_gif(filenames,gif_file_path)