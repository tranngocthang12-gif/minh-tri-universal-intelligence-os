@echo off
setlocal
set "MINHTRI_DEMO_HOME=%TEMP%\minhtri-demo-%RANDOM%-%RANDOM%"
call "%~dp0minhtri.bat" --home "%MINHTRI_DEMO_HOME%" init || exit /b 1
for %%F in (01-domain-youtube 02-goal-youtube 03-domain-finance 04-problem-youtube) do (
  call "%~dp0minhtri.bat" --home "%MINHTRI_DEMO_HOME%" apply "%~dp0examples\%%F.json" || exit /b 1
)
call "%~dp0minhtri.bat" --home "%MINHTRI_DEMO_HOME%" status || exit /b 1
call "%~dp0minhtri.bat" --home "%MINHTRI_DEMO_HOME%" verify || exit /b 1
echo Demo data: %MINHTRI_DEMO_HOME%
