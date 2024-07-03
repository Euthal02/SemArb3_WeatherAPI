---
layout: default
title: 3.1.6 OpenWeatherMap
parent: 3.1 Backend
grand_parent: 3. Hauptteil
nav_order: 316
---

# 3.1.6 OpenWeatherMap

Um die eigentlichen Wetterdaten zu holen, nutzen wir die öffentliche (und auch kostenlose) API von OpenWeatherMap.

Es ist notwendig ein Konto zu erstellen, jedoch muss kein Betrag für dieses Konto 

Von diesem Anbieter nutzen wir zwei Routen:

## 5 Tages Vorhersage in 3 Stunden Blöcken

Diese Route bietet eine Vorhersage für 5 Tage. Sie ist in 3 Stunden Blöcke aufgeteilt.

Man braucht drei notwendige Attribute um diese Route aufzurufen:

* "latitude", der geografische Breitengrad des Ortes für die Vorhersage.
* "longitude", der geografische Längengrad des Ortes für die Vorhersage.
* API Key, welcher man beim erstellen des Kontos erhält.

Den geografischen Standpunkt des Benutzers unserer Applikation wird Dennis ermitteln und dies dem Backend so übermitteln.

Für den API Key habe ich [den Weg über die Environment Variable genommen.](./313-sicherheitsaspekte.md)

<https://openweathermap.org/forecast5>

## Reverse Geocoding

Nebst der eigentlichen Vorhersage möchte ich auch wissen, welche Stadt / Ortschaft dies genau betrifft.

Dazu biete OpenWeatherMap eine API an, welche genau dies erreicht. Ich kann wieder die Breiten- und Längengrade angeben und als Antwort bekomme ich eine Stadt und einen Ländercode.

Ich nutze diese Werte vorallem um besser beschreiben zu können, was meine API genau als Antwort gibt.

In anderen Worten, diese Werte werden 1 zu 1 an das Frontend weitergegeben.

![OpenWeatherMap](../ressources/images/general/openweathermap.png)

[Quelle Bild - OpenWeatherMap](../anhang/600-quellen.html#611-openweathermap)
