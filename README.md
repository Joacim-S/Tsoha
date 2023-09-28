# NerDate
Nörteille suunnattu deittisovellus, jossa painotus on tilastoitavasa yksinkertaisessa datassa profiilikuvan ja bion sijaan.
* Käyttäjä voi luoda tunnuksen ja kirjautua sisään ja ulos.
* Käyttäjä voi lisätä profiiliin perustietotonsa, eli iän, sukupuolen ja suuntautumisen.
* Käyttäjä voi lisätä profiiliinsa asioita, joista hän tykkää tai ei tykkää.
* Käyttäjä voi selata muita käyttäjiä, ja joko ohittaa käyttäjän tai lähettää hänelle chat pyynnön, tai saman tien estää tämän pysyvästi.
* Ohitukset voi nollata, jos valintojaan haluaa harkita uudelleen.
* Muiden käyttäjien kanssa voi viestitellä ja itselle saapuneita pyyntöjä voi hyväksyä tai hylätä.
* Keskustelukumppanin voi estää ja eston voi poistaa.
* Varsinaisesti mitään tilastoja en palautukseen ehtinyt tehdä.
## Testausohje
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
