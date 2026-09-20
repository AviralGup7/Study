# tools/slides — reading the lecture decks

```bash
python3 tools/slides/pages.py "<deck.pptx|deck.pdf>" /tmp/pages            # one PNG per page
python3 tools/slides/pages.py "<deck.pptx>" /tmp/pages --pages 1,2,5        # just these pages
python3 tools/slides/pages.py "<deck.pptx>" /tmp/pages --sheet 4            # 2x2 sheets, tiles
                                                                            # labelled '#<page>'
```

Dependencies (both pip-installable, no system packages available in this sandbox):

```bash
pip install --break-system-packages --user pillow pypdfium2
```

## The rule this tool exists for

**Every slide is read as a rendered image. Text extraction from a deck is not used.**
Most of these decks are hand-written ink pages — PowerPoint ink exported as pictures, or
photographs of a blackboard — so their text layer is empty or misleading and `pdftotext` on
them produces plausible-looking nonsense. Anything "read" that way in these notes would be a
guess, and the notes claim to be quoted from the source.

So: render the page, look at it, and write down only what is actually legible.

## What has to be handled (and is)

* `.pdf` decks — rasterised with pdfium.
* `.pptx` decks — rasterised by `PptxRenderer` in `pages.py`, with no LibreOffice and no
  internet: it paints `p:pic`, `p:sp`, `p:graphicFrame` and `p:grpSp` (honouring the group's
  `chOff`/`chExt`), and recurses into `sp` because WPS nests pictures there.
* **Ink strokes** are exported as a PNG of *white* strokes on a fully transparent field, which
  pastes onto a white page as nothing at all. `_ink_fix` detects that case (mostly transparent
  + near-white opaque pixels) and repaints the strokes dark, using alpha as the mask.
* **Equations pasted from Word** arrive as an EMF whose entire content is one `EMR_STRETCHDIBITS`
  bitmap; `emf_dib` decodes the DIB straight out of the record. `emf_text` (the
  `EMR_EXTTEXTOUTW` strings) is only a fallback.
* Anything still undecodable is drawn as a labelled grey placeholder, so a page is never
  silently blank — a blank page in a sheet means the deck really is blank there.

Worth knowing when reading the output: a page rendered years-old PowerPoint may still hide
content behind an ink layer, and some decks ship the same slide twice; both show up here
honestly rather than being smoothed over.
