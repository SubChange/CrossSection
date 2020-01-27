import base64
open_icon = open("img/logo.jpg","rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "logo = %s" %b64str
f = open("images.py","w+")
f.write(write_data)
f.close()
open_icon = open("img/display.jpg","rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "display = %s" %b64str
f = open("images.py","a+")
f.writelines("\n") 
f.write(write_data)
f.close()

