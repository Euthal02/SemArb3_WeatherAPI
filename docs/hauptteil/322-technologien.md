---
layout: default
title: 3.2.2 Technologien
parent: 3.2 Frontend
grand_parent: 3. Hauptteil
nav_order: 322
---

# 3.2.2 Technologien

In diesem Abschnitt werden die im Frontend verwendeten Technologien genauer beschrieben und die Gründe für meine Entscheidungen erläutert.

![Anforderungen](../ressources/icons/technology.png){: width="250px" }

[Quelle Bild - Icons](../anhang/quellen.html#54-icons)

## GUI

### Vue und Vite

Was ist Vue und Vite ?
Vue ist ein JavaScript-Framework, das Entwicklern hilft, interaktive Webseiten zu erstellen. Es ist einfach zu benutzen und macht es leicht, Teile der Webseite
wiederzuverwenden.

Vite ist ein Werkzeug, das den Entwicklungsprozess beschleunigt. Es startet die Entwicklungsumgebung schnell und aktualisiert die Webseite sofort, wenn man Änderungen vornimmt. Ausserdem sorgt es dafür, dass die fertige Webseite schnell geladen wird.

Da wir bei Boris Langer das Modul Microservice with Python behandelt haben und darin ebenfalls ein Frontend mit Vue bearbeiten durften, fiel die Entscheidung für mich relativ schnell und einfach. Obwohl die Frontend-Entwicklung für mich komplettes Neuland ist, war ich überzeugt, dass ich mit Vue etwas hinbekomme. Es gibt einige Tutorials für Vue welche es einem den Einstieg erleichtern. Ich habe so direkt default Template von Vue installiert und dieses dann auf meine/unsere Anforderungen angepasst.

## Standordermittlung

### JavaScript vs IP-Location

Zuerst wollte ich die Standorte der Clientanfragen über einen IP-Location-Finder ermitteln und fand auch schnell eine API, die dies ermöglicht. Nach dem Testen des Tools auf deren Website (https://tools.keycdn.com/geo) stellte ich jedoch schnell fest, dass diese Anfragen nur für IPv6-Adressen genau sind. Bei IPv4-Adressen erhält man den Standort des Providers, was für uns leider nicht wirklich nützlich ist. Ich habe dann weitere Lösungsmöglichkeiten Recherchiert. 

Ich habe dann herausgefunden, wie wir die Geolocation-API in unserem Projekt einsetzen können, um den geografischen Standort der Benutzer zu ermitteln. Diese API ist bereits in modernen Webbrowsern integriert, was bedeutet, dass wir keine zusätzlichen Bibliotheken benötigen. Die Geolocation-API ermöglicht es, den aktuellen Standort des Benutzers durch verschiedene Methoden wie GPS, WLAN und IP-Adressen zu bestimmen. Für die Nutzung der API ist die Zustimmung des Benutzers erforderlich, was eine kleine Herausforderung darstellte. Lokal funktionierte das Testing problemlos, jedoch wurde das erforderliche Pop-Up für die Standortfreigabe nicht angezeigt, als wir es online testen wollten. Wir haben herausgefunden, dass ein SSL-Zertifikat benötigt wird. Daher haben wir über AWS einen Load Balancer eingerichtet und das dort gelöste SSL-Zertifikat angehängt.

## Webserver

### Ngnix

Ich habe mich für Nginx entschieden, weil Nginx ideal für das Bereitstellen statischer Inhalte, das Weiterleiten von Anfragen an Backend-Server und das Verwalten des Datenverkehrs in verteilten Systemen ist. Diese Eigenschaften machen Nginx zu einer ausgezeichneten Wahl für moderne Webanwendungen, wie unsere.
