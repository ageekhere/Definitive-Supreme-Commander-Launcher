;//Supreme Commander Definitive Windowed Borderless Script
;//ageekhere, tatsu, IO_Nox other sources on the net
;//1.08

;//Supports 
;//dual Monitors of the same resolution
;//mouse cursor traping
;//Supreme Commander steam version
;//Supreme Commander Forged Alliance steam version
;//Forged Alliance Forever 
;//Downlord's FAF Client
;//LOUD

;//limitations
;//Only supports monitors of the same resolution
;//ui-party does not support steam Supreme Commander (9350)

#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%
#Persistent

global gamePathArg:= A_Args[2]
global lockCursorArg:= A_Args[3]
global autoSetMonitorArg:= A_Args[4]
global autoSetDualScreenArg:= A_Args[5]
global gameExe:= A_Args[6]

;//all personal variables are here
global moveX := 0 ;//Sets the main screen x location, 0 being the "main display" X location
global moveY := 0 ;//Sets the main screen x location, 0 being the "main display" Y location
global width := 0 ;//resolution width (do not change)
global height := 0 ;//resolution height (do not change)
global clipMouse = true ;//This will trap the mouse cursor within the game while the game window is active, you can use windows key to deactivate the game window,
global restoreWindow = false

if(lockCursorArg = 0)
{ ;//Disable the mouse clip from user settings
	clipMouse := false
}

global autoSetMonitorSize := true ;//set to use auto set resolution 
if(autoSetMonitorArg = 0)
{ ;//Disable auto monitor size
	autoSetMonitorSize := false
}

global enableAutoDualScreen := true ;//Auto checks if a game is loading and switches to dual screen mode
if(autoSetDualScreenArg = 0)
{ ;//Disable auto dual screen switcher
	enableAutoDualScreen := false 
} 
else
{ ;//Only support FA, FAF,downlord client and loud for auto dual screen 
	enableAutoDualScreen := false 
	if(A_Args[1] == "fa" || A_Args[1] =="faf" || A_Args[1] == "client" ||  A_Args[1] == "loud")
	{
		enableAutoDualScreen := true 
	}
}

if(autoSetMonitorSize == true)
{
	SysGet, primMon, Monitor ;//Get the current primary monitor that is active
	if(primMonRight != 0 || primMonBottom !="")
		width := primMonRight ; //set width resolution
	else if(primMonLeft != 0 || primMonBottom !="")
		width := % primMonLeft
	else 
		width := %A_ScreenWidth%

	if(primMonBottom != 0 || primMonBottom !="")
		height := primMonBottom ; //set width resolution
	else if(primMonTop != 0 || primMonBottom !="")
		height := primMonTop
	else 
		height := %A_ScreenHeight%
	
	;//if the value is negative change it to positive number
	if(width < 0)
	{
		width := (-1 * width)
	}
	if(height < 0)
	{
		height := (-1 * height)
	}	
}
else
{ ;//manually set monitor resolution size
	width := 1920  ;2560, 3840 ;//Sets the width resolution, for 1080p use (1920), for 1440p use (2560), for 4k use (3840) or use a custom value
	height := 1080  ;1440, 2160 ;//Sets the height resolution
}

global startInDualScreenMode := false ;//Set the default Screen mode on startup, true is start in dual screen mode
global dualScreenActive := startInDualScreenMode ;//(do not change)
;//hotkey for dual screen mode is Ctrl F12
;//hotkey for single screen mode is Ctrl F11
;//hotkey for exit script is Ctrl F10

;//Set the number of processor threads to use, by default it will find auto find the max supported processors
EnvGet, ProcessorCount, NUMBER_OF_PROCESSORS

firstArg := A_Args[1] ;//get shortcut parameters command line first arguments 
StringLower, lowerCaseFirstArg, firstArg ;//Sets firstArg to lower case, not really needed but just in case the user puts in a uppercase value

;//Run the following exe based off pram from shortcut
;//procGame - Sets which game exe name to use, this is the exe that will have the width and height changed
;//procName - Sets which exe that needs to be closed to stop the ahk script (e.g for the Downlord's FAF Client the script will stop once the client is shutdown and not the game exe)
;//procPath - Sets the game path
;//Run, %procName%, %procPath% - run the exe at the path
global loaded := false ;// has the game loaded
global procGame := 0
global procName := 0
global procPath := 0


if(lowerCaseFirstArg = "client")
{ ;//Run the Downlord's FAF Client
	procGame := "ForgedAlliance.exe"
	procName := gameExe
	procPath := gamePathArg
	checkGameFile(procName,procPath)
	WinMinimizeAll
	Run, %procName%, %procPath%
}
else if(lowerCaseFirstArg = "faf" )
{ ;//Run Forged Alliance Forever
	
	procGame := gameExe
	procName := gameExe
	procPath := gamePathArg
	checkGameFile(procName,procPath)
	WinMinimizeAll
	Run, %procName%, %procPath%
}
else if(lowerCaseFirstArg = "steamFAF")
{ ;//Run upreme Commander Forged Alliance steam version
	procGame := gameExe
	procName := gameExe
	procPath := gamePathArg
	WinMinimizeAll
	Run, %procPath%
}
else if(lowerCaseFirstArg = "loud")
{ ;//Run LOUD 
	procGame := "ForgedAlliance.exe"
	procName := gameExe
	procPath := gamePathArg
	checkGameFile(procName,procPath)
	WinMinimizeAll
	Run, %procName%, %procPath%
}
else if(lowerCaseFirstArg = "steamSC")
{ ;
	procGame := gameExe
	procName := gameExe
	procPath := gamePathArg
	WinMinimizeAll
	Run, %procPath%
}

else if(lowerCaseFirstArg = "sc2Steam")
{ ;
	procGame := gameExe
	procName := gameExe
	procPath := gamePathArg
	WinMinimizeAll
	Run, %procPath%
	quit()
}
else if(lowerCaseFirstArg = "taSteam")
{ ;
	procGame := gameExe
	procName := gameExe
	procPath := gamePathArg
	WinMinimizeAll
	Run, %procPath%
	quit()
}
else if(lowerCaseFirstArg = "ZeroK")
{ ;
	procGame := gameExe
	procName := gameExe
	procPath := gamePathArg
	WinMinimizeAll
	Run, %procPath%
	quit()
}
else if(lowerCaseFirstArg = "paSteam")
{ ;
	procGame := gameExe
	procName := gameExe
	procPath := gamePathArg
	WinMinimizeAll
	Run, %procPath%
	quit()
}

else if(lowerCaseFirstArg = "mapeditor")
{ ;//Run LOUD 
	procGame := gameExe
	procName := gameExe
	procPath := gamePathArg
	checkGameFile(procName,procPath)
	WinMinimizeAll
	Run, %procName%, %procPath%
	quit()
}

else
{ ;
	procGame := gameExe
	procName := gameExe
	procPath := gamePathArg
	checkGameFile(procName,procPath)
	WinMinimizeAll
	Run, %procName%, %procPath%
	quit()
}

checkGameFile(exe,path)
{
	join = %path%%exe%
	if !FileExist(join)
	{
		MsgBox, Could not find %join% make sure you set the correct game location 
		quit()
	}
}

Process, Wait, %procName%, 120 ;//Wait upto 120 seconds for the exe to start
procPID := ErrorLevel ;//set the error level

;//if the exe does not start show an error message and exit the script
if not procPID
{ 
	MsgBox The specified process did not appear.
    ExitApp ; Stop this script
}

;//Call the exitProc function after the set time
SetTimer, exitProc, 1000 
;//Call the CheckProc function after the set time
SetTimer, CheckProc, 1000
if(clipMouse == true)
{
	SetTimer, clipProc, 100 
}

;// Try and auto detect if the game is loading or has finished
if(enableAutoDualScreen = true)
{
	SetTimer, loadingSearch, 10
	SetTimer, endGameSearch, 1000
	SetTimer, endGameSearch, OFF
}
;//Function that will Manually switch from dual screen to single screen
resize(x, y, gametype,active) 
{
	if(active = true)
	{
		if(dualScreenActive = true)
			return
		dualScreenActive := true
	}
	else
	{
		if(dualScreenActive = false)
			return
		dualScreenActive := false
	}	
		WinMove, % "ahk_exe " gametype , , moveX, moveY, %x%, %y% 
		WinMaximize, % "ahk_exe " gametype
		WinRestore, % "ahk_exe " gametype
		WinActivate ;
}

;//Hot key to switch from dual screen to single screen or to exit the script
^F12::resize(width*2, height,procGame,true) ;//Ctrl F12 to enter dual screen mode
^F11::resize(width, height,procGame,false) ;//Ctrl F11 to enter single screen mode
^F10::quit() ;//Ctrl F10 to stop the script

;//Resize the game on start up,
CheckProc:
	if (!ProcessExist(procGame)) 
		return
	WinGet Style, Style, % "ahk_exe " procGame ;
	
	;//Get game Process Priority of the game
	GetPriority(P="current") 
	{
		static r32:="N", r64:="L", r128:="H" , r256:="R", r16384:="B", r32768:="A"
		Process, Exist, % (P="current") ? "" : (P="") ? 0 : P
		R:=DllCall("GetPriorityClass","UInt",hP:=DllCall("OpenProcess","UInt",0x400,"Int",0,"UInt",(P+1) ? P : ErrorLevel))
		DllCall("CloseHandle","UInt",hP)
		return r%R%
	}
	procPriority := GetPriority(procGame)
	;//Set the game Process Priority when it is not H
	;//NOTE procPriority != "H" does not seem to work correctly
	if(procPriority == "N" or procPriority == "L" or procPriority == "R" or procPriority == "B" or procPriority == "A")
	{ 
		Process, Priority, %procGame%, H
	}
	
	if (Style & 0xC40000)
	{ 
        WinSet, Style, -0xC40000, % "ahk_exe " procGame ;//removes the titlebar and borders
		windowWidth := width ;//sets the windowWidth value to width
		;//Checks the default screen mode
		if(startInDualScreenMode = true) 
		{ 
			windowWidth := windowWidth*2 ;//use dual screen mode as default
		}
		; //move the window to 0,0 and resize it to fit across 1 or 2 monitors.
		WinMove, % "ahk_exe " procGame , , moveX, moveY, windowWidth, height
        WinMaximize, % "ahk_exe " procGame
        WinRestore, % "ahk_exe " procGame
		; //sets the number of processors to use, by default it will use all processor
		gamePID := ErrorLevel
        ProcessHandle := DllCall("OpenProcess", "UInt", 0x1F0FFF, "Int", false, "UInt", gamePID)
        DllCall("SetProcessAffinityMask", "UInt", ProcessHandle, "UInt", ProcessorCount )
		DllCall("CloseHandle", "UInt", ProcessHandle)
		loaded := true
		restoreWindow := true
		
		; //Minimize all windows except the active game
		WinGet, id, list,,, Program Manager
		Loop, %id%
		{
			this_ID := id%A_Index%
			WinGetTitle, active_title, A
			WinGetTitle, title, ahk_id %this_ID%
			If title = %active_title%
			Continue
			WinMinimize, %title%
		}
    }
return

clipProc: 
	if (!ProcessExist(procGame)) 
		return
	
	;//checks if the game window is active
	if !WinActive("ahk_exe " procGame)
	{
		return
	}	
	;//trap mouse
	Confine := !Confine
	setWidth := width
	;//trap mouse to dual screen
	if(dualScreenActive == true)
	{
		setWidth := setWidth * 2
	}
	ClipCursor( Confine, 0, 0, setWidth, height)
	
return

loadingSearch:
	if (!ProcessExist(procGame)) 
	{
		settimer, endGameSearch, OFF
		settimer, loadingSearch, ON
		if(dualScreenActive = true)
		{
			dualScreenActive := false
		}
		return
	}

	if !WinActive("ahk_exe " procGame)
	{
		return
	}	
	;
	if(dualScreenActive = true)
		return
	if(!loaded) 
		return
	
	loop, %A_ScriptDir%\pics\loadgame\*.*
	{
	  CoordMode Pixel,Relative
	  ImageSearch, FoundX, FoundY, 0, 0, width, height, *50, %A_ScriptDir%\pics\loadgame\%A_Index%.jpg ;
	  if (ErrorLevel = 0)
	  {
		resize(width*2, height,procGame,true)
		settimer, endGameSearch, ON
		settimer, loadingSearch, OFF
		break
	  }
	 }
return

; //Check to see if the game has ended are the users in at the stats menu, working for FAF and LOUD 
endGameSearch:
	if (!ProcessExist(procGame)) 
	{ ;//Check if the game is running
		settimer, endGameSearch, OFF
		settimer, loadingSearch, ON
		if(dualScreenActive = true)
		{ ;//disable dual screen
			dualScreenActive := false
		}
		return
	}
	if !WinActive("ahk_exe " procGame)
	{
		return
	}	
	;//return if not in dual screen mode
	if(dualScreenActive = false)
		return
	
	;//checks if game is loaded
	if(!loaded) 
		return
	
	loop, %A_ScriptDir%\pics\endgame\*.*
	{ ;//Loop through all the images in endgame
	  CoordMode Pixel,Relative
	  ImageSearch, FoundX, FoundY, 0, 0, width*2, height, *80, %A_ScriptDir%\pics\endgame\%A_Index%.jpg ;
	  if (ErrorLevel = 0)
	  {
		resize(width, height,procGame,false)
		settimer, endGameSearch, OFF
		settimer, loadingSearch, ON
		break
	  }
	 }
return

; //lock the mouse within the game window
ClipCursor( Confine=True, x1=0 , y1=0, x2=1, y2=1 ) 
{
	VarSetCapacity(R,16,0),  NumPut(x1,&R+0),NumPut(y1,&R+4),NumPut(x2,&R+8),NumPut(y2,&R+12)
	return Confine ? DllCall( "ClipCursor", UInt,&R ) : DllCall( "ClipCursor" )
}

;//Check if the process exist
ProcessExist(exeName)
{ 
   Process, Exist, %exeName%
   return !!ERRORLEVEL
}

;//exit script if the procName is not running
exitProc:
	if (ProcessExist(procName) = 0)
	{
		;//NOTE due to a bug Restoring the Launcher window after the game exits does not work correctly
		;if (ProcessExist("Definitive Supreme Commander Launcher.exe") != 0)
		;{
			;WinRestore , ahk_exe Definitive Supreme Commander Launcher.exe	
		;}
		quit()
	}
	; //Restore the client once (if used) when game has stopped running
	if (ProcessExist(procGame) = 0 && restoreWindow = true && ProcessExist(procName) != 0)
	{
		WinRestore , ahk_exe %procName%
		restoreWindow := false
	}	
return	

;//exit the script
quit()
{ 	
	ExitApp
}
return