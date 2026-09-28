import pypdf

def analyze(fpath, outpath):
    reader = pypdf.PdfReader(fpath)
    page = reader.pages[0]
    out = [f"File: {fpath}", f"MediaBox: {page.mediabox}"]
    
    # fonts
    if '/Resources' in page and '/Font' in page['/Resources']:
        fonts = page['/Resources']['/Font']
        for k, v in fonts.items():
            out.append(f"Font {k}: {v.get('/BaseFont', '?')}, Subtype: {v.get('/Subtype', '?')}")

    def visitor(text, cm, tm, font_dict, font_size):
        if text.strip():
            fname = font_dict.get('/BaseFont', 'Unknown') if font_dict else 'Unknown'
            clean_text = text.strip()
            out.append(f"x={tm[4]:.1f}, y={tm[5]:.1f}, size={font_size:.1f}, font={fname}: {clean_text}")

    page.extract_text(visitor_text=visitor)
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

analyze("Hrushikesh_wadekar_DBA.pdf", "dba_layout.txt")
analyze("Hrushikesh_Wadekar_Resume.pdf", "de_layout.txt")
print("Analysis complete")
