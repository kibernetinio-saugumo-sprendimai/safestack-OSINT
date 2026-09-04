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
- Ataskaitų pasirašymas SafeStack raw Ed25519 v1 formatu
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
> Tinklo moduliai nevykdomi be aiškaus `--policy` failo su leidžiamais moduliais, režimais ir tikslais.

----------

## 🚀 Naudojimas:

### Vienas modulis:

ss-osint run dns.live example.com --policy policy.json

### Visi moduliai:

ss-osint run all example.com --policy policy.json

### Su politika:

ss-osint run all example.com --mode network --policy policy.json

### Alternatyvus paleidimas per Python:

python -m cli.ss_osint run all example.com --policy policy.json

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
* report.json.sig, tik jei pateiktas išorinis `--signing-key`

#### 🔐 Report Verification (kritiškai svarbu)

SafeStack OSINT palaiko aiškiai apibrėžtą raw Ed25519 v1 parašo formatą. Tai nėra Minisign formatas.

Verifikacija (offline):

python verify_raw_ed25519.py --message report.json --signature report.json.sig --public-key safestack.pub


Jei viskas teisinga:

Signature verified: SafeStack raw Ed25519 v1


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
├── verify_raw_ed25519.py
└── safestack.pub      # Viešas raw Ed25519 raktas

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

Versioning discipline starts from **v1.5.0**. Production readiness is not implied by a version number; it requires current tests, dependency review and a signed release decision.
