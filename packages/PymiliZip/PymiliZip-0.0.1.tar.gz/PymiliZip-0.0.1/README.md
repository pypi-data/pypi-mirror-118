# 一个基于zipfile的压缩库|A compressed Library Based on zipfile

使用方法在作者的第三方仓库中，可以自行查看
The usage method is in the author's third-party warehouse and can be used by yourself

[codechina.csdn 教程链接|Tutorial links](https://codechina.csdn.net/qq_53280175/pymilizip)


一个基于zipfile的压缩库

导入库：from PymiliZip import milizip

new = milizip.newzip(name,number,file,files,numbers)

new.new_zip#创建一个zip

new.new_zips#创建多个zip

name:创建压缩包的名字如 a.zip

number:压缩文件数量（现在只限添加2个文件）

file:文件路径1

files：文件路径2

numbers:创建文件数量

#----------------------------------------------------------------------

A compressed Library Based on zipfile

导入库：from PymiliZip import milizip

new = milizip.newzip(name,number,file,files,numbers)

new.new_zip#Create a zip

new.new_zips#Create multiple zips

name:Create the name of the compressed package, such as a.zip

number:Number of compressed files (now only 2 files can be added)

file:File path 1

files：File path 2

numbers:Number of files created
