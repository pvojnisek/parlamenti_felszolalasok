# parlamenti_felszolalasok

Parlamenti felszolalasok letolteseval, rendszerezesevel es feldolgozasaval kapcsolatos scriptek.

szukseges: python3
eddig linuxon volt tesztelve

install:

```bash
git clone https://github.com/boapps/parlamenti_felszolalasok
cd parlamenti_felszolalasok
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt # ez sok ido lesz
```

hasznalat:

```bash
python dl.py # ez letolti az aktualis ciklus parlamenti politikusainak aktualis ciklusban tett felszolalasait a raw.csv-be

python pre.py # a raw.csv-bol kiszedi a sallangokat, az eredmenyt beirja a preprocessed.csv-be

python train.py # a preprocessed.csv alapjan betanit egy szovegkategorizalo neuralis halot, a model mappaba menti az eredmenyt

python rsstest.py # a modelt lefutattja nehany hirportal utolso nehany belpolitikaval kapcsolatos cikken
```

A scriptek Orosz György magyar nyelvű spacy modeljét használják:
https://github.com/spacy-hu/spacy-hungarian-models

A kod nagy resze eleg ronda lett, majd javitom ha lesz egy kis szabadidom, illetve jelenleg csak az aktualis ciklusrol gyujt infot, ez terveim szerint valtozni fog.

Mindenfele politikai elfogultsagot visszautasitok, ez a projekt kizarolag kutatasi celbol jott letre es semmikep sem lejartni egyes politikai partokat, kepviseloket lapokat vagy ujsagirokat.

A hirtportalok politikai oldal szerinti osztalyzasa nem celom es a scriptek eredmenyet nem tartom beszamithatonak, mert kepviseloi felszolalasokon tanitottt neuralis halozat (tobb okbol, amire itt nem terek ki) nem kepes hibatlanul kategorizalni cikkeket.

Az adathalmazt tartalmazo csv fajlok github releasebol elerhetok

Lescrapeltem még egy csomó információt a parlament.hu-ról, amit nem használtam fel, de még valakinek jól jöhet, ezért ezt is kitettem releasebe.
