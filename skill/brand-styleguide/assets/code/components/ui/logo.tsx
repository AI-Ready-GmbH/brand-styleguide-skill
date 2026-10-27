import Image from 'next/image'

/**
 * Logo · Guide 3.x (Logo)
 *
 * Regel: nur die gelieferten Dateien, nie nachgezeichnet, nie per CSS eingefärbt, gedreht, verzerrt oder
 * mit Effekten versehen. Schutzraum und Mindestgröße aus Guide 3.x; die Höhe setzt der Aufrufer über
 * className (Höhen-Klasse), die Breite folgt dem Seitenverhältnis.
 * `alt` ist Pflicht: der Name der Marke, wie er verbindlich geschrieben wird. Im Link zur Startseite reicht
 * das als Linktext.
 * `dateiDunkel`: Datei für den Modus dunkel. Sie erscheint über die Variante `dunkel:` aus globals.css
 * (siehe Einbau); ohne Modus dunkel bleibt sie weg.
 * `breite`/`hoehe`: Maße der Datei in Pixeln, verhindern Layout-Sprünge. SVG liefert next/image unverändert aus.
 */
export function Logo({
  datei,
  dateiDunkel,
  alt,
  breite,
  hoehe,
  vorladen = false,
  className,
}: {
  datei: string
  dateiDunkel?: string
  alt: string
  breite: number
  hoehe: number
  /** im Seitenkopf über dem Falz: true (Next 16: `preload`, ältere Versionen: `priority`) */
  vorladen?: boolean
  className?: string
}) {
  const gemeinsam = {alt, width: breite, height: hoehe, preload: vorladen, 'data-baustein': 'logo'}
  const klassen = (modus: string) => ['w-auto', modus, className].filter(Boolean).join(' ')
  if (!dateiDunkel) return <Image src={datei} {...gemeinsam} className={klassen('')} />
  return (
    <>
      <Image src={datei} {...gemeinsam} className={klassen('dunkel:hidden')} />
      <Image src={dateiDunkel} {...gemeinsam} className={klassen('hidden dunkel:block')} />
    </>
  )
}
