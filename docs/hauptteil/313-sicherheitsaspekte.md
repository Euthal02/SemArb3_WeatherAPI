---
layout: default
title: 3.1.3 Sicherheitsaspekte
parent: 3.1 Backend
grand_parent: 3. Hauptteil
nav_order: 313
---

# 3.1.3 Sicherheitsaspekte

## Containersicherheit

Wir möchten gerne erwähnen, dass das Thema Containersicherheit nicht gross behandelt wurde.

Dieses Thema haben wir erst kürzlich mit Marcel Bernet angefangen und er hat uns mitgeteilt, dass dies nicht in die Bewertung einfliessen muss.

Folgende Punkte betreffen auch uns, welche wir während dem CSEC Modul angeschaut haben.

* User und Gruppe in Dockerfile setzen
* Ressourcen beschränken (Memory, CPU)
* Schwachstellen Scanner, z.B. trivy
* Bei Verwendung CI/CD: SaST aktivieren
* Netzwerksicherheit, Eigene Netzwerke verwenden
* Container Tags verwenden
* Signalhandling beachten, <https://github.com/Yelp/dumb-init>
* Logfiles weiterleiten <https://github.com/kubernetes/ingress-nginx/blob/main/rootfs/Dockerfile>
* setproctitle - verwenden für korrekten Prozess-Namen in Linux
* Für Monitoring (Prometheus), /metrics implementieren.
* Klein-/Grossschreibung berücksichtigen. Problem Windows/Linux siehe writer
* TCP/IP Port 5000 wird auch von der Docker Registry verwendet, 8080 verwenden
* .dockerignore verwenden
* ADD berücksichtigt auch gepackte Dateien und entpackt diese zuerst. Wo möglich COPY verwenden

All diese Punkte sind an unseren Dockerfiles zu bemängeln. Dies ist uns bewusst, in Anbetracht der 50 Stunden Limitierung haben wir diese Punkte aber nicht miteinbezogen.

## Variablen / Secrets

Das Backend beinhaltet viele "geheime" Variablen und Werte.

Da diese Werte nicht via Github geteilt werden sollten, habe ich einen Mechanismus eingerichtet, mit welchem ich diese Werte lokal abrufen kann, und ohne Changes dies auch in der Production Umgebung nutzen kann.

Über Environment Variablen kann ich diese Werte geheim halten und dies auch lokal nutzen.

Die funktioniert folgendermassen, im Dockerfile spezifiziere ich, dass der Container ein .env File nutzen soll.

``` yaml
version: '3.9'
services:
  semarb3_flask_prod:
    image: ghcr.io/euthal02/semarb3_weatherapi:latest
    restart: always
    container_name: semarb3_flask_prod
    env_file:
      - path: .env
    ...
```

Dies nutze ich auch in der Entwicklungsumgebung.

Lokal habe ich dieses .env File, welches direkt eingebunden wird. Dieses File wird nicht über GIT geteilt:

``` yaml
version: '3.9'
services:
  semarb3_flask_dev:
    container_name: semarb3_flask_dev
    restart: no
    build:
      context: .
    ...
    env_file:
      - path: .env
    ...
```

``` bash
MYSQL_ROOT_PASSWORD='xxx'
MYSQL_DATABASE='xxx'
DATABASE_URI='xxx'
SECRET_KEY='xxx'
```

In der Github-Pipeline habe ich das ganze mit einem Zwischenschritt gelöst.

Ich erstelle ein .env File und kopiere dieses anschliessend auf den Server:

``` yaml
jobs:
  deploy-job:
    runs-on: ubuntu-latest
    environment: backend_env_vars
    needs: build-job
    steps:

      - name: Create .env file
        run: |
          touch .env
          echo API_KEY="${{ secrets.API_KEY }}" >> .env
          echo ASSISTANT_ID="${{ secrets.ASSISTANT_ID }}" >> .env
          echo ORGANIZATION="${{ secrets.ORGANIZATION }}" >> .env
          echo PROJECT="${{ secrets.PROJECT }}" >> .env
          echo SECRET_KEY="${{ secrets.SECRET_KEY }}" >> .env
          echo MYSQL_ROOT_PASSWORD="${{ secrets.MYSQL_ROOT_PASSWORD }}" >> .env
          echo MYSQL_DATABASE="${{ vars.MYSQL_DATABASE }}" >> .env
          echo DASHBOARD_ENABLED="${{ vars.DASHBOARD_ENABLED }}" >> .env
          echo DATABASE_URI="${{ vars.DATABASE_URI }}" >> .env
          echo WEATHER_API_KEY="${{ secrets.WEATHER_API_KEY }}" >> .env

      - name: Copy files to Server
        run: |
          ...
          scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -q .env ${{ vars.DEPLOY_USER }}@${{ vars.DEPLOY_HOST }}:/home/${{ vars.DEPLOY_USER }}/.env

      ...
```

Mit dieser Variante kann ich API-Keys und andere wichtige Werte verstecken.
