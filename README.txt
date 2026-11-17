Evermore — Free Wedding Invitation Website Template by uiCookies
https://uicookies.com/

Evermore is a free wedding invitation website template built on Bootstrap 5,
styled like a letterpress stationery suite: ink-navy type on cotton paper, a
deckled invitation card, gold-foil accents, Bodoni Moda headings and Hanken
Grotesk body text. It opens with an envelope intro (press the wax seal, the flap
lifts and the card slides out) that can be skipped and never plays under
prefers-reduced-motion. The invitation page carries formal wording, a countdown,
the couple's story, ceremony and reception cards, the order of the day, an
illustrated venue map with directions, accommodation, dress code, registry, FAQ
and an RSVP call to action. The RSVP page is a reply card with conditional
plus-one fields, a three-course menu choice, validation and a success state with
a save-to-calendar (.ics) link. Everything is plain vanilla JavaScript, no jQuery.
Free for personal and commercial use. Attribution is optional but always welcome — https://uicookies.com/license/

WHAT'S INSIDE
  index.html            The invitation: wording, countdown, story, ceremony and
                        reception, order of the day, venue map, stay, dress
                        code, registry, FAQ, RSVP call to action
  rsvp.html             Reply card: guest details, accept/decline, plus-one,
                        three-course menu, dietary needs, note to the couple
  css/vendor/           Bootstrap 5.3.8 (minified, self-hosted)
  css/style.css         Design layer: palette, type, paper texture, foil, components
  js/vendor/            Bootstrap 5.3.8 bundle (used for the mobile menu)
  js/main.js            Template behaviour — vanilla JavaScript, no jQuery
  img/                  Demo photographs (public domain, see CREDITS.txt)
  CREDITS.txt           Provenance of every demo image

NOTES
  - Built on Bootstrap 5.3.8. No jQuery, no plugins, inline SVG icons only.
  - Colours, fonts and textures are CSS custom properties at the top of
    css/style.css. The paper grain is an inline SVG, so there is no texture file.
  - The wedding date, venue and calendar text live in the EVENT object at the
    top of js/main.js; the countdown reads data-countdown in index.html.
  - The envelope intro plays once per visit. It is skipped under
    prefers-reduced-motion, for automated screenshot tools and when a visitor
    arrives at a #section link. Add ?intro to the URL to watch it again, or
    delete the #envelopeIntro block in index.html to remove it.
  - The RSVP form is front-end only: it validates in the browser and shows a
    success state. Point the form at a form service or your own backend to
    receive replies.
  - The venue map is an inline SVG illustration; edit its labels and pins in
    index.html. There are no external map embeds.
  - couple.jpg ships as a plain placeholder; replace it with your own photo.
    Replace the other demo images in img/ before launch too.
  - All content is visible without JavaScript; animations are progressive
    enhancements and respect prefers-reduced-motion.
