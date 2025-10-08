#!/bin/bash
cd rail-assets/images

# Download SVGs
curl -s -o check-circle.svg "https://cdn.prod.website-files.com/62434fa732124a0fb112aab4/62434fa732124a700a12aad4_check%20circle.svg"
curl -s -o preview-image.svg "https://cdn.prod.website-files.com/67804fa80e81c597eb4f59ac/678806b3a3c94c82025919fc_Preview%20image.svg"
curl -s -o logo.svg "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de07_Logo.svg"
curl -s -o footer.svg "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de13_Footer.svg"
curl -s -o rail.svg "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de14_rail.svg"
curl -s -o map.svg "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de15_Frame%201828.svg"
curl -s -o indicator-1.svg "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de16_67804fa80e81c597eb4f5a08_Group%201669%201.svg"
curl -s -o testimonial-bg.svg "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de17_Testamonial%20background.svg"
curl -s -o scroll-bg.svg "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de20_Scroll%20background.svg"
curl -s -o indicator-2.svg "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de26_67804fa80e81c597eb4f59f5_Vector%205%201.svg"
curl -s -o webclip.svg "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de30_webclip.svg"
curl -s -o favicon.svg "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de31_Favicon.svg"
curl -s -o map-mobile.svg "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/686bed9bdd70955a9921e84f_Map_mobile.svg"

# Download PNGs
curl -s -o mask-group-4.png "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44ddff_Mask%20group-4.png"
curl -s -o mask-group-5.png "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de01_Mask%20group-5.png"
curl -s -o mask-group-1.png "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de02_Mask%20group-1.png"
curl -s -o mask-group.png "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de03_Mask%20group.png"
curl -s -o mask-group-3.png "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de04_Mask%20group-3.png"
curl -s -o m-scroll-bg.png "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de36_m.%20Scroll%20background.png"
curl -s -o m-scroll-bg-blank.png "https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de39_m.%20Scroll%20background_blank.png"

# Download video poster images
curl -s -o video1-poster.jpg "https://cdn.prod.website-files.com/67804fa80e81c597eb4f59ac%2F67917ac8f5c215b9e436c24a_rail%20video%201-poster-00001.jpg"
curl -s -o video2-poster.jpg "https://cdn.prod.website-files.com/67804fa80e81c597eb4f59ac%2F67917adff66792c665b8c1a9_rail%20video%202-poster-00001.jpg"
curl -s -o video3-poster.jpg "https://cdn.prod.website-files.com/67804fa80e81c597eb4f59ac%2F67917ae8f7c29db00d3801a8_rail%20video%203-poster-00001.jpg"

echo "Downloaded images"
ls -lh | wc -l
