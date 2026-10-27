import Image from 'next/image'

/**
 * Zitat · Guide 8.x (Zitate)
 *
 * Regel: nur echte Zitate mit Namen und Freigabe der Person, nie erfunden oder umformuliert (Guide 12.x).
 * Aufbau: <figure> mit <blockquote> und <figcaption>. Die Anführungszeichen der Markensprache setzt der
 * Baustein; Zeichen am Anfang und Ende des Texts werden entfernt, damit sie nicht doppelt erscheinen.
 * Foto optional mit alt="", weil der Name direkt daneben steht.
 */

/* MARKE: Anführungszeichen der Markensprache (Guide 5.x, typografische Zeichen) */
const ZEICHEN: readonly [string, string] = ['„', '“']

/* MARKE: Stufe des Zitats, Abstände, Größe und Form des Fotos (z. B. Größe in Rasterschritten, rounded-full) */
const TEXT = 'text-lead text-pretty'
const FOTO = 'shrink-0 object-cover'

const RAND = /^[\s„“”"«»‚‘’']+|[\s„“”"«»‚‘’']+$/g

export function Zitat({
  text,
  person,
  rolle,
  quelle,
  foto,
  className,
}: {
  text: string
  person: string
  rolle?: string
  /** URL der Quelle, landet im cite-Attribut */
  quelle?: string
  /** Bildmaße in Pixeln der Datei (verhindert Layout-Sprünge) */
  foto?: {src: string; breite: number; hoehe: number}
  className?: string
}) {
  return (
    <figure data-baustein="zitat" className={['flex flex-col gap-6', className].filter(Boolean).join(' ')}>
      <blockquote cite={quelle} className={TEXT}>
        <p>
          {ZEICHEN[0]}
          {text.replace(RAND, '')}
          {ZEICHEN[1]}
        </p>
      </blockquote>
      <figcaption className="flex items-center gap-4">
        {foto && <Image src={foto.src} alt="" width={foto.breite} height={foto.hoehe} className={FOTO} />}
        <span className="flex flex-col">
          <span className="font-text text-fliesstext">{person}</span>
          {rolle && <span className="text-klein text-text-leise">{rolle}</span>}
        </span>
      </figcaption>
    </figure>
  )
}
