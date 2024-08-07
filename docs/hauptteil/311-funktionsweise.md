---
layout: default
title: 3.1.1 Funktionsweise
parent: 3.1 Backend
grand_parent: 3. Hauptteil
nav_order: 311
---

# 3.1.1 Funktionsweise

Das ganze Backend basiert auf den Erkenntnissen und Technologien, welche wir im diesjährigen Modul MSVC erarbeitet haben.
Das heisst, dass das ganze Backend mit Python geschrieben ist und die entsprechenden Module mitinstalliert. [Die genauen Module sind hier zu finden.](https://github.com/Euthal02/SemArb3_WeatherAPI/blob/main/backend/requirements.txt)

Die Applikation basiert auf dem REST Prinzip und ist mit Python umgesetzt. Genauere Infos zu den Systemabhängigkeiten findet man im [SEUSAG](../einleitung/206-seusag.html). Als Basis für die API wurde Flask genutzt.

Diese Flask API besteht aus zwei Basisrouten. */user*, welche das ganze Userhandling erledigt, inklusive Login und */weather*, welche den Locationinput annimmt und eine Voraussage zurückgibt. Wir benötigen ein Login, um eine unerwünschte Ausnutzung unserer API zu verhindern, da die Anbindung an ChatGPT uns etwas Geld kostet.

Als Webserver für die API nutzen wir Gunicorn, welcher auch ganz einfach mittels PIP im Container Image installiert werden kann.

Flask hat einen integrierten Webserver, dieser ist aber nur für Development Zwecke gedacht, deshalb benötigen wir einen separaten Webserver.

Für das Deployment der Applikation nutzen wir die Github Pipeline, welche einen Container auf einer AWS Instanz startet.

[Mehr zu den Pipelines hier.](330-pipelines.html)

[Mehr zur Infrastruktur hier.](312-infrastruktur.html)
