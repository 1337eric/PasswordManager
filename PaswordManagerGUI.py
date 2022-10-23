import os
import sys
import random
import time
import datetime
import ctypes
import threading
import hashlib
import string
import platform
import glfw
import requests
import OpenGL.GL as gl
import imgui
import json
import base64 as b64
import pyperclip
from imgui.integrations.glfw import GlfwRenderer
from threading import Thread

ShowMainMenu = False
path_to_font = None
opened_state = True
masterKeyEntered = False
showPassword = False

showPasswordsPage = False
addPasswordsPage = False

masterKey = ""

passwordToShow = 0

def encrypt(message):
    lkey=len(masterKey)
    secret=[]
    num=0
    for each in message:
        if num>=lkey:
            num = num % lkey
        secret.append(chr(ord(each)^ord(masterKey[num])))
        num += 1
    return b64.b64encode("".join(secret).encode()).decode()

def decrypt(message):
    leter = b64.b64decode(message.encode()).decode()
    lkey = len(masterKey)
    string = []
    num = 0
    for each in leter:
        if num >= lkey:
            num = num%lkey
        string.append( chr( ord(each)^ord(masterKey[num]) ) )
        num+=1
    return "".join(string)

def genrandompassword(amount):
    characters = string.ascii_letters + string.punctuation + string.digits
    password = "".join(random.choice(characters) for x in range(amount))
    return password

def ColorDownscale(number):
    downscaledNumber = number / 255
    return downscaledNumber


tempPasswordList = []
def showShowPasswordsPage():
    global tempPasswordList, passwordToShow
    i = 0
    with open("PasswordData.json") as passwordDataRawFile:
        passwordDataFormatted = json.load(passwordDataRawFile)
    for entry in passwordDataFormatted:
        i += 1
        if entry not in tempPasswordList:
            tempPasswordList.append(entry)

    imgui.set_cursor_pos((10,50))
    imgui.push_item_width(250)
    clicked, passwordToShow = imgui.listbox("##Passowrds", passwordToShow, tempPasswordList, 15)
    imgui.pop_item_width()

    i = 0
    for entry in passwordDataFormatted:
        if i == int(passwordToShow):
            imgui.set_cursor_pos((280,50))
            decryptedusername = decrypt(passwordDataFormatted[entry]["Email"])
            imgui.text(f"Email/Username: {decryptedusername}")
            imgui.set_cursor_pos((280,70))
            decryptedpassword = decrypt(passwordDataFormatted[entry]["Password"])
            imgui.text(f"Password: {decryptedpassword}")
            imgui.set_cursor_pos((280,90))
            if imgui.button("Copy password to clipboard"):
                pyperclip.copy(decryptedpassword)
                pass
            imgui.set_cursor_pos((280,290))
            if imgui.button(f"Delete {entry}"):
                del passwordDataFormatted[entry]
                with open('PasswordData.json', 'w') as passwordDataRawFile:
                    json.dump(passwordDataFormatted, passwordDataRawFile, indent=4)
                tempPasswordList.remove(entry)
                break
        i += 1
    
    pass

temporarySite = ""
temporaryEmail = ""
temporaryPassword = ""

def showAddPasswordsPage():
    global temporarySite, temporaryEmail, temporaryPassword, passwordToShow
    i = 0
    with open("PasswordData.json") as passwordDataRawFile:
        passwordDataFormatted = json.load(passwordDataRawFile)
    for entry in passwordDataFormatted:
        i += 1
        if entry not in tempPasswordList:
            tempPasswordList.append(entry)
    imgui.set_cursor_pos((10,50))
    imgui.push_item_width(250)
    clicked, passwordToShow = imgui.listbox("##Passowrds", passwordToShow, tempPasswordList, 15)
    imgui.pop_item_width()
    imgui.push_item_width(275)

    imgui.set_cursor_pos((270,50))
    imgui.text("Site Name:")

    imgui.set_cursor_pos((395,50))
    changed, temporarySite = imgui.input_text("##temporarysite", temporarySite, 300)

    imgui.set_cursor_pos((270,75))
    imgui.text("Username / Email:")

    imgui.set_cursor_pos((395,75))
    changed, temporaryEmail = imgui.input_text("##temporaryemail", temporaryEmail, 300)

    imgui.set_cursor_pos((270,100))
    imgui.text("Password:")

    imgui.set_cursor_pos((395,100))
    changed, temporaryPassword = imgui.input_text("##temporarypassword", temporaryPassword, 300)

    imgui.pop_item_width()


    imgui.set_cursor_pos((270,125))
    if imgui.button("Generate Password"):
        temporaryPassword = genrandompassword(random.randint(16,32))

    imgui.set_cursor_pos((400,125))
    if imgui.button("Copy To Clipboard"):
        pyperclip.copy(temporaryPassword)

    imgui.set_cursor_pos((270,150))
    if imgui.button("Add Credentials", width = 125):
        encryptedEmail = encrypt(temporaryEmail)
        encryptedPassword = encrypt(temporaryPassword)
        try:
            with open("PasswordData.json", "r") as passwordDataRawFile:
                passwordDataFormattedJson = json.load(passwordDataRawFile)
                passwordDataFormattedJson[temporarySite] = {}
                passwordDataFormattedJson[temporarySite]["Email"] = encryptedEmail
                passwordDataFormattedJson[temporarySite]["Password"] = encryptedPassword
                try:
                    passwordDataRawFile.close()
                except:
                    pass
            with open('PasswordData.json', 'w') as passwordDataRawFile:
                json.dump(passwordDataFormattedJson, passwordDataRawFile, indent=4)
                try:
                    passwordDataRawFile.close()
                except:
                    pass
        except Exception as e:
            print(e)
            pass
        temporarySite = ""
        temporaryEmail = ""
        temporaryPassword = ""



    pass

def MainMenu():
    global showPasswordsPage, addPasswordsPage
    imgui.set_cursor_pos((10,23))
    if imgui.button("Show Password", width = 125):
        showPasswordsPage = True
        addPasswordsPage = False
    imgui.set_cursor_pos((135,23))
    if imgui.button("Add Password", width = 125):
        showPasswordsPage = False
        addPasswordsPage = True
    pass

def render_frame(impl, window, font):
    global ShowMainMenu, masterKeyEntered, masterKey, showPassword, showPasswordsPage, addPasswordsPage

    glfw.poll_events()
    impl.process_inputs()
    imgui.new_frame()

    gl.glClearColor(0.1, 0.1, 0.1, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    io = imgui.get_io()

    style = imgui.get_style()

    style.colors[imgui.COLOR_BUTTON] = (ColorDownscale(30), ColorDownscale(30), ColorDownscale(30), 1.0)
    style.colors[imgui.COLOR_BUTTON_HOVERED] = (ColorDownscale(80), ColorDownscale(80), ColorDownscale(80), 1.0)
    style.colors[imgui.COLOR_BUTTON_ACTIVE] = (ColorDownscale(100), ColorDownscale(100), ColorDownscale(100), 1.0)
    
    style.colors[imgui.COLOR_HEADER] = (ColorDownscale(100), ColorDownscale(100), ColorDownscale(100), 1.0)

    style.colors[imgui.COLOR_TEXT] = (1.00, 1.00, 1.00, 1.00)
    style.colors[imgui.COLOR_TEXT_DISABLED] = (0.40, 0.40, 0.40, 1.00)
    style.colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.06, 0.06, 0.06, 0.94)
    style.colors[imgui.COLOR_CHILD_BACKGROUND] = (0.10, 0.10, 0.10, 1.00)
    style.colors[imgui.COLOR_POPUP_BACKGROUND] = (0.09, 0.11, 0.11, 1.00)
    style.colors[imgui.COLOR_BORDER] = (0.47, 0.47, 0.47, 0.75)
    style.colors[imgui.COLOR_BORDER_SHADOW] = (1.00, 1.00, 1.00, 0.06)
    style.colors[imgui.COLOR_FRAME_BACKGROUND] = (0.13, 0.13, 0.13, 1.00)
    style.colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED] = (0.42, 0.42, 0.42, 0.40)
    style.colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE] = (0.56, 0.56, 0.56, 0.67)
    style.colors[imgui.COLOR_TITLE_BACKGROUND] = (0.19, 0.19, 0.19, 1.00)
    style.colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE] = (0.22, 0.22, 0.22, 1.00)
    style.colors[imgui.COLOR_TITLE_BACKGROUND_COLLAPSED] = (0.17, 0.17, 0.17, 0.90)
    style.colors[imgui.COLOR_MENUBAR_BACKGROUND] = (0.34, 0.34, 0.34, 1.00)
    style.colors[imgui.COLOR_SCROLLBAR_BACKGROUND] = (0.13, 0.13, 0.13, 0.00)
    style.colors[imgui.COLOR_SCROLLBAR_GRAB] = (0.00, 0.00, 0.00, 1.00)
    style.colors[imgui.COLOR_SCROLLBAR_GRAB_HOVERED] = (0.53, 0.53, 0.53, 1.00)
    style.colors[imgui.COLOR_SCROLLBAR_GRAB_ACTIVE] = (0.76, 0.76, 0.76, 1.00)
    style.colors[imgui.COLOR_CHECK_MARK] = (ColorDownscale(190), ColorDownscale(75), ColorDownscale(255), 1.0)
    style.colors[imgui.COLOR_SLIDER_GRAB] = (ColorDownscale(190), ColorDownscale(75), ColorDownscale(255), 1.0)
    style.colors[imgui.COLOR_SLIDER_GRAB_ACTIVE] = (0.64, 0.64, 0.64, 1.00)
    style.colors[imgui.COLOR_BUTTON] = (0.26, 0.26, 0.26, 1.00)
    style.colors[imgui.COLOR_BUTTON_HOVERED] = (0.46, 0.46, 0.46, 1.00)
    style.colors[imgui.COLOR_HEADER] = (0.38, 0.38, 0.38, 1.00)
    style.colors[imgui.COLOR_HEADER_HOVERED] = (0.47, 0.47, 0.47, 1.00)
    style.colors[imgui.COLOR_HEADER_ACTIVE] = (0.76, 0.76, 0.76, 0.77)
    style.colors[imgui.COLOR_SEPARATOR] = (0.00, 0.00, 0.00, 0.14)
    style.colors[imgui.COLOR_SEPARATOR_HOVERED] = (0.70, 0.67, 0.60, 0.29)
    style.colors[imgui.COLOR_SEPARATOR_ACTIVE] = (0.70, 0.67, 0.60, 0.67)
    style.colors[imgui.COLOR_RESIZE_GRIP] = (0.16078, 0.16078, 0.16078, 0.25)
    style.colors[imgui.COLOR_RESIZE_GRIP_HOVERED] = (0.26, 0.59, 0.98, 0.67)
    style.colors[imgui.COLOR_RESIZE_GRIP_ACTIVE] = (0.26, 0.59, 0.98, 0.95)

    if io.key_ctrl and io.keys_down[glfw.KEY_Q]:
        sys.exit(0)

    imgui.set_next_window_position(-1, -19)
    imgui.set_next_window_size(675, 425)

    imgui.begin("Password Manager", flags=imgui.WINDOW_NO_RESIZE)

    if masterKeyEntered != True:
        imgui.text("Enter your Master Password!")
        imgui.push_item_width(450)
        if showPassword:
            changed, masterKey = imgui.input_text("##masterkey", masterKey, 300)
        else:
            changed, masterKey = imgui.input_text("##masterkey", masterKey, 300, flags=imgui.INPUT_TEXT_PASSWORD)
        imgui.pop_item_width()
        changed, showPassword = imgui.checkbox("Show Password?", showPassword)
        if imgui.button("Enter", width = 100) and len(masterKey) > 0:
            masterKeyEntered = True
            ShowMainMenu = True
            showPasswordsPage = True

    if ShowMainMenu:
        MainMenu()

    if showPasswordsPage:
        showShowPasswordsPage()

    if addPasswordsPage:
        showAddPasswordsPage()

    imgui.end()

    imgui.render()
    impl.render(imgui.get_draw_data())
    glfw.swap_buffers(window)


def impl_glfw_init():
    width, height = 673, 300
    window_name = "Password Manager By Eric"

    if not glfw.init():
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, 0)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        sys.exit(1)

    return window


def main():
    imgui.create_context()
    window = impl_glfw_init()

    impl = GlfwRenderer(window)

    io = imgui.get_io()
    jb = io.fonts.add_font_from_file_ttf(path_to_font, 30) if path_to_font is not None else None
    impl.refresh_font_texture()

    while not glfw.window_should_close(window):
        render_frame(impl, window, jb)

    impl.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()
