AvtaleGiro™
===========

Work in progress ...

- - -

Brukerdokumentasjon:
<http://www.avtalegiro.no/bedrift/Brukerdokumentasjon/Pages/default.aspx>

[System specification (sep. 2015)](http://www.avtalegiro.no/bedrift/Brukerdokumentasjon/Documents/AvtaleGiro%20Systemspesifikasjon(eng)%20v%203.2%20sept%202015.pdf)

- - -

## Notater

Forsendelse. En forsendelse kan bestå av et eller flere oppdrag, som
dekker en eller flere tjenester.

Oppdrag. Et oppdrag kan kun inneholde transaksjoner for én oppdragstype
som gjelder én avtale.

### Start record transmission

DATAAVSENDER / DATA SENDER:
Fylles ut med dataavsenders KUNDEENHET-ID

FORSENDELSESNUMMER / TRANSMISSION NUMBER (len=7):
Dataavsenders unike nummerering av forsendelser. (F.eks. DD MM (dag,
måned) + løpenr. e.l.)).
Forsendelsesnummer bør fremkomme i interne systemer/dokumenter.

### Start record payment claim order & cancelation request order

OPPDRAGSNUMMER / ORDER NUMBER (len=7):
Må være unik nummerering av oppdrag pr. betalingsmottakers mottakeravtale 12
måneder + en dag fram i tid. (f.eks. DD MM (dag, måned) + løpenummer e.l.).

### Amount posting

TRANSAKSJONSNUMMER / TRANSACTION NUMBER (len=7):
Unik nummerering av transaksjonen pr. oppdrag i stigende sekvens.
