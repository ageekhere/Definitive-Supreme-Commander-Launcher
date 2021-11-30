"""
Definitive Supreme Commander Launcher 1.03

Created by
ageekhere

Suported games
-----------------------------
Supreme Commander
Forged Alliance
Supreme Commander(Steam)
Forged Alliance(Steam)
Forged Alliance Forever
Downlord's FAF Client
Forged Alliance LOUD
FAF Map Editor
Supreme Commander 2
Supreme Commander 2(Steam)
Planetary Annihilation
Total Annihilation
Total Annihilation Forever
Total Annihilation Escalation
Total Annihilation Mayhem
Total Annihilation ProTA
Total Annihilation Twilight
Total Annihilation Zero
Zero-K
Beyond All Reason
-----------------------------
"""
import tkinter
from tkinter import *
import sys, string, os
from PIL import ImageTk, Image
from configparser import ConfigParser
from pathlib import Path
from functools import partial
import subprocess as subCall
from tkinter.filedialog import askopenfilename
import ctypes

launcherName = "Definitive Supreme Commander Launcher"
version = "1.03" #version of launcher
scriptVersion = "1.10" #version of script
userData = ConfigParser() #New ConfigParser to reference an INI file
my_config = Path("./config/config.ini") #Relative path to INI file
if my_config.is_file(): #Check if the INI file exists
    userData.read("./config/config.ini") #read the INI file to load data
else: #set the defaults of the INI file if the file does not exists
    userData["USERINFO"] = {
    "scSteamEnabled": "0",
    "scSteamPath": r"steam://rungameid/9350",
    "scfaSteamEnabled": "0",
    "scfaSteamPath": r"steam://rungameid/9420",
    "scEnabled": "0",
    "scPath": r"C:\SupremeCommander.exe",
    "scfaEnabled": "0",
    "scfaPath": r"C:\ForgedAlliance.exe",
    "fafEnabled": "0",
    "fafPath": r"C:\ProgramData\FAForever\bin\ForgedAlliance.exe",
    "downlordClientEnabled": "0",
    "downlordClientPath": r"C:\Downlord's FAF Client\downlords-faf-client.exe",
    "loudEnabled": "0",
    "loudPath": r"C:\LOUD\SCFA_Updater.exe",
    "mapeditorEnabled": "0",
    "mapedirorscPath": r"C:\FAForeverMapEditor\FAForeverMapEditor.exe",
    "paSteamEnabled": "0",
    "paSteamPath": r"steam://rungameid/386070",
    "sc2SteamEnabled":"0",
    "sc2SteamPath": r"steam://rungameid/40100",
    "sc2Enabled":"0",
    "sc2Path": r"C:\SupremeCommander2.exe",
    "taforeverEnabled":"0", 
    "taforeverPath": r"C:\Downlord's TAF Client\downlords-taf-client",
    "taSteamEnabled":"0",
    "taSteamPath":r"steam://rungameid/298030",
    "taEnabled":"0",
    "taPath":r"C:\TotalA.exe",
    "taEscalationEnabled":"0",
    "taEscalationPath": r"C:\TotalA.exe",
    "taMayhemEnabled":"0",
    "taMayhemPath": r"C:\totala.exe",
    "taProTAEnabled":"0",
    "taProTAPath": r"C:\TotalA.exe",
    "taTwilightEnabled":"0",
    "taTwilightPath": r"C:\totala.exe",
    "taZeroEnabled":"0",
    "taZeroPath": r"C:\TotalA.exe",
    "barEnabled":"0",
    "barPath": r"C:\Beyond-All-Reason.exe",
    "ZerokEnabled":"0",
    "ZerokPath": r"steam://rungameid/334920",
    "lockCursorEnabled": "1",
    "autoSetMonitorEnabled": "1",
    "autoSetDualScreenEnabled": "0",
    }
    #Write the above default settings to the INI file
    with open('./config/config.ini', 'w') as conf: 
        userData.write(conf)
    userData.read("./config/config.ini") #Read the ini file

userinfo = userData["USERINFO"] #Store the INI settings information
window = Tk() #Create the main window interface
window.title(launcherName + " - " + version) #Set the title of the window

p1 = PhotoImage(file = 'data\dscl.png')
window.iconphoto(False, p1)

#window.iconbitmap(r"data\dscl.ico")

#Fixes DPI scaling issues
awareness = ctypes.c_int()
errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
success = ctypes.windll.user32.SetProcessDPIAware()

#set the size and position of the main window
w = 1110 # width for the Tk root
h = 720 # height for the Tk root
x = (w/3) #Center the main window
y = (h/6)
window.geometry('%dx%d+%d+%d' % (w, h, x, y)) #set window size and location
window['background']='#1A1A1A' #Set background color
window.resizable(0,0) #disable window maximize

#Creates a file menu
my_menu=Menu(window)
window.config(menu=my_menu)

#global variables
gameLinkArray = []
interfaceRow = 0
interfaceCol = 0
settingsRow = 0
settingsCol = 0

#When active Popen to the AHK script with parameters
def supremeCommanderSteamClick():
    subCall.Popen(["scripts/AutoHotkeyU32.exe", "scripts/main.ahk","steamSC",userinfo["scSteamPath"],
    userinfo["lockCursorEnabled"],userinfo["autoSetMonitorEnabled"],userinfo["autoSetDualScreenEnabled"],"SupremeCommander.exe"])

def supremeCommanderFaSteamClick():
    subCall.Popen(["scripts/AutoHotkeyU32.exe", "scripts/main.ahk","steamFAF",userinfo["scfaSteamPath"],
    userinfo["lockCursorEnabled"],userinfo["autoSetMonitorEnabled"],userinfo["autoSetDualScreenEnabled"],"SupremeCommander.exe"])

def supremeCommanderClick():
    startGame(userinfo["scPath"],"sc")

def supremeCommanderFaClick():
    startGame(userinfo["scfaPath"],"fa")

def ForgedAllianceForeverClick():
    startGame(userinfo["fafPath"],"faf")

def downlordsClientClick():
    startGame(userinfo["downlordClientPath"],"client")

def loudClick():
    startGame(userinfo["loudPath"],"loud")

def fafMapEditorClick():
    startGame(userinfo["mapedirorscPath"],"mapeditor")

def taforeverClick():
    startGame(userinfo["taforeverPath"],"taforever")

def sc2Click():
    startGame(userinfo["sc2Path"],"sc2")

def sc2SteamClick():
    subCall.Popen(["scripts/AutoHotkeyU32.exe", "scripts/main.ahk","sc2Steam",userinfo["sc2SteamPath"],
    userinfo["lockCursorEnabled"],userinfo["autoSetMonitorEnabled"],userinfo["autoSetDualScreenEnabled"],"SupremeCommander2.exe"])

def taSteamClick():
    subCall.Popen(["scripts/AutoHotkeyU32.exe", "scripts/main.ahk","taSteam",userinfo["taSteamPath"],
    userinfo["lockCursorEnabled"],userinfo["autoSetMonitorEnabled"],userinfo["autoSetDualScreenEnabled"],"TotalA.exe"])

def taClick():
    startGame(userinfo["taPath"],"ta")

def taEscClick():
    startGame(userinfo["taEscalationPath"],"taEscalation")

def taMayClick():
    startGame(userinfo["taMayhemPath"],"taMay")

def taProClick():
    startGame(userinfo["taProTAPath"],"taPro")

def taTwiClick():
    startGame(userinfo["taTwilightPath"],"taTwilight")

def taZeroClick():
    startGame(userinfo["taZeroPath"],"taZero")

def zerokClick():
    subCall.Popen(["scripts/AutoHotkeyU32.exe", "scripts/main.ahk","ZeroK",userinfo["ZerokPath"],
    userinfo["lockCursorEnabled"],userinfo["autoSetMonitorEnabled"],userinfo["autoSetDualScreenEnabled"],"Zero-K.exe"])

def barClick():
    startGame(userinfo["barPath"],"bar")

def paSteamClick():
    subCall.Popen(["scripts/AutoHotkeyU32.exe", "scripts/main.ahk","paSteam",userinfo["paSteamPath"],
    userinfo["lockCursorEnabled"],userinfo["autoSetMonitorEnabled"],userinfo["autoSetDualScreenEnabled"],"PA.exe"])

def startGame(path,name):
    gameLocation = r'%s' %path
    gameExe = gameLocation.split('\\')[-1]
    fixedGameLocation = gameLocation.replace(gameExe, "", 1)
    subCall.Popen(["scripts/AutoHotkeyU32.exe", "scripts/main.ahk",name,fixedGameLocation,
    userinfo["lockCursorEnabled"],userinfo["autoSetMonitorEnabled"],userinfo["autoSetDualScreenEnabled"],gameExe])

#new interface canvas
interface = Canvas(window, bg="#1A1A1A", height=h, width=w-22,confine = True)
home_scroll_y = Scrollbar(interface, orient="vertical", command=interface.yview,bg="#1A1A1A") #Scrollbar
interface.configure(yscrollcommand=home_scroll_y.set) #Configure interface to use scrollbar
    
homeContainer = Frame(interface) #New frame
homeCanvas = Canvas(homeContainer,width= w-22,height=h,bg="#1A1A1A") #New Canvas
homeScrollbar = Scrollbar(homeContainer, orient="vertical", command=homeCanvas.yview) #New scrollbar
homeScrollable_frame = Frame(homeCanvas,bg="#1A1A1A") #New frame
#Scrollable frame for interface
homeScrollable_frame.bind(
    "<Configure>",
    lambda e: homeCanvas.configure(
        scrollregion=homeCanvas.bbox("all")
    )
)
homeCanvas.create_window((0, 0), window=homeScrollable_frame, anchor="nw") #new window
homeCanvas.configure(yscrollcommand=homeScrollbar.set) #configure scrollbar
#Add the new interface items
homeContainer.pack()
homeCanvas.pack(side="left", fill="both", expand=True)
homeScrollbar.pack(side="right", fill="y")
interface.pack()

#Mouse Scroll funcations
def _bound_to_mousewheelHome(event):
    homeCanvas.bind_all("<MouseWheel>", _on_mousewheelHome)   

def _unbound_to_mousewheelHome(event):
    homeCanvas.unbind_all("<MouseWheel>") 

def _on_mousewheelHome(event):
    homeCanvas.yview_scroll(int(-1*(event.delta/120)), "units")

homeCanvas.bind_all("<MouseWheel>", _on_mousewheelHome)
homeCanvas.bind('<Enter>', _bound_to_mousewheelHome)
homeCanvas.bind('<Leave>', _unbound_to_mousewheelHome)

#Function, Creates the game buttons for the interface
def interfaceCreateGameButton(link,fcommand,labelText,gameEnable):
    if userinfo[gameEnable] == "0":
        return #skip game if not enabled
    global interfaceRow,interfaceCol #Global
    imageName = Image.open(link) #open a new image at the link address
    mW, mH = imageName.size #read image size
    mH = int((mH*0.55)) #set image height
    hpercent = (mH / float(imageName.size[1])) #find height percent
    mW = int((float(imageName.size[0]) * float(hpercent))) #set width to scale with height
    imageName = imageName.resize((mW,mH),Image.ANTIALIAS) #resize the image   
    imageName = ImageTk.PhotoImage(imageName) #create a new PhotoImage of imageName after the resize 
    label = tkinter.Label(image=imageName) #create a label with the image
    label.image = imageName #set the label image
    imageButton = Button(homeScrollable_frame, image=imageName, width=mW, height=mH,command=fcommand,bd=0,highlightthickness=0 ) #Make a image button
    #make a grid with 3 columns
    if interfaceCol > 2:
        interfaceCol = 0
        interfaceRow = interfaceRow + 2
    interfaceCol = interfaceCol + 1
    image1label = Label(homeScrollable_frame,bg="#1A1A1A",fg="#FFF", text = labelText) #Create a new label to act as a title for the image button
    image1label.config(font =("Orbitron", 14), )#Set the font of the Label
    image1label.grid(row=interfaceRow,column=interfaceCol) #add lable as grid
    imageButton.grid(row=interfaceRow+1,column=interfaceCol,padx=30, pady=10) #add button as grid
    interface.config(scrollregion=interface.bbox(ALL)) #configure the scroll region 

#Function, create the main interface
def createInterface(): 
    #reset the col and row number
    global interfaceRow
    global interfaceCol
    interfaceRow = 0
    interfaceCol = 0
    #delete all content form the homeScrollable_frame
    for widget in homeScrollable_frame.winfo_children():
        widget.destroy()
    #Add images to interface,interfaceCreateGameButton(string image location, function click, string name, string enabled)
    interfaceCreateGameButton(r"data\scSteam.png",supremeCommanderSteamClick,"Supreme Commander Steam","scSteamEnabled") #Supreme Commander(Steam)
    interfaceCreateGameButton(r"data\scfaSteam.png",supremeCommanderFaSteamClick,"Forged Alliance Steam","scfaSteamEnabled") #Supreme Commander Forged Alliance(Steam)
    interfaceCreateGameButton(r"data\sc.png",supremeCommanderClick,"Supreme Commander","scEnabled") #Supreme Commander
    interfaceCreateGameButton(r"data\scfa.png",supremeCommanderFaClick,"Forged Alliance","scfaEnabled") #Supreme Commander Forged Alliance
    interfaceCreateGameButton(r"data\imagefaf.png",ForgedAllianceForeverClick,"Forged Alliance Forever","fafEnabled") #Supreme Commander Forged Alliance Forever
    interfaceCreateGameButton(r"data\client.png",downlordsClientClick,"Downlord's FAF Client","downlordClientEnabled") #Downlord's FAF Client
    interfaceCreateGameButton(r"data\loud.png",loudClick,"Forged Alliance LOUD","loudEnabled") #Supreme Commander Forged Alliance LOUD
    interfaceCreateGameButton(r"data\mapeditor.png",fafMapEditorClick,"FAF Map Editor","mapeditorEnabled") #FAF Map Editor
    interfaceCreateGameButton(r"data\sc2Steam.png",sc2SteamClick,"Supreme Commander 2 Steam","sc2SteamEnabled") #Supreme Commander 2 Steam
    interfaceCreateGameButton(r"data\sc2.png",sc2Click,"Supreme Commander 2","sc2Enabled") #Supreme Commander 2
    interfaceCreateGameButton(r"data\paSteam.png",paSteamClick,"Planetary Annihilation Steam","paSteamEnabled") #Planetary Annihilation (Steam)
    interfaceCreateGameButton(r"data\client_taforever.png" ,taforeverClick,"Total Annihilation Forever","taforeverEnabled") #Total Annihilation Forever
    interfaceCreateGameButton(r"data\taSteam.png",taSteamClick,"Total Annihilation Steam","taSteamEnabled") #Total Annihilation (Steam)
    interfaceCreateGameButton(r"data\ta.png",taClick,"Total Annihilation","taEnabled") #Total Annihilation
    interfaceCreateGameButton(r"data\escalation.png",taEscClick,"Total Annihilation Escalation","taEscalationEnabled") #Total Annihilation Escalation
    interfaceCreateGameButton(r"data\tamayhem.png",taMayClick,"Total Annihilation Mayhem","taMayhemEnabled") #Total Annihilation Mayhem
    interfaceCreateGameButton(r"data\prota.png",taProClick,"Total Annihilation ProTA","taProTAEnabled") #Total Annihilation ProTA
    interfaceCreateGameButton(r"data\twilight.png",taTwiClick,"Total Annihilation Twilight","taTwilightEnabled") #Total Annihilation Twilight
    interfaceCreateGameButton(r"data\taZero.png",taZeroClick,"Total Annihilation Zero","taZeroEnabled") #Total Annihilation Zero
    interfaceCreateGameButton(r"data\zerok.png",zerokClick,"Zero-K Steam","ZerokEnabled") #Zero-K (Steam)
    interfaceCreateGameButton(r"data\bar.png",barClick,"Beyond All Reason","barEnabled") #Beyond All Reason

createInterface() #create the main interface

#File settings window
def def_settings():
    global gameLinkArray
    gameLinkArray = [] #reinitialize the array
    settingsWindow = Toplevel() #make a new Toplevel window for settings
    settingsWindow.title("Settings") #Settings windows title
    settingsWindow['background']='#1A1A1A' #Settings window background color
    settingsWindow.wait_visibility() #wait for the new window to be visible
    settingsWindow.grab_set() #route events for this application to this widget.
    settingsWindow.resizable(False, False) #Set window resizeable to false 
    w = 700 # width for setting menu
    h = settingsWindow.winfo_screenheight() * 71 * 0.01 #70% of height window
    x = (w/1.2) #Center the main window
    y = (h/7)
    settingsWindow.geometry('%dx%d+%d+%d' % (w, h, x, y)) #set window size and location
    #new interface canvas
    container = Frame(settingsWindow) #New frame window for scroll conent
    canvas = Canvas(container,width= w-20,height=420,bg="#1A1A1A") #new canvas for scroll content
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview) #new Scrollbar
    scrollable_frame = Frame(canvas,bg="#1A1A1A") #scrollable frame
    #bind the frame to the scroll region
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw") #New canvas for scrollable frame
    canvas.configure(yscrollcommand=scrollbar.set) #Configure canvas
    container.pack()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    #Scroll wheel
    def _bound_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", _on_mousewheel)   
    def _unbound_to_mousewheel(event):
        canvas.unbind_all("<MouseWheel>") 
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind('<Enter>', _bound_to_mousewheel)
    canvas.bind('<Leave>', _unbound_to_mousewheel)

    #Create settings menu
    def settingsCreateOptions(labelName,linkDefault,iniData,iniPath):
        #Checkbox change
        def checkboxCheck(varName,entryPath,iniData,iniPath):
            if varName.get() == 1: #check if state of the checkbox is checked
                userinfo[iniData] = "1" #set changed user data of game enabled
                userinfo[iniPath] = entryPath.get() #set changed user data of game path 
                #lock games with steam paths
                if iniData != "scSteamEnabled" and iniData != "sc2SteamEnabled" and iniData != "scfaSteamEnabled" and iniData != "paSteamEnabled" and iniData != "taSteamEnabled" and iniData != "ZerokEnabled":
                    
                    if os.path.isfile(entryPath.get()):
                        entryPath.configure(state=NORMAL) #Unlock the game path location
                    else: 
                        filename = askopenfilename() #open file explorer to locate file
                        filename = filename.replace("/", "\\")
                        entryPath.configure(state=NORMAL) #Unlock the game path location 
                        if filename != "":        
                            entryPath.delete (0, END) #clear the data in entry
                            entryPath.insert(END, filename) #insert file name into 
                                  
            if varName.get() == 0:#check if state of the checkbox is unchecked
                userinfo[iniData] = "0" #set changed user data of game enabled
                userinfo[iniPath] = entryPath.get() #set changed user data of game path
                entryPath.configure(state=DISABLED) #lock the game path location
            #Wright to the ini file with the updated settings
            with open('./config/config.ini', 'w') as conf:
                userData.write(conf)

        global settingsRow        
        varName = IntVar() #var for checkBox variable
        userInfoData = userinfo[iniData] #get data from ini
        settingslabel = Label(scrollable_frame,bg="#1A1A1A",fg="#FFF", text = labelName) #Create a new label
        settingslabel.config(font =("Orbitron", 10)) #Set label font
        entryPath = Entry(scrollable_frame,width=100) #Create a new enray for game location
        gameLinkArray.append(entryPath) #Add game link to array
        #Add a new checkbox
        chckBox = Checkbutton(scrollable_frame, text="Enable",activebackground="#1A1A1A",activeforeground ="#FFF",bg="#1A1A1A",
            fg="#FFF",selectcolor="#000", variable=varName, onvalue=1, offvalue=0, command=partial(checkboxCheck,varName,entryPath,iniData,iniPath),font =("Lato", 9))
        settingslabel.grid(column=1,row=settingsRow,padx=30, pady=2) #set lable location
        settingsRow = settingsRow + 1 #add row count
        chckBox.grid(column=1,row=settingsRow,padx=30, pady=2) #set check box location
        settingsRow = settingsRow + 1 #add row count
        entryPath.grid(column=1,row=settingsRow,padx=30, pady=2) #set entry loation
        settingsRow = settingsRow + 1 #add row count
        entryPath.insert(END, linkDefault) #add the saved game link string
        entryPath.configure(state=DISABLED)#disable the entry
        #Check the saved data if the user has enabled the game
        if userinfo[iniData] == "1":
            chckBox.select() #If game is selected check the box
            if iniData != "scSteamEnabled" and iniData != "sc2SteamEnabled" and iniData != "scfaSteamEnabled" and iniData != "paSteamEnabled" and iniData != "taSteamEnabled" and iniData != "ZerokEnabled":
                entryPath.configure(state=NORMAL) #Enable the entry
    #Create the settings interface 
    settingsCreateOptions("Supreme Commander (Steam)",userinfo["scSteamPath"] ,"scSteamEnabled","scSteamPath")        
    settingsCreateOptions("Forged Alliance (Steam)",userinfo["scfaSteamPath"] ,"scfaSteamEnabled","scfaSteamPath")
    settingsCreateOptions("Supreme Commander",userinfo["scPath"] ,"scEnabled","scPath")        
    settingsCreateOptions("Forged Alliance",userinfo["scfaPath"] ,"scfaEnabled","scfaPath")
    settingsCreateOptions("Forged Alliance Forever",userinfo["fafPath"],"fafEnabled","fafPath")
    settingsCreateOptions("Downlord's FAF Client",userinfo["downlordClientPath"] ,"downlordClientEnabled","downlordClientPath")
    settingsCreateOptions("LOUD Forged Alliance",userinfo["loudPath"] ,"loudEnabled","loudPath")
    settingsCreateOptions("FAF Map Editor",userinfo["mapedirorscPath"] ,"mapeditorEnabled","mapedirorscPath")
    settingsCreateOptions("Supreme Commander 2 (Steam)",userinfo["sc2SteamPath"] ,"sc2SteamEnabled","sc2SteamPath")   
    settingsCreateOptions("Supreme Commander 2",userinfo["sc2Path"] ,"sc2Enabled","sc2Path")   
    settingsCreateOptions("Planetary Annihilation (Steam)",userinfo["paSteamPath"] ,"paSteamEnabled","paSteamPath")
    settingsCreateOptions("Total Annihilation Forever",userinfo["taforeverPath"] ,"taforeverEnabled","taforeverPath")
    settingsCreateOptions("Total Annihilation (Steam)",userinfo["taSteamPath"] ,"taSteamEnabled","taSteamPath")
    settingsCreateOptions("Total Annihilation",userinfo["taPath"] ,"taEnabled","taPath")
    settingsCreateOptions("Total Annihilation Escalation",userinfo["taEscalationPath"] ,"taEscalationEnabled","taEscalationPath")
    settingsCreateOptions("Total Annihilation Mayhem",userinfo["taMayhemPath"] ,"taMayhemEnabled","taMayhemPath")
    settingsCreateOptions("Total Annihilation ProTA",userinfo["taProTAPath"] ,"taProTAEnabled","taProTAPath")
    settingsCreateOptions("Total Annihilation Twilight",userinfo["taTwilightPath"] ,"taTwilightEnabled","taTwilightPath")
    settingsCreateOptions("Total Annihilation Zero",userinfo["taZeroPath"] ,"taZeroEnabled","taZeroPath")
    settingsCreateOptions("Beyond All Reason",userinfo["barPath"] ,"barEnabled","barPath")
    settingsCreateOptions("Zero-K (Steam)",userinfo["ZerokPath"] ,"ZerokEnabled","ZerokPath")

    #Create checkboxes
    def def_settings_CheckBox(iniData,checkboxText):
        def checkboxButtonClick():
            #check if the checkbox is enabled
            if checkboxValue.get() == 1:
                userinfo[iniData] = "1" #set ini data
            if checkboxValue.get() == 0:
                userinfo[iniData] = "0" #set ini data
            #save data
            with open('./config/config.ini', 'w') as conf:
                userData.write(conf)  

        checkboxValue = IntVar() #var for checkboxButton variable
        #Create a new checkbox Button
        checkboxButton = Checkbutton(settingsWindow,bd=10, text=checkboxText,activebackground="#1A1A1A",activeforeground ="#FFF",bg="#1A1A1A",
            fg="#FFF",selectcolor="#000", variable=checkboxValue, onvalue=1, offvalue=0, command=checkboxButtonClick,font =("Lato", 9))

        checkboxButton.pack()#Add the checkbox
        #check ini data for checkbox status
        if userinfo[iniData] == "1":
            checkboxButton.select() #Select the check box if user saved data is checked

    #Create the Checkboxes 
    def_settings_CheckBox("lockCursorEnabled","Lock cursor to active window when in windowed mode (Supported Games: SC,FA,FAF,LOUD)")
    def_settings_CheckBox("autoSetMonitorEnabled","Auto set game window size when in windowed mode (Supported Games: SC,FA,FAF,LOUD)")
    def_settings_CheckBox("autoSetDualScreenEnabled","Enable auto dual screen switcher (Experimental, needs Common Mod Tools and ui-party enabled, only for FA,FAF,LOUD)")

    hotkey1 = Label(settingsWindow,bd= 10,bg="#1A1A1A",fg="#FFF", text = "Ctrl F12 (Switches to dual screen mode)") #Create a new label
    hotkey1.config(font =("Orbitron", 10)) #Set label font
    hotkey1.pack(side = TOP) #Add the label
    hotkey2 = Label(settingsWindow,bd= 10,bg="#1A1A1A",fg="#FFF", text = "Ctrl F11 (Switches to single screen mode)") #Create a new label
    hotkey2.config(font =("Orbitron", 10)) #Set label font
    hotkey2.pack(side = TOP) #Add the label
    hotkey3 = Label(settingsWindow,bd= 10,bg="#1A1A1A",fg="#FFF", text = "Ctrl F10 (End the ahk script)") #Create a new label
    hotkey3.config(font =("Orbitron", 10)) #Set label font
    hotkey3.pack(side = TOP) #Add the label
    Note = Label(settingsWindow,bd= 10,bg="#1A1A1A",fg="#FFF", text = "For windowed dual screen mode install Common Mod Tools Mod and ui-party mod then enabled ui-party in \n \
        the mod menu. Within each game set the primary adapter to windowed and disable the secondary adapter. \n \
        (Supported Games: FA,FAF,LOUD)") #Create a new label
    Note.config(font =("Lato", 10)) #Set label font
    Note.pack(side = TOP) #Add the label

    #Apply button
    def applyCall():
        #Save the user data to the ini
        global gameLinkArray
        #Save the game path data to the config file
        userinfo["scSteamPath"] = gameLinkArray[0].get()
        userinfo["scfaSteamPath"] = gameLinkArray[1].get()
        userinfo["scPath"] = gameLinkArray[2].get()
        userinfo["scfaPath"] = gameLinkArray[3].get()
        userinfo["fafPath"] = gameLinkArray[4].get()
        userinfo["downlordClientPath"] = gameLinkArray[5].get()
        userinfo["loudPath"] = gameLinkArray[6].get()
        userinfo["mapedirorscPath"] = gameLinkArray[7].get()
        userinfo["sc2SteamPath"] = gameLinkArray[8].get()
        userinfo["sc2Path"] = gameLinkArray[9].get()
        userinfo["paSteamPath"] = gameLinkArray[10].get()
        userinfo["taforeverPath"] = gameLinkArray[11].get()
        userinfo["taSteamPath"] = gameLinkArray[12].get()
        userinfo["taPath"] = gameLinkArray[13].get()
        userinfo["taEscalationPath"] = gameLinkArray[14].get()
        userinfo["taMayhemPath"] = gameLinkArray[15].get()
        userinfo["taProTAPath"] = gameLinkArray[16].get()
        userinfo["taTwilightPath"] = gameLinkArray[17].get()
        userinfo["taZeroPath"] = gameLinkArray[18].get()
        userinfo["barPath"] = gameLinkArray[19].get()
        userinfo["ZerokPath"] = gameLinkArray[20].get()
        #Open ini and write to it
        with open('./config/config.ini', 'w') as conf:
            userData.write(conf)
        createInterface() #Recreate the window interface
        settingsWindow.destroy() #close the settings window
    #Add the apply button to the setting menu    
    applyButton = Button(settingsWindow, text = "Apply", width = 10, command = applyCall)
    applyButton.pack()

#About interface
def def_about():
    #Create a simple about page
    aboutWindow = Toplevel()
    aboutWindow.title("About")
    aboutWindow['background']='#1A1A1A'
    aboutWindow.wait_visibility()
    aboutWindow.grab_set()
    aboutWindow.resizable(False, False) 
    w = 700
    h = 583 
    x = (w/1.2)
    y = (h/4)
    aboutWindow.geometry('%dx%d+%d+%d' % (w, h, x, y)) #set window size and location
    aboutWindow['background']='#1A1A1A' #Set background color

    aboutlabel = Label(aboutWindow,bg="#1A1A1A",fg="#FFF", text = launcherName + " - " + version)
    aboutlabel.config(font =("Orbitron", 10))
    aboutlabel.place(x=0, y=0)
    aboutlabel.pack(side = TOP)

    aboutlabel = Label(aboutWindow,bg="#1A1A1A",fg="#FFF", text = "Supreme Commander Definitive Windowed Borderless Script - " + scriptVersion)
    aboutlabel.config(font =("Orbitron", 10))
    aboutlabel.place(x=0, y=0)
    aboutlabel.pack(side = TOP)

    aboutlabel = Label(aboutWindow,bg="#1A1A1A",fg="#FFF", text = "Created by \n ageekhere \n 2021")
    aboutlabel.config(font =("Orbitron", 10))
    aboutlabel.place(x=0, y=0)
    aboutlabel.pack(side = TOP)

    aboutlabel = Label(aboutWindow, bg="#1A1A1A",fg="#FFF", text = "\n Supported Games \n \n \
        Supreme Commander \n \
        Forged Alliance \n \
        Supreme Commander(Steam) \n \
        Forged Alliance(Steam) \n \
        Forged Alliance Forever \n \
        Downlord's FAF Client \n \
        Forged Alliance LOUD \n \
        FAF Map Editor \n \
        Supreme Commander 2 \n \
        Planetary Annihilation(Steam) \n \
        Total Annihilation \n \
        Total Annihilation Forever \n \
        Total Annihilation Escalation \n \
        Total Annihilation Mayhem \n \
        Total Annihilation ProTA \n \
        Total Annihilation Twilight \n \
        Total Annihilation Zero \n \
        Zero-K(Steam) \n \
        Beyond All Reason \n ")
    aboutlabel.config(font =("Lato", 10))
    aboutlabel.place(x=0, y=0)
    aboutlabel.pack(side = LEFT)

#File menu for main window
file_menu= Menu(my_menu,tearoff="off") #Disable tearoff
my_menu.add_cascade(label="File", menu=file_menu) #Add file menu
file_menu.add_command(label="Settings",command=def_settings) #Add settings menu
file_menu.add_command(label="About",command=def_about) #Add about menu
file_menu.add_command(label="Exit",command=window.quit) #Add exit
 
window.mainloop()