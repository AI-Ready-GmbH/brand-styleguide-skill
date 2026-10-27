import type {ReactNode} from 'react'

/**
 * Badge · Guide 8.x (Badges)
 *
 * Regel: kennzeichnet Status oder Art („Neu“, „Ausgebucht“), höchstens ein Badge je Element.
 * Kein Bedienelement: zum Klicken gibt es Button und Textlink. Die Bedeutung steht im Text, nie nur in der Farbe.
 * Schrift in der Stufe `label` (mindestens 12 px laut Prüfskript).
 */

/* MARKE: Töne aus Tokens (Guide 8.x). Schrift auf `akzent` ist nicht kontrastgeprüft, darum `akzent-text`. */
const TON = {
  neutral: 'border border-linie text-text',
  akzent: 'border border-akzent text-akzent-text',
} as const

export type BadgeTon = keyof typeof TON

/* MARKE: Form und Innenabstand in Rasterschritten; Versalien und Laufweite gehören in die Stufe label */
const BASIS = 'inline-flex items-center gap-1 rounded-pille px-2 py-1 font-text text-label'

export function Badge({ton = 'neutral', className, children}: {ton?: BadgeTon; className?: string; children: ReactNode}) {
  return (
    <span data-baustein="badge" data-ton={ton} className={[BASIS, TON[ton], className].filter(Boolean).join(' ')}>
      {children}
    </span>
  )
}
