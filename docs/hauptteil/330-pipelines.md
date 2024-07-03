---
layout: default
title: 3.3 Pipelines
parent: 3. Hauptteil
nav_order: 330
---

# 3.3 Pipelines

Wir arbeiten in dieser Arbeit mit Github Workflows. Diese werden wir in diesem Abschnitt besser beleuchten.
Es gibt 3 Pipelines welche wir nutzen.

1. [Github Pages](https://github.com/Euthal02/SemArb3_WeatherAPI/blob/main/.github/workflows/jekyll-gh-pages.yml)
2. [Frontend](https://github.com/Euthal02/SemArb3_WeatherAPI/blob/main/.github/workflows/frontend-deploy.yml)
3. [Backend](https://github.com/Euthal02/SemArb3_WeatherAPI/blob/main/.github/workflows/backend-deploy.yml)

Der Github Pages Branch unterscheidet sich von den anderen beiden. Dieser dient nur dazu, unsere Dokumentation auf Github Pages zu pushen. Dort benutzen wir grösstenteils Standard Funktionen von Github. Zum Beispiel:

```yaml
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1' # Not needed with a .ruby-version file
          bundler-cache: true # runs 'bundle install' and caches installed gems automatically
          cache-version: 0 # Increment this number if you need to re-download cached gems
          working-directory: '${{ github.workspace }}/docs'
```

Die Pipeline für das Frontend und Backend sind gleich aufgebaut. Darin haben wir mehr selbst gebaute Funktionen. Viele davon haben wir auch bereits im Modul MSVC 

Mittels diesem directive wir gesteuert, dass die Pipelines nur aktiviert werden, wenn es auch Commits gibt, welche den betroffenen Ordner bearbeiten. Ausserdem werden nur Commits beachtet welche auch im Main Branch gepusht werden. Sollte es einen Feature Branch geben, wird nicht auf diesen geachtet.

```yaml
on:
  push:
    # this means that the workflow will only trigger if there are changes in this directory
    paths:
      - 'backend/**'
    branches:
      - main
```
