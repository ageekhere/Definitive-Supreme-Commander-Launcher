;//Supreme Commander Definitive Windowed Borderless Script
;//ageekhere, tatsu, IO_Nox other sources on the net
;//1.11

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

;Values that are passed from python
global gGameName := A_Args[1] ;//get shortcut parameters command line first arguments 
global gGameDir:= A_Args[2]
global gLockCursorArg:= A_Args[3]
global gAutoSetMonitorArg:= A_Args[4]
global gAutoSetDualScreenArg:= A_Args[5]
global gameExe:= A_Args[6]
global minimizeOnGameStart:= A_Args[7]
global gStartInDualScreenMode:= A_Args[8] ;//Set the default Screen mode on startup, true is start in dual screen mode
global gMoveX := 0 ;//Sets the main screen x location, 0 being the "main display" X location
global gMoveY := 0 ;//Sets the main screen x location, 0 being the "main display" Y location
global gResolutionWidth := 0 ;//resolution width (do not change)
global gResolutionHeight := 0 ;//resolution height (do not change)
global gRestoreWindow = false
global gLoadingSearchDelayCount = 0
global gGameLoadCheck := false ;// has the game loaded
global gSelectedGame := 0
global gSelectedGameExe := 0
global gSelectedGameDir := 0
global gEnableAutoDualScreen := false ;//Auto checks if a game is loading and switches to dual screen mode

if(gStartInDualScreenMode = 1)
{
	gStartInDualScreenMode := true
}
Else
{
	gStartInDualScreenMode := false
}
global gDualScreenActive := gStartInDualScreenMode ;//(do not change)
EnvGet, gProcessorCount, NUMBER_OF_PROCESSORS ;//Set the number of processor threads to use, by default it will find auto find the max supported processors

if(gAutoSetDualScreenArg = 1)
{ ;//Only support FA, FAF,downlord client and loud for auto dual screen 
	if(A_Args[1] == "fa" || A_Args[1] =="faf" || A_Args[1] == "client" ||  A_Args[1] == "loud")
	{
		gEnableAutoDualScreen := true 
	}
}

if(gAutoSetMonitorArg = 1)
{
	SysGet, primMon, Monitor ;//Get the current primary monitor that is active
	if(primMonRight != 0 || primMonBottom !="")
		gResolutionWidth := primMonRight ; //set width resolution
	else if(primMonLeft != 0 || primMonBottom !="")
		gResolutionWidth := % primMonLeft
	else 
		gResolutionWidth := %A_ScreenWidth%

	if(primMonBottom != 0 || primMonBottom !="")
		gResolutionHeight := primMonBottom ; //set width resolution
	else if(primMonTop != 0 || primMonBottom !="")
		gResolutionHeight := primMonTop
	else 
		gResolutionHeight := %A_ScreenHeight%
	
	;//if the value is negative change it to positive number
	if(gResolutionWidth < 0)
	{
		gResolutionWidth := (-1 * gResolutionWidth)
	}
	if(gResolutionHeight < 0)
	{
		gResolutionHeight := (-1 * gResolutionHeight)
	}	
}
else
{ ;//manually set monitor resolution size
	gResolutionWidth := 1920 ;2560, 3840 ;//Sets the width resolution, for 1080p use (1920), for 1440p use (2560), for 4k use (3840) or use a custom value
	gResolutionHeight := 1080  ;1440, 2160 ;//Sets the height resolution
}
if(gGameName = "client")
	{ ;//Run the Downlord's FAF Client
		gSelectedGame := "ForgedAlliance.exe"
		gSelectedGameExe := gameExe
		gSelectedGameDir := gGameDir
		checkGameFile(gSelectedGameExe,gSelectedGameDir)
		if(minimizeOnGameStart == 1) 
		{
			WinMinimize, A
		}
		Run, %gSelectedGameExe%, %gSelectedGameDir%
	}
	else if(gGameName = "faf" )
	{ ;//Run Forged Alliance Forever
		
		gSelectedGame := gameExe
		gSelectedGameExe := gameExe
		gSelectedGameDir := gGameDir
		checkGameFile(gSelectedGameExe,gSelectedGameDir)
		if(minimizeOnGameStart == 1) 
		{
			WinMinimizeAll
		}
		Run, %gSelectedGameExe%, %gSelectedGameDir%
	}
	else if(gGameName = "steamFAF")
	{ ;//Run upreme Commander Forged Alliance steam version
		gSelectedGame := gameExe
		gSelectedGameExe := gameExe
		gSelectedGameDir := gGameDir
		if(minimizeOnGameStart == 1) 
		{
			WinMinimizeAll
		}
		Run, %gSelectedGameDir%
	}
	else if(gGameName = "loud")
	{ ;//Run LOUD 
		gSelectedGame := "ForgedAlliance.exe"
		gSelectedGameExe := gameExe
		gSelectedGameDir := gGameDir
		checkGameFile(gSelectedGameExe,gSelectedGameDir)
		if(minimizeOnGameStart == 1) 
		{
			WinMinimizeAll
		}
		Run, %gSelectedGameExe%, %gSelectedGameDir%
	}
	else if(gGameName = "steamSC")
	{ ;
		gSelectedGame := gameExe
		gSelectedGameExe := gameExe
		gSelectedGameDir := gGameDir
		if(minimizeOnGameStart == 1) 
		{
			WinMinimizeAll
		}
		Run, %gSelectedGameDir%
	}
	else if(gGameName = "sc2Steam")
	{ ;
		gSelectedGame := gameExe
		gSelectedGameExe := gameExe
		gSelectedGameDir := gGameDir
		if(minimizeOnGameStart == 1) 
		{
			WinMinimizeAll
		}
		Run, %gSelectedGameDir%
		quit()
	}
	else if(gGameName = "taSteam")
	{ ;
		gSelectedGame := gameExe
		gSelectedGameExe := gameExe
		gSelectedGameDir := gGameDir
		if(minimizeOnGameStart == 1) 
		{
			WinMinimizeAll
		}
		Run, %gSelectedGameDir%
		quit()
	}
	else if(gGameName = "ZeroK")
	{ ;
		gSelectedGame := gameExe
		gSelectedGameExe := gameExe
		gSelectedGameDir := gGameDir
		if(minimizeOnGameStart == 1) 
		{
			WinMinimizeAll
		}
		Run, %gSelectedGameDir%
		quit()
	}
	else if(gGameName = "paSteam")
	{ ;
		gSelectedGame := gameExe
		gSelectedGameExe := gameExe
		gSelectedGameDir := gGameDir
		if(minimizeOnGameStart == 1) 
		{
			WinMinimizeAll
		}
		Run, %gSelectedGameDir%
		quit()
	}
	
	else if(gGameName = "mapeditor")
	{ ;
		gSelectedGame := gameExe
		gSelectedGameExe := gameExe
		gSelectedGameDir := gGameDir
		checkGameFile(gSelectedGameExe,gSelectedGameDir)
		Run, %gSelectedGameExe%, %gSelectedGameDir%
		if(minimizeOnGameStart == 1) 
		{
			WinMinimize, A
		}
		quit()
	}
	
	else if(gGameName = "taforever")
	{ ;
		gSelectedGame := gameExe
		gSelectedGameExe := gameExe
		gSelectedGameDir := gGameDir
		checkGameFile(gSelectedGameExe,gSelectedGameDir)
		Run, %gSelectedGameExe%, %gSelectedGameDir%
		if(minimizeOnGameStart == 1) 
		{
			WinMinimize, A
		}
		quit()
	}
	
	else
	{ ;
		gSelectedGame := gameExe
		gSelectedGameExe := gameExe
		gSelectedGameDir := gGameDir
		checkGameFile(gSelectedGameExe,gSelectedGameDir)
		if(minimizeOnGameStart == 1) 
		{
			WinMinimizeAll
		}
		Run, %gSelectedGameExe%, %gSelectedGameDir% 
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

Process, Wait, %gSelectedGameExe%, 120 ;//Wait upto 120 seconds for the exe to start
gProcPID := ErrorLevel ;//set the error level

;//if the exe does not start show an error message and exit the script
if not gProcPID
{ 
	MsgBox The specified process did not appear.
    ExitApp ; Stop this script
}

;//Call the exitProc function after the set time
SetTimer, exitProc, 1000 
;//Call the CheckProc function after the set time
SetTimer, CheckProc, 1000
if(gLockCursorArg == 1)
{
	SetTimer, clipProc, 1000
}

;// Try and auto detect if the game is loading or has finished
if(gEnableAutoDualScreen = true)
{
	SetTimer, loadingSearch, 10
	if (gGameName != "client") SetTimer, endGameSearch, 1000 
	SetTimer, endGameSearch, OFF
}
;//Function that will Manually switch from dual screen to single screen

SetTimer, testTimer, 10
testTimer:
	PixelSearch, FoundX, FoundY, searchX1, searchY1, searchX2, searchY2, targetColor
return

resize(x, y, gametype, active) 
{	
	if (active != gDualScreenActive) 
	{  ; Check for active state change
		gDualScreenActive := active  ; Update dual screen active flag
		WinMove, % "ahk_exe " gametype , , gMoveX, gMoveY, %x%, %y%
		WinMaximize, % "ahk_exe " gametype
		WinRestore, % "ahk_exe " gametype
		if (active) 
		{  ; Only perform taskbar hide on activation
			WinMinimize, % "ahk_exe " gametype
			WinRestore, % "ahk_exe " gametype
		}
	}
}


;//Hot key to switch from dual screen to single screen or to exit the script
^F12::resize(gResolutionWidth*2, gResolutionHeight,gSelectedGame,true) ;//Ctrl F12 to enter dual screen mode
^F11::resize(gResolutionWidth, gResolutionHeight,gSelectedGame,false) ;//Ctrl F11 to enter single screen mode
^F10::quit() ;//Ctrl F10 to stop the script


;//Resize the game on start up,
CheckProc:
	if (!ProcessExist(gSelectedGame)) 
	{
    	return
  	}
	WinGet Style, Style, % "ahk_exe " gSelectedGame
	GetPriority(P:="current") 
	{
		static r32 := "N", r64 := "L", r128 := "H", r256 := "R", r16384 := "B", r32768 := "A"
		Process, Exist, % (P="current") ? "" : (P="") ? 0 : P
		R := DllCall("GetPriorityClass", "UInt", hP := DllCall("OpenProcess", "UInt", 0x400, "Int", 0, "UInt", (P+1) ? P : ErrorLevel))
		DllCall("CloseHandle", "UInt", hP)
		return r%R%
	}
	; Combined priority check and setting (assuming gSelectedGame is always a string)
	procPriority := GetPriority(gSelectedGame)
	if (procPriority != "H") 
	{
		Process, Priority, %gSelectedGame%, H
  	}
	ProcessHandle := DllCall("OpenProcess", "UInt", 0x1F0FFF, "Int", False, "UInt", PID)
	DllCall("SetProcessAffinityMask", "UInt", ProcessHandle, "UInt", numberOfThreads)
	DllCall("CloseHandle", "UInt", ProcessHandle)
	if (Style & 0xC40000) 
	{  ; Check for titlebar and borders
    	WinSet, Style, -0xC40000, % "ahk_exe " gSelectedGame ;removes the titlebar and borders
    	windowWidth := gResolutionWidth * (gStartInDualScreenMode ? 2 : 1)  ; Combined dual screen check
    	; //move the window to 0,0 and resize it to fit across 1 or 2 monitors.
		WinMove, % "ahk_exe " gSelectedGame , , gMoveX, gMoveY, windowWidth, gResolutionHeight
    	WinMaximize, % "ahk_exe " gSelectedGame
    	WinRestore, % "ahk_exe " gSelectedGame
		; //sets the number of processors to use, by default it will use all processor
		Process, Exist, %ProcessEXE%
		gamePID := ErrorLevel
    	ProcessHandle := DllCall("OpenProcess", "UInt", 0x1F0FFF, "Int", false, "UInt", gamePID)
    	DllCall("SetProcessAffinityMask", "UInt", ProcessHandle, "UInt", gProcessorCount)  ; Note: May not work on Windows 11
    	DllCall("CloseHandle", "UInt", ProcessHandle)
    	gGameLoadCheck := true
    	gRestoreWindow := true

    if (minimizeOnGameStart == 1) 
	{
    	WinGet, idList, list, , Program Manager
    	Loop, Parse(idList, "`n") 	
		{ 
   			thisID := A_Index
    		WinGetTitle, activeTitle, A
    		WinGetTitle, title, ahk_id %thisID%
    		if (title = activeTitle) 
			{
        		continue
    		}
       		WinMinimize, %title%
    	}
	}
}
return




clipProc: 
	if (!ProcessExist(gSelectedGame) || !WinActive("ahk_exe " gSelectedGame)) ;//checks if the game window is active
		return
	; Optimize dual screen handling
	setWidth := (gDualScreenActive ? gResolutionWidth * 2 : gResolutionWidth)
	; Clip cursor only if necessary
	if Confine
	{
		ClipCursor(true, 0, 0, setWidth, gResolutionHeight)
	} 
	else 
	{
		ClipCursor(false)  ; Release cursor
	}
	Confine := !Confine  ; Toggle for next iteration
return

; //lock the mouse within the game window
ClipCursor(Confine=True, x1=0, y1=0, x2=1, y2=1) 
{
	static R
	if !R 
	{ 
		VarSetCapacity(R, 16, 0)  ; Allocate memory only once
	}
	NumPut(x1, &R+0), NumPut(y1, &R+4), NumPut(x2, &R+8), NumPut(y2, &R+12)
	return Confine ? DllCall("ClipCursor", UInt, &R) : DllCall("ClipCursor")
  }



  ;image1Data := FileRead("path/to/image1.jpg")
  ;image2Data := FileRead("path/to/image2.jpg")
  ;images := {"image1": image1Data, "image2": image2Data}

loadingSearch:
	if(gLoadingSearchDelayCount < 500)
	{ ;//A 5 second delay 
		gLoadingSearchDelayCount ++
		return
	}
	if (!ProcessExist(gSelectedGame)) 
	{
		settimer, endGameSearch, OFF
		settimer, loadingSearch, ON
		if(gDualScreenActive = true)
		{
			gDualScreenActive := false
		}
		return
	}

	;PixelGetColor, color, 0, 0
	;MsgBox The color at the current cursor position is %color%.

	if(gDualScreenActive = true || !gGameLoadCheck || !WinActive("ahk_exe " gSelectedGame))
		return

	loop, %A_ScriptDir%\pics\loadgame\*.*
	{
		CoordMode Pixel,Relative
		ImageSearch, FoundX, FoundY, gResolutionWidth * 0.45, gResolutionHeight * 0.28, gResolutionWidth, gResolutionHeight, *50, %A_LoopFileFullPath% 
		if (ErrorLevel = 0)
		{
			resize(gResolutionWidth*2, gResolutionHeight,gSelectedGame,true)
			settimer, endGameSearch, ON
			settimer, loadingSearch, OFF
			break
		}
	}
return


MsgBox, hBitmap: %time1% ms`nImageSearch: %time2% ms

if ErrorLevel = 2
    MsgBox Could not conduct the search.
else if ErrorLevel = 1
    MsgBox Icon could not be found on the screen.
else
    MsgBox The icon was found at %FoundX%x%FoundY%.
return


; //Check to see if the game has ended are the users in at the stats menu, working for FAF and LOUD 
endGameSearch:
	if (!ProcessExist(gSelectedGame)) 
	{ ;//Check if the game is running
		settimer, endGameSearch, OFF
		settimer, loadingSearch, ON
		if(gDualScreenActive = true)
		{ ;//disable dual screen
			gDualScreenActive := false
		}
		return
	}
	
	;//return if not in dual screen mode
	if(gDualScreenActive = false || !WinActive("ahk_exe " gSelectedGame) || !gGameLoadCheck)
		return
	
	loop, %A_ScriptDir%\pics\endgame\*.*
	{ ;//Loop through all the images in endgame
	  CoordMode Pixel,Relative
	  ImageSearch, FoundX, FoundY, gResolutionWidth, gResolutionHeight, gResolutionWidth*2, gResolutionHeight, *80, %A_LoopFileFullPath% ;
	  if (ErrorLevel = 0)
	  {
		resize(gResolutionWidth, gResolutionHeight,gSelectedGame,false)
		settimer, endGameSearch, OFF
		settimer, loadingSearch, ON
		break
	  }
	 }
return

;//Check if the process exist
ProcessExist(exeName)
{ 
   Process, Exist, %exeName%
   return !!ERRORLEVEL
}

;//exit script if the gSelectedGameExe is not running
exitProc:
	if (ProcessExist(gSelectedGameExe) = 0)
	{
		;//NOTE due to a bug Restoring the Launcher window after the game exits does not work correctly
		;if (ProcessExist("Definitive Supreme Commander Launcher.exe") != 0)
		;{
			;WinRestore , ahk_exe Definitive Supreme Commander Launcher.exe	
		;}
		quit()
	}
	; //Restore the client once (if used) when game has stopped running
	if (ProcessExist(gSelectedGame) = 0 && gRestoreWindow = true && ProcessExist(gSelectedGameExe) != 0)
	{
		WinRestore , ahk_exe %gSelectedGameExe%
		gRestoreWindow := false
	}	
return	

;//exit the script
quit()
{ 	
	ExitApp
}
return