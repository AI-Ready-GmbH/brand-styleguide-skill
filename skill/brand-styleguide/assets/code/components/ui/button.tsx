import Link from 'next/link'
import type {ComponentPropsWithRef, ReactNode} from 'react'

/**
 * Button · Guide 8.x (Buttons)
 *
 * Regel: höchstens eine primäre Handlung je Ansicht, jede weitere Handlung ist sekundär (Guide 8.x).
 * Mit `href` entsteht ein Link (intern über next/link; extern, Anker, mailto und tel als <a>), sonst ein <button>.
 * Trefferfläche mindestens 44 × 44 px, sichtbarer Fokus in der Rolle `fokus`, Ladezustand über `laedt`.
 * Beschriftung: Verb + Objekt („Angebot anfordern“), keine Leerformeln wie „Weiter“ (Guide 12.x).
 *
 * Optik nur aus Tokens. Feinheiten, die kein Token abbildet (Versalien, Pfeil, Lader), setzt die Marke in
 * marke.css über `[data-baustein="button"][data-variante="…"]`, nicht hier.
 */
export type ButtonVariante = 'primaer' | 'sekundaer'

/* MARKE: Optik je Variante, nur Token-Klassen (Guide 8.x). Die Rollen stehen fest, der Hover-Zustand ist Pflicht. */
const VARIANTE: Record<ButtonVariante, string> = {
  primaer: 'bg-handlung text-handlung-text hover:bg-handlung-hover',
  sekundaer: 'border border-linie-stark text-text hover:bg-flaeche',
}

const BASIS = [
  'inline-flex items-center justify-center text-center touch-manipulation',
  // Mindeststandard Trefferfläche 44 px: gilt für jede Marke, keine Gestaltung
  'min-h-[44px] min-w-[44px]',
  /* MARKE: Schriftstufe, Radius und Innenabstand in Rasterschritten (Guide 8.x) */
  'font-text text-fliesstext rounded-steuerung px-4 py-2',
  // Rückmeldung mit Dauer-Token, nur Farben, bei reduzierter Bewegung ohne Übergang
  'transition-colors duration-(--m-dauer-kurz) ease-standard motion-reduce:transition-none',
  'focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-fokus',
  'disabled:cursor-not-allowed aria-busy:cursor-wait',
].join(' ')

type Gemeinsam = {
  variante?: ButtonVariante
  /** volle Breite des Containers */
  breit?: boolean
  className?: string
  children: ReactNode
}

type AlsLink = Gemeinsam & Omit<ComponentPropsWithRef<'a'>, 'className' | 'children' | 'href'> & {href: string}

type AlsButton = Gemeinsam &
  Omit<ComponentPropsWithRef<'button'>, 'className' | 'children'> & {
    href?: never
    /** Anfrage läuft: Button gesperrt, `ladeText` sichtbar, Breite bleibt gleich */
    laedt?: boolean
    /** endet mit „…“ (Guide 12.x) */
    ladeText?: string
  }

export type ButtonProps = AlsLink | AlsButton

/** Klassen eines Buttons, z. B. für ein <label> eines Datei-Felds, das wie ein Button aussehen soll */
export function buttonKlassen({variante = 'primaer', breit = false, className}: Pick<Gemeinsam, 'variante' | 'breit' | 'className'> = {}) {
  return [BASIS, VARIANTE[variante], breit && 'w-full', className].filter(Boolean).join(' ')
}

const EXTERN = /^(https?:|mailto:|tel:|#)/

export function Button(props: ButtonProps) {
  if (typeof props.href === 'string') {
    const {variante = 'primaer', breit, className, children, href, ...a} = props
    const gemeinsam = {
      className: buttonKlassen({variante, breit, className}),
      'data-baustein': 'button',
      'data-variante': variante,
    }
    if (EXTERN.test(href) || a.download !== undefined) {
      const rel = a.rel ?? (a.target === '_blank' ? 'noopener noreferrer' : undefined)
      return (
        <a href={href} {...a} rel={rel} {...gemeinsam}>
          {children}
        </a>
      )
    }
    return (
      <Link href={href} {...a} {...gemeinsam}>
        {children}
      </Link>
    )
  }

  /* MARKE: ladeText in der Sprache der Marke */
  const {variante = 'primaer', breit, className, children, laedt = false, ladeText = 'Bitte warten…', disabled, type = 'button', ...b} = props
  return (
    <button
      type={type}
      {...b}
      disabled={disabled || laedt}
      aria-busy={laedt || undefined}
      data-baustein="button"
      data-variante={variante}
      data-laedt={laedt || undefined}
      className={buttonKlassen({variante, breit, className})}
    >
      {/* beide Texte liegen übereinander: die Breite springt nicht, wenn der Ladetext erscheint */}
      <span className="grid">
        <span className={['col-start-1 row-start-1 inline-flex items-center justify-center gap-2', laedt && 'invisible'].filter(Boolean).join(' ')}>
          {children}
        </span>
        {laedt && <span className="col-start-1 row-start-1">{ladeText}</span>}
      </span>
    </button>
  )
}
