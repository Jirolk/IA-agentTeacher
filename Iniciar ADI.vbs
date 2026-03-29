Set WshShell = CreateObject("WScript.Shell")
' Ejecuta el archivo run_adi.bat de forma oculta (0)
WshShell.Run chr(34) & "run_adi.bat" & Chr(34), 0
Set WshShell = Nothing
