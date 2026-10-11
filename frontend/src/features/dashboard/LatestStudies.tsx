import { FileTab } from '@/components/specialty/FileTab'
import { SourcePanel } from '@/features/documents/sources/SourcePanel'
import { StudyItem } from '@/features/documents/sources/StudiesPanel'
import { useLatestStudies } from '@/lib/queries'

export function LatestStudies() {
  const query = useLatestStudies()
  return (
    <section aria-label="Neueste Studien" className="flex min-w-0 flex-col gap-4">
      <h2 className="text-base font-semibold">Neueste Studien</h2>
      <SourcePanel source="PubMed · NCBI" shortName="PubMed" query={query} emptyText="Keine Studien gefunden.">
        {(groups) => (
          <div className="flex flex-col gap-5">
            {groups.map((group) => (
              <div key={group.category} className="flex min-w-0 flex-col">
                <FileTab name={group.category} className="relative z-10 ml-3 -mb-px self-start" />
                <ul className="rounded-xl border bg-card px-5 py-3 text-sm shadow-sheet">
                  {group.studies.slice(0, 3).map((study) => <StudyItem key={study.pmid} study={study} />)}
                </ul>
              </div>
            ))}
          </div>
        )}
      </SourcePanel>
    </section>
  )
}
