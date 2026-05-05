# SafeStack OSINT

**SafeStack OSINT** – tai modulinis, politikomis valdomas OSINT framework’as,
skirtas **kontroliuojamam**, **paaiškinamam** ir **kriptografiškai patikrinamam**
informacijos rinkimui.

Projektas sąmoningai orientuotas ne į „kiekį“, o į:
- atsakomybę
- audituojamumą
- techninį sąžiningumą

> **Your data. Your rules. Your trust chain.**

---

## ✨ Pagrindinės savybės

- Modulinė OSINT architektūra (DNS, WHOIS/RDAP, TLS)
- Centralizuota **Policy** sistema (kas / kada / kaip leidžiama)
- `run all` vykdymo režimas
- Deterministinis **confidence scoring**
- **Risk flags** ir **human-readable hints**
- JSON ataskaitos
- **Ataskaitų pasirašymas su minisign**
- Offline ataskaitų verifikacija

---

## 📦 Diegimas

### 1. Virtual environment (rekomenduojama)

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -e .
```

> Jei `pip install -e .` nepavyksta dėl trūkstamų priklausomybių, įdiekite jas ranka:
>
> ```bash
> pip install dnspython requests
> ```
>
> Ataskaitų pasirašymui reikalingas `minisign` įrankis (atsisiųskite iš https://jedisct1.github.io/minisign/).

----------

## 🚀 Naudojimas:

### Vienas modulis:

ss-osint run dns.passive example.com

### Visi moduliai:

ss-osint run all example.com

### Su politika:

ss-osint run all example.com --policy policy.json

### Alternatyvus paleidimas per Python:

python -m cli.ss_osint run all example.com

### Windows Shell paleidimas

Jei naudodami Windows shell norite paleisti projektą tiesiogiai, galite naudoti `run_osint.bat`:

```bat
run_osint.bat run all example.com
```

Arba PowerShell:

```powershell
.\run_osint.ps1 run all example.com
```

## 📄 Ataskaitos (Report)

ss-osint run all example.com --policy policy.json --report report.json

## Rezultatas:

* report.json
* report.json.sig (arba .minisig)

#### 🔐 Report Verification (kritiškai svarbu)

--- SafeStack OSINT palaiko kriptografiškai pasirašytas ataskaitas.

Verifikacija (offline):

minisign -V -m report.json -p safestack.pub


Jei viskas teisinga:

Signature and comment signature verified


Tai garantuoja, kad:

*ataskaita nebuvo pakeista

*ataskaita kilusi iš patikimo šaltinio

### 🧠 Risk & Confidence modelis
Confidence

Skaičiuojamas tik iš sėkmingų modulių

*Deterministinis (vidurkis)
*Risk flags (pavyzdžiai)

*no_tls
*multiple_ips
*whois_private

Human-readable hints

Pavyzdžiai:

“TLS is present and active.”

“Multiple IP addresses detected – likely CDN usage.”

“WHOIS registrar information is present and identifiable.”

### 🏗️ Projekto struktūra

.
├── adapters/          # Adapteriai (framework ↔ moduliai)
├── cli/               # CLI
│   ├── __init__.py
│   ├── __main__.py
│   └── ss_osint.py
├── core_control/      # Aktyvus vykdymo branduolys
│   ├── context.py
│   ├── exceptions.py
│   ├── module_contract.py
│   ├── registry.py
│   ├── reporting/
│   ├── risk.py
│   ├── result.py
│   ├── runner.py
│   └── policy.py
├── docs/              # Dokumentacija
├── modules/           # OSINT moduliai
├── tests/             # Smoketestai ir integraciniai testai
├── run_osint.bat      # Windows komandų paleidimo skriptas
├── run_osint.ps1      # PowerShell paleidimo skriptas
├── pyproject.toml
├── README.md
├── LICENSE
├── CHANGELOG.md
├── safestack.key      # Privatus verifikavimo raktas (offline)
└── safestack.pub      # Viešas verifikavimo raktas

## 📚 Dokumentacija

Daugiau informacijos apie projektą rasite `docs/` kataloge:

*   [**Politikos sistema**](docs/POLICY.md) – kaip konfigūruoti `policy.json`.
*   [**Auditas ir atsekamumas**](docs/AUDIT.md) – apie žurnalizavimą, ataskaitų ir konfigūracijų pasirašymą.
*   [**Modulių kūrimas**](docs/MODULES.md) – kaip pridėti naujus OSINT modulius.
*   [**Konfigūravimas**](docs/CONFIGURATION.md) – aplinkos paruošimo gidas.
*   [**Reprodukuojamumas**](docs/REPRODUCIBILITY.md) – apie tyrimų pakartojamumą.

## ⚠️ Versioning Notice

Earlier tags (`v0.2.0`, `v0.3.0`, `v0.4.0`, `v1.0.0`) were created during
rapid and non-linear development and **do not represent stable or coherent releases**.

They are preserved for historical reference only.

Versioning discipline and release guarantees start from **v1.5.0** onward.
