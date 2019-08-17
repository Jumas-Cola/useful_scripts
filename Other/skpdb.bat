:: Get Skype DBs
@ECHO off
SET desk=%userprofile%\desktop
SET defpath=%APPDATA%\Skype
SET file=main.db
FOR /F "tokens=*" %%f IN ('dir /b /s /a-d %defpath%\%file%') DO (
	FOR /F "tokens=7 delims=\" %%a IN ("%%f") DO (
		ECHO %%a
		MD "%desk%\skpbat\%%a"
		COPY "%%f" "%desk%\skpbat\%%a"
	)
)
PAUSE
