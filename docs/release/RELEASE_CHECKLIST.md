# Release Checklist — openlineage-llm

## Preflight
- [ ] `make venv && make test` passes
- [ ] `make up && make health` shows healthy admin + API
- [ ] `make demo` posts START/COMPLETE to Marquez (verify via API)

## GitHub
- [ ] `git init` (first time), add remote, commit, push `main`
- [ ] Update `pyproject.toml` version and `.zenodo.json` "version"
- [ ] `make tag version=X.Y.Z` (creates vX.Y.Z), push tags
- [ ] Create GitHub Release `vX.Y.Z` (attach whitepaper PDF if ready)

## Zenodo
- [ ] In Zenodo > GitHub, toggle the repo **on**
- [ ] After Release is created, Zenodo mints a DOI
- [ ] Add DOI badge in README and DOI in `CITATION.cff`

## Whitepaper (optional but recommended)
- [ ] Fill `docs/whitepaper/whitepaper.md` or `ieee_whitepaper.tex`
- [ ] Export to PDF and attach to the GitHub Release

## Post-release
- [ ] Announce: README badge, LinkedIn/X
- [ ] Capture Marquez screenshots for EB-1 packet
