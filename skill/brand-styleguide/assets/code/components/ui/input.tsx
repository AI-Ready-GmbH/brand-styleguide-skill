import {useId, type ComponentPropsWithRef, type ReactNode} from 'react'

/**
 * Eingabefelder · Guide 8.x (Formulare)
 *
 * Regel: jedes Feld hat ein sichtbares Label über dem Feld (kein Platzhalter als Label), Hinweis und Fehler
 * stehen direkt am Feld und sind per aria-describedby verbunden. Schrift in der Stufe `fliesstext`
 * (mindestens 16 px laut Prüfskript, sonst zoomt iOS beim Antippen), Trefferfläche mindestens 44 px.
 * Fehlertexte sagen, was zu tun ist („Bitte eine E-Mail-Adresse mit @ eingeben“), nicht nur, was falsch ist.
 * Platzhalter zeigen ein Beispiel und enden mit „…“. Einfügen wird nie blockiert.
 *
 * Kein 'use client' nötig (useId läuft auch in Server Components). Zustand, Absenden und den Fokus auf das
 * erste fehlerhafte Feld regelt das Formular, das die Felder benutzt.
 */

/* MARKE: Optik des Felds, nur Token-Klassen (Guide 8.x); Innenabstand in Rasterschritten */
const OPTIK = 'bg-flaeche text-text border border-linie-stark rounded-steuerung px-3 py-2 placeholder:text-text-leise'

const STEUERUNG = [
  'block w-full min-h-[44px]',
  'font-text text-fliesstext',
  OPTIK,
  'transition-colors duration-(--m-dauer-kurz) ease-standard motion-reduce:transition-none',
  'focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-fokus',
  'aria-invalid:border-fehler disabled:cursor-not-allowed',
].join(' ')

/* MARKE: Stufe des Labels und des Hinweises; Abstand in Rasterschritten */
const LABEL = 'font-text text-klein text-text'
const HINWEIS = 'text-klein text-text-leise'
const FEHLER = 'mt-2 text-klein text-fehler'

type FeldProps = {
  label: ReactNode
  hinweis?: ReactNode
  /** Fehlertext; gesetzt heißt: Feld ist ungültig */
  fehler?: string
  /** Klassen für den Rahmen um Label, Feld und Meldungen */
  className?: string
}

function useFeld(id: string | undefined, {hinweis, fehler}: Pick<FeldProps, 'hinweis' | 'fehler'>) {
  const automatisch = useId()
  const feldId = id ?? automatisch
  const hinweisId = hinweis != null ? `${feldId}-hinweis` : undefined
  const fehlerId = fehler ? `${feldId}-fehler` : undefined
  return {
    feldId,
    hinweisId,
    fehlerId,
    aria: {
      'aria-invalid': fehler ? true : undefined,
      'aria-describedby': [hinweisId, fehlerId].filter(Boolean).join(' ') || undefined,
    },
  }
}

function Feld({
  feldId,
  hinweisId,
  fehlerId,
  label,
  hinweis,
  fehler,
  pflicht,
  className,
  children,
}: FeldProps & {feldId: string; hinweisId?: string; fehlerId?: string; pflicht?: boolean; children: ReactNode}) {
  return (
    <div data-baustein="feld" data-pflicht={pflicht || undefined} data-fehler={fehler ? true : undefined} className={className}>
      <div className="flex flex-col gap-2">
        <label htmlFor={feldId} className={LABEL}>
          {label}
        </label>
        {hinweis != null && (
          <p id={hinweisId} className={HINWEIS}>
            {hinweis}
          </p>
        )}
        {children}
      </div>
      {/* Region bleibt stehen, damit Screenreader neue Fehler ansagen */}
      <div aria-live="polite">
        {fehler && (
          <p id={fehlerId} data-teil="fehler" className={FEHLER}>
            {fehler}
          </p>
        )}
      </div>
    </div>
  )
}

/** `name` und `autoComplete` sind Pflicht; autoComplete="off" nur bewusst, z. B. bei Feldern ohne Personenbezug */
export type InputProps = FeldProps &
  Omit<ComponentPropsWithRef<'input'>, 'className' | 'name' | 'autoComplete'> &
  Required<Pick<ComponentPropsWithRef<'input'>, 'name' | 'autoComplete'>>

export function Input({id, label, hinweis, fehler, className, type = 'text', spellCheck, ...rest}: InputProps) {
  const f = useFeld(id, {hinweis, fehler})
  // E-Mail, Codes und Namen nicht auf Rechtschreibung prüfen
  const pruefen = spellCheck ?? (type === 'email' || type === 'password' ? false : undefined)
  return (
    <Feld {...f} label={label} hinweis={hinweis} fehler={fehler} pflicht={rest.required} className={className}>
      <input id={f.feldId} type={type} spellCheck={pruefen} {...rest} {...f.aria} className={STEUERUNG} />
    </Feld>
  )
}

export type TextareaProps = FeldProps & Omit<ComponentPropsWithRef<'textarea'>, 'className' | 'name'> & Required<Pick<ComponentPropsWithRef<'textarea'>, 'name'>>

export function Textarea({id, label, hinweis, fehler, className, rows = 4, ...rest}: TextareaProps) {
  const f = useFeld(id, {hinweis, fehler})
  return (
    <Feld {...f} label={label} hinweis={hinweis} fehler={fehler} pflicht={rest.required} className={className}>
      <textarea id={f.feldId} rows={rows} {...rest} {...f.aria} className={`${STEUERUNG} resize-y`} />
    </Feld>
  )
}

export type SelectProps = FeldProps & Omit<ComponentPropsWithRef<'select'>, 'className' | 'name'> & Required<Pick<ComponentPropsWithRef<'select'>, 'name'>>

/** Natives <select> mit gesetzter Grund- und Schriftfarbe (sonst bricht der Dunkelmodus unter Windows). Pfeil-Optik in marke.css. */
export function Select({id, label, hinweis, fehler, className, children, ...rest}: SelectProps) {
  const f = useFeld(id, {hinweis, fehler})
  return (
    <Feld {...f} label={label} hinweis={hinweis} fehler={fehler} pflicht={rest.required} className={className}>
      <select id={f.feldId} {...rest} {...f.aria} className={STEUERUNG}>
        {children}
      </select>
    </Feld>
  )
}
