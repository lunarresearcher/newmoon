# Contributing to Newmoon

The most useful thing you can do is keep the links alive.

## Report a broken link

Open a [broken link issue](../../issues/new?template=broken-link.yml). Never include your own name, address, phone number or profile URLs.

## Fix a link or add a site

1. Edit the site in `src/page.html`: BADBOOL sites live in `SITES`, Newmoon additions in `ADDED`.
2. Only add a site if anyone can check for free whether it lists them, and opt out without an ID, a card or a police report.
3. Rebuild and regenerate:
   ```bash
   python3 build.py
   python3 tools/make_readme.py
   ```
4. Open a pull request with a one-line note on how you checked the new link.

Changes to the 45 BADBOOL sites should also go upstream to [BADBOOL](https://github.com/yaelwrites/Big-Ass-Data-Broker-Opt-Out-List), so everyone gets them.

## Prompts

Prompt changes go in `src/page.html` (`RULES`, `mainPrompt`, `botPrompt`). The rules are safety rules: changes that loosen them (filing without approval, uploading ID, searching for other people) won't be merged.

## License

By contributing you agree that your work is shared under [CC BY-NC-SA 4.0](LICENSE).
