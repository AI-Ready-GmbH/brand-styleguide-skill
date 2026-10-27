import Link from 'next/link'
import type {ComponentPropsWithRef, ReactNode} from 'react'

/**
 * Textlink · Guide 8.x (Links)
 *
 * Regel: Links sind unterstrichen, nicht nur farbig erkennbar (WCAG 1.4.1); Linktext sagt, wohin er führt
 * („Preise ansehen“, nicht „hier“).
 * - `art="im-text"`: Link im Fließtext, erbt Schriftstufe und Zeilenhöhe.
 * - `art="eigenstaendig"`: Link für sich (unter Karten, in Listen), Trefferfläche mindestens 44 px.
 * Intern über next/link, sonst <a>. `neuerTab` setzt rel und einen Hinweis für Screenreader.
 * Für Handlungen gibt es den Button, nicht den Textlink.
 */
type TextLinkProps = Omit<ComponentPropsWithRef<'a'>, 'className' | 'children' | 'href' | 'target'> & {
  href: string
  art?: 'im-text' | 'eigenstaendig'
  neuerTab?: boolean
  /** MARKE: Sprache der Marke */
  neuerTabHinweis?: string
  className?: string
  children: ReactNode
}

/* MARKE: Farbe und Hover-Zustand aus Tokens (Guide 8.x). Dicke und Abstand der Unterstreichung in marke.css. */
const OPTIK = 'text-akzent-text hover:text-text'

const BASIS = [
  'underline',
  'transition-colors duration-(--m-dauer-kurz) ease-standard motion-reduce:transition-none',
  'focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-fokus',
].join(' ')

const ART = {
  'im-text': '',
  // Mindeststandard Trefferfläche 44 px, keine Gestaltung
  eigenstaendig: 'inline-flex min-h-[44px] items-center',
} as const

const EXTERN = /^(https?:|mailto:|tel:|#)/

export function TextLink({href, art = 'im-text', neuerTab = false, neuerTabHinweis = '(öffnet in neuem Tab)', className, children, ...rest}: TextLinkProps) {
  const gemeinsam = {
    className: [BASIS, OPTIK, ART[art], className].filter(Boolean).join(' '),
    'data-baustein': 'textlink',
    'data-art': art,
  }
  const inhalt = (
    <>
      {children}
      {neuerTab && <span className="sr-only"> {neuerTabHinweis}</span>}
    </>
  )
  if (neuerTab) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer" {...rest} {...gemeinsam}>
        {inhalt}
      </a>
    )
  }
  if (EXTERN.test(href) || rest.download !== undefined) {
    return (
      <a href={href} {...rest} {...gemeinsam}>
        {inhalt}
      </a>
    )
  }
  return (
    <Link href={href} {...rest} {...gemeinsam}>
      {inhalt}
    </Link>
  )
}
