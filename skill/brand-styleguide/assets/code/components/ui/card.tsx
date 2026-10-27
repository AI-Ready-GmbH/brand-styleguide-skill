import Link from 'next/link'
import type {ReactNode} from 'react'

/**
 * Karte · Guide 8.x (Karten)
 *
 * Regel: nur die Varianten aus VARIANTEN, keine Karte in einer Karte, jede Karte gleich aufgebaut (Guide 8.x).
 * Mit `href` ist die ganze Karte genau ein Link: Der Titel trägt den Link, eine Fläche darüber macht die
 * ganze Karte klickbar. So heißt der Link wie der Titel und nicht wie der ganze Karteninhalt.
 * Darum in einer verlinkten Karte keine weiteren Links oder Buttons.
 */

/* MARKE: Varianten der Karte, Zahl und Namen aus Guide 8.x, nur Token-Klassen. Mehr als drei sind ein Befund. */
const VARIANTEN = {
  flaeche: 'bg-flaeche',
  linie: 'border border-linie',
} as const

export type KartenVariante = keyof typeof VARIANTEN

/* MARKE: Radius, Innenabstand und Abstand der Teile in Rasterschritten (Guide 6.x, 8.x) */
const BASIS = 'relative flex flex-col gap-3 rounded-karte p-6'

/* MARKE: Hover-Zustand der verlinkten Karte; der Fokus liegt sichtbar um die ganze Karte */
const MIT_LINK = [
  'group hover:border-linie-stark',
  'transition-colors duration-(--m-dauer-kurz) ease-standard motion-reduce:transition-none',
  'has-[a:focus-visible]:outline-2 has-[a:focus-visible]:outline-offset-2 has-[a:focus-visible]:outline-fokus',
].join(' ')

/* MARKE: Schriftstufe des Kartentitels */
const TITEL = 'font-titel text-titel-3 text-balance'

type Basis = {
  variante?: KartenVariante
  als?: 'div' | 'article' | 'li' | 'section'
  titelAls?: 'h2' | 'h3' | 'h4'
  /** steht über dem Titel, z. B. ein Bild (bei verlinkter Karte mit alt="", der Titel benennt den Link) */
  kopf?: ReactNode
  className?: string
  children?: ReactNode
}

export type CardProps = (Basis & {href: string; titel: ReactNode}) | (Basis & {href?: undefined; titel?: ReactNode})

export function cardKlassen(variante: KartenVariante = 'flaeche', mitLink = false, className?: string) {
  return [BASIS, VARIANTEN[variante], mitLink && MIT_LINK, className].filter(Boolean).join(' ')
}

export function Card({variante = 'flaeche', als: Tag = 'div', titelAls: Titel = 'h3', href, titel, kopf, className, children}: CardProps) {
  let titelInhalt: ReactNode = titel
  if (href) {
    // Fläche über der ganzen Karte; der Fokusring sitzt an der Karte (has-[a:focus-visible]), darum hier outline-hidden
    const linkKlassen = 'after:absolute after:inset-0 focus-visible:outline-hidden group-hover:underline'
    titelInhalt = /^(https?:|mailto:|tel:)/.test(href) ? (
      <a href={href} className={linkKlassen}>
        {titel}
      </a>
    ) : (
      <Link href={href} className={linkKlassen}>
        {titel}
      </Link>
    )
  }
  return (
    <Tag data-baustein="karte" data-variante={variante} className={cardKlassen(variante, !!href, className)}>
      {kopf}
      {titel != null && <Titel className={TITEL}>{titelInhalt}</Titel>}
      {children}
    </Tag>
  )
}
