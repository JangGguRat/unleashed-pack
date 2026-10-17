@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion
cd /d "%~dp0"

rem ============================================================
rem  UNLEASHED 모드팩 업데이트 (더블클릭)
rem   1) tools\mod-projects.txt 에 적힌 모드 프로젝트들을 빌드
rem   2) 빌드된 jar 를 mods\ 폴더에 복사 (+ 서버 mods 폴더에도)
rem   3) git commit + push  →  GitHub 가 자동으로 배포
rem ============================================================

rem 1 이면 gradle 빌드부터, 0 이면 이미 빌드된 jar 만 복사
set "BUILD=1"

rem 테스트 서버 mods 폴더 경로 (비워두면 서버 복사 생략)
rem 예: set "SERVER_MODS=C:\server\unleashed\mods"
set "SERVER_MODS="

set "FAILED="
for /f "usebackq eol=# tokens=1,* delims=|" %%A in ("tools\mod-projects.txt") do (
    call :publish "%%A" "%%B"
)
if defined FAILED goto :fail

echo.
echo [git] 변경사항 업로드 중...
git add -A
git diff --cached --quiet
if not errorlevel 1 (
    echo 바뀐 내용이 없어서 업로드할 게 없습니다.
    goto :end
)
git commit -q -m "modpack update %date% %time%"
if errorlevel 1 goto :fail
git push -q
if errorlevel 1 goto :fail

echo.
echo 완료! 1~2분 뒤 친구들이 게임을 켜면 자동으로 업데이트됩니다.
goto :end

rem ------------------------------------------------------------
:publish
set "NAME=%~1"
set "PROJ=%~2"
echo.
echo [%NAME%] %PROJ%
if not exist "%PROJ%\" (
    echo   폴더가 없습니다: %PROJ%
    set "FAILED=1"
    exit /b 1
)
if "%BUILD%"=="1" (
    echo   빌드 중...
    pushd "%PROJ%"
    call gradlew.bat build -q
    if errorlevel 1 (
        popd
        echo   빌드 실패!
        set "FAILED=1"
        exit /b 1
    )
    popd
)
set "JAR="
for /f "delims=" %%J in ('dir /b /a-d /o-d "%PROJ%\build\libs\*.jar" 2^>nul ^| findstr /v /i /e /c:"-sources.jar" /c:"-dev.jar"') do (
    if not defined JAR set "JAR=%%J"
)
if not defined JAR (
    echo   build\libs 에서 jar 를 찾지 못했습니다.
    set "FAILED=1"
    exit /b 1
)
copy /y "%PROJ%\build\libs\%JAR%" "mods\%NAME%.jar" >nul
echo   %JAR%  →  mods\%NAME%.jar
if defined SERVER_MODS (
    copy /y "%PROJ%\build\libs\%JAR%" "%SERVER_MODS%\%NAME%.jar" >nul
    echo   서버에도 복사: %SERVER_MODS%\%NAME%.jar
)
exit /b 0

rem ------------------------------------------------------------
:fail
echo.
echo 실패했습니다. 위 메시지를 확인하세요.
pause
exit /b 1

:end
pause
exit /b 0
