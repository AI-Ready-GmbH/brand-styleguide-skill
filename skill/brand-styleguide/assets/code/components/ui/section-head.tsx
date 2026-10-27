import type {ReactNode} from 'react'

/**
 * Sektionskopf · Guide 8.x (Sektionen) und 5.x (Typografie)
 *
 * Regel: eine h1 je Seite, jede Sektion beginnt mit einer h2; Überschriften springen keine Ebene.
 * `als` bestimmt die Ebene (Gliederung), `stufe` nur die Optik. Lead ist ein Satz, der den Nutzen sagt.
 * Mit `id` ist die Sektion als Anker erreichbar; den Abstand zum festen Seitenkopf setzt marke.css
 * (scroll-margin-top über `[data-baustein="sektionskopf"] [id]`).
 */
export type TitelStufe = 'display' | 'titel-1' | 'titel-2' | 'titel-3'

const STUFE: Record<TitelStufe, string> = {
  display: 'text-display',
  'titel-1': 'text-titel-1',
  'titel-2': 'text-titel-2',
  'titel-3': 'text-titel-3',
}

/* MARKE: Standardstufe je Ebene (Guide 5.x) */
const STANDARD: Record<'h1' | 'h2', TitelStufe> = {h1: 'titel-1', h2: 'titel-2'}

/* MARKE: Farbe und Stufe des Leads, Abstand zwischen Titel und Lead in Rasterschritten. Zeilenlänge über className. */
const LEAD = 'text-lead text-text-leise text-pretty'

export function SectionHead({
  titel,
  lead,
  als: Tag = 'h2',
  stufe,
  id,
  className,
}: {
  titel: ReactNode
  lead?: ReactNode
  als?: 'h1' | 'h2'
  stufe?: TitelStufe
  id?: string
  className?: string
}) {
  return (
    <div data-baustein="sektionskopf" className={['flex flex-col gap-4', className].filter(Boolean).join(' ')}>
      <Tag id={id} className={['font-titel text-balance break-words', STUFE[stufe ?? STANDARD[Tag]]].join(' ')}>
        {titel}
      </Tag>
      {lead != null && <p className={LEAD}>{lead}</p>}
    </div>
  )
}
