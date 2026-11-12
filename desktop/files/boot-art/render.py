#!/usr/bin/env python3
"""Render Debian's existing swirl vector; no external artwork or fonts."""
from pathlib import Path
import gi,cairo
import xml.etree.ElementTree as ET

gi.require_foreign('cairo')
gi.require_version('Rsvg','2.0')
from gi.repository import Rsvg
here=Path(__file__).resolve().parent
root=ET.parse(here/'debian-logo-source.svg').getroot()
for node in root.iter():
 style=node.get('style','')
 for gray in ['#e6e6e6','#d1d1d1','#666666']:style=style.replace(gray,'#f2f3f5')
 style=style.replace('opacity:0.71','opacity:1')
 if style:node.set('style',style)
svg=ET.tostring(root,encoding='utf-8');(here/'debian-logo.svg').write_bytes(svg)
handle=Rsvg.Handle.new_from_data(svg)
image=cairo.ImageSurface(cairo.FORMAT_ARGB32,480,240);cr=cairo.Context(image)
rect=Rsvg.Rectangle();rect.x=156;rect.y=28;rect.width=168;rect.height=168
handle.render_document(cr,rect)
image.write_to_png(str(here/'watermark.png'))
# A preview of layout only; actual Plymouth rendering is validated after reboot.
preview=cairo.ImageSurface(cairo.FORMAT_ARGB32,1200,800);cr=cairo.Context(preview)
cr.set_source_rgb(0.025,0.03,0.045);cr.paint();cr.set_source_surface(image,360,170);cr.paint()
spinner=cairo.ImageSurface.create_from_png(str(here.parent/'rootfs/usr/share/plymouth/themes/surface-debian/animation-0014.png'))
cr.set_source_surface(spinner,600-spinner.get_width()/2,535-spinner.get_height()/2);cr.paint()
preview.write_to_png(str(here/'preview.png'))
print(here/'preview.png')
