/**
 * Leitplanken für Inhalte im Sanity Studio · Guide 8.x (Komponenten), 10.x (Bildwelt), 11.x (Bewegung), 12.x (Text)
 *
 * Wiederverwendbare Prüfungen für Schemas. Fehler (.error()) blockieren das Veröffentlichen, Warnungen
 * (.warning()) zeigen nur an. Einbinden, Beispiele:
 *
 *   import {altTextFeld, autoplayFeld, hoechstensEinePrimaereHandlung, hervorhebungPruefen, laengeHoechstens} from './leitplanken'
 *
 *   // jeder Block (Sektion) einer Seite
 *   defineType({name: 'heroBlock', type: 'object', fields: [...],
 *     validation: (r) => [r.custom(hoechstensEinePrimaereHandlung).error(), r.custom(hervorhebungPruefen).warning()]})
 *
 *   // Titel und Button-Beschriftung
 *   defineField({name: 'titel', type: 'string', validation: (r) => [r.required(), r.custom(laengeHoechstens('titel')).warning()]})
 *
 *   // Bild oder Logo als Sanity-Bild: Alt-Text als Unterfeld
 *   defineField({name: 'bild', type: 'image', fields: [altTextFeld()]})
 *
 *   // Video
 *   defineField({name: 'video', type: 'object', fields: [defineField({name: 'datei', type: 'file'}), autoplayFeld()]})
 *
 * Die Prüfungen kennen keine Inhalte der Marke. Was die Marke festlegt, steht in den MARKE-Blöcken.
 */
import {defineField, type CustomValidator} from 'sanity'

/* MARKE: Wie eine Handlung (CTA) im Schema aussieht. Standard: Objekt mit `label` und `ziel`, Variante in
   `variante`; primär ist alles, was nicht ausdrücklich sekundär ist. An die Feldnamen des Projekts anpassen. */
const HANDLUNG = {
  istHandlung: (v: Record<string, unknown>) => typeof v.label === 'string' && typeof v.ziel === 'string',
  istPrimaer: (v: Record<string, unknown>) => v.variante !== 'sekundaer',
  hoechstens: 1,
}

/* MARKE: Längengrenzen in Zeichen aus Guide 12.x. null heißt: keine Grenze gesetzt, die Prüfung schweigt.
   Der Lauf trägt die Werte aus dem Guide ein; offene null-Werte meldet die Prüfung in P7. */
export const GRENZEN: Record<'titel' | 'lead' | 'label' | 'altText', number | null> = {
  titel: null,
  lead: null,
  label: null,
  altText: null,
}

/* MARKE: Hervorhebungs-Syntax, falls die Marke eine nutzt (z. B. ein Wort in {Klammern} im Titel wird betont).
   null heißt: keine Syntax, die Regel ist aus. Sonst: Muster (mit Gruppe 1 = hervorgehobener Text), erlaubte Felder,
   höchstens wie viele je Feld und höchstens wie viele Wörter je Hervorhebung. */
export type Hervorhebung = {muster: RegExp; felder: string[]; hoechstens: number; woerter: number}
export const HERVORHEBUNG = null as Hervorhebung | null
// Beispiel: {muster: /\{([^}]*)\}/g, felder: ['titel'], hoechstens: <n>, woerter: <m>} aus Guide 5.x

// · Hilfen

type Wert = unknown
const istObjekt = (v: Wert): v is Record<string, Wert> => !!v && typeof v === 'object' && !Array.isArray(v)

/** geht alle Werte eines Blocks durch, ohne Sanity-Systemfelder (_key, _type, _ref …) */
function durchlaufe(v: Wert, pfad: string[], besuche: (wert: Wert, pfad: string[]) => void) {
  besuche(v, pfad)
  if (Array.isArray(v)) v.forEach((x, i) => durchlaufe(x, [...pfad, String((istObjekt(x) && x._key) || i)], besuche))
  else if (istObjekt(v)) for (const [k, x] of Object.entries(v)) if (!k.startsWith('_')) durchlaufe(x, [...pfad, k], besuche)
}

// · Prüfungen

/** Guide 8.x: höchstens eine primäre Handlung je Block, weitere als sekundär. Als .error() einbinden. */
export const hoechstensEinePrimaereHandlung: CustomValidator<Wert> = (block) => {
  let n = 0
  durchlaufe(block, [], (v) => {
    if (istObjekt(v) && HANDLUNG.istHandlung(v) && HANDLUNG.istPrimaer(v)) n++
  })
  return n > HANDLUNG.hoechstens
    ? `${n} primäre Handlungen in diesem Block, erlaubt ist ${HANDLUNG.hoechstens} (Guide 8.x). Die weiteren auf „sekundär“ stellen.`
    : true
}

/** Guide 12.x: Längengrenze für Titel, Lead, Labels, Alt-Texte. Als .warning() einbinden, bei harten Grenzen .error(). */
export function laengeHoechstens(art: keyof typeof GRENZEN): CustomValidator<string | undefined> {
  return (wert) => {
    const max = GRENZEN[art]
    if (max == null || !wert) return true
    return wert.length > max ? `${wert.length} Zeichen, erlaubt sind ${max} (Guide 12.x). Kürzer fassen, nicht abkürzen.` : true
  }
}

/** Guide 10.x: Alt-Text ist Pflicht, sobald ein Bild gesetzt ist. Für das Unterfeld `alt` eines image-Felds. */
export const altTextPflicht: CustomValidator<string | undefined> = (wert, kontext) => {
  const bild = kontext.parent as {asset?: unknown} | undefined
  if (!bild?.asset) return true
  if (!wert?.trim()) return 'Alt-Text fehlt: in einem Satz sagen, was das Bild zeigt (bei Logos: der Name der Marke). Rein schmückende Bilder gehören nicht in Inhalte.'
  return laengeHoechstens('altText')(wert, kontext)
}

/** Unterfeld `alt` für image-Felder (Bilder und Logos), mit altTextPflicht als Fehler */
export const altTextFeld = () =>
  defineField({
    name: 'alt',
    title: 'Alt-Text',
    type: 'string',
    description: 'Was zeigt das Bild? Ein Satz, ohne „Bild von“. Bei Logos der Name der Marke.',
    validation: (r) => r.custom(altTextPflicht).error(),
  })

/** Guide 11.x: Autoplay ist aus, bis jemand es bewusst einschaltet; dann eine Warnung mit den Bedingungen. */
export const autoplayFeld = () =>
  defineField({
    name: 'autoplay',
    title: 'Automatisch abspielen',
    type: 'boolean',
    initialValue: false,
    description: 'Standard: aus. An nur ohne Ton, mit Pause-Steuerung und still bei reduzierter Bewegung.',
    validation: (r) =>
      r
        .custom((an) =>
          an ? 'Autoplay ist an: nur stumm, mit sichtbarer Pause und mit Standbild bei reduzierter Bewegung (Guide 11.x).' : true,
        )
        .warning(),
  })

/** Guide 5.x: Hervorhebungs-Syntax nur in erlaubten Feldern, je Feld höchstens n, je Hervorhebung höchstens m Wörter. Als .warning(). */
export const hervorhebungPruefen: CustomValidator<Wert> = (block) => {
  if (!HERVORHEBUNG) return true
  const {muster, felder, hoechstens, woerter} = HERVORHEBUNG
  const erlaubt = new Set(felder)
  const hinweise: string[] = []
  durchlaufe(block, [], (v, pfad) => {
    if (typeof v !== 'string') return
    const funde = [...v.matchAll(new RegExp(muster.source, muster.flags.includes('g') ? muster.flags : `${muster.flags}g`))]
    if (!funde.length) return
    const feld = pfad.join(' › ')
    if (!erlaubt.has(pfad[pfad.length - 1] ?? '')) hinweise.push(`${feld}: Hervorhebung wirkt hier nicht`)
    if (funde.length > hoechstens) hinweise.push(`${feld}: ${funde.length} Hervorhebungen, erlaubt ist ${hoechstens}`)
    for (const f of funde) if ((f[1] ?? '').trim().split(/\s+/).length > woerter) hinweise.push(`${feld}: „${f[1]}“ hat mehr als ${woerter} Wörter`)
  })
  return hinweise.length ? `${hinweise.join('; ')} (Guide 5.x)` : true
}
