# Licencias

Este repositorio es público por razones técnicas —para que los entornos de
generación puedan leerlo sin credenciales— **no** para liberar la marca.

Tres regímenes distintos conviven acá. No son intercambiables.

---

## 1. Código y hojas de estilo — MIT

`bootstrap.sh`, `scripts/`, `example/`, `brand/eumera-brand.css`

Licencia MIT (ver `LICENSE`). Uso, copia y modificación libres.

---

## 2. Tipografías — SIL Open Font License 1.1

`fonts/otf/` — IBM Plex, © 2017 IBM Corp.

Origen: los releases oficiales de [IBM/plex](https://github.com/IBM/plex/releases)
`@ibm/plex-sans@1.1.0`, `@ibm/plex-serif@1.1.0` y `@ibm/plex-mono@1.1.0`
(`fonts/complete/otf/`), copiados sin modificar. Caras incluidas:

| familia | caras |
| --- | --- |
| Sans | Light, Regular, Italic, Medium, SemiBold, Bold |
| Serif | Regular, Italic, SemiBold, SemiBoldItalic, Bold, BoldItalic |
| Mono | Regular, Medium, SemiBold |

Son las que usa la web (`eumera-sourcing`, `src/lib/fonts.ts`). Si se suma una
cara, que salga del mismo release para no mezclar versiones.

Ver `fonts/OFL-LICENSE.txt`. Redistribuidas acá bajo los términos de la OFL, que
permite uso comercial. **La licencia debe viajar con los archivos**: si copiás las
fuentes a otro lado, copiá también `OFL-LICENSE.txt`. No es una formalidad, es lo
que exige la licencia.

EUMERA no reclama ningún derecho sobre IBM Plex.

---

## 3. Logos y marca — TODOS LOS DERECHOS RESERVADOS

`brand/logos/` — el isotipo, el wordmark y todos los lockups de EUMERA son marca
de **EUMERA GmbH** (Viena, FN 679621 v).

**Que estos archivos sean accesibles públicamente no otorga a nadie licencia,
permiso ni derecho de uso.** Están acá para que los sistemas de EUMERA los
consuman. No están disponibles para reutilización, modificación, redistribución ni
uso en materiales de terceros.

Es la misma situación que un logo publicado en un sitio web: ser visible no es ser
libre. Publicarlos acá no debilita la marca, del mismo modo que publicarlos en
eumera.eu no la debilita.

Consultas sobre uso de marca: office@eumera.eu
