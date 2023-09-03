# NerDate
Nörteille suunnattu deittisovellus, jossa painotus on tilastoitavasa datassa profiilikuvan ja bion sijaan.
* Käyttäjä voi luoda tunnuksen ja kirjautua sisään ja ulos
* Käyttäjä voi lisätä profiiliinsa asioita, joista hän tykkää tai ei tykkää
* Profiiliin voi lisätä tietoja itsestää, kuten sukupuoli, suuntautuminen, ikä, harrastukset jne.
* Käyttäjä voi selata muita käyttäjiä, ja joko ohittaa käyttäjän tai lähettää hänelle chat pyynnön.
* Muiden käyttäjien kanssa voi viestitellä ja itselle saapuneita pyyntöjä voi hyväksyä tai hylätä
* Sovellus tarjoaa tilastoja esimerkiksi eniten käyttäjän valintoihin vaikuttavista tekijöistä, sekä yhteensopivuus prosentin käyttäjiä selatessa.
* Mahdollisia lisäominaisuuksiä riippuen laajuuden riittävyydestä:
  * Ryhmäkeskustelut
  * Profiilikuvat
## Loppupalautus
* Sovellus on yhä melko keskeneräinen pitkälti kesätöiden takia
* Sovellusta voi testata paikallisesti alempaa löytyvän ohjeen avulla
* Käyttäjän luonti ja kirjautuminen toimii
* Profiilin perustiedot voi lisätä, ja niitä voi muokata
* Tykkäyksiä/ei tykkäyksiä voi lisätä ja muokata
* Muiden tilien selausnäkymässä näkee vain yhden tietoja raa'assa muodossa, mikäli on olemassa käyttäjä, jonka suuntautuminen ja sukupuoli sopivat.
  * En saanut pyyntöjä ja estoja huomioivaa sql queryä toimimaan.
* Viestiominaisuus puuttuu
* Pyyntöjä ei voi katsella
* Kloonaa repositorio koneellesi, ja luo sen juurikansioon .env tiedosto.
* Lisää .env tiedostoon rivit:
  * DATABASE_URL=tietokannan-paikallinen-osoite
  * SECRET_KEY=salainen-avain
* Aktivoi virtuaaliympäristö ja asenna riippuvuudet seuraavilla komennoilla:
  * $ python3 -m venv venv
  * $ source venv/bin/activate
  * $ pip install -r ./requirements.txt

* Määritä tietokanta komennolla:
  * $ psql < schemas/schema.sql
* Käynnistä sovellus komennolla:
  * $ flask run
