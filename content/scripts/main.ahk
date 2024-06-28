; Supreme Commander Definitive Windowed Borderless Script
; version 1.14
; ageekhere, tatsu, IO_Nox other sources on the net
; Supports 
; dual Monitors of the same resolution
; mouse cursor traping
; Supreme Commander steam version
; Supreme Commander Forged Alliance steam version
; Forged Alliance Forever 
; FAF Client
; LOUD
; limitations
; Only supports monitors of the same resolution
; ui-party does not support steam Supreme Commander (9350)

#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%
#Persistent

;Values that are passed from python
global gGameName := A_Args[1] ; get shortcut parameters command line first arguments 
global gGameDir:= A_Args[2]
global gLockCursorArg:= A_Args[3]
global gAutoSetMonitorArg:= A_Args[4]
global gAutoSetDualScreenArg:= A_Args[5]
global gameExe:= A_Args[6]
global minimizeOnGameStart:= A_Args[7]
global gStartInDualScreenMode:= A_Args[8] ; Set the default Screen mode on startup, true is start in dual screen mode
global gGameType:= A_Args[9]
global gMoveGameToFarLeft:= A_Args[10]
global gMoveX := 0 ; Sets the main screen x location, 0 being the "main display" X location
global gMoveY := 0 ; Sets the main screen x location, 0 being the "main display" Y location
global gResolutionWidth := 0 ; resolution width (do not change)
global gResolutionHeight := 0 ; resolution height (do not change)
global gRestoreWindow = false
global gLoadingSearchDelayCount = 0
global gGameLoadCheck := false ;  has the game loaded
global gSelectedGame := 0
global gSelectedGameExe := 0
global gSelectedGameDir := 0
global gEnableAutoDualScreen := false ; Auto checks if a game is loading and switches to dual screen mode

quit()
{ ; exit the script 	
	ExitApp
	return
} ; end quit()

if(gStartInDualScreenMode = 1)
{
	gStartInDualScreenMode := true
}
Else
{
	gStartInDualScreenMode := false
}
global gDualScreenActive := gStartInDualScreenMode ; (do not change)
EnvGet, gProcessorCount, NUMBER_OF_PROCESSORS ; Set the number of processor threads to use, by default it will find auto find the max supported processors

if(gAutoSetDualScreenArg = 1)
{ ; Only support FA, FAF, FAF client and loud for auto dual screen 
	if(A_Args[1] == "fa" || A_Args[1] =="faf" || A_Args[1] == "client" ||  A_Args[1] == "loud")
	{
		gEnableAutoDualScreen := true 
	}
}

if(gAutoSetMonitorArg = 1)
{
	gResolutionWidth := A_ScreenWidth
	gResolutionHeight := A_ScreenHeight
}

else
{ ; manually set monitor resolution size
	gResolutionWidth := 1920 ;2560, 3840 ; Sets the width resolution, for 1080p use (1920), for 1440p use (2560), for 4k use (3840) or use a custom value
	gResolutionHeight := 1080  ;1440, 2160 ; Sets the height resolution
}

if(gGameName = "client")
	{ ; Run the FAF Client
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
	else if(gGameName = "faf" or gGameName = "fa")
	{ ; Run Forged Alliance Forever
		
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
	{ ; Run upreme Commander Forged Alliance steam version
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
	{ ; Run LOUD 
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
	{
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
	{
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
	{
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
	{
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
	{
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
	{
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
	{
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
	{
		if (gGameType = "steam")
		{
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
		else 
		{
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

movetofarleft(active_id)
{
	if (gMoveGameToFarLeft = 0)
	{
		return
	}
	; Get the dimensions of all monitors
	SysGet, MonitorCount, MonitorCount
	leftmost := 0

	; Loop through all monitors to find the leftmost one
	Loop, %MonitorCount%
	{
		SysGet, Monitor, MonitorWorkArea, %A_Index%
		if (MonitorLeft < leftmost)
		{
			leftmost := MonitorLeft
		}
	}
	; Move the active window to the far left of the leftmost monitor
	WinGet, active_id, ID, A
	WinMove, ahk_id %active_id%, , %leftmost%, , , 
	WinGetPos, newX, newY, , , ahk_id %active_id%
	gMoveX:= newX
}

Process, Wait, %gSelectedGameExe%, 120 ; Wait upto 120 seconds for the exe to start
gProcPID := ErrorLevel ; set the error level

if not gProcPID
{  ; if the exe does not start show an error message and exit the script
	MsgBox The specified process did not appear.
    ExitApp ; Stop this script
} ; end if

SetTimer, exitProc, 1000 ; Call the exitProc function
SetTimer, CheckGameStart, 1000 ; Call the CheckGameStart function

if(gLockCursorArg == 1)
{ ; check for settings
	SetTimer, clipTimer, 500 ; Call the clipTimer function
} ; end if

if(gEnableAutoDualScreen = true)
{ ;  Try and auto detect if the game is loading or has finished
	SetTimer, loadingSearch, 10
	if (gGameName != "client") SetTimer, endGameSearch, 1000 
	SetTimer, endGameSearch, OFF
} ; end if

resize(x, y, gametype, active) 
{ ; Function that will switch from dual screen to single screen	
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
		} ; end if
		movetofarleft(gSelectedGame)
	} ; end if
} ; end resize

ProcessExist(exeName)
{ ; check if process exist
   Process, Exist, %exeName%
   return !!ERRORLEVEL
} ; end ProcessExist

; Hot key to switch from dual screen to single screen or to exit the script
^F12::resize(gResolutionWidth*2, gResolutionHeight,gSelectedGame,true) ; Ctrl F12 to enter dual screen mode
^F11::resize(gResolutionWidth, gResolutionHeight,gSelectedGame,false) ; Ctrl F11 to enter single screen mode
^F10::quit() ; Ctrl F10 to stop the script

GetPriority(P:="current") 
{ ; get game Priority
	static TimerOne := 0
	static r32 := "N", r64 := "L", r128 := "H", r256 := "R", r16384 := "B", r32768 := "A"
	Process, Exist, % (P="current") ? "" : (P="") ? 0 : P
	R := DllCall("GetPriorityClass", "UInt", hP := DllCall("OpenProcess", "UInt", 0x400, "Int", 0, "UInt", (P+1) ? P : ErrorLevel))
	DllCall("CloseHandle", "UInt", hP)
	return r%R%
} ; end GetPriority

CheckGameStart()
{ ; set game Priority, removes titlebar and borders and set window size and position
	if (!ProcessExist(gSelectedGame)) 
	{ ; wait for process to exist
    	return
  	} ; end if
	WinGet Style, Style, % "ahk_exe " gSelectedGame ; get the window style
	static procPriority := "null"
	if(procPriority = "null")
	{ ; set process to high priority
		procPriority := GetPriority(gSelectedGame) ; get process priority 
		if (procPriority != "H") 
		{ 
			Process, Priority, %gSelectedGame%, H	
		} ;end if
	} ; end if

	if (Style & 0xC40000) 
	{  ; Check for titlebar and borders
    	WinSet, Style, -0xC40000, % "ahk_exe " gSelectedGame ;removes the titlebar and borders
    	windowWidth := gResolutionWidth * (gStartInDualScreenMode ? 2 : 1)  ; Combined dual screen check
    	; move the window to 0,0 and resize it to fit across 1 or 2 monitors.
		WinMove, % "ahk_exe " gSelectedGame , , gMoveX, gMoveY, windowWidth, gResolutionHeight
    	WinMaximize, % "ahk_exe " gSelectedGame
    	WinRestore, % "ahk_exe " gSelectedGame
		movetofarleft(gSelectedGame)
		
		Process, Exist, %ProcessEXE%
		gamePID := ErrorLevel
    	ProcessHandle := DllCall("OpenProcess", "UInt", 0x1F0FFF, "Int", false, "UInt", gamePID) ; open
    	DllCall("SetProcessAffinityMask", "UInt", ProcessHandle, "UInt", gProcessorCount)  ; set processor Count
    	DllCall("CloseHandle", "UInt", ProcessHandle) ; close
    	gGameLoadCheck := true ; game has passed the load check
    	gRestoreWindow := true ; restore window
		if (minimizeOnGameStart == 1) 
		{ ; check if minimize all windows is enabled
			WinGet, idList, list, , Program Manager
			Loop, Parse(idList, "`n") 	
			{ ; minimize all windows when game starts
				thisID := A_Index
				WinGetTitle, activeTitle, A
				WinGetTitle, title, ahk_id %thisID%
				if (title = activeTitle) 
				{ ; check for active windows
					continue
				} ; end if
				WinMinimize, %title%
			} ;end loop
		} ; end if
		SetTimer, CheckGameStart, OFF ; turn off CheckGameStart timer
	} ; end if
	return
} ; end CheckGameStart

ClipCursor(Confine=True, x1=0, y1=0, x2=1, y2=1) 
{ ; lock the mouse within the game window	
	static setR := False
	if (setR = False) 
	{ ; Allocate memory only once
		setR := True
		VarSetCapacity(R, 16, 0)  
	} ; end if
	NumPut(x1, &R+0), NumPut(y1, &R+4), NumPut(x2, &R+8), NumPut(y2, &R+12) ; set the NumPut
	return Confine ? DllCall("ClipCursor", UInt, &R) : DllCall("ClipCursor") ; confine the mouse cursor
} ; end ClipCursor

clipTimer()
{ ; Timer for locking the mouse within the game window	
	if (!ProcessExist(gSelectedGame) || !WinActive("ahk_exe " gSelectedGame)) 
	{ ; checks if the game window is active
		return
	} ; end if
	
	setWidth := (gDualScreenActive ? gResolutionWidth * 2 : gResolutionWidth) ; set width of screen
	if (Confine := True)
	{ ; Clip cursor only if necessary
		
		ClipCursor(true, gMoveX, 0, setWidth + gMoveX, gResolutionHeight)
	}  ; end if
	else 
	{ 
		ClipCursor(false)  ; Release cursor
	} ; end else
	Confine := !Confine  ; Toggle for next iteration
} ; end clipTimer

loadingSearch()
{ ; Check to see if the game has entered the loading screen, working for FAF and LOUD
	if(gLoadingSearchDelayCount < 500)
	{ ; A 5 second delay 
		gLoadingSearchDelayCount ++
		return
	} ; end if

	if (!ProcessExist(gSelectedGame)) 
	{ ; Check if the game is running
		settimer, endGameSearch, OFF ; turn off endGameSearch timer 
		settimer, loadingSearch, ON ; turn on loadingSearch timer
		if(gDualScreenActive = true)
		{ ; check if dual screen is already active
			gDualScreenActive := false
		} ; end if
		return
	} ; end if

	if(gDualScreenActive = true || !gGameLoadCheck || !WinActive("ahk_exe " gSelectedGame))
	{ ; check if dual screen is active and other conditions
		return	
	} ; end if

	loop, %A_ScriptDir%\pics\loadgame\*.*
	{ ; Loop through all the images in load game
		ImageSearch, FoundX, FoundY, gResolutionWidth * 0.45, gResolutionHeight * 0.28, gResolutionWidth, gResolutionHeight, *50, %A_LoopFileFullPath% ; search for loading screen images to auto switch to dual screen
		if (ErrorLevel = 0)
		{ ; if no error
			resize(gResolutionWidth*2, gResolutionHeight,gSelectedGame,true) ; resize screen
			settimer, endGameSearch, ON ; turn endGameSearch on
			settimer, loadingSearch, OFF ; turn loadingSearch off
			break
		} ; end if
	} ; end loop
} ;return ; loadingSearch

endGameSearch()
{ ; Check to see if the game has ended, is the user in at the stats menu, working for FAF and LOUD
	if (!ProcessExist(gSelectedGame)) 
	{ ; Check if the game is running
		settimer, endGameSearch, OFF ; Turn off the endGameSearch time
		settimer, loadingSearch, ON ; Turn on the loadingSearch timer
		if(gDualScreenActive = true)
		{ ; disable dual screen
			gDualScreenActive := false
		} ; end if
		return
	} ; end if

	if(gDualScreenActive = false || !WinActive("ahk_exe " gSelectedGame) || !gGameLoadCheck)
	{ ; return if not in dual screen mode
		return
	} ; end if

	loop, %A_ScriptDir%\pics\endgame\*.*
	{ ; Loop through all the images in endgame
		ImageSearch, FoundX, FoundY, 0, 0, gResolutionWidth*2, gResolutionHeight, *80, %A_LoopFileFullPath% ; search for end screen images to auto switch to dual screen
		if (ErrorLevel = 0)
		{ ; if no error
			resize(gResolutionWidth, gResolutionHeight,gSelectedGame,false) ; resize screen
			settimer, endGameSearch, OFF ; turn endGameSearch off
			settimer, loadingSearch, ON ; turn loadingSearch on
			break
		} ; end if
	} ; end loop
} ;return ; endGameSearch

exitProc()
{ ; exit script if the gSelectedGameExe is not running
	if (ProcessExist(gSelectedGameExe) = 0)
	{ ; Check if the current game has stoped
		WinMinimizeAllUndo ; Restore all windows
		quit() ; Exit the script
	} ; end if

	if (ProcessExist(gSelectedGame) = 0 && gRestoreWindow = true && ProcessExist(gSelectedGameExe) != 0)
	{ ; Restore the client once (if used) when game has stopped running, do not quit
		WinRestore , ahk_exe %gSelectedGameExe% ; restore the client
		gRestoreWindow := false ; set so the client window has been restored
	} ; end if	
} ; end exitProc

return