"""
Install the following for python
pip3 install customtkinter
python -m pip install requests or pip install requests
pip install pillow

How to update all modules

For Windows
Open Windows PowerShell
1. pip list --outdated
2. pip freeze | %{$_.split('==')[0]} | %{pip install --upgrade $_}
3. pip list --outdated
"""

# Standard library imports
import configparser
from configparser import ConfigParser
import ctypes
import os
import platform
import requests
import shutil
import string
import subprocess as subCall
import sys
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from datetime import date
from functools import partial
from pathlib import Path
import webbrowser
# Third-party library imports
import customtkinter
from customtkinter import CTkToplevel
from customtkinter import get_appearance_mode
from PIL import Image, ImageTk

# Checks for updates from github and displays an update button if a new version is available.
def gUpdateChecker() -> None:
    pUpdateErrorCheck = 0 # Error checker for updater
    pUpdateLastCheck = str(date.today()) # Get todays date
    # Check for an already detected updated
    if gUserinfo["updateLatestVersion"] != gLauncherGitVersionName : 
        pUpdateButton = customtkinter.CTkButton(
            gMainWindow, # App main window
            text="Update Available " + gUserinfo["updateLatestVersion"], # Text for update button 
            command=gGithubReleases # Command for the github check
        )
        pUpdateButton.pack(side="bottom", anchor=N) # Add button to interface    
    elif pUpdateLastCheck != gUserinfo["updateLastCheck"] : # Check if the updater has already checked for an update today
        gUserinfo["updateLastCheck"] = pUpdateLastCheck # Update last update check
        gReadWriteConfig("w") # Wright to config
        try:
            pResponse = requests.get(
                "https://api.github.com/repos/ageekhere/Definitive-Supreme-Commander-Launcher/releases/latest", # Github releases url
                timeout=1 # Timeout value
            ) # Check for updates
            pResponse.raise_for_status() # Store the status value
        except requests.exceptions.HTTPError as errh:
            raise SystemExit(errh)
            pUpdateErrorCheck = 1 # ("errh",errh)
        except requests.exceptions.RequestException as errex: 
            pUpdateErrorCheck = 2 # ("Exception request",errex)
        except requests.exceptions.ReadTimeout as errrt: 
            pUpdateErrorCheck = 3 # ("Time out",errrt) 
        except RequestException as e:
            pUpdateErrorCheck = 4 # (f"An error occurred: {e}")
        else:    
            if str(pResponse) != "<Response [403]>" and str(pResponse) == "<Response [200]>": # Check data to see if the site was able to be reached
                pResponse = pResponse.json()["tag_name"] # Get version name
                gUserinfo["updateLatestVersion"] = str(pResponse) # Update latest version
                gReadWriteConfig("w") # Wright to config
                if pResponse != gLauncherGitVersionName: # Check if the update button is added
                    pUpdateButton = customtkinter.CTkButton(
                        gMainWindow, # App main window
                        text="Update Available " + pResponse, # Text for button 
                        command=gGithubReleases # Command for the github check
                    ) # Create new update button
                    pUpdateButton.pack(side="bottom", anchor=N) # Add update button

# Reads and writes to the config file, pass "r"" for read and "w" for write
def gReadWriteConfig(
    pOption: str # r or w values only
) -> None:
    if pOption not in ("r", "w"): # The operation to perform, either "r" for reading or "w" for writing.
        raise ValueError("Invalid option: must be 'r' or 'w'") # If an invalid option is provided.
    if pOption == "w": # Check for write
        with open(gConfigPath, 'w') as pConfigfile: # Open the file to wright
            gUserData.write(pConfigfile) # Wright to the file
    elif pOption == "r": # Check for read
        gUserData.read(gConfigPath) #Read the ini file

# Create a new label
def gCreateLabel(
    pWindow: customtkinter.CTkToplevel, # The window 
    pText: str, # Label text
    pFont: tkinter.font.Font, # Label font 
    pSide: str = "top", # Side value
    pJustify: str = "left", # Justify value
    pAnchor: str = "w" # Anchor value
) -> customtkinter.CTkLabel: # Using customtkinter.CTkLabel
    pLabel = customtkinter.CTkLabel(pWindow, text=pText, font =pFont,justify=pJustify) # Creates a new label with specified properties
    pLabel.pack(side = pSide,anchor=pAnchor,padx=5) # Packs new label with specified properties
    return pLabel

# Set the theme to use for the app
def gChangeTheme() -> None: 
    pColor = "blue" # Default color value
    pTheme = "Light" # Default theme value
    if gUserinfo["darkModeEnabled"] == "1": # 0 is light, 1 is dark
        pTheme = "Dark" # Change to dark theme value
    if customtkinter.get_appearance_mode() != pTheme:
        customtkinter.set_appearance_mode(pTheme)  # Set theme appearance mode
    customtkinter.set_default_color_theme(pColor)  # Set color theme

# Menu options, pass a string value
def gMainOptionsMenu(choice:str) -> None:
    gOptionsMenu.set("Menu") # Resets the file menu name back to Menu
    if choice == "Settings":
        gSettingsWindow() # Settings menu
    elif choice == "Game URLs":
        gGameUrlWindow() # Game urls menu
    elif choice == "About":
        gAboutWindow() # About menu
    elif choice == "Exit":
        gMainWindow.quit() # Exit app

# Update app link
def gGithubReleases() -> None:
    webbrowser.open(gGitHubReleasesLink)

# Mouse wheel bound for home canvas
def gBoundHomeCanvasMousewheel(event: tkinter.Event) -> None:
    gHomeCanvas.bind_all("<MouseWheel>", gHomeCanvasMousewheel)

# Mouse wheel unbound for home canvas
def gUnboundHomeCanvasMousewheel(event: tkinter.Event) -> None:
    gHomeCanvas.unbind_all("<MouseWheel>")

# Mouse wheel on for home canvas
def gHomeCanvasMousewheel(event: tkinter.Event) -> None:
    pScrollUnits = 120 # Scroll units
    if gHomeScrollable_frame.winfo_reqheight() > gMainWindowHeight:
        gHomeCanvas.yview_scroll(int(-1*(event.delta/pScrollUnits)), "units") # Scroll by units

# Work around to remove window white flashing when using dark mode on loading new window for titlebar
# see see https://github.com/TomSchimansky/CustomTkinter/discussions/2469
def gExternal_handle_for_titlebar(win: CTkToplevel):
    color_mode = get_appearance_mode()
    error = "none"
    if sys.platform.startswith("win"):
        if color_mode.lower() == "dark":
            value = 1
        elif color_mode.lower() == "light":
            value = 0
        else:
            return
        try:
            hwnd = ctypes.windll.user32.GetParent(win.winfo_id())
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 = 19

            # try with DWMWA_USE_IMMERSIVE_DARK_MODE
            if ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
                                                            ctypes.byref(ctypes.c_int(value)),
                                                            ctypes.sizeof(ctypes.c_int(value))) != 0:
                # try with DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20h1
                ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1,
                                                            ctypes.byref(ctypes.c_int(value)),
                                                            ctypes.sizeof(ctypes.c_int(value)))
        except Exception as err:
            error = "error"
            
        finally:
            win.lift()

# Work around to remove window white flashing when using dark mode on loading new window for resizable
# see https://github.com/TomSchimansky/CustomTkinter/discussions/2469
def gExternal_handle_for_resizable(toplevel: CTkToplevel):
    # Create a CTk button with functionality inside the new window
    Toplevel.resizable(toplevel, False, False)
    gExternal_handle_for_titlebar(toplevel)

# Function, create the main interface
def gCreateInterface() -> None: 
    # Launches the specified game with given parameters.
    def pLoadGame(pGameName:str, # The name of the game
        pGamePath:str, # The path to the game executable
        pGameType:str, # The type of the game ('local' or 'steam')
        pExeName:str # The name of the game executable
    ) -> None:
        if pGameType != "steam": # Check for a steam game
            pGameLocation = r'%s' %pGamePath # Store game location without the exe
            pGameExe = pGameLocation.split('\\')[-1] # Store just the exe name
            pGamePath = pGameLocation.replace(pGameExe, "", 1) # Change path for steam game
            pExeName = pGameExe # Change exe name to game exe for steam
    
        subCall.Popen([gAutoHotkeyLocation, 
        gAutoHotkeyScriptLocation,
        pGameName,
        pGamePath,
        gUserinfo["lockCursorEnabled"],
        gUserinfo["autoSetMonitorEnabled"],
        gUserinfo["autoSetDualScreenEnabled"],
        pExeName, 
        gUserinfo["minimizeallEnabled"],
        gUserinfo["dualScreenDefaultEnabled"],
        pGameType,
        gUserinfo["moveToFarLeftEnabled"]
        ])

    # Function, Creates the game buttons for the interface
    def pInterfaceCreateGameButton(pImagePath:str, # Path to the button image
        pFcommand, # Command to be executed when the button is clicked
        pLabelText:str, # Text label for the button
        gameEnable:str, # Key to check if the game is enabled
        pGameName:str, # Name of the game
        pGamePath:str, # Path to the game
        pGameType:str, # Type of the game
        pExeName:str # Name of the game's executable
    ) -> None:
        if gUserinfo[gameEnable] == "0": # Check if the game has been enabled
            return # Skip creating the button if the game is not enabled
        global gInterfaceRow, gInterfaceCol # Globals
        pImateResizeValue = 0.55 # Image resize amount
        pImageName = Image.open(pImagePath) # Open a new image at the pImagePath address
        pImageWidth, pImageHeight = pImageName.size # Read image size
        pImageHeight = int((pImageHeight*pImateResizeValue)) # Set image height
        pHeightPercent = (pImageHeight / float(pImageName.size[1])) # Find height percent
        pImageWidth = int((float(pImageName.size[0]) * float(pHeightPercent))) # Set width to scale with height
        pImageName = pImageName.resize((pImageWidth,pImageHeight),Image.Resampling.LANCZOS) # Resize the image   
        pImageName = ImageTk.PhotoImage(pImageName) # Create a new PhotoImage of pImageName after the resize 
        pImageLabel = customtkinter.CTkLabel(gHomeScrollable_frame)
        pImageLabel.image = pImageName # Set the label image
        pImageButton = Button(
            gHomeScrollable_frame, 
            image=pImageName, # Image name value 
            width=pImageWidth, # Image width value
            height=pImageHeight, # Image heiht value
            command=partial(pFcommand, pGameName, pGamePath, pGameType, pExeName), # Values for when a button is clicked
            bd=0,
            highlightthickness=0 ) #Make a image button 
        #make a grid with 3 columns
        if gInterfaceCol > 2:
            gInterfaceCol = 0 # Reset col 
            gInterfaceRow += 2 # Add row value
        gInterfaceCol += 1 # Add col value
        pGameLabel = customtkinter.CTkLabel(gHomeScrollable_frame, text=pLabelText) # Create new label name
        pGameLabel.configure(font =("Orbitron", 20)) # Set the font of the Label
        pGameLabel.grid(row=gInterfaceRow, column=gInterfaceCol) # Add lable as grid
        pImageButton.grid(row=gInterfaceRow+1, column=gInterfaceCol, padx=30, pady=10) # Add button as grid
        gMainWindowCanvas.config(scrollregion=gMainWindowCanvas.bbox(ALL)) # Configure the scroll region

    global gInterfaceRow, gInterfaceCol # Globals
    gInterfaceRow = 0 # Reset row
    gInterfaceCol = 0 # Reset Col
    for widget in gHomeScrollable_frame.winfo_children(): #delete all content form the gHomeScrollable_frame
        widget.destroy()
    # Add images to interface,pInterfaceCreateGameButton(string image location, function click, string name, string enabled)
    pInterfaceCreateGameButton(r"content\data\absoluteAnnihilation.png",pLoadGame,"Absolute Annihilation","absoluteAnnEnabled","absoluteAnn", gUserinfo["absoluteAnnPath"],"na","na") # Absolute Annihilation
    pInterfaceCreateGameButton(r"content\data\bar.png",pLoadGame,"Beyond All Reason","barEnabled","bar", gUserinfo["barPath"],"na","na") # Beyond All Reason
    pInterfaceCreateGameButton(r"content\data\client.png",pLoadGame,"Forged Alliance Forever Client","fafClientEnabled","client", gUserinfo["fafClientPath"],"na","na") # FAF Client
    pInterfaceCreateGameButton(r"content\data\escalation.png",pLoadGame,"Total Annihilation Escalation","taEscalationEnabled","taEscalation", gUserinfo["taEscalationPath"],"na","na") # Total Annihilation Escalation
    pInterfaceCreateGameButton(r"content\data\imagefaf.png",pLoadGame,"Offline Forged Alliance Forever","fafEnabled","faf", gUserinfo["fafPath"],"na","na") # Supreme Commander Forged Alliance Forever
    pInterfaceCreateGameButton(r"content\data\loud.png",pLoadGame,"Forged Alliance LOUD","loudEnabled","loud", gUserinfo["loudPath"],"na","na") # Supreme Commander Forged Alliance LOUD
    pInterfaceCreateGameButton(r"content\data\mapeditor.png",pLoadGame,"FAF Map Editor","mapeditorEnabled","mapeditor", gUserinfo["mapedirorscPath"],"na","na") # FAF Map Editor
    pInterfaceCreateGameButton(r"content\data\prota.png",pLoadGame,"Total Annihilation ProTA","taProTAEnabled","taPro", gUserinfo["taProTAPath"],"na","na") # Total Annihilation ProTA
    pInterfaceCreateGameButton(r"content\data\sc.png",pLoadGame,"Supreme Commander","scEnabled","sc", gUserinfo["scPath"],"na","na") # Supreme Commander
    pInterfaceCreateGameButton(r"content\data\sc2.png",pLoadGame,"Supreme Commander 2","sc2Enabled","sc2", gUserinfo["sc2Path"],"na","na") # Supreme Commander 2
    pInterfaceCreateGameButton(r"content\data\scfa.png",pLoadGame,"Forged Alliance","scfaEnabled","fa", gUserinfo["scfaPath"],"na","na") # Supreme Commander Forged Alliance
    pInterfaceCreateGameButton(r"content\data\tamayhem.png",pLoadGame,"Total Annihilation Mayhem","taMayhemEnabled","taMay", gUserinfo["taMayhemPath"],"na","na") # Total Annihilation Mayhem
    pInterfaceCreateGameButton(r"content\data\ta.png",pLoadGame,"Total Annihilation","taEnabled","ta", gUserinfo["taPath"],"na","na") # Total Annihilation
    pInterfaceCreateGameButton(r"content\data\twilight.png",pLoadGame,"Total Annihilation Twilight","taTwilightEnabled","taTwilight", gUserinfo["taTwilightPath"],"na","na") # Total Annihilation Twilight
    pInterfaceCreateGameButton(r"content\data\taZero.png",pLoadGame,"Total Annihilation Zero","taZeroEnabled","taZero", gUserinfo["taZeroPath"],"na","na") # Total Annihilation Zero
    pInterfaceCreateGameButton(r"content\data\client_taforever.png" ,pLoadGame,"Total Annihilation Forever","taforeverEnabled","taforever", gUserinfo["taforeverPath"],"na","na") # Total Annihilation Forever
    pInterfaceCreateGameButton(r"content\data\taSteam.png",pLoadGame,"Total Annihilation Steam","taSteamEnabled","taSteam", gUserinfo["taSteamPath"],"steam","TotalA.exe") # Total Annihilation (Steam)
    pInterfaceCreateGameButton(r"content\data\scSteam.png",pLoadGame,"Supreme Commander Steam","scSteamEnabled","steamSC", gUserinfo["scSteamPath"],"steam","SupremeCommander.exe") # Supreme Commander(Steam)
    pInterfaceCreateGameButton(r"content\data\scfaSteam.png",pLoadGame,"Forged Alliance Steam","scfaSteamEnabled","steamFAF", gUserinfo["scfaSteamPath"],"steam","SupremeCommander.exe") # Supreme Commander Forged Alliance(Steam)
    pInterfaceCreateGameButton(r"content\data\sc2Steam.png",pLoadGame,"Supreme Commander 2 Steam","sc2SteamEnabled","sc2Steam", gUserinfo["sc2SteamPath"],"steam","SupremeCommander2.exe") # Supreme Commander 2 Steam
    pInterfaceCreateGameButton(r"content\data\paSteam.png",pLoadGame,"Planetary Annihilation Steam","paSteamEnabled","paSteam", gUserinfo["paSteamPath"],"steam","PA.exe") # Planetary Annihilation (Steam)
    pInterfaceCreateGameButton(r"content\data\zerok.png",pLoadGame,"Zero-K Steam","ZerokEnabled","ZeroK", gUserinfo["ZerokPath"],"steam","Zero-K.exe") # Zero-K (Steam)
    
    # Add custom games into the interface
    pPositionFound = False # Position in the ini to start adding new data
    pCount=0 # loop count
    for key, value in gUserData.items('USERINFO'): # Loop through the values in USERINFO
        if pPositionFound == False and key == "movetofarleftenabled": # check if the loop is upto moveToFarLeftEnabled
            pPositionFound = True # Found the start position
            continue
        elif pPositionFound == False :
            continue
        if pCount == 0 :
            pCustomTitleValue = value # Title value
            pCustomTitleKey = key # Title key
            pCount = 1
        elif pCount == 1 :
            pCustomPathValue = value # Path value
            pCustomPathKey = key # Path key
            pCount =2
        elif pCount == 2:
            pCustomEnabledValue = value # Enabled value
            pCustomEnabledKey = key # Enabled key
            pCount =3
        elif pCount == 3:
            pCount = 4
            pCustomImagePathValue = value # Image path value
            pCustomImagePathKey = key # Image path key
            pCustomImageName = os.path.basename(pCustomImagePathValue) # Get he base name for the path
        elif pCount == 4:
            pCutsomExeValue = value # Exe Value
            pCutsomExeKey = key # Exe key
            pCount = 0 # Reset count
            pGameType = "na" # Default game type
            pExeName = "na" # Default exe name
            if "steam://" in pCustomPathValue: # Check the the custom game is a steam game
                pGameType = "steam" # Set the game type to steam
                pExeName = pCutsomExeValue # Set the exe to steam type

            pInterfaceCreateGameButton(r"content\customGameData\\" + pCustomImageName, pLoadGame, pCustomTitleValue, pCustomEnabledKey, pCustomTitleValue, pCustomPathValue, pGameType, pExeName)

# File settings window
def gSettingsWindow() -> None:
    def pBoundSettingsCanvasMousewheel(event: tkinter.Event):
        pSettingsCanvas.bind_all("<MouseWheel>", pSettingsCanvasMousewheel)  

    def pUnboundSettungsCanvasMousewheel(event: tkinter.Event):
        pSettingsCanvas.unbind_all("<MouseWheel>") 

    def pSettingsCanvasMousewheel(event: tkinter.Event):
        pScrollUnits = 120 # Scroll units
        pSettingsCanvas.yview_scroll(int(-1*(event.delta/pScrollUnits)), "units")

    # Settings check box
    def pSettingsCheckboxCheck(
        pVarName: tkinter.IntVar,
        pEntryPath: tkinter.Entry, 
        pIniData:str, 
        pIniPath:str
    ) -> None:
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
        gReadWriteConfig("w") # Wright to the ini file with the updated settings

    #Create checkboxes
    def pSettingsCheckBox(
        pIniData,
        pCheckboxText
    ) -> None:
        def pCheckboxButtonClick(): # Check if the checkbox is enabled
            if pCheckboxValue.get() == 1:
                gUserinfo[pIniData] = "1" # Set ini data
            if pCheckboxValue.get() == 0:
                gUserinfo[pIniData] = "0" # Set ini data
            gReadWriteConfig("w") 
        pCheckboxValue = IntVar() # Var for pCheckboxButton variable
        # Create a new checkbox Button
        pCheckboxButton = customtkinter.CTkCheckBox(
            pSettingsScrollFrame, 
            text=pCheckboxText,
            variable=pCheckboxValue, 
            onvalue=1, 
            offvalue=0, 
            command=pCheckboxButtonClick,
            font =("Orbitron", 14)
        )
        pCheckboxButton.pack(
        anchor="w",
        pady=4,
        padx=5
        ) # Add the checkbox 
        if gUserinfo[pIniData] == "1": # Check ini data for checkbox status
            pCheckboxButton.select() # Select the check box if user saved data is checked

    # Apply button
    def pSettingApply() -> None:
        pSettingsWindow.destroy() # Close the settings window
        gChangeTheme()

    pSettingsWindow = customtkinter.CTkToplevel(gMainWindow) # Use customtkinter for the style of the toplevel window
    pSettingsWindow.title("Settings") # Set the Window title name
    pWindowWidth = gMainWindowWidth
    pWindowHeight = gMainWindowHeight
    pSettingsWindowX = (gWinfo_screenwidth - pWindowWidth) // 2 # Center window to X
    pSettingsWindowY = (gWinfo_screenheight - pWindowHeight) // 6 # Center window to Y
    pSettingsWindow.geometry(f"{pWindowWidth}x{pWindowHeight}+{pSettingsWindowX}+{pSettingsWindowY}")
    gExternal_handle_for_resizable(pSettingsWindow)
    pSettingsWindow.grab_set()
    pGameLinkArray = [] # Array to hold all the game urls 
    pSettingsWindow.after(200, lambda: pSettingsWindow.iconbitmap(gIconPath))
    pSettingsFrame = customtkinter.CTkFrame(master=pSettingsWindow,border_width=0) # Create frame
    pSettingsCanvas = Canvas(pSettingsFrame,bd=0, width= pWindowWidth-40, height=gMainWindowHeight - 30, bg="#2B2B2B", highlightthickness=0) # Create canvas for frame
    pSettingsFrameScrollbar = customtkinter.CTkScrollbar(pSettingsFrame, command=pSettingsCanvas.yview) # Create Scrollbar for canvas
    pSettingsScrollFrame = customtkinter.CTkFrame(master=pSettingsCanvas) # Create frame
    pSettingsScrollFrame.bind("<Configure>", lambda e: pSettingsCanvas.configure(scrollregion=pSettingsCanvas.bbox("all"))) # bind pSettingsScrollFrame to pSettingsCanvas 
    pSettingsCanvas.create_window((0, 0), window=pSettingsScrollFrame, anchor="nw") # New canvas for scrollable frame
    pSettingsCanvas.configure(yscrollcommand=pSettingsFrameScrollbar.set) # Configure canvas
    pSettingsFrame.pack()
    pSettingsCanvas.pack(side="left", fill="both", expand=False)
    pSettingsFrameScrollbar.pack(side="right", fill="y")    
    #Create the Checkboxes 
    pSettingsCheckBox("darkModeEnabled","Dark Mode")
    pSettingsCheckBox("minimizeallEnabled","Minimize all windows on game launch")
    pSettingsCheckBox("lockCursorEnabled","Lock cursor to active window when in windowed mode (Supported Games: SC,FA,FAF,LOUD) ")
    pSettingsCheckBox("autoSetMonitorEnabled","Auto set game window size when in windowed mode (Supported Games: SC,FA,FAF,LOUD Default 1920x1080) ")
    pSettingsCheckBox("autoSetDualScreenEnabled","Enable auto dual screen switcher (Experimental, needs Common Mod Tools and ui-party enabled, only for FA,FAF,LOUD)")
    pSettingsCheckBox("dualScreenDefaultEnabled","Start supported games in dual screen by default")
    pSettingsCheckBox("moveToFarLeftEnabled","Move game window to the far left (Disabled will use the main monitor position for game)")

    pHotkey1 = gCreateLabel(pSettingsScrollFrame, "Ctrl F12 (Switches to dual screen mode)", ("Orbitron", 14), TOP, "left","w") 
    pHotkey2 = gCreateLabel(pSettingsScrollFrame, "Ctrl F11 (Switches to single screen mode)", ("Orbitron", 14), TOP, "left","w") 
    pHotkey3 = gCreateLabel(pSettingsScrollFrame, "Ctrl F10 (End the ahk script)", ("Orbitron", 14), TOP, "left","w") 
    pNote1 = gCreateLabel(pSettingsScrollFrame, "For windowed dual screen mode install Common Mod Tools Mod and ui-party mod then enabled ui-party in", ("Orbitron", 14), TOP, "left","w") 
    pNote2 = gCreateLabel(pSettingsScrollFrame, "the mod menu. Within each game set the primary adapter to windowed and disable the secondary adapter.", ("Orbitron", 14),TOP, "left","w") 
    pNote3 = gCreateLabel(pSettingsScrollFrame, "(Supported Games for dual screen: FA,FAF,LOUD)", ("Orbitron", 14), TOP, "left","w") 
    #Add the apply button to the setting menu    
    pApplyButton = customtkinter.CTkButton(pSettingsWindow, text = "Apply", width = 10, command = pSettingApply)
    pSettingsWindow.protocol("WM_DELETE_WINDOW", pSettingApply)
    pApplyButton.pack(side = TOP)

# Url interface window
def gGameUrlWindow() -> None:
    def pUrlCanvasMousewheel(event):
        pUrlCanvas.yview_scroll(int(-1*(event.delta/120)), "units") # Mouse Y Scroll amount

    def pBoundUrlCanvasMousewheel(event):
        pUrlCanvas.bind_all("<MouseWheel>", pUrlCanvasMousewheel) # Bind mouse wheel to Canvas

    def pUnboundUrlCanvasMousewheel(event):
        pUrlCanvas.unbind_all("<MouseWheel>") # Unbind mouse wheel form Canvas

    # Remove a custom game from the config
    def pDeleteCustomGame(pCustomGameName:str) -> None:
        pFound = False
        pCount = 0
        # Look for the game name and then delete the next 4 settings after it
        for key, value in gUserData.items('USERINFO'):
            if value == pCustomGameName:
                pFound = True     
            if pFound == True:
                pCount = pCount + 1
                del gUserData["USERINFO"][key]
            if pCount == 5:
                pFound = False
                break
        gReadWriteConfig("w") 
        pUrlWindow.destroy()
        gGameUrlWindow()
        
    def pUrlCreateOptions(
        pLabelName,
        pLinkDefault,
        pIniData,
        pIniPath,
        pCustomGame) -> None:   
        def urlcheckboxCheck(
            pVarName,
            pEntryPath,
            pIniData,
            pIniPath):
            pVarNameValue = pVarName.get() # Cache the get() value of pVarName
            pEntryPathValue = pEntryPath.get() # Cache the get() value of pEntryPath
            if pVarNameValue == 1: # Check if state of the checkbox is checked
                gUserinfo[pIniData] = "1" # Set changed user data of game enabled
                gUserinfo[pIniPath] = pEntryPathValue # Set changed user data of game path 
                if pIniData not in pLockedGamePaths and not pEntryPathValue.startswith("steam://"): # Lock games with steam paths
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
            gReadWriteConfig("w") # Wright to the ini file with the updated settings

        global gSettingsRow  
        pVarName = IntVar() # Var for checkBox variable
        pUrlSettingsGamelabel = customtkinter.CTkLabel(pUrlScrollFrame, text=pLabelName,font =("Orbitron", 14)) # Create label for grid layout

        if pCustomGame == True:        
            pDelete = customtkinter.CTkButton(pUrlScrollFrame,
                fg_color="#1A1A1A",
                hover_color="red", 
                text = "X", 
                width = 10, 
                command=partial(pDeleteCustomGame,pLabelName))
            pDelete.grid(column=1,row=gSettingsRow,sticky = E,padx=50, pady=0)

        pEntryPath = customtkinter.CTkEntry(pUrlScrollFrame,width=900) # Create a new enray for game location
        pGameLinkArray.append(pEntryPath) # Add game link to array  
        pGameCheckBox = customtkinter.CTkCheckBox(pUrlScrollFrame, text="Enable", command=partial(urlcheckboxCheck,pVarName,pEntryPath,pIniData,pIniPath),
            font =("Orbitron", 14), variable=pVarName, onvalue=1, offvalue=0)
        pUrlSettingsGamelabel.grid(column=1,row=gSettingsRow,padx=100, pady=2) # Set lable location
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
   
    # Add Custom game settings
    def pUrlCreateCustomOptions() -> None:
        pCount = 0
        pCustomTitleValue = None
        pCustomTitleKey = None
        pCustomPathValue = None
        pCustomPathKey = None
        pCustomEnabledValue = None
        pCustomEnabledKey = None
        pPositionFound = False
        for key, value in gUserData.items('USERINFO'):
            if pPositionFound == False and key == "movetofarleftenabled":
                pPositionFound = True
                continue
            elif pPositionFound == False :
                continue
            if pCount == 0 :
                pCustomTitleValue = value
                pCustomTitleKey = key
                pCount = 1
            elif pCount == 1 :
                pCustomPathValue = value
                pCustomPathKey = key
                pCount =2
            elif pCount == 2 :
                pCount = 3
                pCustomEnabledValue = value
                pCustomEnabledKey = key
            elif pCount == 3:
                pCount = 4
                pUrlCreateOptions(pCustomTitleValue,pCustomPathValue ,pCustomEnabledKey,pCustomPathKey,True)
            else:
                pCount = 0

    # Apply button
    def pUrlApply() -> None:
        # Save the game path data to the config file
        gUserinfo["scSteamPath"] = pGameLinkArray[0].get()
        gUserinfo["scfaSteamPath"] = pGameLinkArray[1].get()
        gUserinfo["scPath"] = pGameLinkArray[2].get()
        gUserinfo["scfaPath"] = pGameLinkArray[3].get()
        gUserinfo["fafPath"] = pGameLinkArray[4].get()
        gUserinfo["fafClientPath"] = pGameLinkArray[5].get()
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
        gReadWriteConfig("w")
        gCreateInterface() # Recreate the window interface
        pUrlWindow.destroy()
        gMainWindow.deiconify()
        gChangeTheme()

    # Add new game
    def pNewGameApply() -> None:
        def newGameApplyCall() ->bool:
            #Copies a file from the source path to the destination folder. 
            def copy_file(pSourcePath, pDestinationFolder):
                if "steam://rungameid/" in pSourcePath:
                    return
                try: # Check if destination folder exists
                    if not os.path.exists(pDestinationFolder):
                        os.makedirs(pDestinationFolder)  # Create the folder if it doesn't exist

                    pDestinationFolder = os.path.join(pDestinationFolder, os.path.basename(pSourcePath))  # Combine folder and filename
                    shutil.copy2(pSourcePath, pDestinationFolder)  # Copy the file with preserving metadata
                except OSError as e:
                    pErrorCopyLabel.configure(text="InvalidError Error writing image file to content\\customGameData: check folder permissions ")
                    pErrorCopyLabel.pack()

            def get_image_dimensions(pImagePath):
                """
                Gets the height and width of an image at the given path.

                Args:
                    pImagePath (str): The local file path of the image.

                Returns:
                    tuple: A tuple containing the image width and height (width, height).
                    None: If there's an error opening the image.
                """

                try:
                    with Image.open(pImagePath) as image:
                        width, height = image.size
                        return width, height
                except OSError as e:
                    return None

            pAddWindow.focus_force()
            pErrorNameLabel.pack_forget()
            pErrorPathLabel.pack_forget()
            pErrorExeLabel.pack_forget()
            pErrorImageLabel.pack_forget()
            pErrorCopyLabel.pack_forget()    
            pNamePass = True
            pPathPass = True
            pExePass = True
            pImagePass = True
            pNamePassError = "None"
            pPathPassError = "None"
            pExePassError = "None"
            pImagePassError = "None"
            pGameName = pNewGameEntry.get()
            if pGameName:
                pNamePass = True
            else:
                pNamePassError = "InvalidError Game name: No game name provided"
                pNamePass = False
            if pNamePass == False :
                pErrorNameLabel.configure(text=pNamePassError)
                pErrorNameLabel.pack() 
            pGamePath = pGamePathEntry.get()
            if pGamePath:
                #Make a for loop to check game names
                for pGameUrl in pGameLinkArray:
                    if pGameUrl.get() == pGamePathEntry.get():
                        pPathPassError = "InvalidError Game path: Game with that path already exists"
                        pPathPass = False
                        break
            else:
                pPathPassError = "InvalidError Game path: No game path provided"
                pPathPass = False

            pGameExe = pGameExeEntry.get()
            if pGameExe: #check for game exe match
                pExePass = True
            else:
                pExePassError = "InvalidError Game exe: No game exe name provided"
                pExePass = False
            if pPathPass == False :
                pErrorPathLabel.configure(text=pPathPassError)
                pErrorPathLabel.pack()    

            pImagePath = pGameImagePathEntry.get()
            if(pImagePath == ""):
                pImagePath = ".\\content\\customGameData\\default.png"
          
            if pImagePath:
                if os.path.isfile(pImagePath):
                    width, height = get_image_dimensions(pImagePath)
                    if width == 554 and 300:
                        pImagePass = True
                    else:
                        pImagePass = False
                        pImagePassError = "InvalidError Game image: Failed image dimensions needs to be 554x300"
                else:
                    pImagePass = False
                    pImagePassError = f"InvalidError Game image: Error File not found at '{pImagePath}'"
            else:
                pImagePassError = "InvalidError Game image: No image path provided"
                pImagePass = False    

            if pImagePass == False :
                pErrorImageLabel.configure(text=pImagePassError)
                pErrorImageLabel.pack()

            if pNamePass and pPathPass and pExePass and pImagePass:
                pDestinationFolder = ".\\content\\customGameData"
                copy_file(pImagePath, pDestinationFolder)
                pInfoTitle = pGameName.replace(" ", "") 
                pInfoName = pGameName + "Path"
                pInfoName = pInfoName.replace(" ", "")
                pInfoState = pGameName + "Enabled"
                pInfoState = pInfoState.replace(" ", "")
                pInfoImageName = pInfoTitle + "ImagePath"
                pIntoExeNameTitle = pGameName.replace(" ", "") 
                pIntoExeNameTitle = pIntoExeNameTitle + "Exe"
                gUserData.set("USERINFO", pInfoTitle, pGameName)
                gUserData.set("USERINFO", pInfoName, pGamePath)
                gUserData.set("USERINFO", pInfoState, "1")
                gUserData.set("USERINFO", pInfoImageName, pImagePath)
                gUserData.set("USERINFO", pIntoExeNameTitle, pGameExe)
                gReadWriteConfig("w") 
                pAddWindow.destroy()
                pUrlWindow.destroy()
                gGameUrlWindow()

        pAddWindow = customtkinter.CTkToplevel(gMainWindow) # Use customtkinter for the style of the toplevel window
        pAddWindow.title("Add Custom Game URL") # Set the Window title name
        pAddWindowWidth = 800 # width for the Tk root
        pAddWindowHeight = 300  # height for the Tk root
        pAddWindowX = (gWinfo_screenwidth - pAddWindowWidth) // 2
        pAddWindowY = (gWinfo_screenheight - pAddWindowHeight) // 6
        pAddWindow.geometry(f"{pAddWindowWidth}x{pAddWindowHeight}+{pAddWindowX}+{pAddWindowY}")
        gExternal_handle_for_resizable(pAddWindow)
        pAddWindow.grab_set()
        pNewGameLabel = gCreateLabel(pAddWindow, "Game name", ("Orbitron", 14), LEFT, "left","center")
        pNewGameLabel.pack(side = TOP)
        pNewGameEntry = customtkinter.CTkEntry(pAddWindow, placeholder_text="Enter new game name",width= 700)
        pNewGameEntry.pack(side = TOP)
        pGamePathLabel = gCreateLabel(pAddWindow, "Game path (steam://rungameid/<numberID> or C:\\mygame\\mygame.exe)", ("Orbitron", 14), LEFT, "left","center") 
        pGamePathLabel.pack(side = TOP)
        pGamePathEntry = customtkinter.CTkEntry(pAddWindow, placeholder_text="Enter path to game exe",width= 700)
        pGamePathEntry.pack(side = TOP)
        pGameExeLabel = gCreateLabel(pAddWindow, "Game exe name (mygame.exe)", ("Orbitron", 14), LEFT, "left","center") 
        pGameExeLabel.pack(side = TOP)
        pGameExeEntry = customtkinter.CTkEntry(pAddWindow, placeholder_text="Enter the game exe name",width= 700)
        pGameExeEntry.pack(side = TOP)
        pGameImagePathLabel = gCreateLabel(pAddWindow, "Game image (must be 554x300)", ("Orbitron", 14), LEFT, "left","center") 
        pGameImagePathLabel.pack(side = TOP)
        pGameImagePathEntry = customtkinter.CTkEntry(pAddWindow, placeholder_text="\\content\\customGameData\\default.png",width= 700)
        pGameImagePathEntry.pack(side = TOP)
        pErrorNameLabel = gCreateLabel(pAddWindow, "Error", ("Orbitron", 14), LEFT, "left","center") 
        pErrorNameLabel.configure(text_color="red")
        pErrorNameLabel.pack(side = TOP)
        pErrorNameLabel.pack_forget()
        pErrorPathLabel = gCreateLabel(pAddWindow, "Error", ("Orbitron", 14), LEFT, "left","center") 
        pErrorPathLabel.configure(text_color="red")
        pErrorPathLabel.pack(side = TOP)
        pErrorPathLabel.pack_forget()
        pErrorExeLabel = gCreateLabel(pAddWindow, "Error", ("Orbitron", 14), LEFT, "left","center") 
        pErrorExeLabel.configure(text_color="red")
        pErrorExeLabel.pack(side = TOP)
        pErrorExeLabel.pack_forget()
        pErrorImageLabel = gCreateLabel(pAddWindow, "Error", ("Orbitron", 14), LEFT, "left","center") 
        pErrorImageLabel.configure(text_color="red")
        pErrorImageLabel.pack(side = TOP)
        pErrorImageLabel.pack_forget()
        pErrorCopyLabel = gCreateLabel(pAddWindow, "Error", ("Orbitron", 14), LEFT, "left","center") 
        pErrorCopyLabel.configure(text_color="red")
        pErrorCopyLabel.pack(side = TOP)
        pErrorCopyLabel.pack_forget()
        pApplyButton = customtkinter.CTkButton(pAddWindow, text = "Apply", width = 10, command = newGameApplyCall)
        pApplyButton.pack(side = BOTTOM)

    pLockedGamePaths = ["scSteamEnabled", "sc2SteamEnabled", "scfaSteamEnabled","paSteamEnabled", "taSteamEnabled", "ZerokEnabled"] # List of Locked games with paths
    pGameLinkArray = []
    pUrlWindow = customtkinter.CTkToplevel(gMainWindow) # Create new game url window
    pUrlWindow.title("Game URLs") # Set the Window title name
    pUrlWindowWidth = gMainWindowWidth # width for the Tk root
    pUrlWindowHeight = gMainWindowHeight  # height for the Tk root
    pUrlWindowX = (gWinfo_screenwidth - pUrlWindowWidth) // 2
    pUrlWindowY = (gWinfo_screenheight - pUrlWindowHeight) // 6
    pUrlWindow.geometry(f"{pUrlWindowWidth}x{pUrlWindowHeight}+{pUrlWindowX}+{pUrlWindowY}")
    gExternal_handle_for_resizable(pUrlWindow)
    pUrlWindow.grab_set()
    pUrlFrame = customtkinter.CTkFrame(master=pUrlWindow, border_width=0) # Create frame
    pUrlCanvas = Canvas(pUrlFrame,bd=0, width= pUrlWindowWidth-20, height=pUrlWindowHeight -30, bg="#2B2B2B", highlightthickness=0) # Create canvas for frame
    pUrlFrameScrollbar = customtkinter.CTkScrollbar(pUrlFrame, command=pUrlCanvas.yview) # Create Scrollbar for canvas
    pUrlScrollFrame = customtkinter.CTkFrame(master=pUrlCanvas) # Create 
    pUrlScrollFrame.bind("<Configure>", lambda e: pUrlCanvas.configure(scrollregion=pUrlCanvas.bbox("all"))) # bind pUrlScrollFrame to pUrlCanvas 
    pUrlCanvas.create_window((0, 0), window=pUrlScrollFrame, anchor="nw") # New canvas for scrollable frame
    pUrlCanvas.configure(yscrollcommand=pUrlFrameScrollbar.set) # Configure canvas
    pUrlCanvas.bind_all("<MouseWheel>", pUrlCanvasMousewheel) # Mouse Wheel scroll
    pUrlCanvas.bind('<Enter>', pBoundUrlCanvasMousewheel)
    pUrlCanvas.bind('<Leave>', pUnboundUrlCanvasMousewheel)
    pUrlFrame.pack()
    pUrlCanvas.pack(side="left", fill="both", expand=False)
    pUrlFrameScrollbar.pack(side="right", fill="y")
    #Create the settings interface 
    pUrlCreateOptions("Supreme Commander (Steam)",gUserinfo["scSteamPath"] ,"scSteamEnabled","scSteamPath",False)        
    pUrlCreateOptions("Forged Alliance (Steam)",gUserinfo["scfaSteamPath"] ,"scfaSteamEnabled","scfaSteamPath",False)
    pUrlCreateOptions("Supreme Commander",gUserinfo["scPath"] ,"scEnabled","scPath",False)        
    pUrlCreateOptions("Forged Alliance",gUserinfo["scfaPath"] ,"scfaEnabled","scfaPath",False)
    pUrlCreateOptions("Forged Alliance Forever",gUserinfo["fafPath"],"fafEnabled","fafPath",False)
    pUrlCreateOptions("Forged Alliance Forever Client",gUserinfo["fafClientPath"] ,"fafClientEnabled","fafClientPath",False)
    pUrlCreateOptions("LOUD Forged Alliance",gUserinfo["loudPath"] ,"loudEnabled","loudPath",False)
    pUrlCreateOptions("FAF Map Editor",gUserinfo["mapedirorscPath"] ,"mapeditorEnabled","mapedirorscPath",False)
    pUrlCreateOptions("Supreme Commander 2 (Steam)",gUserinfo["sc2SteamPath"] ,"sc2SteamEnabled","sc2SteamPath",False)   
    pUrlCreateOptions("Supreme Commander 2",gUserinfo["sc2Path"] ,"sc2Enabled","sc2Path",False)   
    pUrlCreateOptions("Planetary Annihilation (Steam)",gUserinfo["paSteamPath"] ,"paSteamEnabled","paSteamPath",False)
    pUrlCreateOptions("Total Annihilation Forever",gUserinfo["taforeverPath"] ,"taforeverEnabled","taforeverPath",False)
    pUrlCreateOptions("Total Annihilation (Steam)",gUserinfo["taSteamPath"] ,"taSteamEnabled","taSteamPath",False)
    pUrlCreateOptions("Total Annihilation",gUserinfo["taPath"] ,"taEnabled","taPath",False)
    pUrlCreateOptions("Total Annihilation Escalation",gUserinfo["taEscalationPath"] ,"taEscalationEnabled","taEscalationPath",False)
    pUrlCreateOptions("Total Annihilation Mayhem",gUserinfo["taMayhemPath"] ,"taMayhemEnabled","taMayhemPath",False)
    pUrlCreateOptions("Total Annihilation ProTA",gUserinfo["taProTAPath"] ,"taProTAEnabled","taProTAPath",False)
    pUrlCreateOptions("Total Annihilation Twilight",gUserinfo["taTwilightPath"] ,"taTwilightEnabled","taTwilightPath",False)
    pUrlCreateOptions("Total Annihilation Zero",gUserinfo["taZeroPath"] ,"taZeroEnabled","taZeroPath",False)
    pUrlCreateOptions("Absolute Annihilation",gUserinfo["absoluteAnnPath"] ,"absoluteAnnEnabled","absoluteAnnPath",False)
    pUrlCreateOptions("Beyond All Reason",gUserinfo["barPath"] ,"barEnabled","barPath",False)
    pUrlCreateOptions("Zero-K (Steam)",gUserinfo["ZerokPath"] ,"ZerokEnabled","ZerokPath",False)
    pUrlCreateCustomOptions()
    pAdd = customtkinter.CTkButton(pUrlWindow, text = "Add Custom Game", width = 10, command = pNewGameApply)
    pAdd.pack(side = LEFT)
    pApplyButton = customtkinter.CTkButton(pUrlWindow, text = "Apply", width = 10, command = pUrlApply)
    pUrlWindow.protocol("WM_DELETE_WINDOW", pUrlApply)
    pApplyButton.pack(side = RIGHT)

#About interface window
def gAboutWindow() -> None:
    pAboutWindow = customtkinter.CTkToplevel(gMainWindow) # Create the about window
    pAboutWindow.title("About") # Set the Window title name
    pAboutWindow.after(200, lambda: pAboutWindow.iconbitmap(gIconPath)) # Set window icon (after a slight delay to avoid potential issues)
    # Define window dimensions and position
    pAboutWindowWidth = 700
    pAboutWindowHeight = gMainWindowHeight
    pAboutWindowX = (gWinfo_screenwidth - pAboutWindowWidth) // 2
    pAboutWindowY = (gWinfo_screenheight - pAboutWindowHeight) // 6
    pAboutWindow.geometry(f"{pAboutWindowWidth}x{pAboutWindowHeight}+{pAboutWindowX}+{pAboutWindowY}")
    gExternal_handle_for_resizable(pAboutWindow)
    pAboutWindow.grab_set()
    #Labels for about page
    pAppVersionLabel = gCreateLabel(pAboutWindow, gLauncherName + " - " + gLauncherVersion, ("Orbitron", 14), TOP, "left","center") 
    pScriptVersionLabel = gCreateLabel(pAboutWindow, "Supreme Commander Definitive Windowed Borderless Script - " + gAutoHotKeyScriptVersion + " " + gAutoHotKeyVersion, ("Orbitron", 14), TOP,"left","center") 
    pPythonVersionLabel = gCreateLabel(pAboutWindow, "Python Version - " + gPythonVersion, ("Orbitron", 14), TOP,"left","center") 
    pCreatedByLabel = gCreateLabel(pAboutWindow, "Created by ageekhere 2024", ("Orbitron", 14), TOP,"left","center")
    pGithubLabel = gCreateLabel(pAboutWindow, "https://github.com/ageekhere/Definitive-Supreme-Commander-Launcher", ("Orbitron", 14), TOP,"left","center")
    pGithubLabel.configure(text_color=("white", "blue"))
    pGithubLabel.bind("<Button-1>", lambda event, link="https://github.com/ageekhere/Definitive-Supreme-Commander-Launcher": webbrowser.open(link))
    pGameListLabel = gCreateLabel(pAboutWindow, "\n\
        Supported Games \n \n\
        Absolute Annihilation \n\
        Forged Alliance Forever Client \n\
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

#--------------------------------------------------------------------------------------------------
customtkinter.deactivate_automatic_dpi_awareness() # Disable DPI scaling for now
# load the splash screen 
if getattr(sys, 'frozen', False):
    import pyi_splash

# Close the splash screen
if getattr(sys, 'frozen', False):
    pyi_splash.close()

#global variables
gLauncherName = "Definitive Supreme Commander Launcher" # App name
gLauncherVersion = "1.0.8.1" # App version
gLauncherGitVersionName ="version1.081" # Current app git version name
gPythonVersion = "3.12.4" # Python version app is using
gAutoHotKeyScriptVersion = "1.14" # Version of autohotkey script
gAutoHotKeyVersion = "AutoHotkeyU32 1.1.37.02"
gAutoHotkeyLocation = "content/scripts/AutoHotkeyU32.exe" # Path to AutoHotkeyU32 
gAutoHotkeyScriptLocation = "content/scripts/main.ahk" # Path to AutoHotKey script
gGitHubReleasesLink = "https://github.com/ageekhere/Definitive-Supreme-Commander-Launcher/releases"
gConfigPath = Path("content/config/config.ini") # Relative path to INI file
gIconPath = "content/icon/dscl_icon.ico" # Icon path
gUserData = ConfigParser() # New ConfigParser to reference an INI file
gInterfaceRow = 0 # Row grid layout of the main interface
gInterfaceCol = 0 # Col grid layout of the main interface
gSettingsRow = 0 # Keeps track of the row in settings

# User saved data
if gConfigPath.is_file(): # Check if the INI file exists
    gReadWriteConfig("r") # Read the config file
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
    "fafClientEnabled": "0",
    "fafClientPath": r"C:\faf-client.exe",
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
    "taforeverPath": r"C:\taf-java-client",
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
    "updateLastCheck": "2024-01-01",
    "updateLatestVersion": gLauncherGitVersionName,
    "darkModeEnabled":"1",
    "minimizeallEnabled":"1",
    "dualScreenDefaultEnabled":"0",
    "moveToFarLeftEnabled":"0",
    }
    
    gReadWriteConfig("w") # Wright to the config
    gReadWriteConfig("r") # Read the new config
gUserinfo = gUserData["USERINFO"] # Store the INI settings information
gChangeTheme() # Update the app theme

# Create the main window for the app 
gMainWindow = customtkinter.CTk() # Use customtkinter for the style of the main window
gMainWindow.title(gLauncherName + " - " + gLauncherVersion) # Set the title of the Main window
gMainWindow.iconbitmap(gIconPath) # Set the icon image for the window
gMainWindow.resizable(0,0) # disable window maximize
gWinfo_screenwidth = gMainWindow.winfo_screenwidth()
gWinfo_screenheight = gMainWindow.winfo_screenheight()
# set the size and position of the main window
gMainWindowWidth = 1110 # width for the Tk root
gMainWindowHeight = 680  # height for the Tk root
gMainWindowX = (gWinfo_screenwidth - gMainWindowWidth) // 2
gMainWindowY = (gWinfo_screenheight - gMainWindowHeight) // 6
gMainWindow.geometry(f"{gMainWindowWidth}x{gMainWindowHeight}+{gMainWindowX}+{gMainWindowY}")

#Options menu
gOptionMenuVar = customtkinter.StringVar(value="Menu")  # set the menu option for the file menu
gOptionsMenu = customtkinter.CTkOptionMenu(master=gMainWindow,
    values=["Game URLs", "Settings", "About", "Exit"], # Different options
    command=gMainOptionsMenu, # Options menu function
    variable=gOptionMenuVar, # Options menu var
    width=80, # Options menu width
    corner_radius=0, # Options menu button radius
    font=("Orbitron", 16), # Options menu font and size
    dropdown_font=("Orbitron", 15)) # Options menu dropdown font and size
gOptionsMenu.pack(side="top", anchor=NW) # Add options menu 

gUpdateChecker() # Check for app updates

gReadWriteConfig("r") # Read updated config
# Main interface
gMainWindowCanvas = customtkinter.CTkCanvas(master=gMainWindow) # Create the main canvas (outermost) 
gHomeContainer = customtkinter.CTkFrame(master=gMainWindowCanvas) # Create the main frame (contained within the main canvas)
# Create the scrollable canvas (innermost)
gHomeCanvas = customtkinter.CTkCanvas(
    master=gHomeContainer,
    width=gMainWindowWidth - 22,
    height=gMainWindowHeight,
    bg="#2B2B2B",
    highlightthickness=0,
    bd=0,
)
pHomeScrollbar = customtkinter.CTkScrollbar(master=gHomeContainer, command=gHomeCanvas.yview)# Create the scrollbar for the scrollable canvas
gHomeScrollable_frame = customtkinter.CTkFrame(master=gHomeCanvas) # Create the scrollable frame (content to be scrolled)
gHomeScrollable_frame.bind("<Configure>", lambda e: gHomeCanvas.configure(scrollregion=gHomeCanvas.bbox("all"))) # Bind the scrollable frame size to the canvas scrollregion
gHomeCanvas.create_window((0, 0), window=gHomeScrollable_frame, anchor="nw") # Create a window within the scrollable canvas to hold the scrollable frame
gHomeCanvas.configure(yscrollcommand=pHomeScrollbar.set) # Configure the scrollbar command for the scrollable canvas
# Layout the widgets
gHomeContainer.pack(fill="both", expand=True)  # Pack the container within the outer canvas (fill and expand)
pHomeScrollbar.pack(side="right", fill="y")  # Pack the scrollbar on the right side
gHomeCanvas.pack(side="left", fill="both", expand=True) # Pack the innermost canvas within the main window (fill and expand)
gMainWindowCanvas.pack()
# Bind mouse wheel and enter/leave events
gHomeCanvas.bind_all("<MouseWheel>", gHomeCanvasMousewheel)
gHomeCanvas.bind('<Enter>', gBoundHomeCanvasMousewheel)
gHomeCanvas.bind('<Leave>', gUnboundHomeCanvasMousewheel)
gCreateInterface() #create the main gMainWindowCanvas

gMainWindow.mainloop()