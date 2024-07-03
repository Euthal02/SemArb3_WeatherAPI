---
layout: default
title: 5.2 Gemachte Erfahrungen
parent: 5. Schlussteil
nav_order: 502
---

# 5.2 Gemachte Erfahrungen

In diesem Abschnitt werden wir unsere Semesterarbeit reflektieren. Wir werden dieses mit dem Titel *Backend* und *Frontend* unterteilen, damit man die Reflexion auch voneinander trennen kann.

![Finish](../ressources/icons/exchange.png){: width="250px" }

[Quelle Bild - Icons](../anhang/600-quellen.html#64-icons)

## Backend (Marco)

Während dieser Semesterarbeit hat es mir enorm Spass gemacht, mit KI zu experimentieren und API Anbindungen mit dieser KI zu machen. Ich bin froh, dass ich nun genauer verstehe, was diese KIs können und was sie alles benötigen um zu funktionieren.

Unser Versuch als Gruppe eine Arbeit zu machen kann als Erfolg angesehen werden. Wir hatten ein bischen Mühe immer einen guten Zeitpunkt zu finden um zusammen zu arbeiten, jedoch haben wir alle unsere Ziele erreicht. Da wir oft voneinander abhängig waren, konnten wir nur begrenzt separat arbeiten.

Ich finde auch, dass wir in dieser Arbeit gemerkt haben, wie wichtig die Rollenzuteilung ist. Anfangs haben wir uns beide nicht fest definierte Rollen zugeteilt. Dies führte zu einigen Missverständnissen während der Arbeit. In einer nächsten Gruppenarbeit würde ich dies besser festlegen und kommunizieren.

Während meinen vorherigen Semesterarbeiten hatte ich ja immer viele Probleme mit dem Zeitmanagement. Dies hat sich mit zwei Personen definitiv nicht verbessert. Wir haben beide einen gefüllten Kalender und konnten beide nicht immer einen Termin vereinbaren. Ich würde dies in Zukunft direkt bei Projektbeginn definieren, wann wir uns für jeden Sprintabschluss treffen.

Generell habe ich bemerkt, dass die Vorbereitung auf ein Projekt wichtiger ist, wenn man mehrere Personen ist. Es ist besser alle offenen Fragen zu klären bevor man beginnt, anstatt im Nachhinein die Fehler zu bereinigen.

## Frontend (Dennis)

### Start der Semesterarbeit

Am Meisten mühe hatte ich bei dieser Semestarbeit mit dem Start... ich wusse nicht wirklich wie und wo zu beginnen. Marco konnte mich dann unterstützen und hat mir geholfen die Entwicklungsumgebung aufzubauen. Ich war darüber sehr froh, da ich keinerlei Berührungspunkte während der Arbeit damit habe.

### Geolocation

Wie bereits in der Dokumentation beschrieben, hatte ich Probleme mit dem Auslesen der Geolocation. In der lokalen Entwicklungsumgebung hat das reibungslos funktioniert, aber in der Produktivumgebung (online) nicht. Der Grund dafür war, dass die Geolocation-Funktion verlangt, dass die Webseite mit HTTPS verschlüsselt ist. Das bedeutete, dass ich für die Webseite ein SSL-Zertifikat ausstellen musste. Yves Wetter hat mir dann den Tipp gegeben, dass dies ganz einfach über AWS gemacht werden kann. Da die Produktivumgebung bereits in AWS läuft, erschien mir das sinnvoll. So sieht die Abfrage für die Geolocation aus:

``` javascript
async function getLocation() {
  // Funktion zur Ermittlung der aktuellen Geoposition
  return new Promise((resolve, reject) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          lat.value = position.coords.latitude;
          lng.value = position.coords.longitude;
          resolve([position.coords.latitude, position.coords.longitude]);
        },
        (error) => {
          reject(error);
        }
      );
    } else {
      reject(new Error("Geolocation is not supported by this browser."));
    }
  });
}
```

Um die Zertifizierung zu ermöglichen, musste ich einen Load Balancer einrichten und die EC2-Instanz, auf der die Produktivumgebung läuft, dahinter stellen. Marco hatte glücklicherweise eine Domain, in der wir die CNAME-Einträge vornehmen konnten, sodass die Webseite schließlich erfolgreich verschlüsselt wurde. Jetzt funktioniert die Abfrage einwandfrei.

### GET-Anfrage ins Backend

Nachdem das Problem mit der Geolocation gelöst war und ich die Längen und Breitengrade erhalten habe, tauche bereits das nächste Problem auf. Ich konnte die Anfrage nicht ans Backend senden, obwohl ich ein Authenfizierzungs Token hatte. Nach längerem recherchieren und zusammenarbeiten mit Marco hat sich herausgestellt, dass ich den Header für die GET-Anfrage nicht richtig konfiguriert hatte. Das API Verlangt dass im Header der Authentifizierungstoken als *Bearer* mitgegeben wird. Nach dieser Anpassung konnte ich mich dann Erfolgreich am Backend authentifizieren.

``` javascript
    const apiUrl = `https://backend.meuthak.ch/weather/lookup?lattitude=${latitude}&longitude=${longitude}`;

    const response = await axios.get(apiUrl, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
        'Access-Control-Allow-Origin': '*'
      }
    });
```

### Reflexion der ganzen Semesterarbeit

Ich habe in dieser Semesterarbeit viel gelernt. Da dies meine erste Semsterarbeit in einem Team war, gab eis einige Herauserforderungen welche ich vorhin noch nicht hatte. Jedoch hat das Zusammenspiel zwischen mir und Marco hervorragend funktioniert. Unserer APP Funktioniert wie wir uns es gewünscht haben und ich konnte meine Ziele erreichen. Auch hat das Dokumentieren auf Github Pages sich wieder bewährt.

Was ich jedoch bereits weiss ist, dass das Programmieren und ich nicht so schnell *beste Freunde* werden. Nach wie vor fällt es mir eher Schwer in der Entwicklung Fuss zu fassen. Nichts desto trotz hat mir das Frontend-Entwickeln spass gemacht und ich bin sehr zufrieden mit dem Ergebis.

Meiner Meinung nach war die 3. Semesterarbeit ein Erfolg !
