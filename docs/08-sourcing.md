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
- **The catalog contains mis-mapped placeholder rows.** Searching `6CJ1NOPR`
  returns a second "APEM" hit (`C22408213`) whose `describe` is just
  `- New Arrivals`. Rows priced at **$0.0398 with `minPurchaseNum` 441** and an
  empty description are that junk signature — ignore them.
- **`stockCount: 0` means it will not be placed.** The quote silently drops the
  position. `canPresaleNumber` is the restock-order figure; `0` means no
  pre-order either, and `-1` appears on some rows with meaning unclear — treat
  it as unknown, not as "unlimited".
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

Every part in [07-bom.md](07-bom.md) that could plausibly come off a JLCPCB
reel, checked **2026-11-17** against the endpoint above. Stock figures move;
re-check before ordering.

> [!NOTE]
> **Most of this table is now historical.** The LED driver, both switch
> families, the toggle, the keycaps and the RGB LED all belonged to PCB 1,
> which is [not built in v1](01-architecture.md#no-controls-in-v1). **Only the
> GCT USB-C receptacle and the two hand-mounted modules are live parts.**
>
> The table is kept because the *method* is the point — and because the
> zero-stock findings are what settled the switch choice, which a v2 front
> panel would otherwise rediscover.

| BOM part | LCSC code | Stock | Presale | Price @1 / @100 | Verdict |
|---|---|---:|---:|---|---|
| TI `TLC59116IPWR` LED driver | `C131194` | 3,611 | 3,463 | $1.79 / $1.11 | ✅ **Available**, TSSOP-28 |
| GCT `USB4120-03-C` USB-C | `C3445864` | 1,253 | 896 | $1.37 / $0.87 | ✅ **Available** |
| C&K `KSC221JLFS` switch **(chosen)** | `C221726` | 16,623 | 15,660 | $0.76 / $0.46 | ✅ **Available**, 6.2 × 6.2 mm J-lead |
| APEM/MEC `6CJ1NOPR` switch | `C5518654` | **0** | −1 (unclear) | $5.66 / $3.94 | ❌ Not placeable |
| NKK `MN12LL4G01` toggle | `C20103999` | **0** | 0 | $15.13 / $15.13 | ❌ Not placeable |
| MEC `10G09` keycap | `C5381950` | **0** | 0 | $1.18 (min 8) | ❌ Not placeable |
| MEC `10G08` keycap | `C6063604` | **0** | 0 | $1.00 (min 10) | ❌ Not placeable |
| Common-anode RGB LED | — | — | — | — | 🔴 No PN chosen yet |
| Pololu `D42V55F5`, CentyLab RotoPD | — | — | — | — | Not catalogued — modules, hand-mounted |

Through-hole switch alternatives, checked the same day, since the plan is to
hand-install them:

| Family | Example | Stock | Note |
|---|---|---:|---|
| MEC Multimec 5G | `5GTH935` (`C6075999`) | **0** | Whole 5G range reads 0. Source from DigiKey. |
| C&K PTS645 | `PTS645TH50` (`C19288452`) | **0** | Entire PTS645 range reads 0. |
| Alps `SKHH` | `SKHHLWA010` (`C125050`) | 12,834 | The *only* through-hole tactiles in stock. 6 × 6 mm, 1–2.6 N, $0.09–0.17. Generic feel, different cap system. |

So there is **no JLC fallback for a premium through-hole switch** — that path is
DigiKey-only, by choice rather than by accident.

Three things this settles:

1. **The electronics are all sourceable; the controls are not.** The driver and
   the USB-C receptacle are in stock. Every tactile/mechanical part specified by
   name — the 6C switch, both keycaps, the NKK toggle — is at zero stock with no
   pre-order. That is the split the build already assumed: JLC assembles the
   electronics, the controls go in by hand.
2. **The C&K part is the only tactile switch actually in stock**, at 16,623
   pieces and $0.46 in hundreds — which is why it was chosen on 2026-11-17.
   Match the code exactly: the bare `KSC221J` listing (`C19458559`) is a
   separate zero-stock row.
3. **Nothing on this list is a `basic` part.** All are `expand`, so any
   assembled board here pays the extended-part feeder fee per distinct part.

Two notes on the 6C row: LCSC gives its actuation force as **3.7 N**, against
the ~3.6 N quoted elsewhere in this repo; and JLC's price in hundreds ($3.94) is
*above* the $3.07 DigiKey figure in the BOM. Even restocked, JLC is not the
cheaper path for this switch.

For the RGB LED, the catalog has a deep in-stock selection of explicitly
common-anode parts — `C404275` (MHT194CRGBCT, 16,563) and `C389528`
(MHS110RGBCT, 7,572) among them. Neither is validated or chosen; the LED still
has to be picked **as a pair with its optic**, which is what sets standoff
height.

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
section of [09-software-and-bringup.md](09-software-and-bringup.md) — the PD profile and the converter
feeding the board are both still unresolved.

This part is not committed to the BOM. It was a lookup, not a selection.
