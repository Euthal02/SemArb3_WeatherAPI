---
layout: default
title: 3.1.1 Funktionsweise
parent: 3.1 Backend
grand_parent: 3. Hauptteil
nav_order: 310
---

# 3.1.1 Funktionsweise

Das ganze Backend basiert auf den Erkenntnissen und Technologien, welche wir im diesjährigen Modul MSVC erarbeitet haben.
Das heisst, dass das ganze Backend mit Python geschrieben ist und die entsprechenden Module mitinstalliert. [Die genauen Module sind hier zu finden.](https://github.com/Euthal02/SemArb3_WeatherAPI/blob/main/backend/requirements.txt)

Die ganze Flask API besteht aus zwei Basisrouten. */user*, welche das ganze Userhandling erledigt, inklusive Login und */weather*, welche den Locationinput annimmt und eine Voraussage zurückgibt. Wir benötigen ein Login, um eine unerwünschte Ausnutzung unserer API zu verhindern, da Anbindung an ChatGPT und etwas Geld kostet.

Die ganze API basiert auf dem REST Prinzip und ist mit Python umgesetzt. Genauere Infos zu den Systemabhängigkeiten findet man im [SEUSAG] 
