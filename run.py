#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python 3
 
"""
Icone sous Windows: il faut:
=> un xxx.ico pour integration dans le exe, avec "icon=xxx.ico"
=> un xxx.png pour integration avec PyQt4 + demander la recopie avec includefiles.
"""
 
import sys, os
from cx_Freeze import setup, Executable

buildOptions = dict(include_files = ['incl/'])

my_exe = Executable(
	# what to build
	script = "game.py",
	initScript = None,
	base = 'Win32GUI',
	targetName = "game.exe",
	icon = "incl/game-icon.ico")

setup(
     name = "appname",
     version = "1.0",
     description = "description",
     author = "your name",
     options = dict(build_exe = buildOptions),
     executables = [my_exe])