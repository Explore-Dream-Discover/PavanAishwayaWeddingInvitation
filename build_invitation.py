import os
import sys
import base64
import subprocess
import shutil
import qrcode
from PIL import Image
import numpy as np
import pdf2image

def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    images_dir = os.path.join(base_dir, "static", "images")
    downloads_dir = os.path.join(base_dir, "static", "downloads")
    os.makedirs(downloads_dir, exist_ok=True)

    artifact_dir = r"C:\Users\elang\.gemini\antigravity\brain\c35b15e5-a9f5-4a7d-8beb-c58092248324"
    os.makedirs(artifact_dir, exist_ok=True)

    # 1. Generate Venue Google Maps QR Code
    maps_url = "https://maps.app.goo.gl/j1HJmygQAsjiv335A"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=2,
    )
    qr.add_data(maps_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#4A0E17", back_color="white").convert("RGB")
    qr_path = os.path.join(images_dir, "venue_map_qr.png")
    qr_img.save(qr_path)
    print(f"QR code saved: {qr_path}")

    # Read couple infinity image - Use the highest quality full artwork
    couple_img_path = os.path.join(images_dir, "couple_infinity.jpg")
    with open(couple_img_path, "rb") as f:
        couple_b64 = base64.b64encode(f.read()).decode("utf-8")

    with open(qr_path, "rb") as f:
        qr_b64 = base64.b64encode(f.read()).decode("utf-8")

    # Auspicious Golden Emblem Motif
    emblem_svg = """<svg width="42" height="42" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="50" cy="50" r="44" stroke="#D4AF37" stroke-width="2" stroke-dasharray="3 3"/>
      <circle cx="50" cy="50" r="38" stroke="#845E16" stroke-width="1.5"/>
      <path d="M50 18C50 18 53 32 66 35C53 38 50 52 50 52C50 52 47 38 34 35C47 32 50 18 50 18Z" fill="#D4AF37" stroke="#845E16" stroke-width="1.5"/>
      <circle cx="50" cy="35" r="4" fill="#8E1638"/>
      <path d="M50 58C45 66 38 72 38 78C38 84 43 88 50 88C57 88 62 84 62 78C62 72 55 66 50 58Z" fill="#FAF0D6" stroke="#845E16" stroke-width="1.5"/>
      <path d="M50 64V82M45 74H55" stroke="#8E1638" stroke-width="1.5" stroke-linecap="round"/>
    </svg>"""

    # 2. Build Royal Invitation HTML with UNCROPPED Heart & Infinity Sketch
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Wedding Invitation &mdash; Pavan Kumar &amp; Aishwarya</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Great+Vibes&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    @page {{
      size: A4 portrait;
      margin: 0;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    html, body {{
      width: 100%;
      height: 100%;
      background-color: #FAF5ED;
      color: #2D080E;
      font-family: 'Plus Jakarta Sans', sans-serif;
      -webkit-font-smoothing: antialiased;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    .page-wrapper {{
      width: 100%;
      min-height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 20px;
    }}
    .border-frame {{
      width: 860px;
      border: 3.5px solid #845E16;
      padding: 5px;
      position: relative;
      background: #FAF5ED;
      box-shadow: 0 10px 30px rgba(74, 14, 23, 0.1);
    }}
    .border-inner {{
      border: 1.5px solid #D4AF37;
      padding: 22px 28px 18px 28px;
      position: relative;
      background: #FDFBF7;
      background-image: radial-gradient(rgba(212, 175, 55, 0.09) 1.2px, transparent 0);
      background-size: 22px 22px;
    }}
    /* Corner Ornaments */
    .corner-tl, .corner-tr, .corner-bl, .corner-br {{
      position: absolute;
      width: 38px;
      height: 38px;
      pointer-events: none;
    }}
    .corner-tl {{ top: 5px; left: 5px; border-top: 3px solid #D4AF37; border-left: 3px solid #D4AF37; }}
    .corner-tr {{ top: 5px; right: 5px; border-top: 3px solid #D4AF37; border-right: 3px solid #D4AF37; }}
    .corner-bl {{ bottom: 5px; left: 5px; border-bottom: 3px solid #D4AF37; border-left: 3px solid #D4AF37; }}
    .corner-br {{ bottom: 5px; right: 5px; border-bottom: 3px solid #D4AF37; border-right: 3px solid #D4AF37; }}

    .center {{ text-align: center; }}
    
    .emblem-box {{
      margin-bottom: 3px;
      text-align: center;
    }}
    .blessing-tag {{
      color: #845E16;
      font-size: 12.5px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      margin-bottom: 3px;
    }}
    .invitation-badge {{
      display: inline-block;
      color: #4A0E17;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 5px;
      text-transform: uppercase;
      padding: 2px 18px;
      border-top: 1.5px solid #D4AF37;
      border-bottom: 1.5px solid #D4AF37;
      margin-bottom: 8px;
    }}
    .invitation-line {{
      font-family: 'Playfair Display', serif;
      font-size: 14px;
      color: #5C1521;
      font-style: italic;
      line-height: 1.45;
      margin-bottom: 8px;
    }}
    .couple-title {{
      font-family: 'Cinzel', serif;
      font-size: 36px;
      font-weight: 800;
      color: #4A0E17;
      letter-spacing: 1.5px;
      line-height: 1.1;
      margin-bottom: 2px;
    }}
    .ampersand {{
      font-family: 'Great Vibes', cursive;
      font-size: 40px;
      color: #C59B27;
      font-weight: 400;
      vertical-align: middle;
      margin: 0 8px;
    }}
    
    /* Couple Section - UNMASKED FULL HEART & INFINITY ARTWORK */
    .couple-section {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 16px;
      margin: 12px 0 14px 0;
    }}
    .person-card {{
      flex: 1;
      background: #FFFFFF;
      border: 1.5px solid #EEDDAF;
      border-radius: 14px;
      padding: 14px 16px;
      text-align: center;
      box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }}
    .person-role {{
      display: inline-block;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: #845E16;
      background: #FAF0D6;
      padding: 2.5px 12px;
      border-radius: 20px;
      margin-bottom: 6px;
    }}
    .person-name {{
      font-family: 'Cinzel', serif;
      font-size: 21px;
      font-weight: 800;
      color: #4A0E17;
      margin-bottom: 5px;
    }}
    .parents-line {{
      font-size: 12.5px;
      color: #444;
      line-height: 1.45;
    }}
    .parents-names {{
      font-weight: 700;
      color: #1A0508;
    }}

    /* Full Uncropped Heart & Infinity Medallion */
    .artwork-card {{
      width: 205px;
      flex-shrink: 0;
      background: #FFFFFF;
      border: 1.5px solid #D4AF37;
      border-radius: 16px;
      padding: 8px 10px 8px 10px;
      text-align: center;
      box-shadow: 0 4px 14px rgba(132, 94, 22, 0.15);
      position: relative;
    }}
    .artwork-img {{
      width: 100%;
      height: auto;
      max-height: 175px;
      object-fit: contain;
      display: block;
      margin: 0 auto;
      border-radius: 8px;
    }}
    .tagline {{
      font-family: 'Great Vibes', cursive;
      font-size: 16px;
      color: #845E16;
      margin-top: 4px;
      line-height: 1.2;
    }}

    /* Gold Ornate Divider */
    .divider {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
      margin: 10px 0;
      color: #D4AF37;
      font-size: 14px;
    }}
    .divider::before, .divider::after {{
      content: "";
      height: 1px;
      width: 100px;
      background: linear-gradient(to right, transparent, #D4AF37);
    }}
    .divider::after {{
      background: linear-gradient(to left, transparent, #D4AF37);
    }}

    /* Events Section */
    .events-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin-bottom: 12px;
    }}
    .event-card {{
      background: #FFFFFF;
      border: 1.5px solid #D4AF37;
      border-radius: 12px;
      padding: 12px 16px;
      position: relative;
      overflow: hidden;
      box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }}
    .event-card.reception {{
      border-left: 5px solid #720026;
    }}
    .event-card.muhurtham {{
      border-left: 5px solid #C59B27;
      background: #FFFDF9;
    }}
    .event-badge {{
      display: inline-block;
      font-size: 9.5px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      padding: 2px 8px;
      border-radius: 4px;
      margin-bottom: 4px;
    }}
    .reception-badge {{ background: #FDE8EC; color: #720026; }}
    .muhurtham-badge {{ background: #FAF0D6; color: #845E16; }}
    .event-title {{
      font-family: 'Cinzel', serif;
      font-size: 17px;
      font-weight: 800;
      color: #4A0E17;
      margin-bottom: 3px;
    }}
    .event-datetime {{
      font-size: 12.5px;
      font-weight: 700;
      color: #845E16;
      margin-bottom: 4px;
    }}
    .event-desc {{
      font-size: 11.5px;
      color: #555;
      line-height: 1.45;
    }}

    /* Venue & Map Section */
    .venue-map-container {{
      background: #FFFFFF;
      border: 2px solid #845E16;
      border-radius: 14px;
      padding: 13px 18px;
      display: flex;
      align-items: center;
      gap: 18px;
      margin-bottom: 11px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.04);
    }}
    .venue-info {{
      flex: 1;
    }}
    .venue-tag {{
      font-size: 10.5px;
      font-weight: 800;
      letter-spacing: 2px;
      color: #845E16;
      text-transform: uppercase;
      margin-bottom: 3px;
    }}
    .venue-name {{
      font-family: 'Cinzel', serif;
      font-size: 17.5px;
      font-weight: 800;
      color: #4A0E17;
      margin-bottom: 4px;
      line-height: 1.25;
    }}
    .venue-address {{
      font-size: 12px;
      color: #333;
      line-height: 1.45;
      margin-bottom: 4px;
    }}
    .venue-landmark {{
      font-size: 11.5px;
      color: #720026;
      font-weight: 600;
    }}

    .qr-side {{
      flex-shrink: 0;
      text-align: center;
      background: #FAF6EF;
      border: 1.5px dashed #C59B27;
      border-radius: 10px;
      padding: 7px 12px;
      width: 195px;
    }}
    .qr-img {{
      width: 108px;
      height: 108px;
      display: block;
      margin: 0 auto 5px auto;
      border: 2px solid #FFFFFF;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}
    .qr-label {{
      font-size: 10px;
      font-weight: 800;
      color: #4A0E17;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      line-height: 1.2;
    }}
    .qr-help {{
      font-size: 9px;
      color: #666;
      margin: 2px 0 1px 0;
      line-height: 1.2;
    }}
    .qr-link {{
      font-size: 8px;
      font-weight: 600;
      color: #845E16;
      display: block;
    }}

    /* Compliments Footer - Formal Dignified Typography (No Pill/Badge) */
    .footer-section {{
      text-align: center;
      padding-top: 4px;
    }}
    .compliments-title {{
      font-family: 'Playfair Display', serif;
      font-size: 13.5px;
      font-style: italic;
      color: #845E16;
      letter-spacing: 0.5px;
      margin-bottom: 2px;
    }}
    .compliments-name {{
      font-family: 'Cinzel', serif;
      font-size: 17px;
      font-weight: 800;
      color: #4A0E17;
      letter-spacing: 2px;
      text-transform: uppercase;
      margin-bottom: 5px;
    }}
    .site-note {{
      font-size: 9.5px;
      color: #845E16;
      font-family: monospace;
    }}

    /* PRINT SPECIFIC STYLING - PERFECT SINGLE PAGE A4 */
    @media print {{
      html, body {{
        width: 210mm !important;
        height: 297mm !important;
        margin: 0 !important;
        padding: 0 !important;
        background: #FAF5ED !important;
      }}
      .page-wrapper {{
        padding: 8mm !important;
        min-height: 0 !important;
        height: 297mm !important;
        box-sizing: border-box !important;
      }}
      .border-frame {{
        width: 194mm !important;
        box-shadow: none !important;
      }}
      .border-inner {{
        padding: 18px 22px 14px 22px !important;
      }}
    }}
  </style>
</head>
<body>

<div class="page-wrapper">
  <div class="border-frame" id="wedding-card">
    <div class="border-inner">
      <!-- Golden Corners -->
      <div class="corner-tl"></div>
      <div class="corner-tr"></div>
      <div class="corner-bl"></div>
      <div class="corner-br"></div>

      <!-- Top Auspicious Invocations (English) -->
      <div class="center">
        <div class="emblem-box">
          {emblem_svg}
        </div>
        <div class="blessing-tag">&#10022; With the Divine Blessings of God &amp; Elders &#10022;</div>
        <div class="invitation-badge">&#10022; Wedding Invitation &#10022;</div>
        
        <p class="invitation-line">
          Together with our beloved parents, we cordially invite you and your family<br>
          to grace the auspicious wedding ceremony of
        </p>

        <!-- Couple Name -->
        <h1 class="couple-title">
          Pavan Kumar <span class="ampersand">&amp;</span> Aishwarya
        </h1>
      </div>

      <!-- Couple Photo & Family Cards - FULL UNCROPPED ARTWORK -->
      <div class="couple-section">
        <!-- Groom Card -->
        <div class="person-card">
          <span class="person-role">The Groom</span>
          <div class="person-name">Pavan Kumar</div>
          <div class="parents-line">
            Son of<br>
            <span class="parents-names">Mr. V. Elango</span><br>
            &amp; <span class="parents-names">Mrs. E. Dhanalakshmi</span>
          </div>
        </div>

        <!-- Center Full Heart & Infinity Artwork (Uncropped) -->
        <div class="artwork-card">
          <img src="data:image/jpeg;base64,{couple_b64}" class="artwork-img" alt="Pavan Kumar &amp; Aishwarya">
          <div class="tagline">Two Hearts &bull; One Soul</div>
        </div>

        <!-- Bride Card -->
        <div class="person-card">
          <span class="person-role">The Bride</span>
          <div class="person-name">Aishwarya</div>
          <div class="parents-line">
            Daughter of<br>
            <span class="parents-names">Mr. K. Babu</span><br>
            &amp; <span class="parents-names">Mrs. K. Latha</span>
          </div>
        </div>
      </div>

      <!-- Gold Divider -->
      <div class="divider">&#10047;</div>

      <!-- Events Schedule -->
      <div class="events-grid">
        <!-- Reception -->
        <div class="event-card reception">
          <span class="event-badge reception-badge">Evening Celebration</span>
          <div class="event-title">Wedding Reception</div>
          <div class="event-datetime">Sunday, December 13, 2026 &bull; 6:30 PM Onwards</div>
          <div class="event-desc">
            Musical evening, stage greetings with Pavan Kumar &amp; Aishwarya, followed by a grand wedding dinner feast.
          </div>
        </div>

        <!-- Muhurtham -->
        <div class="event-card muhurtham">
          <span class="event-badge muhurtham-badge">Sacred Muhurtham</span>
          <div class="event-title">Marriage Ceremony</div>
          <div class="event-datetime">Monday, December 14, 2026 &bull; 4:30 AM &ndash; 6:00 AM IST</div>
          <div class="event-desc">
            Auspicious marriage rites and sacred Mangalya Dharanam solemnising the holy union.
          </div>
        </div>
      </div>

      <!-- Venue & Map QR Section -->
      <div class="venue-map-container">
        <div class="venue-info">
          <div class="venue-tag">&#10022; Wedding Venue &amp; Mandapam &#10022;</div>
          <div class="venue-name">Arulmigu Bala Murugan Temple A/C Mandapam</div>
          <div class="venue-address">
            Ratnagiri, Kilminnal, Vellore District, Tamil Nadu &ndash; 632517
          </div>
          <div class="venue-landmark">
            &#9679; Landmark: Near Ratnagiri Murugan Temple / Bangalore-Chennai Highway (NH 48)
          </div>
        </div>

        <!-- Scannable Map QR Code -->
        <div class="qr-side">
          <img src="data:image/png;base64,{qr_b64}" class="qr-img" alt="Google Maps QR Code">
          <div class="qr-label">Scan For Location</div>
          <div class="qr-help">Open camera for Google Maps GPS</div>
          <span class="qr-link">maps.app.goo.gl/j1HJmygQAsjiv335A</span>
        </div>
      </div>

      <!-- Compliments Footer -->
      <div class="footer-section">
        <div class="compliments-title">With Best Compliments From</div>
        <div class="compliments-name">Pradeep Kumar E</div>
        <div class="site-note">
          Digital Invitation: pavanaishwayaweddinginvitation.onrender.com
        </div>
      </div>

    </div>
  </div>
</div>

</body>
</html>"""

    html_path = os.path.join(base_dir, "invitation_card.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML invitation card written: {html_path}")

    # 3. Render PDF using Chrome Headless
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    file_url = "file:///" + html_path.replace("\\", "/")

    pdf_out = os.path.join(downloads_dir, "Pavan_Aishwarya_Wedding_Invitation.pdf")
    cmd_pdf = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=6000",
        f"--print-to-pdf={pdf_out}",
        "--no-pdf-header-footer",
        file_url
    ]
    print("Generating PDF...")
    subprocess.run(cmd_pdf, check=True)
    
    # Check page count
    pdf_pages = pdf2image.convert_from_path(pdf_out)
    print(f"PDF generated: {pdf_out} ({os.path.getsize(pdf_out):,} bytes, Page count: {len(pdf_pages)})")

    # 4. Render High-Resolution Raw Image
    raw_png = os.path.join(downloads_dir, "raw_card.png")
    cmd_img = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--window-size=1000,1600",
        "--device-scale-factor=2",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=6000",
        f"--screenshot={raw_png}",
        file_url
    ]
    print("Generating high-res PNG...")
    subprocess.run(cmd_img, check=True)

    # 5. Crop precisely to the card border with uniform 40px margin
    with Image.open(raw_png) as im:
        rgb = im.convert("RGB")
        w, h = rgb.size
        bg_col = rgb.getpixel((10, 10))
        
        arr = np.array(rgb)
        diff = np.abs(arr.astype(int) - np.array(bg_col)).sum(axis=2)
        non_bg = np.where(diff > 25)
        if len(non_bg[0]) > 0:
            min_y = int(non_bg[0].min())
            max_y = int(non_bg[0].max())
            min_x = int(non_bg[1].min())
            max_x = int(non_bg[1].max())

        padding = 40
        crop_x0 = max(0, min_x - padding)
        crop_y0 = max(0, min_y - padding)
        crop_x1 = min(w, max_x + padding)
        crop_y1 = min(h, max_y + padding)

        cropped = rgb.crop((crop_x0, crop_y0, crop_x1, crop_y1))
        
        png_out = os.path.join(downloads_dir, "Pavan_Aishwarya_Wedding_Invitation.png")
        jpg_out = os.path.join(downloads_dir, "Pavan_Aishwarya_Wedding_Invitation.jpg")
        
        cropped.save(png_out, "PNG", optimize=True)
        cropped.save(jpg_out, "JPEG", quality=96, optimize=True)
        print(f"Final PNG saved: {png_out} (size: {cropped.size})")
        print(f"Final JPG saved: {jpg_out} (size: {cropped.size})")

    if os.path.exists(raw_png):
        os.remove(raw_png)

    # 6. Copy files to artifact directory for clickable direct links
    for src in [pdf_out, png_out, jpg_out, qr_path]:
        filename = os.path.basename(src)
        dst = os.path.join(artifact_dir, filename)
        shutil.copy2(src, dst)
        print(f"Copied to artifact dir: {dst}")

    print("\nALL INVITATION ASSETS SUCCESSFULLY GENERATED!")

if __name__ == "__main__":
    main()
