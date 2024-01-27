' This example shows how to call vSignalyzer from within CANoe. 
' 
' Usage: Add the following command in Global Option Dialog in CANoe
'        <Options><External Programs><Tools><MDF logging file viewer>
'
'        WScript.exe vSignalyzer.vbs [path to vSignalyzer configuration]
'
'-------------------------------------------------------------------------------
' Copyright (c) 2015 by Vector Informatik GmbH. All rights reserved.
Option Explicit

Const Title          = "Running vSignalyzer from vbScript"
const Regkey         = "HKEY_LOCAL_MACHINE\SOFTWARE\VECTOR\vSignalyzer"


Dim ws, fso
Dim objArgs, strArg
Dim file, logfiles 
Dim vSigExe, vSigCfg, vSigCfgPath

   
  Set ws = CreateObject("WScript.Shell")
  Set fso = CreateObject("Scripting.FileSystemObject" )             
  Set objArgs = Wscript.Arguments
  

  
  ' check vSignalyzer installed 
  On Error Resume Next
  vSigExe = ws.RegRead(RegKey & "\Path")
  If (Err.Number <> 0) Then 
     Msgbox "vSignalyzer is not installed!", 48, Title
     Wscript.Quit 
  Else
     If (Right(1, vSigExe) = "\") Then
        vSigExe = vSigExe & "Exec\vSignalyzer32.exe"
     Else
        vSigExe = vSigExe & "\Exec\vSignalyzer32.exe"       
     End If   
  End If    
  On Error Goto 0
  
    
  ' check arguments, no arguments found -> cannot start 
  If (objArgs.Count = 0) Then     
     Msgbox "No arguments found, cannot start vSignalyzer!", 48, Title
     Wscript.Quit 
  End If    
  

  ' one argument, assume config and loggingfiles in same path  
  If (objArgs.Count = 1) Then  
     strArg = Wscript.Arguments.Item(0)  ' mdf file
     logfiles = fso.GetParentFolderName(strArg) & "\"
     vSigCfgPath = fso.GetParentFolderName(logfiles) & "\vSignalyzer\"
  
     if (fso.FolderExists(vSigCfgPath)) then 
        Set file = fso.OpenTextFile(vSigCfgPath & "LoggingFolder.txt", 2, True, 0) 
        file.WriteLine(logfiles)
        file.close     

        RunMe vSigExe, vSigCfgPath & "vSignalyzer.ini", ""
     Else 
        Msgbox "vSignalyzer configuration not found, cannot start vSignalyzer!", 48, Title
     End If    
  End If
 

  ' two arguments, first has to be the vSignalyzer Configuration 
  If (objArgs.Count = 2) Then  
     strArg = Wscript.Arguments.Item(1)  ' mdf file
     logfiles = fso.GetParentFolderName(strArg) & "\"
     vSigCfg = Wscript.Arguments.Item(0) 

     vSigCfgPath = fso.GetParentFolderName(vSigCfg) & "\"

     Set file = fso.OpenTextFile(vSigCfgPath & "LoggingFolder.txt", 2, True, 0) 
     file.WriteLine(logfiles)
     file.close     
     
     RunMe vSigExe, vSigCfg, ""
  End If
  
  WScript.Quit
  
  
  
'-------------------------------------------------------------------------------
Function Quotes(ByVal strValue)
    Quotes = Chr(34) & strValue & Chr(34)
End Function    

'-------------------------------------------------------------------------------
Function RunMe(FileExe,param1,param2)
Dim command, Exec

    command = Quotes(FileExe) & " " & Quotes(param1) & " " & Quotes(param2) & " "
    ' Msgbox command,64,Title
    Exec = ws.run(command, 0, True)
End Function  
