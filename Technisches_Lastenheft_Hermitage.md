# Technisches Lastenheft
## Website-Überarbeitung: hermitage-frankfurt.de

**Auftraggeber:** Hermitage Home & Design GmbH & Co KG  
**Standort:** Hanauer Landstraße 421, 60314 Frankfurt am Main  
**Datum:** 16. Dezember 2025  
**Version:** 1.0

---

## 1. Projektübersicht

### 1.1 Ist-Zustand
Die bestehende Website hermitage-frankfurt.de ist eine WordPress-basierte Unternehmenswebsite für einen Fliesen- und Innenausstattungsfachhandel mit Showroom in Frankfurt am Main.

### 1.2 Projektziel
Modernisierung und Optimierung der bestehenden WordPress-Website hinsichtlich Performance, Benutzerfreundlichkeit, SEO und rechtlicher Konformität.

---

## 2. Festgestellte Mängel und Optimierungsbedarf

### 2.1 Allgemeine Probleme

| Nr. | Problem | Priorität |
|-----|---------|-----------|
| 2.1.1 | Veralteter Copyright-Hinweis (2020) | Hoch |
| 2.1.2 | Fehlende SSL-Optimierung prüfen | Hoch |
| 2.1.3 | Cookie-Banner DSGVO-Konformität prüfen | Hoch |
| 2.1.4 | Mobile Responsiveness optimieren | Hoch |
| 2.1.5 | Ladezeit-Optimierung erforderlich | Mittel |

### 2.2 Design & UX

| Nr. | Aufgabe | Beschreibung |
|-----|---------|--------------|
| 2.2.1 | Hero-Bereich | Modernisierung des Startseiten-Sliders |
| 2.2.2 | Navigation | Verbesserung der Menüstruktur und Benutzerführung |
| 2.2.3 | Call-to-Action | Optimierung der CTA-Buttons ("Hier anrufen!") |
| 2.2.4 | Bildergalerien | Hochwertige Produktpräsentation der Fliesen |
| 2.2.5 | FAQ-Bereich | Accordion-Funktionalität für häufig gestellte Fragen |

### 2.3 Technische Optimierung

| Nr. | Aufgabe | Beschreibung |
|-----|---------|--------------|
| 2.3.1 | WordPress-Core | Update auf aktuelle Version |
| 2.3.2 | Theme | Theme-Update oder Wechsel zu modernem Theme |
| 2.3.3 | Plugins | Überprüfung und Aktualisierung aller Plugins |
| 2.3.4 | Datenbank | Optimierung und Bereinigung |
| 2.3.5 | Caching | Implementierung eines Caching-Systems |
| 2.3.6 | Bildoptimierung | Komprimierung und WebP-Format |
| 2.3.7 | Lazy Loading | Implementierung für Bilder und Medien |

### 2.4 SEO-Optimierung

| Nr. | Aufgabe | Beschreibung |
|-----|---------|--------------|
| 2.4.1 | Meta-Tags | Überarbeitung aller Title-Tags und Meta-Descriptions |
| 2.4.2 | Strukturierte Daten | Schema.org Markup für lokales Geschäft |
| 2.4.3 | Alt-Texte | Optimierung aller Bild-Alt-Attribute |
| 2.4.4 | Interne Verlinkung | Verbesserung der Link-Struktur |
| 2.4.5 | XML-Sitemap | Aktualisierung und Einreichung bei Google |
| 2.4.6 | Local SEO | Google My Business Integration |

### 2.5 Rechtliche Anpassungen (DSGVO)

| Nr. | Aufgabe | Beschreibung |
|-----|---------|--------------|
| 2.5.1 | Impressum | Überprüfung auf Vollständigkeit |
| 2.5.2 | Datenschutzerklärung | Aktualisierung gemäß aktueller DSGVO |
| 2.5.3 | Cookie-Consent | Rechtskonformes Cookie-Banner (Opt-In) |
| 2.5.4 | Kontaktformulare | DSGVO-konforme Einwilligungserklärung |
| 2.5.5 | Newsletter | Double-Opt-In Verfahren prüfen |

### 2.6 E-Commerce (falls WooCommerce aktiv)

| Nr. | Aufgabe | Beschreibung |
|-----|---------|--------------|
| 2.6.1 | Warenkorb | Funktionalität prüfen und optimieren |
| 2.6.2 | Produktkatalog | Kategorisierung und Filteroptionen |
| 2.6.3 | Checkout | Benutzerfreundlicher Bestellprozess |
| 2.6.4 | Zahlungsarten | Integration gängiger Zahlungsmethoden |

---

## 3. Seitenstruktur (Bestand)

```
hermitage-frankfurt.de/
├── home/
├── fliesen/
│   ├── fliesen-offenbach/
│   ├── fliesen-hanau/
│   ├── fliesen-maintal/
│   ├── fliesen-darmstadt/
│   └── fliesen-aschaffenburg/
├── innenausstattung/
├── interior-design/
├── about/
├── service-new/
├── trends/
├── magazine/
├── kontakt/
├── newsletter/
├── warenkorb/
├── impressum/
├── datenschutzerklaerung/
├── datenschutzvereinbarungen/
└── cookie-richtlinie-eu/
```

---

## 4. Technische Anforderungen

### 4.1 Hosting & Server
- PHP Version: mindestens 8.1
- MySQL Version: mindestens 5.7 oder MariaDB 10.3
- SSL-Zertifikat: aktiv und korrekt konfiguriert
- Backup-System: tägliche automatische Backups

### 4.2 WordPress-Umgebung
- WordPress Version: aktuellste stabile Version (6.x)
- Theme: GPL-lizenziertes, regelmäßig aktualisiertes Theme
- Child-Theme: für individuelle Anpassungen

### 4.3 Empfohlene Plugins

| Plugin | Zweck |
|--------|-------|
| Yoast SEO / RankMath | SEO-Optimierung |
| WP Rocket / LiteSpeed Cache | Performance & Caching |
| Smush / ShortPixel | Bildoptimierung |
| Complianz / Borlabs Cookie | DSGVO Cookie-Consent |
| UpdraftPlus | Backups |
| Wordfence / Sucuri | Sicherheit |
| Elementor / WPBakery | Page Builder (falls vorhanden) |
| Contact Form 7 / WPForms | Kontaktformulare |

---

## 5. Arbeitsschritte (Projektphasen)

### Phase 1: Analyse & Vorbereitung (1-2 Tage)
- [ ] Vollständiges Backup erstellen
- [ ] Plugin- und Theme-Inventar
- [ ] Sicherheitscheck
- [ ] Performance-Baseline messen (PageSpeed, GTmetrix)

### Phase 2: Technische Updates (2-3 Tage)
- [ ] WordPress-Core aktualisieren
- [ ] Alle Plugins aktualisieren
- [ ] Theme aktualisieren oder ersetzen
- [ ] PHP-Version prüfen/aktualisieren
- [ ] Datenbank optimieren

### Phase 3: Design & UX (3-5 Tage)
- [ ] Homepage-Überarbeitung
- [ ] Navigation optimieren
- [ ] Mobile Ansicht verbessern
- [ ] Bildergalerien neu gestalten
- [ ] Call-to-Action Buttons optimieren

### Phase 4: SEO-Optimierung (2-3 Tage)
- [ ] Meta-Tags überarbeiten
- [ ] Schema.org Markup implementieren
- [ ] Alt-Texte ergänzen
- [ ] Interne Verlinkung verbessern
- [ ] XML-Sitemap aktualisieren

### Phase 5: Rechtliche Anpassungen (1-2 Tage)
- [ ] Cookie-Banner aktualisieren
- [ ] Datenschutzerklärung überarbeiten
- [ ] Impressum prüfen
- [ ] Formulare DSGVO-konform gestalten

### Phase 6: Performance & Testing (1-2 Tage)
- [ ] Caching implementieren
- [ ] Bilder optimieren
- [ ] Cross-Browser-Testing
- [ ] Mobile Testing
- [ ] Finale Performance-Messung

### Phase 7: Abnahme & Dokumentation (1 Tag)
- [ ] Kundenabnahme
- [ ] Dokumentation übergeben
- [ ] Schulung für Content-Pflege

---

## 6. Kostenvoranschlag (Deutschland)

### 6.1 Stundensätze in Deutschland (Marktübersicht 2025)

| Qualifikation | Stundensatz (netto) |
|---------------|---------------------|
| Junior Entwickler | 50–70 €/Std. |
| Mid-Level Entwickler | 70–100 €/Std. |
| Senior Entwickler | 100–150 €/Std. |
| Agentur (Durchschnitt) | 80–120 €/Std. |

### 6.2 Geschätzter Arbeitsaufwand

| Phase | Stunden (geschätzt) | Kosten (bei 85€/Std.) |
|-------|---------------------|----------------------|
| Analyse & Vorbereitung | 4-8 Std. | 340–680 € |
| Technische Updates | 8-12 Std. | 680–1.020 € |
| Design & UX | 16-24 Std. | 1.360–2.040 € |
| SEO-Optimierung | 8-12 Std. | 680–1.020 € |
| Rechtliche Anpassungen | 4-6 Std. | 340–510 € |
| Performance & Testing | 6-8 Std. | 510–680 € |
| Abnahme & Dokumentation | 2-4 Std. | 170–340 € |

### 6.3 Gesamtkostenschätzung

| Variante | Stunden | Gesamtkosten (netto) |
|----------|---------|---------------------|
| **Minimale Überarbeitung** | 30-40 Std. | **2.550–3.400 €** |
| **Standard-Überarbeitung** | 50-70 Std. | **4.250–5.950 €** |
| **Umfassende Modernisierung** | 80-100 Std. | **6.800–8.500 €** |

### 6.4 Zusätzliche Kostenfaktoren

| Posten | Kosten (geschätzt) |
|--------|-------------------|
| Premium Theme (einmalig) | 50–80 € |
| Premium Plugins (jährlich) | 100–300 € |
| SSL-Zertifikat (falls nicht vorhanden) | 0–100 €/Jahr |
| Hosting-Upgrade (falls nötig) | 10–50 €/Monat |

### 6.5 Wartungsvertrag (optional)

| Leistung | Monatliche Kosten |
|----------|-------------------|
| Basis (Updates, Backups, Monitoring) | 50–100 €/Monat |
| Standard (+ kleine Änderungen) | 100–200 €/Monat |
| Premium (+ Support, SEO-Betreuung) | 200–400 €/Monat |

---

## 7. Empfehlung: WordPress vs. Flask

### WordPress beibehalten ✅ (Empfohlen)

**Vorteile:**
- Bestehende Inhalte bleiben erhalten
- Keine Neuentwicklung nötig
- CMS für einfache Content-Pflege durch Mitarbeiter
- WooCommerce für E-Commerce bereits integriert
- Große Plugin-Auswahl
- Geringere Kosten

**Nachteile:**
- Plugin-Abhängigkeit
- Regelmäßige Updates erforderlich

### Neuentwicklung mit Flask ❌ (Nicht empfohlen)

**Vorteile:**
- Volle Kontrolle über Code
- Bessere Performance möglich
- Keine Plugin-Abhängigkeit

**Nachteile:**
- **Kosten: 15.000–30.000 € für komplette Neuentwicklung**
- Längere Entwicklungszeit (2-4 Monate)
- Kein CMS – Entwickler für jede Änderung nötig
- E-Commerce müsste komplett neu programmiert werden
- Nicht wirtschaftlich für diesen Anwendungsfall

### Fazit
Für einen Fliesenfachhandel mit Showroom ist **WordPress die richtige Wahl**. Eine Flask-Entwicklung wäre technisch überdimensioniert und wirtschaftlich nicht sinnvoll.

---

## 8. Nächste Schritte

1. **WordPress-Zugangsdaten erhalten** (Admin-Login)
2. **Backup erstellen** vor jeglichen Änderungen
3. **Plugin- und Theme-Analyse** im Backend
4. **Priorisierung der Aufgaben** mit Auftraggeber
5. **Schrittweise Umsetzung** nach Absprache

---

## 9. Kontakt für Rückfragen

Bei technischen Fragen zur Umsetzung stehe ich zur Verfügung.

---

*Dieses Lastenheft dient als Grundlage für die Projektplanung und kann nach Erhalt der WordPress-Zugangsdaten präzisiert werden.*
