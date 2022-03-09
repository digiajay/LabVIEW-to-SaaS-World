@echo off

rem This file is UTF-8 encoded, so we need to update the current code page while executing it
for /f "tokens=2 delims=:." %%a in ('"%SystemRoot%\System32\chcp.com"') do (
    set _OLD_CODEPAGE=%%a
)
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" 65001 > nul
)

set VIRTUAL_ENV=C:\Projects\BitBucket\aj_lv_googlesheets_lib\source\DotNET\LV_GSheet_DotNET_Py\soruce\venv
if not defined PROMPT set PROMPT=$P$G

if defined _OLD_VIRTUAL_PROMPT set PROMPT=%_OLD_VIRTUAL_PROMPT%
if defined _OLD_VIRTUAL_PYTHONHOME set PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%

set _OLD_VIRTUAL_PROMPT=%PROMPT%
set PROMPT=(venv) %PROMPT%

if defined PYTHONHOME set _OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%
set PYTHONHOME=

if defined _OLD_VIRTUAL_PATH set PATH=%_OLD_VIRTUAL_PATH%
if not defined _OLD_VIRTUAL_PATH set _OLD_VIRTUAL_PATH=%PATH%

set PATH=%VIRTUAL_ENV%\Scripts;%PATH%

:END
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" %_OLD_CODEPAGE% > nul
    set _OLD_CODEPAGE=
)
set MAILERSEND_API_KEY = eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZDE1MmNiYzkyMjg2MWViYzI0NWZjYjExYTNkMWExYjJmNzQzYjFlZDgyODU5NzZkYTIwZDEzZDMzZjBlYTYyYzFkOGJiM2Q3NDA2ZTVhOWEiLCJpYXQiOjE2MzQ5MjQ0NzcuMDIyMzA0LCJuYmYiOjE2MzQ5MjQ0NzcuMDIyMzExLCJleHAiOjQ3OTA1OTgwNzYuOTcyMTk3LCJzdWIiOiIxNDU3MyIsInNjb3BlcyI6WyJlbWFpbF9mdWxsIiwiZG9tYWluc19mdWxsIiwiYWN0aXZpdHlfZnVsbCIsImFuYWx5dGljc19mdWxsIiwidG9rZW5zX2Z1bGwiLCJ3ZWJob29rc19mdWxsIiwidGVtcGxhdGVzX2Z1bGwiLCJzdXBwcmVzc2lvbnNfZnVsbCJdfQ.fDs4T5TjZ0jY0BJhQZKJXSbei8Y6wxnz0FUU0LXGxDbXRxhvOqZf4dQ7nENR9rMI-r0zcBjql1-_Vv7oUoCIZWIUVsI7A46VadBrHJKNxUYFUFLIRjq8WGZ0nO5Mpyqd8kZw5Hql0pG6hsfqIRBrmiJjNM9suKAWlVb4bltAWcJ7uny90bMDOSs4Rs-JQIP_6un27DyILUoA1LSa1smgy24l3svG071ke2xBMORQ00QjsA09sjT7SU3XbD0qWKSJi_NUoP1yPrV-EifPzj97svQXmJR2ZyLIHtWlqS-KFpBIJXUR_fp_cEoVZKcE7AfG34aSth2KAXS4sXjM1W8J_1lYbxzj1JJPRiGUl3cUxrJ5qbJO6e_pseKbuIlR3Z1dlMqot-hyVry_a1zH_xCXzkf5x1-KYsjeuwOJ72HCCJrkBY3TT1SGvmNqvAS3MCRPGkoIt4ZQmUMHL6irOJqkUzLsfpTXnsLY81OA8dEw0s9a33Cd58XPT0B3jMOVLUOsox1CZ_tGwsBlYXiCCT9t9Spy0GSIs7pZ-vkq5yU0-m16hUkDDFECPVPitTnHY9Y3yD1TaGMJZCySO823yjCsS64xMekMIlVkpvMVqPILVqperJ_xAegpoVGJfAD8dT2X5xbHMZWvtUDmgZ8p84bdT2y8YyiRfwWikqBuM-PqlG0
