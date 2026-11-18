# 08 · Parts Sourcing — JLCPCB / LCSC Lookup

How to check availability and price. Parts themselves are listed in
[07-bom.md](07-bom.md).


Notes on looking up component availability and price while building the BOM.

## JLCPCB component search endpoint

JLCPCB's assembly parts catalog can be queried directly. No authentication,
no API key.

```sh
curl -fsS 'https://jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList/v2' \
  -H 'Content-Type: application/json' \
  --data '{"currentPage":1,"pageSize":10,"keyword":"C3445864"}' \
  | jq -e 'if .code == 200 then .data.componentPageInfo.list else error(tostring) end'
```

`keyword` accepts an LCSC part code (`C3445864`), a manufacturer part number,
or free text.

### Caveats

- **Undocumented internal endpoint.** It backs the JLCPCB web UI and can change
  shape or disappear without notice. Do not build anything load-bearing on it.
- **`keyword` is a general search.** A model number or description returns
  multiple hits. Match on the `componentCode` field rather than taking
  `list[0]`.
- **Image and datasheet URLs are pre-signed and expire in ~30 minutes.** The
  `*AccessIdUrl` fields carry OSS STS tokens. Don't cache them; re-query, or
  keep the stable `lcscGoodsUrl` / `dataManualUrl` links instead.
- Be polite about request rate.

### Fields worth keeping

| Field | Use |
|---|---|
| `componentCode` | LCSC part code — the stable identifier to match on |
| `componentModelEn`, `componentBrandEn` | Manufacturer part number and brand |
| `stockCount`, `canPresaleNumber` | Availability |
| `componentPrices[]` | Price ladder: `startNumber` / `endNumber` / `productPrice` |
| `componentLibraryType` | `basic` vs `expand` — drives JLCPCB assembly cost |
| `isBuyComponent`, `allowPostFlag` | Whether it can be ordered / assembled |
| `describe`, `attributes[]` | Specs, as name/value pairs |
| `lcscGoodsUrl`, `dataManualUrl` | Stable product page and datasheet links |

## Looked up so far

### C3445864 — USB-C receptacle

Checked 2026-11-17. **Global Connector Technology USB4120-03-C** — 24-pin
Type-C female, SMD, USB 2.0, rated 48 V / 5 A, −25 °C to +85 °C, RoHS.

- Stock 1,253, plus 896 presale. Min order 1.
- `expand` library, so it carries the extra-library fee on an assembly order.
- Price ladder: $1.374 @1–9 · $1.142 @10–29 · $1.014 @30–99 · $0.868 @100–599
  · $0.804 @600–1199 · $0.775 @1200+
- [LCSC page](https://www.lcsc.com/product-detail/usb-connectors_global-connector-technology-usb4120-03-c_C3445864.html)
  · [datasheet](https://www.lcsc.com/datasheet/lcsc_datasheet_2411192337_Global-Connector-Technology-USB4120-03-C_C3445864.pdf)

**Important:** 48 V / 5 A is the *connector's contact rating*, not a USB-PD
capability. Negotiating anything above 5 V / 3 A still requires a PD sink
controller, and 5 A specifically requires an e-marked cable. See the power
section of [09-background.md](09-background.md) — the PD profile and the converter
feeding the board are both still unresolved.

This part is not committed to the BOM. It was a lookup, not a selection.
