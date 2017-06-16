set rr="HKCU\Console\%%SystemRoot%%_system32_cmd.exe"
reg add %rr% /v "WindowPosition" /t REG_DWORD /d %1% /f>nul
color 70
mode con cols=30 lines=10
d:
cd d:\Codes\PythonPygithub
echo %2%
echo %3%
echo %4%
python MainFlow-GetOriginalRepoDetailsForkedByTopUsers.py %2 %3 %4


PAUSE