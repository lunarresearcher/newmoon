# Regenerates README.md from kit/brokers.json so the site table always matches the app.
# Usage: python3 tools/make_readme.py [https://yourdomain.com]
import json, sys, pathlib, datetime, math
root = pathlib.Path(__file__).resolve().parent.parent
site = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "https://www.newmoon.website"
data = json.loads((root/"kit/brokers.json").read_text())
sites, regs = data["sites"], data["registries"]

def new_moons(start, n):
    # Meeus, Astronomical Algorithms ch. 49 (same formula as the app)
    rad, out = math.pi/180, []
    k = math.floor((start.year + (start.month-1)/12 - 2000) * 12.3685) - 1
    while len(out) < n:
        T = k/1236.85; T2, T3, T4 = T*T, T**3, T**4
        jde = 2451550.09766 + 29.530588861*k + 0.00015437*T2 - 0.00000015*T3 + 0.00000000073*T4
        E = 1 - 0.002516*T - 0.0000074*T2
        M = (2.5534 + 29.1053567*k - 0.0000014*T2 - 0.00000011*T3)*rad
        Mp = (201.5643 + 385.81693528*k + 0.0107582*T2 + 0.00001238*T3 - 0.000000058*T4)*rad
        F = (160.7108 + 390.67050284*k - 0.0016118*T2 - 0.00000227*T3 + 0.000000011*T4)*rad
        O = (124.7746 - 1.56375588*k + 0.0020672*T2 + 0.00000215*T3)*rad
        s = math.sin
        jde += (-0.4072*s(Mp) + 0.17241*E*s(M) + 0.01608*s(2*Mp) + 0.01039*s(2*F) + 0.00739*E*s(Mp-M) - 0.00514*E*s(Mp+M)
                + 0.00208*E*E*s(2*M) - 0.00111*s(Mp-2*F) - 0.00057*s(Mp+2*F) + 0.00056*E*s(2*Mp+M) - 0.00042*s(3*Mp)
                + 0.00042*E*s(M+2*F) + 0.00038*E*s(M-2*F) - 0.00024*E*s(2*Mp-M) - 0.00017*s(O) - 0.00007*s(Mp+2*M)
                + 0.00004*s(2*Mp-2*F) + 0.00004*s(3*M) + 0.00003*s(Mp+M-2*F) + 0.00003*s(2*Mp+2*F) - 0.00003*s(Mp+M+2*F)
                + 0.00003*s(Mp-M+2*F) - 0.00002*s(Mp-M-2*F) - 0.00002*s(3*Mp+M) + 0.00002*s(4*Mp))
        d = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc) + datetime.timedelta(days=jde - 2440587.5, seconds=-69)
        if d > start: out.append(d)
        k += 1
    return out

now = datetime.datetime.now(datetime.timezone.utc)
moons = new_moons(now, 12)
FLAG = {"email":"email link","url":"listing url","phone":"📞 phone call","id":"🪪 photo id","pay":"💳 card","account":"free account","captcha":"captcha","dob":"birthdate"}
TIER = {1:"crucial",2:"high",3:"more",4:"added"}
n_bad = sum(1 for s in sites if s["src"] == "badbool"); n_nm = len(sites) - n_bad
tier_count = {t: sum(1 for s in sites if s["tier"] <= t) for t in (1,2,3,4)}

def row(i, s):
    flags = [FLAG[f] for f in s["flags"]] + (["check link"] if s["src"] == "nm" else [])
    find = f'[find]({s["find"]})' if s["find"] != s["out"] else ""
    name = s["name"] + (f'<br><sub>also {s["covers"]}</sub>' if s["covers"] else "")
    return f'| {i} | {name} | {TIER[s["tier"]] if s["cat"] != "callerid" else "caller id"} | {", ".join(flags) or "—"} | {find} [opt out]({s["out"]}) |'

table = "\n".join(row(i+1, s) for i, s in enumerate(sites))
regs_md = "\n".join(f'| {r["name"]} | {r["note"]} | [open]({r["out"]}) |' for r in regs)
moons_md = " · ".join(d.strftime("%b %-d, %Y") for d in moons)
B = "https://img.shields.io/badge"
badge = lambda l, m, c: f'<img src="{B}/{l}-{m}-{c}?style=for-the-badge&labelColor=0b1018" alt="{l.replace("%20"," ")}: {m.replace("%20"," ").replace("%24","$").replace("--","-")}">'

readme = f'''<p align="center">
  <a href="{site}"><img src="assets/banner.png" alt="newmoon: your number, off the lists. 73 sites, 6 Grok Bots, rechecks every new moon, $0" width="100%"></a>
</p>

<p align="center">
  {badge("sites", str(len(sites)), "efe9dc")}
  {badge("grok%20bots", "6", "a3b6ff")}
  {badge("price", "%240", "62d3a2")}
  {badge("server", "none", "97a1b5")}
  {badge("license", "CC%20BY--NC--SA%204.0", "5d687d")}
</p>

<p align="center">
  <b><a href="{site}">Open Newmoon</a></b> &nbsp;·&nbsp;
  <a href="{site}/docs.html">Docs</a> &nbsp;·&nbsp;
  <a href="kit/00-main-prompt.txt">Main prompt</a> &nbsp;·&nbsp;
  <a href="#-the-sites">All {len(sites)} sites</a> &nbsp;·&nbsp;
  <a href="#-self-hosting">Self-host</a>
</p>

<br>

**Newmoon is a privacy assistant powered by Grok.** Type your name, and it builds a removal plan for your phone number and home address across {len(sites)} people-search and caller-ID sites. Then Grok does the work in your own account: a one-minute scan in Grok, or a crew of six Grok Bots that files every opt-out, clicks the confirmation emails, puts your number on Do Not Call and checks again on every new moon.

Nothing gets sent without your yes. No ID, no card, no server. DeleteMe charges $129 a year for this; Newmoon is free.

<table>
<tr>
<td width="46%" valign="top">
<img src="assets/orbit.gif" alt="The orbit: the moon in the middle, every site as a satellite, Grok's beam sweeping them one by one" width="100%">
</td>
<td valign="top">

### 🌑 Why "new moon"

A new moon is the night you can't see the moon at all. That's the goal for your listings.

On the site, your plan is drawn as an orbit. Every site is a satellite, and Grok's beam sweeps them one by one: <code>grok ❯ 16/21 Whitepages → needs you</code>. As listings come down, satellites go dark and the moon wanes with them. Clear everything and it's a new moon.

The recheck runs on the real lunar cycle, every 29.5 days, so data brokers that buy your record back get caught on the next new moon.

</td>
</tr>
</table>

## 🌒 Quickstart

1. **Scan.** Open [Newmoon]({site}), type your name, city and state, press **find me with Grok**. Grok opens with a search prompt for the 15 biggest people-search sites and tells you where you're listed.
2. **Plan.** In the planner, add the phone number and a spare inbox for opt-outs, and pick a depth: {tier_count[1]}, {tier_count[2]}, {tier_count[3]} or {tier_count[4]} sites.
3. **Run.** Paste the main prompt into a Grok Bot skill called `newmoon`, add [`routines.yml`](kit/routines.yml), say `start`.

> [!TIP]
> No Grok Bot yet? The prompts work as plain files too: [`kit/00-main-prompt.txt`](kit/00-main-prompt.txt) has a fill-in-the-blanks version with every site in priority order.

## 🌓 How it works

```mermaid
flowchart LR
  A["Your browser<br/>newmoon page<br/><i>plan + progress in localStorage</i>"] -- "prompt" --> B["Your Grok account<br/>Grok · Grok Bot"]
  B -- "after your yes" --> C["{len(sites)} opt-out pages<br/>forms · emails · registries"]
  B -. "ledger: one sheet, every line with proof" .-> A
```

Newmoon is one static page. It builds text: a plan and a set of prompts. Grok does the searching, filling and clicking, inside your account. Newmoon has no backend, so it can't see your data, and it can't look anyone up by itself.

<p align="center">
  <img src="assets/run.png" alt="A replay of a Newmoon run: listings found, opt-outs filed, a draft waiting for approval" width="88%">
</p>

## 🌔 The crew

| | Bot | Job | Never |
|---|---|---|---|
| `01` | **Scout** | Searches each plan site by name + city, phone and address. Saves the listing URL and a screenshot. | searches for anyone but you |
| `02` | **Filer** | Fills each site's own opt-out form with only what the listing already shows. Drafts first, number masked. | submits without your yes |
| `03` | **Clerk** | Opens confirmation emails from plan sites and clicks the link after you approve. | opens any other email |
| `04` | **Registry** | Do Not Call, Google "Results about you", OptOutPrescreen, California DROP. | hands over an SSN, ID or card |
| `05` | **Watch** | Searches every cleared site again on each new moon. Reopens anything that came back. | re-files without asking |
| `06` | **Ledger** | One table: site, status, listing URL, dates, proof. Sent after every run. | marks removed without proof |

<details>
<summary><b>Commands you can type to your bot</b></summary>
<br>

| You say | What happens |
|---|---|
| `start` | Registry runs, then Scout searches the first five sites and reports |
| `status` | One line per bot: what it's doing, what's waiting on you |
| `what needs me` | Every NEEDS YOU item, with the exact link and step |
| `yes` / `no` | Approve or reject the draft on screen |
| `yes to all Spokeo` | Approve every draft for one site |
| `skip MyLife` | Mark it skipped and move on |
| `ledger` | Send the table now |
| `watch now` | Recheck today instead of waiting for the new moon |
| `pause` / `resume` | Stop every bot, or carry on |

</details>

## 🌕 The sites

{n_bad} sites come from [BADBOOL](https://github.com/yaelwrites/Big-Ass-Data-Broker-Opt-Out-List), the volunteer opt-out list Yael Grauer has kept up since 2017 (updated Sep 27, 2026). {n_nm} more are Newmoon additions: caller-ID apps like Truecaller and Sync.me, the Dataveria network, ClustrMaps, PeekYou, Pipl, LexisNexis and others.

| Depth | Sites | What's in it |
|---|---:|---|
| Crucial | {tier_count[1]} | what BADBOOL marks crucial |
| Priority | {tier_count[2]} | crucial + high priority |
| Full BADBOOL | {tier_count[3]} | the whole BADBOOL list |
| Max | {tier_count[4]} | plus caller-ID apps and Newmoon additions |

<details>
<summary><b>All {len(sites)} sites with direct opt-out links</b></summary>
<br>

| # | Site | Tier | Needs | Links |
|---:|---|---|---|---|
{table}

**Registries** (every plan)

| Registry | What it does | |
|---|---|---|
{regs_md}

</details>

> [!NOTE]
> Sites marked **check link** are Newmoon additions. Opt-out pages move, so the prompts tell your bot to open each link first and find the site's own opt-out if it changed. Spotted a dead link? [Open an issue](../../issues/new?template=broken-link.yml).

> [!IMPORTANT]
> Some steps need a human: verification calls (Whitepages, MyLife), ID or face uploads (PimEyes, Facecheck) and card-first searches (Archives, Searchbug). Your bot marks them **needs you** and tells you exactly what to do.

## 🌖 Rechecks

Watch runs on each new moon. The next twelve, computed with Jean Meeus' lunar phase formulas:

{moons_md}

The planner's **recheck dates .ics** button puts them in your calendar.

## 🌗 Privacy

- **Only you.** Every prompt limits the bots to the person in ABOUT ME. They ask before touching a relative's listing.
- **Nothing without a yes.** No form, email or confirmation link goes out until you approve it.
- **Nothing new.** A site only gets details its listing already shows. Your number appears masked in chat.
- **Nothing stored by us.** Your plan lives in your browser's `localStorage`. There is no server to send it to.

> [!CAUTION]
> Newmoon is for removing your own data. Don't use it to look up other people. If you're dealing with stalking or domestic violence, look up your state's address confidentiality program.

## 🌘 Self-hosting

```bash
git clone <this repo> && cd newmoon
python3 build.py https://yourdomain.com   # src/ → site/, sets link-preview URLs
npx vercel deploy site --prod             # or drag site/ onto app.netlify.com/drop
```

**GitHub Pages (no extra account):** push the repo, then Settings → Pages → Source: **GitHub Actions**. The workflow in `.github/workflows/pages.yml` publishes `site/` on every push, at `https://<you>.github.io/newmoon/`.

**Vercel / Netlify:** import the repo. `vercel.json` and `netlify.toml` already point them at `site/`.

| Setting | Where | What it does |
|---|---|---|
| `GROK_BOT_SHARE` | `src/page.html` | Your x.ai share link for the Newmoon bot. Shows a one-click "add to my Grok Bot" button. |
| `SITE_URL` | `src/page.html` | Used in prompts and share posts. Picks up your real domain automatically. |

<details>
<summary><b>Project structure</b></summary>
<br>

```
site/        what you deploy: index.html, docs.html, favicon.svg, og.png
src/         page.html (app) and docs.html (docs), the files you edit
kit/         main prompt, six bot prompts, routines.yml, brokers.json, newmoon-kit.md
motion/      launch video (newmoon-launch.mp4) and its frame renderer
assets/      README images, social preview, X header, the NEWMOON mascot
tools/       make_readme.py regenerates this file from kit/brokers.json
build.py     src → site
```

</details>

<p align="center">
  <img src="assets/docs.png" alt="The Newmoon docs: quickstart, how it works, commands, statuses, site flags" width="88%">
</p>

## Meet NEWMOON

<p align="center"><img src="assets/mascot/newmoon-sheet.png" alt="NEWMOON, the mascot, in five moods: idle, scanning, found you, removed, asleep at new moon" width="100%"></p>

The mascot's mood follows your plan: scanning while Scout searches, amber when it finds you, green when a listing comes down, asleep when every site is cleared. SVGs and transparent PNGs are in [`assets/mascot`](assets/mascot).

## Credits

- Site list adapted from **[BADBOOL](https://github.com/yaelwrites/Big-Ass-Data-Broker-Opt-Out-List)** by Yael Grauer, CC BY-NC-SA 4.0. If it helps you, [buy her a coffee](https://ko-fi.com/kofisupporter11745).
- Built on **Grok** and **Grok Bot** by xAI. Newmoon is independent and not affiliated with or endorsed by xAI.
- Made by [@lunarresearcher](https://x.com/lunarresearcher).

## License

[CC BY-NC-SA 4.0](LICENSE). Keep the credit, keep it non-commercial, share changes under the same license.

<p align="center"><sub>🌑 &nbsp;your number, off the lists</sub></p>
'''
(root/"README.md").write_text(readme)
print("README.md", len(readme), "chars,", len(sites), "sites, next new moon", moons[0].date())
