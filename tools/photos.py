"""Placeholder photos (free Unsplash licence, hotlinked from images.unsplash.com). Credits: CREDITS.md."""
import re

PHOTOS = [
 {
  "slug": "pool-water-ripples",
  "image_url": "https://images.unsplash.com/photo-1562016600-ece13e8ba570",
  "page_url": "https://unsplash.com/photos/rippling-crystal-blue-water-9-OCsKoyQlk",
  "photographer": "Wesley Tingey",
  "photographer_url": "https://unsplash.com/@wesleyphotography",
  "description": "Full-frame texture of clear turquoise pool water with sunlit caustic ripples.",
  "faces": "none",
  "keywords": "water texture ripple archive vintage calm"
 },
 {
  "slug": "lane-lines-pool-floor",
  "image_url": "https://images.unsplash.com/photo-1558617320-e695f0d420de",
  "page_url": "https://unsplash.com/photos/swimming-pool-close-up-photography-QGdRrty4054",
  "photographer": "Thomas Park",
  "photographer_url": "https://unsplash.com/@thomascpark",
  "description": "Close-up of dark lane lines on a blue tiled pool floor seen through the water.",
  "faces": "none",
  "keywords": "lane lines pool floor scoreboard clock pace"
 },
 {
  "slug": "indoor-pool-lane-ropes",
  "image_url": "https://images.unsplash.com/photo-1576610616656-d3aa5d1f4534",
  "page_url": "https://unsplash.com/photos/blue-olympic-pool-n2v3lTWy74Y",
  "photographer": "Marcelo Uva",
  "photographer_url": "https://unsplash.com/@marcelouva",
  "description": "Empty indoor competition pool viewed down the lanes from the end wall, red and blue lane ropes.",
  "faces": "none",
  "keywords": "empty pool lanes lane ropes ernest bevin no people session venue balcony wide"
 },
 {
  "slug": "pool-edge-ladder",
  "image_url": "https://images.unsplash.com/photo-1557459325-b6733cbeae9c",
  "page_url": "https://unsplash.com/photos/blue-swimming-pool-vy_cVJCAVG0",
  "photographer": "Thom Milkovic",
  "photographer_url": "https://unsplash.com/@thommilkovic",
  "description": "Corner of an empty pool with steel ladder, depth markings and bright turquoise water.",
  "faces": "none",
  "keywords": "empty pool edge ladder shallow end wall"
 },
 {
  "slug": "indoor-pool-timber-roof",
  "image_url": "https://images.unsplash.com/photo-1730244548329-4ae2f4fcaa7c",
  "page_url": "https://unsplash.com/photos/an-indoor-swimming-pool-with-blue-water-xs9r8fPUats",
  "photographer": "Mariusz Smenzyk",
  "photographer_url": "https://unsplash.com/@msmenzyk",
  "description": "Wide shot of an empty indoor lane pool with timber roof, lane ropes and backstroke flags (landscape).",
  "faces": "none",
  "keywords": "indoor pool wide stands gala venue no people session"
 },
 {
  "slug": "outdoor-pool-empty-lanes",
  "image_url": "https://images.unsplash.com/photo-1775993167757-f919582c62da",
  "page_url": "https://unsplash.com/photos/an-empty-outdoor-swimming-pool-with-lane-markers-E3ZDdKuQh1M",
  "photographer": "Palak Pitroda",
  "photographer_url": "https://unsplash.com/@palak_pitroda",
  "description": "Empty outdoor lane pool with marked lanes, hedges and a large building behind (landscape).",
  "faces": "none",
  "keywords": "pool lanes from above empty venue"
 },
 {
  "slug": "outdoor-pool-blocks-bunting",
  "image_url": "https://images.unsplash.com/photo-1772519275437-3029ac1d3941",
  "page_url": "https://unsplash.com/photos/outdoor-swimming-pool-with-lanes-and-diving-blocks-LVn0HMq1Pcg",
  "photographer": "Alea Long",
  "photographer_url": "https://unsplash.com/@along27",
  "description": "Outdoor 50m-style pool under grey sky with a row of starting blocks, lane ropes and backstroke flags.",
  "faces": "none",
  "keywords": "blocks start starting heat diving gala race meet"
 },
 {
  "slug": "indoor-pool-natural-light",
  "image_url": "https://images.unsplash.com/photo-1782958995190-75701221aab4",
  "page_url": "https://unsplash.com/photos/modern-indoor-swimming-pool-with-lanes-and-natural-light-7D9d-2hnOho",
  "photographer": "Andy Wang",
  "photographer_url": "https://unsplash.com/@space_launch_system",
  "description": "Calm, empty modern indoor lane pool with warm ceiling lights and windows along the far side.",
  "faces": "none",
  "keywords": "calm empty indoor pool poolside kit bench"
 },
 {
  "slug": "butterfly-lane-from-above",
  "image_url": "https://images.unsplash.com/photo-1560089000-7433a4ebbd64",
  "page_url": "https://unsplash.com/photos/person-on-swimming-pool-hawN8XnaJuY",
  "photographer": "Serena Repice Lentini",
  "photographer_url": "https://unsplash.com/@serenarepice",
  "description": "Swimmer in a blue cap doing butterfly between lane ropes, shot from above and behind.",
  "faces": "none (head down)",
  "keywords": "squad training lane swimmer mid-race above butterfly"
 },
 {
  "slug": "freestyle-breathing-lane",
  "image_url": "https://images.unsplash.com/photo-1560088937-d46f082d558b",
  "page_url": "https://unsplash.com/photos/man-swimming-in-competition-q4tScOAuIm8",
  "photographer": "Serena Repice Lentini",
  "photographer_url": "https://unsplash.com/@serenarepice",
  "description": "Adult swimmer in cap and goggles mid-freestyle stroke in an outdoor lane, splash-heavy.",
  "faces": "partial side profile under cap and goggles, not identifiable",
  "keywords": "adult swimmer mid-stroke freestyle masters triathlon"
 },
 {
  "slug": "underwater-glide-from-above",
  "image_url": "https://images.unsplash.com/photo-1530138948699-6a75eebc9d9b",
  "page_url": "https://unsplash.com/photos/man-doing-swimming-ZmZEkO-pb7M",
  "photographer": "Richard R. Schünemann",
  "photographer_url": "https://unsplash.com/@richardrschunemann",
  "description": "Overhead view of a swimmer gliding underwater along a lane between lane ropes (landscape).",
  "faces": "none",
  "keywords": "glide underwater above young swimmer streamline academy"
 },
 {
  "slug": "race-dive-entries-overhead",
  "image_url": "https://images.unsplash.com/photo-1560090947-5307abc46ffc",
  "page_url": "https://unsplash.com/photos/swimming-competition-during-daytime-Ue24S2JU81k",
  "photographer": "Serena Repice Lentini",
  "photographer_url": "https://unsplash.com/@serenarepice",
  "description": "Overhead shot of a row of swimmers entering the water from a racing start, legs and splashes across red lane ropes.",
  "faces": "none",
  "keywords": "diving blocks race start dive competition heat gala swimmers"
 },
 {
  "slug": "freestyle-head-down-reflection",
  "image_url": "https://images.unsplash.com/photo-1593055497705-59a84c5928b2",
  "page_url": "https://unsplash.com/photos/person-in-water-during-daytime-F20aPGvyhrQ",
  "photographer": "Talahria Jensen",
  "photographer_url": "https://unsplash.com/@talahria_rose",
  "description": "Freestyle swimmer seen head-on from water level, arm recovering, reflection over the black lane line.",
  "faces": "none (top of head only)",
  "keywords": "swimmer stroke technique coach freestyle"
 },
 {
  "slug": "underwater-fins",
  "image_url": "https://images.unsplash.com/photo-1566356767553-e118792cae7f",
  "page_url": "https://unsplash.com/photos/under-water-photography-of-man-wearing-blue-flippers-X8RgOcqugtQ",
  "photographer": "Dylan Alcock",
  "photographer_url": "https://unsplash.com/@dylan_alcock",
  "description": "Underwater view of a swimmer's body and legs wearing long blue fins in deep blue water.",
  "faces": "none (head above frame)",
  "keywords": "underwater fins training kit"
 },
 {
  "slug": "backstroke-lane",
  "image_url": "https://images.unsplash.com/photo-1519315901367-f34ff9154487",
  "page_url": "https://unsplash.com/photos/person-swimming-on-an-olympic-pool-ZbbhkQ0M2AM",
  "photographer": "Marcus Ng",
  "photographer_url": "https://unsplash.com/@marcusxsnapz",
  "description": "Swimmer doing backstroke in a lane between blue and orange lane ropes (landscape).",
  "faces": "small side view with goggles, effectively not identifiable",
  "keywords": "backstroke lane swimmer flags"
 },
 {
  "slug": "lap-swimmers-aerial",
  "image_url": "https://images.unsplash.com/photo-1544698203-58ceea4b787b",
  "page_url": "https://unsplash.com/photos/three-men-swimming-in-swimming-pool-NHmWnOt2nsM",
  "photographer": "Fiona Smallwood",
  "photographer_url": "https://unsplash.com/@mrsfionasmallwood",
  "description": "High-angle view of three adult men swimming laps in adjacent lanes of a green-tinted outdoor pool.",
  "faces": "none",
  "keywords": "adult swimmers lanes masters lap fitness from above"
 },
 {
  "slug": "lap-swimmers-multiple-lanes",
  "image_url": "https://images.unsplash.com/photo-1560088939-ddaf4d3e0d0b",
  "page_url": "https://unsplash.com/photos/three-person-swimming-on-pool-9rwxZcJPdpI",
  "photographer": "Serena Repice Lentini",
  "photographer_url": "https://unsplash.com/@serenarepice",
  "description": "Several swimmers doing freestyle across many coloured lane ropes, distant elevated view.",
  "faces": "none",
  "keywords": "squad session lanes busy group swimmers walking together relay celebrating"
 },
 {
  "slug": "breaststroke-from-behind",
  "image_url": "https://images.unsplash.com/photo-1560088939-a88259febdce",
  "page_url": "https://unsplash.com/photos/woman-swimming-TU18VGBB9W4",
  "photographer": "Serena Repice Lentini",
  "photographer_url": "https://unsplash.com/@serenarepice",
  "description": "Adult woman in white cap and red suit swimming breaststroke in a lane, seen from behind.",
  "faces": "none",
  "keywords": "adult breaststroke returner woman behind"
 },
 {
  "slug": "kickboard-poolside",
  "image_url": "https://images.unsplash.com/photo-1752910179995-9d269ebe253c",
  "page_url": "https://unsplash.com/photos/a-yellow-kickboard-sits-beside-a-pool-nFA4T1M40Iw",
  "photographer": "rizal mustiko adji",
  "photographer_url": "https://unsplash.com/@studioduabelas",
  "description": "Yellow kickboard lying on the pool edge beside blue tiled water, top-down (landscape).",
  "faces": "none",
  "keywords": "kickboard float kicking academy young teaching group lesson"
 },
 {
  "slug": "goggles-poolside-sunset",
  "image_url": "https://images.unsplash.com/photo-1533060629428-48484ce98a74",
  "page_url": "https://unsplash.com/photos/black-goggles-on-dock-zEO9BGCNbhE",
  "photographer": "Akshat Jain",
  "photographer_url": "https://unsplash.com/@akshat_worldwide",
  "description": "Black swim goggles on a wet pool edge at sunset, palm trees and a blurred person in the water behind.",
  "faces": "none identifiable (background figure is out of focus, back turned)",
  "keywords": "goggles caps bench poolside phone"
 },
 {
  "slug": "starting-block-lane-8",
  "image_url": "https://images.unsplash.com/photo-1543168449-582b8edc70a6",
  "page_url": "https://unsplash.com/photos/number-8-on-pool-miUKObXBpA0",
  "photographer": "Markus Spiske",
  "photographer_url": "https://unsplash.com/@markusspiske",
  "description": "Close-up of a starting block with backstroke handle and large '8', tiled pool behind, cool-toned (landscape).",
  "faces": "none",
  "keywords": "starting block blocks on the blocks number cap"
 },
 {
  "slug": "open-water-swimmer-sunset",
  "image_url": "https://images.unsplash.com/photo-1578253734010-32bb761af7e3",
  "page_url": "https://unsplash.com/photos/person-swimming-on-body-of-water-HuXaTzMDNWc",
  "photographer": "Dallas Morgan",
  "photographer_url": "https://unsplash.com/@bondibarrister",
  "description": "Open-water swimmer in the sea at sunrise/sunset, arm raised mid-stroke at water level (landscape).",
  "faces": "none (silhouette)",
  "keywords": "open water triathlon university beyond outdoor"
 },
 {
  "slug": "strength-dumbbells-band",
  "image_url": "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2",
  "page_url": "https://unsplash.com/photos/dumbbells-and-resistance-band-workout-IZOAOjvwhaM",
  "photographer": "Kelly Sikkema",
  "photographer_url": "https://unsplash.com/@kellysikkema",
  "description": "Two black dumbbells and an orange resistance band with handles on rustic wood, top-down (landscape).",
  "faces": "none",
  "keywords": "s&c gym strength conditioning bands medicine resistance land"
 },
 {
  "slug": "fins-poolside",
  "image_url": "https://images.unsplash.com/photo-1683885667028-1b2a91820d16",
  "page_url": "https://unsplash.com/photos/a-pair-of-black-flippers-sitting-next-to-a-swimming-pool-6dbhNuWa5oI",
  "photographer": "Kajetan Sumila",
  "photographer_url": "https://unsplash.com/@kajtek",
  "description": "Black training fins and a blue float on the edge of an outdoor lane pool with bunting behind (portrait).",
  "faces": "none",
  "keywords": "kit flat lay fins pull buoy training equipment"
 },
 {
  "slug": "goggles-pink-towel",
  "image_url": "https://images.unsplash.com/photo-1747494749148-c3f5018799c2",
  "page_url": "https://unsplash.com/photos/swimming-goggles-rest-on-a-pink-towel-_BMp61GG7SY",
  "photographer": "Andrea Stuart",
  "photographer_url": "https://unsplash.com/@andreastuart",
  "description": "Clear swim goggles resting on a pink towel on wooden slats (portrait).",
  "faces": "none",
  "keywords": "towel kit goggles hat costume bag cap"
 }
]


def pick_photo(desc, used, n):
    """Choose the photo whose keywords best match a [PHOTO: ...] brief, avoiding repeats on a page."""
    words = set(re.findall(r"[a-z&]+", desc.lower()))
    best, best_score = None, -1
    for i, p in enumerate(PHOTOS):
        kws = p["keywords"].split()
        score = sum(2 for k in kws if k in words) + sum(1 for k in kws if any(w.startswith(k[:5]) for w in words if len(k) > 4))
        if p["slug"] in used:
            score -= 100
        score += ((i * 7 + n * 3) % len(PHOTOS)) / 1000.0  # stable tie-break
        if score > best_score:
            best, best_score = p, score
    return best
