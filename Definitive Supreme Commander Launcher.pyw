"""
Install the following for python
pip3 install customtkinter
python -m pip install requests
pip install pillow
"""
import configparser
import customtkinter
import ctypes
import platform
import requests
import subprocess as subCall
import sys, string, os
import tkinter
import tkinter as tk
import webbrowser
from tkinter import *
from configparser import ConfigParser
from datetime import date
from functools import partial
from pathlib import Path
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import subprocess
def read_wright_config(pOption: str # r = read, w = wright
    ) -> None:
    # Read for write to the config file
    if pOption not in ("r", "w"): # The operation to perform, either "r" for reading or "w" for writing.
        raise ValueError("Invalid option: must be 'r' or 'w'") # If an invalid option is provided.
    if pOption == "w": # Check for wright
        with open(gConfigPath, 'w') as pConfigfile: # Open the file 
            gUserData.write(pConfigfile) # Wright to the file
    elif pOption == "r": # Check for read
        gUserData.read(gConfigPath) #Read the ini file

def create_Label(pWindow: customtkinter.CTkToplevel, # The window 
    pText: str, # Label text
    pFont: tkinter.font.Font, # Label font 
    pSide: str = "top", # Side value
    pJustify: str = "left", # Justify value
    pAnchor: str = "w" # Anchor value
    ) -> customtkinter.CTkLabel: # Using customtkinter.CTkLabel
    pLabel = customtkinter.CTkLabel(pWindow, text=pText, font =pFont,justify=pJustify) # Creates a new label with specified properties.
    pLabel.pack(side = pSide,anchor=pAnchor,padx=5) # Packs new label with specified properties.
    return pLabel

def weblink_open(pLink: str, *args: any) -> None:
    webbrowser.open(pLink) # Opens the specified web link in the default browser 

def theme_update() -> None: 
    # Set the theme to use for the app
    if gUserinfo["darkModeEnabled"] == "1": # 0 is light, 1 is dark
        pTheme = "dark"
        pColor = "blue"    
    else:
        pTheme = "light"
        pColor = "blue"
    customtkinter.set_appearance_mode(pTheme) # Set theme appearance mode
    customtkinter.set_default_color_theme(pColor) # Set color theme

def gameClick(pGameName:str, pGamePath:str, pGameType:str, pExeName):
    # Load game on image click
    if pGameType != "steam": # Check for steam game
        startGame(pGamePath,pGameName) # call startGame to load the game
    else: # Is a steam game
        subCall.Popen(["scripts/AutoHotkeyU32.exe", "scripts/main.ahk",pGameName,pGamePath,
        gUserinfo["lockCursorEnabled"],gUserinfo["autoSetMonitorEnabled"],gUserinfo["autoSetDualScreenEnabled"],pExeName,gUserinfo["minimizeallEnabled"],gUserinfo["dualScreenDefaultEnabled"] ]) # load steam game via steam

def startGame(pPath:str, pName:str) -> None:
    game_dir = os.path.dirname(pPath)
    pGameLocation = r'%s' %pPath
    pGameExe = pGameLocation.split('\\')[-1]
    pFixedGameLocation = pGameLocation.replace(pGameExe, "", 1)
    subCall.Popen(["scripts/AutoHotkeyU32.exe", "scripts/main.ahk",pName,pFixedGameLocation,
    gUserinfo["lockCursorEnabled"],gUserinfo["autoSetMonitorEnabled"],gUserinfo["autoSetDualScreenEnabled"],pGameExe, gUserinfo["minimizeallEnabled"],gUserinfo["dualScreenDefaultEnabled"] ])

def optionmenu_callback(choice) -> None:
    if choice == "Settings":
        optionsMenu.set("Menu")
        def_settings()
    if choice == "About":
        optionsMenu.set("Menu")
        def_about()
    if choice == "Exit":
        optionsMenu.set("Menu")
        gMainWindow.quit()

def update_event() -> None:
    webbrowser.open("https://github.com/ageekhere/Definitive-Supreme-Commander-Launcher/releases")

def _bound_to_mousewheelHome(event) -> None:
    gHomeCanvas.bind_all("<MouseWheel>", _on_mousewheelHome)

def _unbound_to_mousewheelHome(event) -> None:
    gHomeCanvas.unbind_all("<MouseWheel>")

def _on_mousewheelHome(event) -> None:
    pScrollUnits = 120
    if gHomeScrollable_frame.winfo_reqheight() > gMainWindowHeight:
        gHomeCanvas.yview_scroll(int(-1*(event.delta/pScrollUnits)), "units")

# Function, Creates the game buttons for the interface
def interfaceCreateGameButton(pImagePath, pFcommand, pLabelText, gameEnable, pGameName:str, pGamePath:str, pGameType:str, pExeName:str) -> None:
    if gUserinfo[gameEnable] == "0": # Check if the game has been enabled
        return # Skip game if not enabled
    global gInterfaceRow,gInterfaceCol # Global
    pImageName = Image.open(pImagePath) # Open a new image at the pImagePath address
    pImageWidth, pImageHeight = pImageName.size # Read image size
    pImageHeight = int((pImageHeight*0.55)) # Set image height
    pHeightPercent = (pImageHeight / float(pImageName.size[1])) # Find height percent
    pImageWidth = int((float(pImageName.size[0]) * float(pHeightPercent))) # Set width to scale with height
    pImageName = pImageName.resize((pImageWidth,pImageHeight),Image.Resampling.LANCZOS) # Resize the image   
    pImageName = ImageTk.PhotoImage(pImageName) # Create a new PhotoImage of pImageName after the resize 
    pImageLabel = tkinter.Label(image=pImageName) # Create a label with the image
    pImageLabel.image = pImageName # Set the label image
    pImageButton = Button(gHomeScrollable_frame, image=pImageName, width=pImageWidth, height=pImageHeight,command=partial(pFcommand,pGameName,pGamePath,pGameType,pExeName),bd=0,highlightthickness=0 ) #Make a image button

    #make a grid with 3 columns
    if gInterfaceCol > 2:
        gInterfaceCol = 0
        gInterfaceRow = gInterfaceRow + 2
    gInterfaceCol = gInterfaceCol + 1
    pGameLabel = customtkinter.CTkLabel(gHomeScrollable_frame, text=pLabelText) # Create new label name
    pGameLabel.configure(font =("Orbitron", 20)) # Set the font of the Label
    pGameLabel.grid(row=gInterfaceRow,column=gInterfaceCol) # Add lable as grid
    pImageButton.grid(row=gInterfaceRow+1,column=gInterfaceCol,padx=30, pady=10) # Add button as grid
    gMainWindowCanvas.config(scrollregion=gMainWindowCanvas.bbox(ALL)) # Configure the scroll region 

#Function, create the main interface
def createInterface() -> None: 
    #reset the col and row number
    global gInterfaceRow
    global gInterfaceCol
    gInterfaceRow = 0
    gInterfaceCol = 0
    #delete all content form the gHomeScrollable_frame
    for widget in gHomeScrollable_frame.winfo_children():
        widget.destroy()
    # Add images to interface,interfaceCreateGameButton(string image location, function click, string name, string enabled)
    interfaceCreateGameButton(r"data\absoluteAnnihilation.png",gameClick,"Absolute Annihilation","absoluteAnnEnabled","absoluteAnn", gUserinfo["absoluteAnnPath"],"na","na") # Absolute Annihilation
    interfaceCreateGameButton(r"data\bar.png",gameClick,"Beyond All Reason","barEnabled","bar", gUserinfo["barPath"],"na","na") # Beyond All Reason
    interfaceCreateGameButton(r"data\client.png",gameClick,"Downlord's FAF Client","downlordClientEnabled","client", gUserinfo["downlordClientPath"],"na","na") # Downlord's FAF Client
    interfaceCreateGameButton(r"data\escalation.png",gameClick,"Total Annihilation Escalation","taEscalationEnabled","taEscalation", gUserinfo["taEscalationPath"],"na","na") # Total Annihilation Escalation
    interfaceCreateGameButton(r"data\imagefaf.png",gameClick,"Forged Alliance Forever","fafEnabled","faf", gUserinfo["fafPath"],"na","na") # Supreme Commander Forged Alliance Forever
    interfaceCreateGameButton(r"data\loud.png",gameClick,"Forged Alliance LOUD","loudEnabled","loud", gUserinfo["loudPath"],"na","na") # Supreme Commander Forged Alliance LOUD
    interfaceCreateGameButton(r"data\mapeditor.png",gameClick,"FAF Map Editor","mapeditorEnabled","mapeditor", gUserinfo["mapedirorscPath"],"na","na") # FAF Map Editor
    interfaceCreateGameButton(r"data\prota.png",gameClick,"Total Annihilation ProTA","taProTAEnabled","taPro", gUserinfo["taProTAPath"],"na","na") # Total Annihilation ProTA
    interfaceCreateGameButton(r"data\sc.png",gameClick,"Supreme Commander","scEnabled","sc", gUserinfo["scPath"],"na","na") # Supreme Commander
    interfaceCreateGameButton(r"data\sc2.png",gameClick,"Supreme Commander 2","sc2Enabled","sc2", gUserinfo["sc2Path"],"na","na") # Supreme Commander 2
    interfaceCreateGameButton(r"data\scfa.png",gameClick,"Forged Alliance","scfaEnabled","fa", gUserinfo["scfaPath"],"na","na") # Supreme Commander Forged Alliance
    interfaceCreateGameButton(r"data\tamayhem.png",gameClick,"Total Annihilation Mayhem","taMayhemEnabled","taMay", gUserinfo["taMayhemPath"],"na","na") # Total Annihilation Mayhem
    interfaceCreateGameButton(r"data\ta.png",gameClick,"Total Annihilation","taEnabled","ta", gUserinfo["taPath"],"na","na") # Total Annihilation
    interfaceCreateGameButton(r"data\twilight.png",gameClick,"Total Annihilation Twilight","taTwilightEnabled","taTwilight", gUserinfo["taTwilightPath"],"na","na") # Total Annihilation Twilight
    interfaceCreateGameButton(r"data\taZero.png",gameClick,"Total Annihilation Zero","taZeroEnabled","taZero", gUserinfo["taZeroPath"],"na","na") # Total Annihilation Zero
    interfaceCreateGameButton(r"data\client_taforever.png" ,gameClick,"Total Annihilation Forever","taforeverEnabled","taforever", gUserinfo["taforeverPath"],"na","na") # Total Annihilation Forever
    interfaceCreateGameButton(r"data\taSteam.png",gameClick,"Total Annihilation Steam","taSteamEnabled","taSteam", gUserinfo["taSteamPath"],"steam","TotalA.exe") # Total Annihilation (Steam)
    interfaceCreateGameButton(r"data\scSteam.png",gameClick,"Supreme Commander Steam","scSteamEnabled","steamSC", gUserinfo["scSteamPath"],"steam","SupremeCommander.exe") # Supreme Commander(Steam)
    interfaceCreateGameButton(r"data\scfaSteam.png",gameClick,"Forged Alliance Steam","scfaSteamEnabled","steamFAF", gUserinfo["scSteamPath"],"steam","SupremeCommander.exe") # Supreme Commander Forged Alliance(Steam)
    interfaceCreateGameButton(r"data\sc2Steam.png",gameClick,"Supreme Commander 2 Steam","sc2SteamEnabled","sc2Steam", gUserinfo["sc2SteamPath"],"steam","SupremeCommander2.exe") # Supreme Commander 2 Steam
    interfaceCreateGameButton(r"data\paSteam.png",gameClick,"Planetary Annihilation Steam","paSteamEnabled","paSteam", gUserinfo["paSteamPath"],"steam","PA.exe") # Planetary Annihilation (Steam)
    interfaceCreateGameButton(r"data\zerok.png",gameClick,"Zero-K Steam","ZerokEnabled","ZeroK", gUserinfo["ZerokPath"],"steam","Zero-K.exe") # Zero-K (Steam)
    
#File settings window
def def_settings() -> None:
    def f_bound_to_mousewheel(event):
        pSettingsCanvas.bind_all("<MouseWheel>", f_on_mousewheel)  

    def f_unbound_to_mousewheel(event):
        pSettingsCanvas.unbind_all("<MouseWheel>") 

    def f_on_mousewheel(event):
        pSettingsCanvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def checkboxCheck(pVarName,pEntryPath,pIniData,pIniPath):
            pVarNameValue = pVarName.get() # Cache the get() value of pVarName
            pEntryPathValue = pEntryPath.get() # Cache the get() value of pEntryPath
            if pVarNameValue == 1: # Check if state of the checkbox is checked
                gUserinfo[pIniData] = "1" # Set changed user data of game enabled
                gUserinfo[pIniPath] = pEntryPathValue # Set changed user data of game path 
                if pIniData not in pLockedGamePaths: # Lock games with steam paths
                    if os.path.isfile(pEntryPathValue): # Check path of pEntryPathValue
                        pEntryPath.configure(state=NORMAL) # Unlock the game path location
                    else: 
                        pFilename = askopenfilename() # Open file explorer to locate file
                        pEntryPath.configure(state=NORMAL) # Unlock the game path location
                        if pFilename != "": # Check for blank path        
                            pEntryPath.delete (0, END) # Clear the data in entry
                            pEntryPath.insert(END, Path(pFilename)) # Insert file name into
            elif pVarNameValue == 0: # Check if state of the checkbox is unchecked
                gUserinfo[pIniData] = "0" # Set changed user data of game enabled
                gUserinfo[pIniPath] = pEntryPathValue # Set changed user data of game path
                pEntryPath.configure(state=DISABLED) # Lock the game path location
            read_wright_config("w") # Wright to the ini file with the updated settings

    #Create settings menu
    def settingsCreateOptions(pLabelName,pLinkDefault,pIniData,pIniPath) -> None:     
        global gSettingsRow  
        pVarName = IntVar() # Var for checkBox variable
        pSettingsGamelabel = customtkinter.CTkLabel(pSettingsScrollFrame, text=pLabelName,font =("Orbitron", 14)) # Create label for grid layout
        pEntryPath = Entry(pSettingsScrollFrame,width=100) # Create a new enray for game location
        pGameLinkArray.append(pEntryPath) # Add game link to array  
        pGameCheckBox = customtkinter.CTkCheckBox(pSettingsScrollFrame, text="Enable", command=partial(checkboxCheck,pVarName,pEntryPath,pIniData,pIniPath),
            font =("Orbitron", 14), variable=pVarName, onvalue=1, offvalue=0)
        pSettingsGamelabel.grid(column=1,row=gSettingsRow,padx=100, pady=2) # Set lable location
        gSettingsRow = gSettingsRow + 1 # Add row count
        pGameCheckBox.grid(column=1,row=gSettingsRow,padx=100, pady=2) # Set check box location
        gSettingsRow = gSettingsRow + 1 # Add row count
        pEntryPath.grid(column=1,row=gSettingsRow,padx=100, pady=2) # Set entry loation
        gSettingsRow = gSettingsRow + 1 # Add row count
        pEntryPath.insert(END, pLinkDefault) # Add the saved game link string
        pEntryPath.configure(state=DISABLED)# Disable the entry 
        if gUserinfo[pIniData] == "1": # Check the saved data if the user has enabled the game
            pGameCheckBox.select() # If game is selected check the box
            if pIniData not in pLockedGamePaths: # Exclude steam paths
                pEntryPath.configure(state=NORMAL) # Enable the entry

    #Create checkboxes
    def def_settings_CheckBox(pIniData,pCheckboxText) -> None:
        def checkboxButtonClick(): # Check if the checkbox is enabled 
            if pCheckboxValue.get() == 1:
                gUserinfo[pIniData] = "1" # Set ini data
            if pCheckboxValue.get() == 0:
                gUserinfo[pIniData] = "0" # Set ini data
            read_wright_config("w") 
        pCheckboxValue = IntVar() # Var for pCheckboxButton variable
        # Create a new checkbox Button
        pCheckboxButton = customtkinter.CTkCheckBox(pSettingsWindow, text=pCheckboxText,variable=pCheckboxValue, onvalue=1, offvalue=0, command=checkboxButtonClick,font =("Orbitron", 14))
        pCheckboxButton.pack(anchor="w",pady=4,padx=5) # Add the checkbox 
        if gUserinfo[pIniData] == "1": # Check ini data for checkbox status
            pCheckboxButton.select() # Select the check box if user saved data is checked

    #Apply button
    def applyCall() -> None:
        # Save the user data to the ini
        # global pGameLinkArray
        # Save the game path data to the config file
        gUserinfo["scSteamPath"] = pGameLinkArray[0].get()
        gUserinfo["scfaSteamPath"] = pGameLinkArray[1].get()
        gUserinfo["scPath"] = pGameLinkArray[2].get()
        gUserinfo["scfaPath"] = pGameLinkArray[3].get()
        gUserinfo["fafPath"] = pGameLinkArray[4].get()
        gUserinfo["downlordClientPath"] = pGameLinkArray[5].get()
        gUserinfo["loudPath"] = pGameLinkArray[6].get()
        gUserinfo["mapedirorscPath"] = pGameLinkArray[7].get()
        gUserinfo["sc2SteamPath"] = pGameLinkArray[8].get()
        gUserinfo["sc2Path"] = pGameLinkArray[9].get()
        gUserinfo["paSteamPath"] = pGameLinkArray[10].get()
        gUserinfo["taforeverPath"] = pGameLinkArray[11].get()
        gUserinfo["taSteamPath"] = pGameLinkArray[12].get()
        gUserinfo["taPath"] = pGameLinkArray[13].get()
        gUserinfo["taEscalationPath"] = pGameLinkArray[14].get()
        gUserinfo["taMayhemPath"] = pGameLinkArray[15].get()
        gUserinfo["taProTAPath"] = pGameLinkArray[16].get()
        gUserinfo["taTwilightPath"] = pGameLinkArray[17].get()
        gUserinfo["taZeroPath"] = pGameLinkArray[18].get()
        gUserinfo["absoluteAnnPath"] = pGameLinkArray[19].get()
        gUserinfo["barPath"] = pGameLinkArray[20].get()
        gUserinfo["ZerokPath"] = pGameLinkArray[21].get()
        read_wright_config("w")
        createInterface() # Recreate the window interface
        pSettingsWindow.destroy() # Close the settings window
        theme_update()

    pLockedGamePaths = ["scSteamEnabled", "sc2SteamEnabled", "scfaSteamEnabled","paSteamEnabled", "taSteamEnabled", "ZerokEnabled"] # List of Locked games with paths
    pGameLinkArray = [] # Array to hold all the game urls 
    pWindowWidth = 810
    pWindowHeight = 768
    pSettingsWindow = customtkinter.CTkToplevel(gMainWindow) #Use customtkinter for the style of the toplevel window
    pSettingsWindow.title("Settings") # Set the Window title name
    pSettingsWindow.after(200, lambda: pSettingsWindow.iconbitmap(gIconPath))
    pSettingsWindow.grab_set() # Makes the window modal (blocks interaction with the main window)
    pSettingsWindow.resizable(False, False) # Disables window resizing 
    pSettingsWindow.geometry('%dx%d+%d+%d' % (pWindowWidth, pWindowHeight, (pWindowWidth / 1.5), (pWindowHeight / 6))) #set window size and location
    pSettingsFrame = customtkinter.CTkFrame(master=pSettingsWindow, border_width=0) # Create frame
    pSettingsCanvas = Canvas(pSettingsFrame,bd=0, width= pWindowWidth-40, height=380, bg="#2B2B2B", highlightthickness=0) # Create canvas for frame
    pSettingsFrameScrollbar = customtkinter.CTkScrollbar(pSettingsFrame, command=pSettingsCanvas.yview) # Create Scrollbar for canvas
    pSettingsScrollFrame = customtkinter.CTkFrame(master=pSettingsCanvas) # Create 
    pSettingsScrollFrame.bind("<Configure>", lambda e: pSettingsCanvas.configure(scrollregion=pSettingsCanvas.bbox("all"))) # bind pSettingsScrollFrame to pSettingsCanvas 
    pSettingsCanvas.create_window((0, 0), window=pSettingsScrollFrame, anchor="nw") # New canvas for scrollable frame
    pSettingsCanvas.configure(yscrollcommand=pSettingsFrameScrollbar.set) # Configure canvas
    pSettingsCanvas.bind_all("<MouseWheel>", f_on_mousewheel) # Mouse Wheel scroll
    pSettingsCanvas.bind('<Enter>', f_bound_to_mousewheel)
    pSettingsCanvas.bind('<Leave>', f_unbound_to_mousewheel)
    pSettingsFrame.pack()
    pSettingsCanvas.pack(side="left", fill="both", expand=False)
    pSettingsFrameScrollbar.pack(side="right", fill="y")    
    #Create the settings interface 
    settingsCreateOptions("Supreme Commander (Steam)",gUserinfo["scSteamPath"] ,"scSteamEnabled","scSteamPath")        
    settingsCreateOptions("Forged Alliance (Steam)",gUserinfo["scfaSteamPath"] ,"scfaSteamEnabled","scfaSteamPath")
    settingsCreateOptions("Supreme Commander",gUserinfo["scPath"] ,"scEnabled","scPath")        
    settingsCreateOptions("Forged Alliance",gUserinfo["scfaPath"] ,"scfaEnabled","scfaPath")
    settingsCreateOptions("Forged Alliance Forever",gUserinfo["fafPath"],"fafEnabled","fafPath")
    settingsCreateOptions("Downlord's FAF Client",gUserinfo["downlordClientPath"] ,"downlordClientEnabled","downlordClientPath")
    settingsCreateOptions("LOUD Forged Alliance",gUserinfo["loudPath"] ,"loudEnabled","loudPath")
    settingsCreateOptions("FAF Map Editor",gUserinfo["mapedirorscPath"] ,"mapeditorEnabled","mapedirorscPath")
    settingsCreateOptions("Supreme Commander 2 (Steam)",gUserinfo["sc2SteamPath"] ,"sc2SteamEnabled","sc2SteamPath")   
    settingsCreateOptions("Supreme Commander 2",gUserinfo["sc2Path"] ,"sc2Enabled","sc2Path")   
    settingsCreateOptions("Planetary Annihilation (Steam)",gUserinfo["paSteamPath"] ,"paSteamEnabled","paSteamPath")
    settingsCreateOptions("Total Annihilation Forever",gUserinfo["taforeverPath"] ,"taforeverEnabled","taforeverPath")
    settingsCreateOptions("Total Annihilation (Steam)",gUserinfo["taSteamPath"] ,"taSteamEnabled","taSteamPath")
    settingsCreateOptions("Total Annihilation",gUserinfo["taPath"] ,"taEnabled","taPath")
    settingsCreateOptions("Total Annihilation Escalation",gUserinfo["taEscalationPath"] ,"taEscalationEnabled","taEscalationPath")
    settingsCreateOptions("Total Annihilation Mayhem",gUserinfo["taMayhemPath"] ,"taMayhemEnabled","taMayhemPath")
    settingsCreateOptions("Total Annihilation ProTA",gUserinfo["taProTAPath"] ,"taProTAEnabled","taProTAPath")
    settingsCreateOptions("Total Annihilation Twilight",gUserinfo["taTwilightPath"] ,"taTwilightEnabled","taTwilightPath")
    settingsCreateOptions("Total Annihilation Zero",gUserinfo["taZeroPath"] ,"taZeroEnabled","taZeroPath")
    settingsCreateOptions("Absolute Annihilation",gUserinfo["absoluteAnnPath"] ,"absoluteAnnEnabled","absoluteAnnPath")
    settingsCreateOptions("Beyond All Reason",gUserinfo["barPath"] ,"barEnabled","barPath")
    settingsCreateOptions("Zero-K (Steam)",gUserinfo["ZerokPath"] ,"ZerokEnabled","ZerokPath")

    #Create the Checkboxes 
    def_settings_CheckBox("darkModeEnabled","Dark Mode")
    def_settings_CheckBox("minimizeallEnabled","Minimize all windows on game launch")
    def_settings_CheckBox("lockCursorEnabled","Lock cursor to active window when in windowed mode (Supported Games: SC,FA,FAF,LOUD) ")
    def_settings_CheckBox("autoSetMonitorEnabled","Auto set game window size when in windowed mode (Supported Games: SC,FA,FAF,LOUD Default 1920x1080) ")
    def_settings_CheckBox("autoSetDualScreenEnabled","Enable auto dual screen switcher (Experimental, needs Common Mod Tools and ui-party enabled, only for FA,FAF,LOUD)")
    def_settings_CheckBox("dualScreenDefaultEnabled","Start supported games in dual screen by default")

    pHotkey1 = create_Label(pSettingsWindow, "Ctrl F12 (Switches to dual screen mode)", ("Orbitron", 14), TOP, "left","w") 
    pHotkey2 = create_Label(pSettingsWindow, "Ctrl F11 (Switches to single screen mode)", ("Orbitron", 14), TOP, "left","w") 
    pHotkey3 = create_Label(pSettingsWindow, "Ctrl F10 (End the ahk script)", ("Orbitron", 14), TOP, "left","w") 
    pNote1 = create_Label(pSettingsWindow, "For windowed dual screen mode install Common Mod Tools Mod and ui-party mod then enabled ui-party in", ("Orbitron", 14), TOP, "left","w") 
    pNote2 = create_Label(pSettingsWindow, "the mod menu. Within each game set the primary adapter to windowed and disable the secondary adapter.", ("Orbitron", 14),TOP, "left","w") 
    pNote3 = create_Label(pSettingsWindow, "(Supported Games for dual screen: FA,FAF,LOUD)", ("Orbitron", 14), TOP, "left","w") 

    #Add the apply button to the setting menu    
    pApplyButton = customtkinter.CTkButton(pSettingsWindow, text = "Apply", width = 10, command = applyCall)
    pSettingsWindow.protocol("WM_DELETE_WINDOW", applyCall)
    pApplyButton.pack(side = TOP)

#A bout interface
def def_about() -> None:
    pAboutWindow = customtkinter.CTkToplevel(gMainWindow) # Use customtkinter for the style of the toplevel window
    pAboutWindow.title("About") # Set the Window title name
    pAboutWindow.grab_set() # Makes the window modal (blocks interaction with the main window)
    pAboutWindow.resizable(False, False) # Disables window resizing 
    pAboutWindow.geometry('%dx%d+%d+%d' % (700, 583, (700/1.2), (583/4))) # Set window size and location (consider margins and window manager decorations)
    #Labels
    pAppVersionLabel = create_Label(pAboutWindow, gLauncherName + " - " + gVersion, ("Orbitron", 14), TOP, "left","center") 
    pScriptVersionLabel = create_Label(pAboutWindow, "Supreme Commander Definitive Windowed Borderless Script - " + gScriptVersion + " AutoHotkeyU32 1.1.37.02", ("Orbitron", 14), TOP,"left","center") 
    pPythonVersionLabel = create_Label(pAboutWindow, "Python Version - " + gPythonVersion, ("Orbitron", 14), TOP,"left","center") 
    pCreatedByLabel = create_Label(pAboutWindow, "Created by ageekhere 2024", ("Orbitron", 14), TOP,"left","center")
    pGithubLabel = create_Label(pAboutWindow, "https://github.com/ageekhere/Definitive-Supreme-Commander-Launcher", ("Orbitron", 14), TOP,"left","center")
    pGithubLabel.configure(text_color=("white", "blue"))
    pGithubLabel.bind("<Button-1>", lambda event, link="https://github.com/ageekhere/Definitive-Supreme-Commander-Launcher": weblink_open(link, event))
    pGameListLabel = create_Label(pAboutWindow, "\n\
        Supported Games \n \n\
        Absolute Annihilation \n\
        Downlord's FAF Client \n\
        FAF Map Editor \n\
        Forged Alliance \n\
        Forged Alliance Forever \n\
        Forged Alliance LOUD \n\
        Forged Alliance(Steam) \n\
        Planetary Annihilation(Steam) \n\
        Supreme Commander \n\
        Supreme Commander 2 \n\
        Supreme Commander(Steam) \n\
        Total Annihilation \n\
        Total Annihilation Escalation \n\
        Total Annihilation Forever \n\
        Total Annihilation Mayhem \n\
        Total Annihilation ProTA \n\
        Total Annihilation Twilight \n\
        Total Annihilation Zero \n\
        Zero-K(Steam)", ("Orbitron", 14), LEFT,"left","center")

#global variables
gLauncherName = "Definitive Supreme Commander Launcher" # App name
gPythonVersion = "3.12.2" # Python version app is using
gVersion = "1.04" # App version
gGitVersionName ="version1.04" # Current app git version name
gScriptVersion = "1.11" # Version of autohotkey script
gConfigPath = Path("./config/config.ini") # Relative path to INI file
gIconPath = "icon/dscl_icon.ico" # Icon path
gUserData = ConfigParser() # New ConfigParser to reference an INI file
gInterfaceRow = 0 # Row grid layout of the main interface
gInterfaceCol = 0 # Col grid layout of the main interface
gSettingsRow = 0 # Keeps track of the row in settings
#Main
customtkinter.deactivate_automatic_dpi_awareness() # Disable DPI scaling for now - note that this can be improved to scale
if gConfigPath.is_file(): # Check if the INI file exists
    read_wright_config("r") # Read the config file
else: # Set the defaults of the INI file if the file does not exists and create it
    gUserData["USERINFO"] = {
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
    "absoluteAnnEnabled":"0",
    "absoluteAnnPath": r"C:\TotalA.exe",
    "barEnabled":"0",
    "barPath": r"C:\Beyond-All-Reason.exe",
    "ZerokEnabled":"0",
    "ZerokPath": r"steam://rungameid/334920",
    "lockCursorEnabled": "1",
    "autoSetMonitorEnabled": "1",
    "autoSetDualScreenEnabled": "0",
    "updateLastCheck": "2024-03-27",
    "updateLatestVersion": "version1.04",
    "darkModeEnabled":"1",
    "minimizeallEnabled":"1",
    "dualScreenDefaultEnabled":"0",
    } 
    read_wright_config("w") # Wright to the config
    read_wright_config("r") # Read the new config

gUserinfo = gUserData["USERINFO"] # Store the INI settings information
theme_update() # Update the app theme

# Create the main window for the app 
gMainWindow = customtkinter.CTk() # Use customtkinter for the style of the main window
gMainWindow.title(gLauncherName + " - " + gVersion) # Set the title of the Main window
gMainWindow.iconbitmap(gIconPath) # Set the icon image for the window
#set the size and position of the main window
gMainWindowWidth = 1110 # width for the Tk root
gMainWindowHeight = 768  # height for the Tk root
gMainWindowX = (gMainWindowWidth/3) #Center the main window
gMainWindowY = (gMainWindowHeight/6)
gMainWindow.geometry('%dx%d+%d+%d' % (gMainWindowWidth, gMainWindowHeight, gMainWindowX, gMainWindowY)) #set window size and location
gMainWindow.resizable(0,0) #disable window maximize

#Options menu
optionmenu_var = customtkinter.StringVar(value="Menu")  # set the menu option for the file menu
# Options menu settings
optionsMenu = customtkinter.CTkOptionMenu(master=gMainWindow,
    values=["Settings", "About", "Exit"],
    command=optionmenu_callback,
    variable=optionmenu_var,
    width=80,
    corner_radius=0,
    font=("Orbitron", 16),
    dropdown_font=("Orbitron", 15))
optionsMenu.pack(side="top", anchor=NW) # Add options menu 

pError = 0 # Error checker for updater
pToday = str(date.today()) # Get todays date

if gUserinfo["updateLatestVersion"] != gGitVersionName : # Check for an already detected updated
    pUpdateButton = customtkinter.CTkButton(gMainWindow, text="Update Available " + gUserinfo["updateLatestVersion"], command=update_event) # Add update button
    pUpdateButton.pack(side="bottom", anchor=N) # Pack button    

elif pToday != gUserinfo["updateLastCheck"] : # Check if the updater has already checked for an update today
    gUserinfo["updateLastCheck"] = pToday # Update last update check
    read_wright_config("w") # Wright to config
    try:
        pResponse = requests.get("https://api.github.com/repos/ageekhere/Definitive-Supreme-Commander-Launcher/releases/latest",timeout=1) # Check for update
        pResponse.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
        pError = 1 # ("errh",errh)
    except requests.exceptions.RequestException as errex: 
        pError = 2 # ("Exception request",errex)
    except requests.exceptions.ReadTimeout as errrt: 
        pError = 3 # ("Time out",errrt) 
    except RequestException as e:
        pError = 4 # (f"An error occurred: {e}")
    else:    
        if str(pResponse) != "<Response [403]>" and str(pResponse) == "<Response [200]>": # Check data
            pResponse = pResponse.json()["tag_name"] # Get version name
            gUserinfo["updateLatestVersion"] = str(pResponse) # Update latest version
            read_wright_config("w") # Wright to config
            if pResponse != gGitVersionName: # Check if the update button is added
                pUpdateButton = customtkinter.CTkButton(gMainWindow, text="Update Available " + pResponse, command=update_event) # Create new update button
                pUpdateButton.pack(side="bottom", anchor=N) # Add button

read_wright_config("r") # Read updated config
#new interface canvas
gMainWindowCanvas = Canvas(gMainWindow) # Main canvas 
pHomeContainer = customtkinter.CTkFrame(master=gMainWindowCanvas) # New frame
gHomeCanvas = Canvas(pHomeContainer,width= gMainWindowWidth-22,height=gMainWindowHeight,bg="#2B2B2B",highlightthickness=0,bd=0) #New Canvas
pHomeScrollbar = customtkinter.CTkScrollbar(pHomeContainer, command=gHomeCanvas.yview) # Scroll bar for pHomeContainer 
gHomeScrollable_frame = customtkinter.CTkFrame(master=gHomeCanvas) #Scrollable frame for gHomeCanvas 
gHomeScrollable_frame.bind("<Configure>",lambda e: gHomeCanvas.configure(scrollregion=gHomeCanvas.bbox("all"))) #Scrollable frame for bind gHomeCanvas 
gHomeCanvas.create_window((0, 0), window=gHomeScrollable_frame, anchor="nw") # New window
gHomeCanvas.configure(yscrollcommand=pHomeScrollbar.set) # Configure scrollbar
pHomeContainer.pack() # Add the new gMainWindowCanvas items
gHomeCanvas.pack(side="left", fill="both", expand=True)
pHomeScrollbar.pack(side="right", fill="y")
gMainWindowCanvas.pack()
gHomeCanvas.bind_all("<MouseWheel>", _on_mousewheelHome)
gHomeCanvas.bind('<Enter>', _bound_to_mousewheelHome)
gHomeCanvas.bind('<Leave>', _unbound_to_mousewheelHome)
createInterface() #create the main gMainWindowCanvas

gMainWindow.mainloop()