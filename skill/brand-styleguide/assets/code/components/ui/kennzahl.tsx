import type {ReactNode} from 'react'

/**
 * Kennzahl · Guide 8.x (Kennzahlen) und 12.x (Zahlen und Einheiten)
 *
 * Regel: keine Zahl ohne Bedeutung (`label` ist Pflicht) und ohne Beleg im Inhalt. Zahlen formatiert
 * Intl.NumberFormat in der Sprache der Marke, Ziffern gleich breit, Einheit mit geschütztem Leerzeichen.
 * Höchstens eine betonte Kennzahl je Ansicht (Guide 8.x).
 * `imDl`: als Eintrag einer <dl> (dt = Bedeutung, dd = Zahl); optisch steht die Zahl trotzdem oben.
 */

/* MARKE: Sprache der Marke für Zahlenformate */
const SPRACHE = 'de-DE'

/* MARKE: Stufe und Farbe der Zahl (Guide 8.x); Farbe der Bedeutung */
const ZAHL = {standard: 'font-titel text-titel-1 text-text', betont: 'font-titel text-display text-text'} as const
const BEDEUTUNG = 'text-klein text-text-leise'

export function Kennzahl({
  wert,
  label,
  einheit,
  format,
  betont = false,
  imDl = false,
  className,
}: {
  wert: number | string
  label: ReactNode
  einheit?: string
  format?: Intl.NumberFormatOptions
  betont?: boolean
  imDl?: boolean
  className?: string
}) {
  const zahl = typeof wert === 'number' ? new Intl.NumberFormat(SPRACHE, format).format(wert) : wert
  const text = einheit ? `${zahl} ${einheit}` : zahl
  const zahlKlassen = [ZAHL[betont ? 'betont' : 'standard'], 'tabular-nums'].join(' ')

  if (imDl) {
    return (
      <div data-baustein="kennzahl" className={['flex flex-col-reverse justify-end', className].filter(Boolean).join(' ')}>
        <dt className={BEDEUTUNG}>{label}</dt>
        <dd className={zahlKlassen}>{text}</dd>
      </div>
    )
  }
  return (
    <div data-baustein="kennzahl" className={className}>
      <p className={zahlKlassen}>{text}</p>
      <p className={BEDEUTUNG}>{label}</p>
    </div>
  )
}
