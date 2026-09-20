#!/usr/bin/env python3
"""pages.py -- render course decks to images, or read them as montage sheets.

    python3 tools/slides/pages.py <deck.pptx|deck.pdf> <outdir> [options]

    --prefix NAME   file names become NAME-01.png ... (default: deck stem)
    --width  N      rendered page width in pixels (default 1500)
    --pages  1,2,5  render only these page numbers
    --sheet N       write montage sheets of N pages each into <outdir>/sheets/
                    with every tile labelled '#<page>', for reading in batches

WHY THIS EXISTS (house rule for this repository)

    The lecture decks are mostly hand-written ink pages: PowerPoint ink strokes
    exported as pictures and photos of blackboards.  Their text layer is empty
    or meaningless and `pdftotext` on them invents nonsense, so anything read
    out of them that way is a guess.  **Every slide is therefore read as a
    rendered image.**  This script is the only sanctioned way to look at a deck;
    no text extraction anywhere in the pipeline.

    Consequences that the scripts below encode:

    * a .pdf page is rasterised with pdfium;
    * a .pptx page is rasterised by this file's own renderer -- no LibreOffice
      and no internet in this sandbox.  It walks p:spTree and paints
      p:pic / p:graphicFrame / p:grpSp, follows the mc:Fallback of an ink
      contentPart, paints pictures that are used as a *shape fill*, and recurses
      into groups using the group's own chOff/chExt transform;
    * ink strokes are exported as a PNG of WHITE strokes on a fully transparent
      field, which pastes to nothing on a white page; `_ink_fix` repaints them
      dark using the alpha channel as the mask;
    * equations pasted from Word arrive as EMF whose whole content is one
      STRETCHDIBITS bitmap, decoded by `emf_dib`;
    * anything still undecodable is drawn as a labelled grey placeholder, so a
      page is never silently blank.

  Requires Pillow (always) and pypdfium2 (PDF decks only):
      pip install --break-system-packages --user pillow pypdfium2
"""
import io
import os
import re
import struct
import sys
import zipfile
from xml.etree import ElementTree as ET

from PIL import Image, ImageDraw, ImageFont

A = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
P = '{http://schemas.openxmlformats.org/presentationml/2006/main}'
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}'
REL = '{http://schemas.openxmlformats.org/package/2006/relationships}'

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


# ------------------------------------------------------------------ EMF/DIB
EMR_STRETCHDIBITS = 81


def emf_records(data):
    """Yield (record_type, offset, size) for each EMF record in `data`."""
    i = 0
    while i + 8 <= len(data):
        rtype, rsize = struct.unpack_from('<II', data, i)
        if rsize < 8 or i + rsize > len(data):
            break
        yield rtype, i, rsize
        i += rsize


def emf_text(data):
    """Last resort: strings out of EMR_EXTTEXTOUTA/W records."""
    out = []
    for rtype, off, rsize in emf_records(data):
        if rtype not in (83, 84):
            continue
        try:
            nchars = struct.unpack_from('<I', data, off + 8 + 8 + 8)[0]
            stroff = struct.unpack_from('<I', data, off + 8 + 8 + 12)[0]
            if rtype == 84:
                s = data[off + stroff:off + stroff + 2 * nchars].decode('utf-16-le', 'ignore')
            else:
                s = data[off + stroff:off + stroff + nchars].decode('latin1', 'ignore')
            s = ''.join(c for c in s if c.isprintable()).strip()
            if s:
                out.append(s)
        except Exception:
            pass
    return out


def emf_dib(record):
    """Decode the bitmap of one EMR_STRETCHDIBITS record -> (PIL image, geometry)."""
    (l, t, r, b) = struct.unpack_from('<4i', record, 8)
    x_dest, y_dest = struct.unpack_from('<2i', record, 24)
    cx_src, cy_src = struct.unpack_from('<2i', record, 40)
    off_bmi, cb_bmi, off_bits, cb_bits = struct.unpack_from('<4I', record, 48)
    cx_dest, cy_dest = struct.unpack_from('<2i', record, 72)
    bmi = record[off_bmi:off_bmi + cb_bmi]
    if len(bmi) < 40:
        return None
    (hdr, w, h, planes, bpp, compression, size_img, xppm, yppm,
     clr_used, clr_important) = struct.unpack_from('<IiiHHIIiiII', bmi, 0)
    if compression not in (0, 3):
        return None
    bits = record[off_bits:off_bits + cb_bits]
    palette = bmi[40:40 + 4 * clr_used] if clr_used else b''
    bottom_up, h = h > 0, abs(h)
    try:
        if bpp == 24:
            stride = (w * 3 + 3) & ~3
            im = Image.frombuffer('RGB', (w, h), bits[:stride * h], 'raw', 'BGR', stride, 1)
        elif bpp == 32:
            stride = (w * 4 + 3) & ~3
            im = Image.frombuffer('RGBA', (w, h), bits[:stride * h], 'raw', 'BGRA', stride, 1).convert('RGB')
        elif bpp in (8, 4):
            stride = ((w * bpp + 7) // 8 + 3) & ~3
            pal = []
            for i in range(len(palette) // 4):
                bl, gr, rd, _ = palette[4 * i:4 * i + 4]
                pal += [rd, gr, bl]
            im = Image.frombuffer('P', (w, h), bits[:stride * h], 'raw', 'P', stride, 1)
            im.putpalette(pal)
            im = im.convert('RGB')
        elif bpp == 1:
            stride = ((w + 7) // 8 + 3) & ~3
            im = Image.frombuffer('1', (w, h), bits[:stride * h], 'raw', '1', stride, 1).convert('RGB')
        else:
            return None
    except Exception:
        return None
    if bottom_up:
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
    return im, (x_dest, y_dest, cx_dest, cy_dest, (l, t, r, b))


# ------------------------------------------------------------------ EMF vector
# Records used by the decks that export their diagrams and ink as EMF vector
# art (no bitmap, no text to fall back on): pens, brushes, paths and the
# 16-bit polyline/polygon family.
EMR_HEADER, EMR_POLYBEZIER, EMR_POLYGON, EMR_POLYLINE = 1, 2, 3, 4
EMR_SETWINDOWEXTEX, EMR_SETWINDOWORGEX = 9, 10
EMR_SETVIEWPORTEXTEX, EMR_SETVIEWPORTORGEX = 11, 12
EMR_SETPOLYFILLMODE, EMR_SETROP2 = 19, 20
EMR_MOVETOEX, EMR_SAVEDC, EMR_RESTOREDC = 27, 33, 34
EMR_SETWORLDTRANSFORM, EMR_MODIFYWORLDTRANSFORM = 35, 36
EMR_SELECTOBJECT, EMR_CREATEPEN, EMR_CREATEBRUSHINDIRECT = 37, 38, 39
EMR_DELETEOBJECT, EMR_ELLIPSE, EMR_RECTANGLE = 40, 42, 43
EMR_LINETO, EMR_BEGINPATH, EMR_ENDPATH, EMR_CLOSEFIGURE = 54, 59, 60, 61
EMR_FILLPATH, EMR_STROKEANDFILLPATH, EMR_STROKEPATH = 62, 63, 64
EMR_POLYBEZIER16, EMR_POLYGON16, EMR_POLYLINE16 = 85, 86, 87
EMR_POLYBEZIERTO16, EMR_POLYLINETO16 = 88, 89
EMR_POLYPOLYLINE16, EMR_POLYPOLYGON16, EMR_POLYDRAW16 = 90, 91, 92
EMR_EXTCREATEPEN = 95

_PEN_STYLE_DASH = {1, 2, 3, 4, 5}          # PS_DASH .. PS_ALTERNATE


def _colorref(v):
    return ((v >> 0) & 0xFF, (v >> 8) & 0xFF, (v >> 16) & 0xFF)


def _mul(a, b):
    """2x3 affine matrices, [a b c d e f] meaning x'=ax+cy+e, y'=bx+dy+f."""
    return [a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3],
            a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
            a[4] * b[0] + a[5] * b[2] + b[4], a[4] * b[1] + a[5] * b[3] + b[5]]


def emf_vector(data, size=(1200, 900), bg=(255, 255, 255)):
    """Rasterise an EMF of vector records (the 16-bit polyline/polygon art).

    Returns a PIL image, or None if the stream held nothing drawable.  It is
    deliberately small: it implements the records these decks use (pens,
    brushes, paths, the 16-bit poly* family) and ignores the rest.

    Layout note that cost a debugging cycle: in the 16-bit poly records
    (EMR_POLYLINE16/POLYGON16/POLYBEZIERTO16/... 85-89) the record is
    { iType, nSize, rclBounds, cpts, apts } -- the count is at +24 and the
    points start at +28.  Reading the count at +8 quietly hands back the left
    edge of the bounding box.

    The header's rclBounds cannot be trusted either (these files carry
    nonsense there), so the extent is measured by a dry run of the whole
    stream and the real render is fitted to it.
    """
    from PIL import ImageDraw
    W, H = size
    wins = {'win_org': (0, 0), 'win_ext': (1, 1), 'vp_org': (0, 0), 'vp_ext': (1, 1)}

    def poly_count_off(off, family):
        """(cpts, points offset) for the record families we understand."""
        if family == 'polypoly':
            n = struct.unpack_from('<I', data, off + 24)[0]
            return None, off + 32 + 4 * n
        return struct.unpack_from('<I', data, off + 24)[0], off + 28

    class Sink:
        """Records the bounding box, then draws into the fitted canvas."""

        def __init__(self, draw=None, tf=None):
            self.draw, self.tf = draw, tf
            self.box = None

        def note(self, pts):
            for x, y in pts:
                if self.box is None:
                    self.box = [x, y, x, y]
                else:
                    self.box[0] = min(self.box[0], x)
                    self.box[1] = min(self.box[1], y)
                    self.box[2] = max(self.box[2], x)
                    self.box[3] = max(self.box[3], y)

        def line(self, pts, colour, width, dashed=False):
            self.note(pts)
            if not (self.draw and self.tf):
                return
            pts = [self.tf(p[0], p[1]) for p in pts]
            if dashed and len(pts) > 1:
                for i in range(0, len(pts) - 1, 2):
                    self.draw.line([pts[i], pts[i + 1]], fill=colour, width=width)
            else:
                self.draw.line(pts, fill=colour, width=width, joint='curve')

        def polygon(self, pts, colour):
            self.note(pts)
            if self.draw and self.tf and colour and len(pts) > 2:
                self.draw.polygon([self.tf(p[0], p[1]) for p in pts], fill=colour)

        def ellipse(self, box, fill_col, line_col, width):
            self.note([(box[0], box[1]), (box[2], box[3])])
            if self.draw and self.tf:
                b = list(self.tf(box[0], box[1])) + list(self.tf(box[2], box[3]))
                b = [min(b[0], b[2]), min(b[1], b[3]), max(b[0], b[2]), max(b[1], b[3])]
                if fill_col:
                    self.draw.ellipse(b, fill=fill_col)
                if line_col:
                    self.draw.ellipse(b, outline=line_col, width=width)

    def run(sink):
        """Execute the stream once.  `sink` decides whether anything is drawn."""
        dr = getattr(sink, 'draw', None)
        img = None
        st = {'world': [1, 0, 0, 1, 0, 0], 'pen': (0, 0, 0, 1, 0), 'brush': None,
              'poly_fill': 1, 'path': None, 'in_path': False, 'cur': None}
        stack, objs, nid = [], {}, [1]

        def logical(p):
            wx, wy = wins['win_org']
            wex, wey = wins['win_ext']
            vox, voy = wins['vp_org']
            vex, vey = wins['vp_ext']
            x = (p[0] - wx) * (vex / wex if wex else 1) + vox
            y = (p[1] - wy) * (vey / wey if wey else 1) + voy
            w = st['world']
            return (w[0] * x + w[2] * y + w[4], w[1] * x + w[3] * y + w[5])

        def pts16(off, family='poly'):
            c, po = poly_count_off(off, family)
            if c is None:
                return []
            return [logical(struct.unpack_from('<hh', data, po + 4 * i)) for i in range(c)]

        def stroke(pts, close=False, raw=False):
            pen = st['pen']
            if not pts or pen is None:
                return
            seq = [logical(p) for p in pts] if raw else pts
            if close and len(seq) > 2:
                seq = seq + [seq[0]]
            sink.line(seq, pen[:3], max(2, int(round(pen[3]))),
                      dashed=len(pen) > 4 and pen[4] in _PEN_STYLE_DASH)

        def fillp(pts):
            if st['brush'] is None:
                return
            sink.polygon(pts if isinstance(pts[0], tuple) else pts, st['brush'])

        for rtype, off, rsize in emf_records(data):
            if rtype in (EMR_SETWINDOWEXTEX, EMR_SETVIEWPORTEXTEX, EMR_SETWINDOWORGEX,
                         EMR_SETVIEWPORTORGEX):
                key = {EMR_SETWINDOWEXTEX: 'win_ext', EMR_SETVIEWPORTEXTEX: 'vp_ext',
                       EMR_SETWINDOWORGEX: 'win_org', EMR_SETVIEWPORTORGEX: 'vp_org'}[rtype]
                wins[key] = struct.unpack_from('<2i', data, off + 8)
            elif rtype in (EMR_SETWORLDTRANSFORM, EMR_MODIFYWORLDTRANSFORM):
                m = list(struct.unpack_from('<6f', data, off + 8))
                mode = struct.unpack_from('<I', data, off + 32)[0] if rtype == EMR_MODIFYWORLDTRANSFORM else 0
                if rtype == EMR_SETWORLDTRANSFORM or mode == 1:
                    st['world'] = _mul(m, st['world']) if mode == 1 else m
                elif mode == 2:
                    st['world'] = _mul(st['world'], m)
            elif rtype == EMR_SAVEDC:
                stack.append({k: (list(v) if isinstance(v, list) else v) for k, v in st.items()})
            elif rtype == EMR_RESTOREDC:
                if stack:
                    st.update(stack.pop())
            elif rtype in (EMR_CREATEPEN, EMR_EXTCREATEPEN):
                style, width, _bs = struct.unpack_from('<3I', data, off + 8)
                colour = struct.unpack_from('<I', data, off + 20)[0]
                objs[nid[0]] = ('pen', _colorref(colour) + (max(1, width), style))
                nid[0] += 1
            elif rtype == EMR_CREATEBRUSHINDIRECT:
                style, colour, _hatch = struct.unpack_from('<III', data, off + 8)
                objs[nid[0]] = ('brush', None if style == 1 else _colorref(colour))
                nid[0] += 1
            elif rtype in (93, 94):
                objs[nid[0]] = ('brush', None)
                nid[0] += 1
            elif rtype == EMR_SELECTOBJECT:
                obj = objs.get(struct.unpack_from('<I', data, off + 8)[0])
                if obj:
                    if obj[0] == 'pen':
                        st['pen'] = obj[1]
                    else:
                        st['brush'] = obj[1]
            elif rtype == EMR_DELETEOBJECT:
                objs.pop(struct.unpack_from('<I', data, off + 8)[0], None)
            elif rtype == EMR_SETPOLYFILLMODE:
                st['poly_fill'] = struct.unpack_from('<I', data, off + 8)[0]
            elif rtype == EMR_MOVETOEX:
                st['cur'] = struct.unpack_from('<2i', data, off + 8)
            elif rtype == EMR_LINETO:
                p = struct.unpack_from('<2i', data, off + 8)
                stroke([st['cur'] or p, p], raw=True)
                st['cur'] = p
            elif rtype in (EMR_POLYLINE16, EMR_POLYBEZIER16, EMR_POLYGON16, EMR_POLYDRAW16,
                           EMR_POLYLINETO16, EMR_POLYBEZIERTO16):
                pts = pts16(off)
                if rtype in (EMR_POLYLINETO16, EMR_POLYBEZIERTO16):
                    if st['cur'] is not None:
                        pts = [logical(st['cur'])] + pts
                    if pts:
                        st['cur'] = struct.unpack_from('<hh', data, off + rsize - 4)
                if rtype == EMR_POLYGON16:
                    fillp(pts)
                    stroke(pts, close=True)
                else:
                    stroke(pts)
                    if st['in_path'] and st['path'] is not None:
                        st['path'] += pts
            elif rtype in (EMR_POLYPOLYLINE16, EMR_POLYPOLYGON16):
                pts = pts16(off, 'polypoly')
                if pts:
                    if rtype == EMR_POLYPOLYGON16:
                        fillp(pts)
                    stroke(pts, close=(rtype == EMR_POLYPOLYGON16))
                    if st['in_path'] and st['path'] is not None:
                        st['path'] += pts
            elif rtype == EMR_RECTANGLE:
                l2, t2, r2, b2 = struct.unpack_from('<4i', data, off + 8)
                pts = [logical(p) for p in ((l2, t2), (r2, t2), (r2, b2), (l2, b2))]
                fillp(pts)
                stroke(pts, close=True)
            elif rtype == EMR_ELLIPSE:
                l2, t2, r2, b2 = struct.unpack_from('<4i', data, off + 8)
                pen = st['pen']
                sink.ellipse((l2, t2, r2, b2), st['brush'],
                             pen[:3] if pen else None,
                             max(1, int(round(pen[3]))) if pen else 1)
            elif rtype == EMR_BEGINPATH:
                st['in_path'], st['path'] = True, []
            elif rtype == EMR_ENDPATH:
                st['in_path'] = False
            elif rtype == EMR_CLOSEFIGURE:
                if st['path']:
                    st['path'].append(st['path'][0])
            elif rtype in (EMR_FILLPATH, EMR_STROKEANDFILLPATH, EMR_STROKEPATH):
                pts = st['path'] or []
                if rtype == EMR_FILLPATH:
                    fillp(pts)
                elif rtype == EMR_STROKEPATH:
                    stroke(pts)
                else:
                    fillp(pts)
                    stroke(pts, close=True)
                st['path'] = []
        return img

    probe = Sink()
    run(probe)
    if probe.box is None:
        return None
    x0, y0, x1, y1 = probe.box
    if x1 - x0 < 1e-9 or y1 - y0 < 1e-9:
        return None
    sc = min((W - 2) / (x1 - x0), (H - 2) / (y1 - y0))
    img = Image.new('RGB', size, bg)
    dr = ImageDraw.Draw(img)
    real = Sink(dr, lambda x, y: ((x - x0) * sc + 1, (y - y0) * sc + 1))
    run(real)
    return img


def _ink_fix(im):
    """White ink strokes on a transparent field -> dark strokes (see docstring)."""
    from PIL import ImageStat
    a = im.getchannel('A')
    hist = a.histogram()
    total = sum(hist) or 1
    if sum(hist[:16]) / total < 0.3:                 # mostly opaque: leave it
        return im
    mask = a.point(lambda v: 255 if v >= 128 else 0)
    if not mask.getbbox():
        return im
    if min(ImageStat.Stat(im.convert('RGB'), mask).mean) < 200:
        return im                                    # already dark strokes
    out = Image.new('RGBA', im.size, (17, 17, 17, 0))
    out.putalpha(a)
    return out


# ------------------------------------------------------------------ pptx
def _xfrm(el):
    x = el.find('.//' + A + 'xfrm')
    if x is None:
        return None
    off, ext = x.find(A + 'off'), x.find(A + 'ext')
    if off is None or ext is None:
        return None
    return (int(off.get('x')), int(off.get('y')), int(ext.get('cx')), int(ext.get('cy')))


def _chx(el):
    x = el.find('.//' + A + 'xfrm')
    if x is None:
        return None
    o, e = x.find(A + 'chOff'), x.find(A + 'chExt')
    if o is None or e is None:
        return None
    return (int(o.get('x')), int(o.get('y')), int(e.get('cx')), int(e.get('cy')))



def _ph_key(el):
    """(type, idx) of a shape's <p:ph>, or None if the shape is not a placeholder."""
    ph = el.find('.//' + P + 'ph')
    if ph is None:
        return None
    return (ph.get('type') or 'body', ph.get('idx') or '0')


def _placeholder_box(tree, key):
    """The xfrm a placeholder inherits from its layout/master, or None."""
    for sp in tree.iter(P + 'sp'):
        if _ph_key(sp) != key:
            continue
        box = _xfrm(sp)
        if box:
            return box
    return None


class PptxRenderer:
    def __init__(self, path, width=1500):
        self.z = zipfile.ZipFile(path)
        pres = ET.fromstring(self.z.read('ppt/presentation.xml'))
        sz = pres.find(P + 'sldSz')
        self.sw, self.sh = int(sz.get('cx')), int(sz.get('cy'))
        self.W = width
        self.scale = width / self.sw
        self.H = int(round(self.sh * self.scale))
        names = [n for n in self.z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$', n)]
        self.slides = sorted(names, key=lambda n: int(re.search(r'(\d+)', n.split('/')[-1]).group(1)))

    def render(self, part):
        img = Image.new('RGB', (self.W, self.H), 'white')
        dr = ImageDraw.Draw(img)
        root = ET.fromstring(self.z.read(part))
        rels = self._rels(part)
        # A placeholder that carries no <a:xfrm> of its own takes its position
        # from the slide LAYOUT (and the layout's from the master).  Without
        # this, every such shape -- which is most body text in a deck built
        # from a template -- is dropped and the page renders blank.
        self._ph = {}
        for chain in ('ppt/slideLayouts', 'ppt/slideMasters'):
            for name in self.z.namelist():
                if not name.startswith(chain + '/') or not name.endswith('.xml'):
                    continue
                tree = ET.fromstring(self.z.read(name))
                for sp in tree.iter(P + 'sp'):
                    key = _ph_key(sp)
                    box = _xfrm(sp)
                    if key and box and key not in self._ph:
                        self._ph[key] = box
        texts = []
        self.walk(list(root.find('.//' + P + 'spTree')), rels, (0, 0, 1.0), img, dr, texts)
        for t in texts:
            self._text(dr, *t)
        return img

    def _box_of(self, el):
        """A shape's own xfrm, else the one its placeholder inherits."""
        box = _xfrm(el)
        if box:
            return box
        key = _ph_key(el)
        if key is None:
            return None
        box = getattr(self, '_ph', {}).get(key)
        if box:
            return box
        # last resort: place it in the body block so the text is never lost
        return (609600, 1600000, self.sw - 1219200, self.sh - 2200000)


    def _rels(self, part):
        rp = os.path.join(os.path.dirname(part), '_rels', os.path.basename(part) + '.rels')
        rp = rp.replace('\\', '/')
        if rp not in self.z.namelist():
            return {}
        return {r.get('Id'): r.get('Target')
                for r in ET.fromstring(self.z.read(rp)).findall(REL + 'Relationship')}

    def walk(self, children, rels, tf, img, dr, texts):
        for el in children:
            tag = el.tag
            if tag == P + 'pic':
                self._pic(el, rels, tf, img, dr)
            elif tag == P + 'sp':
                if el.find('.//' + A + 'blipFill/' + A + 'blip') is not None:
                    self._pic(el, rels, tf, img, dr)
                self._text_shape(el, tf, texts)
                self.walk(list(el), rels, tf, img, dr, texts)   # WPS nests pic in sp
            elif tag == P + 'graphicFrame':
                self._table(el, tf, img, dr, texts)
            elif tag == P + 'grpSp':
                box, ch = _xfrm(el), _chx(el)
                sub = tf
                if box and ch and ch[2] and ch[3]:
                    ox, oy, cx, cy = box
                    cox, coy, ccx, ccy = ch
                    sx, sy = cx / ccx, cy / ccy
                    sub = (tf[0] + (ox - cox * sx) * tf[2], tf[1] + (oy - coy * sy) * tf[2], tf[2] * sx)
                self.walk(list(el), rels, sub, img, dr, texts)
            else:
                self.walk(list(el), rels, tf, img, dr, texts)   # mc:AlternateContent etc.

    def _pic(self, el, rels, tf, img, dr):
        blip, box = el.find('.//' + A + 'blip'), self._box_of(el)
        if blip is None or box is None:
            return
        target = rels.get(blip.get(R + 'embed'))
        if not target:
            return
        name = os.path.normpath(os.path.join('ppt/slides', target)).replace('\\', '/')
        if name not in self.z.namelist():
            return
        raw = self.z.read(name)
        ext = name.rsplit('.', 1)[-1].lower()
        ox, oy, cx, cy = (v * tf[2] for v in box)
        x0, y0 = self.px(ox + tf[0], oy + tf[1])
        x1, y1 = self.px(ox + tf[0] + cx, oy + tf[1] + cy)
        w, h = max(1, int(round(x1 - x0))), max(1, int(round(y1 - y0)))
        if ext in ('png', 'jpg', 'jpeg', 'gif', 'bmp'):
            im = _ink_fix(Image.open(io.BytesIO(raw)).convert('RGBA')).resize((w, h), Image.LANCZOS)
            img.paste(im, (int(x0), int(y0)), im)
            return
        if ext in ('emf', 'wmf'):
            for rtype, off, size in emf_records(raw):
                if rtype == EMR_STRETCHDIBITS:
                    got = emf_dib(raw[off:off + size])
                    if got:
                        im = got[0].convert('RGBA').resize((w, h), Image.LANCZOS)
                        img.paste(im, (int(x0), int(y0)), im)
                        return
            vec = emf_vector(raw, (max(8, w), max(8, h)))
            if vec is not None:
                img.paste(vec, (int(x0), int(y0)))
                return
            lines = emf_text(raw)
            if lines:
                dr.rectangle([x0, y0, x1, y1], outline=(200, 200, 200))
                f = ImageFont.truetype(FONT, 16)
                for i, ln in enumerate(lines[:12]):
                    dr.text((x0 + 4, y0 + 4 + 18 * i), ln, fill='black', font=f)
                return
        dr.rectangle([x0, y0, x1, y1], outline=(190, 190, 190), fill=(245, 245, 245))
        dr.text((x0 + 4, y0 + 4), '[%s]' % ext, fill=(120, 120, 120),
                font=ImageFont.truetype(FONT, 13))

    def px(self, x, y):
        return x * self.scale, y * self.scale

    def _text_shape(self, el, tf, texts):
        box, tx = self._box_of(el), el.find('.//' + P + 'txBody')
        if box is None or tx is None:
            return
        ox, oy, cx, cy = (v * tf[2] for v in box)
        x0, y0 = self.px(ox + tf[0], oy + tf[1])
        paras = []
        for p in tx.findall(A + 'p'):
            runs, size, bold = [], 18, False
            for r in p.findall(A + 'r'):
                rPr = r.find(A + 'rPr')
                if rPr is not None and rPr.get('sz'):
                    size = int(rPr.get('sz')) / 100
                if rPr is not None and rPr.get('b') == '1':
                    bold = True
                t = r.find(A + 't')
                if t is not None and t.text:
                    runs.append(t.text)
            line = ''.join(runs).strip()
            if line:
                paras.append((line, size, bold))
        if paras:
            texts.append((x0, y0, paras))

    def _text(self, dr, x0, y0, paras):
        sc = self.scale * 72 / 914400.0
        y = y0
        for line, size, bold in paras:
            px = max(8, int(round(size * sc * 1.6)))
            try:
                f = ImageFont.truetype(FONT_B if bold else FONT, px)
            except Exception:
                f = ImageFont.load_default()
            words, cur, out = line.split(), '', []
            for wd in words:
                trial = (cur + ' ' + wd).strip()
                if dr.textlength(trial, font=f) > self.W - x0 - 12 and cur:
                    out.append(cur)
                    cur = wd
                else:
                    cur = trial
            out.append(cur)
            for ln in out:
                dr.text((x0, y), ln, fill=(20, 20, 20), font=f)
                y += px * 1.22
            y += 3

    def _table(self, el, tf, img, dr, texts):
        box, tbl = _xfrm(el), el.find('.//' + A + 'tbl')
        if box is None or tbl is None:
            return
        ox, oy, cx, cy = (v * tf[2] for v in box)
        x0, y0 = self.px(ox + tf[0], oy + tf[1])
        x1, y1 = self.px(ox + tf[0] + cx, oy + tf[1] + cy)
        grid = tbl.find(A + 'tblGrid')
        cols = [int(c.get('w')) for c in grid.findall(A + 'gridCol')] if grid is not None else []
        total = sum(cols) or 1
        rows = tbl.findall(A + 'tr')
        heights = [int(tr.get('h') or 0) for tr in rows]
        htot = sum(heights) or 1
        yy = y0
        for ri, tr in enumerate(rows):
            rh = (y1 - y0) * (heights[ri] / htot) if htot else (y1 - y0) / max(1, len(rows))
            xx = x0
            for ci, tc in enumerate(tr.findall(A + 'tc')):
                cw = (x1 - x0) * (cols[ci] / total) if ci < len(cols) and total else (x1 - x0) / 4
                dr.rectangle([xx, yy, xx + cw, yy + rh], outline=(150, 150, 150))
                lines = [(s, 11, False) for s in
                         (''.join(t.text or '' for t in p.iter(A + 't')).strip()
                          for p in tc.findall('.//' + A + 'p')) if s]
                if lines:
                    texts.append((xx + 3, yy + 2, lines))
                xx += cw
            yy += rh


# ------------------------------------------------------------------ pdf
def pdf_pages(path, width):
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(path)
    out = []
    for i in range(len(doc)):
        page = doc[i]
        out.append(page.render(scale=width / page.get_width()).to_pil().convert('RGB'))
    return out


def pptx_pages(path, width):
    r = PptxRenderer(path, width)
    return [r.render(part) for part in r.slides]


# ------------------------------------------------------------------ montage
def sheet(imgs, idx, out, per_sheet=4, label=True):
    """2-up montage sheets, each tile labelled '#<page number>', for reading."""
    h = max(im.height for im in imgs)
    imgs = [im if im.height == h else im.resize((im.width, h)) for im in imgs]
    made = []
    for k in range(0, len(imgs), per_sheet):
        chunk, nums = imgs[k:k + per_sheet], idx[k:k + per_sheet]
        cols = 2
        rows = (len(chunk) + 1) // 2
        w = max(im.width for im in chunk)
        sh = Image.new('RGB', (w * cols + 6, h * rows + 6), (110, 110, 110))
        dr = ImageDraw.Draw(sh)
        for j, im in enumerate(chunk):
            x, y = (j % cols) * (w + 6), (j // cols) * (h + 6)
            sh.paste(im, (x, y))
            if label:
                dr.text((x + 8, y + 6), '#%d' % nums[j], fill=(200, 30, 30),
                        font=ImageFont.truetype(FONT_B, 22))
        name = '%s-%02d.png' % (out, k // per_sheet + 1)
        sh.save(name)
        made.append(name)
    return made


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print(__doc__)
        return 2
    deck, outdir = args[0], args[1]
    width, prefix, pages, per = 1500, None, None, 0
    for key, cast in (('--width', int), ('--prefix', str), ('--sheet', int)):
        if key in args:
            val = cast(args[args.index(key) + 1])
            if key == '--width':
                width = val
            elif key == '--prefix':
                prefix = val
            else:
                per = val
    if '--pages' in args:
        pages = [int(x) for x in args[args.index('--pages') + 1].split(',')]
    os.makedirs(outdir, exist_ok=True)
    prefix = prefix or os.path.splitext(os.path.basename(deck))[0]
    imgs = pdf_pages(deck, width) if deck.lower().endswith('.pdf') else pptx_pages(deck, width)
    idx = list(range(1, len(imgs) + 1))
    if pages:
        keep = [i for i in idx if i in pages]
        imgs = [imgs[i - 1] for i in keep]
        idx = keep
    if per:
        sub = os.path.join(outdir, 'sheets')
        os.makedirs(sub, exist_ok=True)
        for f in sheet(imgs, idx, os.path.join(sub, prefix), per):
            print(f)
    else:
        for n, im in zip(idx, imgs):
            f = os.path.join(outdir, '%s-%02d.png' % (prefix, n))
            im.save(f)
            print(f)
    return 0


if __name__ == '__main__':
    sys.exit(main())
