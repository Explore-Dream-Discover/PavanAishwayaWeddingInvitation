from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np

# Canvas size
W, H = 1000, 950

# Let's create an SVG string for the heart + infinity frame and clip path
svg_template = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 950" width="1000" height="950">
  <defs>
    <!-- Rich 3D Gold Gradient for Frame -->
    <linearGradient id="goldMetallic" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FAF0CD"/>
      <stop offset="20%" stop-color="#D4AF37"/>
      <stop offset="40%" stop-color="#FDF3CD"/>
      <stop offset="60%" stop-color="#AA7C11"/>
      <stop offset="80%" stop-color="#E5C158"/>
      <stop offset="100%" stop-color="#845D08"/>
    </linearGradient>

    <linearGradient id="goldShine" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#997010"/>
      <stop offset="50%" stop-color="#FFE89E"/>
      <stop offset="100%" stop-color="#7D5705"/>
    </linearGradient>

    <!-- Drop Shadow Filter -->
    <filter id="frameShadow" x="-10%" y="-10%" width="130%" height="130%">
      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#32060C" flood-opacity="0.25"/>
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.15"/>
    </filter>

    <!-- Heart Clip for Image -->
    <clipPath id="heartPhotoClip">
      <!-- Heart path matching the inner opening -->
      <path d="M 500,240 
               C 440,110 230,100 170,260 
               C 120,390 280,560 500,690 
               C 720,560 880,390 830,260 
               C 770,100 560,110 500,240 Z" />
    </clipPath>
  </defs>

  <g filter="url(#frameShadow)">
    <!-- Photo inside Heart -->
    <g clip-path="url(#heartPhotoClip)">
      <image href="/static/images/couple_portrait.jpg" 
             x="70" y="110" width="860" height="600" 
             preserveAspectRatio="xMidYMid slice" />
      <!-- Subtle warm glow around edges -->
      <path d="M 500,240 
               C 440,110 230,100 170,260 
               C 120,390 280,560 500,690 
               C 720,560 880,390 830,260 
               C 770,100 560,110 500,240 Z" 
            fill="none" stroke="rgba(212,175,55,0.3)" stroke-width="12" />
    </g>

    <!-- Frame Outline (Heart + Infinity) -->
    <!-- Heart Frame Outer Stroke -->
    <path d="M 500,230 
             C 435,90 210,80 150,250 
             C 100,390 260,570 480,705
             C 410,720 280,720 200,770
             C 100,830 140,920 250,920
             C 380,920 450,780 500,740
             C 550,780 620,920 750,920
             C 860,920 900,830 800,770
             C 720,720 590,720 520,705
             C 740,570 900,390 850,250
             C 790,80 565,90 500,230 Z" 
          fill="none" stroke="url(#goldMetallic)" stroke-width="28" stroke-linecap="round" stroke-linejoin="round" />

    <!-- Inner Highlight Line for 3D Beveled Look -->
    <path d="M 500,230 
             C 435,90 210,80 150,250 
             C 100,390 260,570 480,705
             C 410,720 280,720 200,770
             C 100,830 140,920 250,920
             C 380,920 450,780 500,740
             C 550,780 620,920 750,920
             C 860,920 900,830 800,770
             C 720,720 590,720 520,705
             C 740,570 900,390 850,250
             C 790,80 565,90 500,230 Z" 
          fill="none" stroke="url(#goldShine)" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" />
  </g>
</svg>
"""

with open("test_frame.svg", "w", encoding="utf-8") as f:
    f.write(svg_template)

print("SVG written to test_frame.svg")
