import base64
open_icon = open("img/lo.ico","rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "logo = %s" %b64str
f = open("images.py","w+")
f.write(write_data)
f.close()
open_icon = open("img/SubChangeimg.jpg","rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "SubChangeimg = %s" %b64str
f = open("images.py","a+")
f.writelines("\n") 
f.write(write_data)
f.close()

