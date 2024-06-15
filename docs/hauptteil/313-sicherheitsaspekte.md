---
layout: default
title: 3.1.3 Sicherheitsaspekte
parent: 3.1 Backend
grand_parent: 3. Hauptteil
nav_order: 310
---

# 3.1.3 Sicherheitsaspekte

Das Backend beinhaltet viele "geheime" Variablen und Werte.

Da diese Werte nicht via Github geteilt werden sollten, habe ich einen Mechanismus eingerichtet, mit welchem ich diese Werte lokal abrufen kann, und ohne Changes dies auch in der Production Umgebung nutzen kann.

Todo