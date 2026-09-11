"""
Plain Python service data. Edit this file directly and refresh the page,
no management command or database needed while content is still changing
often. When the site's closer to done and JRF wants to edit services
themselves without touching code, this can move back to the Service model
and admin panel — the field names below match that model already, so
migrating later is a straight copy.
"""

SERVICES = [
    {
        "name": "Storm Drainage",
        "slug": "storm-drainage",
        "icon": "storm-drainage",
        "short_description": "Catch basins, culverts, and drainage systems that move water off your site.",
        "image": "images/storm_drainage.jpg",
        "description": (
            "Poor drainage causes more long-term damage to a property than almost anything else, "
            "flooded basements, washed-out grading, cracked foundations. We design and install catch "
            "basins, culverts, and full drainage systems that move water away from your structure and "
            "off the site entirely, rather than letting it pool or find its own way through your "
            "foundation. Every system is sized to the site's actual runoff, not a generic template."
        ),
        "order": 1,
    },
    {
        "name": "Helical Pile Installation",
        "slug": "helical-pile-installation",
        "icon": "helical-pile",
        "short_description": "Deep foundation support for poor soil or tight-access sites.",
        "image": "images/hellical_pipe.JPG",
        "description": (
            "When soil conditions won't support a standard footing, or when equipment access is too "
            "tight for conventional foundation work, helical piles give you a deep, mechanically "
            "anchored foundation without excavating a full footprint. They're installed with minimal "
            "site disturbance and can bear load almost immediately, useful for additions, decks, and "
            "structures on marginal or previously disturbed ground."
        ),
        "order": 2,
    },
    {
        "name": "Demolition",
        "slug": "demolition",
        "icon": "demolition",
        "short_description": "Structure and slab removal, cleared and hauled off site.",
        "image": "images/",
        "description": (
            "From a single slab to a full structure, we handle demolition and complete removal of the "
            "debris, leaving the lot cleared and ready for what's next. That includes coordinating any "
            "utility disconnects beforehand and proper disposal of what comes down, so you're not left "
            "managing a pile of material after the crew leaves."
        ),
        "order": 3,
    },
    {
        "name": "Site Development",
        "slug": "site-development",
        "icon": "site-development",
        "short_description": "Clearing, grading, and utility rough-in for buildable, permitted lots.",
        "image": "images/site_dev.JPG",
        "description": (
            "Turning raw or undeveloped land into a buildable lot means clearing, grading to the "
            "approved plan, and roughing in the utility connections a future structure will need. We "
            "work directly from civil engineering plans and coordinate with permitting requirements, so "
            "the site is genuinely ready for the next trade when we're done, not close."
        ),
        "order": 4,
    },
    {
        "name": "Retaining Walls",
        "slug": "retaining-walls",
        "icon": "retaining-walls",
        "short_description": "Engineered walls built for New England freeze-thaw conditions.",
        "image": "images/retaining_wall.JPG",
        "description": (
            "A retaining wall that isn't built for local frost conditions will heave, crack, or lean "
            "within a few winters. We build walls with proper drainage behind them and footings set "
            "below the frost line, engineered for the load they're actually holding back, whether that's "
            "a small landscape wall or a structural wall supporting a driveway or grade change."
        ),
        "order": 5,
    },
    {
        "name": "Emergency Utility Repair",
        "slug": "emergency-utility-repair",
        "icon": "emergency-repair",
        "short_description": "Round-the-clock response to broken water and sewer lines.",
        "image": "images/eur.JPEG",
        "description": (
            "A broken water main or sewer line doesn't wait for business hours, so neither do we. Our "
            "emergency line is staffed 24/7 for exactly this: locating the break, excavating safely "
            "around existing utilities, and getting the line repaired and backfilled as quickly as the "
            "situation allows."
        ),
        "order": 6,
    },
    {
        "name": "Foundations",
        "slug": "foundations",
        "icon": "foundations",
        "short_description": "Footing and foundation excavation, poured to spec.",
        "image": "images/",
        "description": (
            "Foundation work is the one part of a project everything else depends on, so it's poured "
            "exactly to spec, at the right depth, on properly compacted and inspected subgrade. We "
            "handle the excavation and footing work for new construction and additions alike, "
            "coordinating closely with your structural plans and inspector sign-offs."
        ),
        "order": 7,
    },
    {
        "name": "Water & Sewer Installations",
        "slug": "water-sewer-installations",
        "icon": "water-sewer",
        "short_description": "New service lines installed and tied into municipal systems.",
        "image": "images/ws_pic.JPG",
        "description": (
            "New construction and additions often need new water or sewer service lines run and "
            "properly tied into the municipal system. We handle the excavation, pipe installation, and "
            "the connection work itself, coordinated with the relevant town or city department so "
            "there's no surprise at inspection."
        ),
        "order": 8,
    },
    {
        "name": "Ledge Breaking",
        "slug": "ledge-breaking",
        "icon": "ledge-breaking",
        "short_description": "Hydraulic hammering and rock removal when the site hits ledge.",
        "image": "images/compressed_ledge_breaking.jpg",
        "description": (
            "Hitting ledge partway through an excavation can stall a project fast if the contractor "
            "isn't equipped for it. We bring hydraulic hammering and rock removal equipment to break "
            "through ledge and keep the job moving, whether that's a small footing obstruction or "
            "ledge across a wider excavation."
        ),
        "order": 9,
    },
]


def get_service(slug):
    """Look up a single service dict by slug, or None if it doesn't exist."""
    return next((s for s in SERVICES if s["slug"] == slug), None)