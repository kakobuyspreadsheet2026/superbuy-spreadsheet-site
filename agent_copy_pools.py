"""Large, section-keyed copy pools for unique agent landing pages (used by build_agent_pages.py).

SEO: each agent page should use that agent’s own “{Name} spreadsheet” phrasing—not “kakobuy spreadsheet” on every page.
"""

from __future__ import annotations

import hashlib

# Guide-style SEO year string (bump when you refresh “{year} guide” copy sitewide).
CONTENT_YEAR = "2026"

# Per-platform wording — pools sized to reduce collisions across 25+ slugs.


def _h(s: str) -> int:
    return int(hashlib.md5(s.encode()).hexdigest(), 16)


def intro_agent_spreadsheet_paragraph(slug: str, name: str) -> str:
    """Second intro paragraph: natural use of “{Name} spreadsheet” for the agent on this page."""
    tpl = INTRO_AGENT_SPREADSHEET_CLUSTER[_h(slug + "|iasc") % len(INTRO_AGENT_SPREADSHEET_CLUSTER)]
    return tpl.format(name=name)


def faq_spreadsheet_meaning(slug: str, name: str) -> str:
    """FAQ answer explaining “{Name} spreadsheet” vs this discovery site."""
    tpl = FAQ_AGENT_SPREADSHEET_ANSWER[_h(slug + "|faqss") % len(FAQ_AGENT_SPREADSHEET_ANSWER)]
    return tpl.format(name=name)

INTRO2 = [
    "Below we contrast tired spreadsheet tabs with this feed, outline a sane order path, and list checks before you fund your agent balance.",
    "Next we explain why crowd-sourced rows go stale, how MaisonLooks keeps listings current when you click through, and what to verify before you commit.",
    "We walk discovery versus checkout, compare shared sheets to this browser, and spell out the safety boundary around passwords and payments.",
    "The sections map the usual haul workflow—shortlist here, paste into your agent, QC, ship—without pretending we see your parcel data.",
    "You will see how image search fills gaps when nobody typed keywords, and why warehouse photos still beat seller marketing shots.",
    "Spreadsheet culture started as generosity: someone else did the link hunt. This site preserves the skim rhythm while removing abandoned-file risk.",
    "If your export still has columns named “W2C” and “batch,” you already speak the language—here the grid is the sheet, MaisonLooks is the live citation.",
    "We avoid pretending every listing is safe; we do reduce the ping-pong between dead URLs and impatient group chats.",
    "Think of this as a browser-native “finds sheet” that does not need version history—scroll beats merge conflicts.",
    "Heavy users often keep three tools: chat for gossip, agent for money, discovery for speed—this page is the third.",
    "When a seller renames a listing, spreadsheets do not auto-heal; a feed tied to storefront pages is less brittle.",
    "You will not find warehouse photos here—by design—because QC belongs to the agent you pay.",
    "The goal is fewer tabs, fewer “link expired” screenshots, and more time reading size charts on the destination page.",
    "We wrote this for people who know what a haul is but want less administrative drag before they paste a URL.",
    "Community vetting still matters; we only replace the file format with something that loads continuously.",
    "If you treat discovery as entertainment and checkout as accounting, this layout matches that mental split.",
    "Seasonal spikes and factory holidays still apply—this guide cannot speed up China, only shorten your search path.",
    "Bookmark this when you want a calm grid session instead of another Google Drive permission request.",
    "Nothing here auto-orders; you always copy with intent after you have read the listing body.",
    "We bias toward clarity over hype—if a title looks too good, the listing page is where you verify.",
    "Spreadsheets rarely encode image angles; image search exists exactly for that blind spot.",
    "You can still share screenshots with friends—this catalog just gives you fresher targets to screenshot.",
    "Returns and disputes are not our lane; we focus on finding candidates worth arguing about.",
    "If you are comparing agents, use the same discovery session for each—fairer than mixing different stale sheets.",
    "Treat every pay click as irreversible; treat every browse click as reversible—that is the boundary we keep.",
    "Noise in group chats scales faster than moderation; a searchable grid is a private filter on top of chaos.",
    "We do not rank sellers; we surface candidates so you can rank them yourself.",
    "Last-mile carriers and customs desks do not read your spreadsheet—only your declaration form—so we keep logistics talk in agent docs.",
    "You will see repeated reminders to verify domains—because typosquatting scales with agent popularity.",
    "This is not a replacement for seller Q&amp;A; it is a replacement for Ctrl+F in a 40 MB CSV.",
]

# Second paragraph: tie in “{Name} spreadsheet” (the platform on that page—use .format(name=name)).
INTRO_AGENT_SPREADSHEET_CLUSTER = [
    "If you searched for <strong>{name} spreadsheet</strong> and landed here, that usually means “finds rows + paste into {name} later”—this guide is the browse-first half of that workflow.",
    "<strong>{name} spreadsheet</strong> is a common way people describe shared link lists; we swap the static file for a live grid tied to MaisonLooks when you click through.",
    "Treat <strong>{name} spreadsheet</strong> as a label for the habit, not a file format: same scanning rhythm, fewer broken URLs and fewer outdated batch notes.",
    "Whether you call it a <strong>{name} spreadsheet</strong>, a finds sheet, or a W2C list, the split stays the same—discover here, pay on <strong>{name}</strong>’s site.",
    "You might have a <strong>{name} spreadsheet</strong> tab open in another window; use this catalog when you want search and image search instead of Ctrl+F in Excel.",
    "Queries like <strong>{name} spreadsheet</strong> often mean fast visual triage—keyword and image search on the home site match that intent before you copy links.",
    "After you outgrow a crowd-maintained <strong>{name} spreadsheet</strong>, a continuous feed is the usual upgrade—especially when sellers rotate links weekly.",
    "This page does not host a downloadable <strong>{name} spreadsheet</strong>; it hosts the same discovery goal—shortlist items, then finish checkout on {name}’s authenticated domain.",
]

H2_CATALOG = [
    "Introducing this catalog",
    "Why this beats a frozen spreadsheet",
    "What you are looking at (and what you are not)",
    "From shared sheets to a live grid",
    "The catalog model in plain language",
    "Browsing habits, upgraded",
]

H2_WHY = [
    "Why bookmark this collection",
    "Why keep this site open",
    "What you gain before you paste a link",
    "Practical reasons to skip the CSV",
    "Speed, search, and a clean hand-off",
]

H2_WHATS_INSIDE = [
    "What’s inside",
    "Tools available on the home site",
    "What you can do before checkout",
    "Discovery features at a glance",
]

H2_READ_LISTING = [
    "How to read a listing after you click through",
    "Listing pages: where to slow down",
    "After the click: what to verify",
    "MaisonLooks detail pages: a checklist mindset",
]

H2_IMAGE = [
    "Image search: when it beats a spreadsheet column",
    "When image search saves your search",
    "Picture-first discovery",
    "Screenshots, memes, and reverse image search",
]

H2_MISTAKES = [
    "Common mistakes (easy to avoid)",
    "Easy-to-fix pitfalls",
    "Before you blame the agent",
    "Discovery mistakes that cost money later",
]

H2_CUSTOMS = [
    "Customs, duties, and VAT",
    "Import rules and your responsibility",
    "Taxes, declarations, and reality checks",
    "Customs is not our lane—yours is",
]

H2_WHEN_NOT = [
    "When this catalog is not enough",
    "Hard limits of a discovery site",
    "What we cannot see or fix",
    "Where you still need forums or tickets",
]

STATS = [
    ("<strong>100,000+</strong> products in the feed", "<strong>Text + image</strong> search in the header", "<strong>MaisonLooks</strong> listings open in a new tab"),
    ("<strong>Continuous grid</strong> instead of a stale export", "<strong>Image search</strong> when keywords fail", "<strong>Category hubs</strong> on MaisonLooks via shortcuts"),
    ("<strong>Fast skim</strong> layout for haul browsing", "<strong>Site-wide search</strong> + image upload", "<strong>External listings</strong> stay authoritative"),
    ("<strong>One home grid</strong> for many agents", "<strong>Search stack</strong> built for discovery", "<strong>New tab</strong> preserves your place here"),
    ("<strong>Broad SKU mix</strong> across categories", "<strong>Header tools</strong> rival marketplace search", "<strong>Click-out</strong> for full seller context"),
    ("<strong>Scroll loading</strong> for long sessions", "<strong>Dual search</strong> (text + image)", "<strong>Listing freshness</strong> tied to storefront pages"),
]

WHATS_INSIDE_BULLETS = [
    [
        "Image-led tiles that deep-link to MaisonLooks for full descriptions, variants, and updates.",
        "Header search that behaves like modern marketplace search—not grepping a CSV.",
        "Image search for “picture but no keywords” moments.",
        "Category shortcuts that mirror spreadsheet tabs—except they open live hubs on MaisonLooks.",
        "Infinite-style loading on the home grid so you are not stuck exporting page 9 to PDF.",
        "An Outfits lane when you want styling context, not only product IDs.",
        "No account required here—your agent credentials stay on the agent.",
    ],
    [
        "Cards prioritize visuals first, details second—exactly how most people scan a finds sheet.",
        "Search is global: useful when you half-remember a model code or a Chinese keyword fragment.",
        "Image search accepts uploads when your only reference is a cropped screenshot.",
        "Category buttons jump to MaisonLooks indexes—use them like tabs in a mega-sheet.",
        "The grid keeps loading so “page 47 of a PDF” is not your life.",
        "Outfits pairs inspiration with product hunting when you are building a coordinated look.",
        "We never ask for agent passwords—discovery stays anonymous on this domain.",
    ],
    [
        "Each tile is a doorway: the heavy reading happens on the listing, not in our card copy.",
        "Text search rewards specificity; image search rewards screenshots—use whichever matches your clue.",
        "Filtering happens mentally by price and vibe on the destination page—our job is surfacing candidates faster.",
        "Shortcuts below mirror how people split spreadsheets by category—except URLs stay current.",
        "Long sessions are normal; infinite scroll exists so you do not ration clicks.",
        "Outfits is optional—skip it when you are hunting a single SKU.",
        "Agent logins remain solely on {name}’s domain.",
    ],
]

CHECKLIST = [
    [
        ("<strong>Returns &amp; cancellations</strong> — policies differ by seller and agent; read while exit is cheap.",),
        ("<strong>Measurements</strong> — convert units; factory charts rarely match mall sizing.",),
        ("<strong>Batch chatter</strong> — hype may reference an older run; verify on the live listing.",),
        ("<strong>Declarations</strong> — you own truthful customs paperwork.",),
        ("<strong>Landed math</strong> — item + fees + freight + possible VAT—sum it before you top up.",),
    ],
    [
        ("<strong>Seller notes</strong> — read the fine print on pre-sale, processing time, and color variance.",),
        ("<strong>Size tolerance</strong> — measure twice; factory tolerances are not boutique tolerances.",),
        ("<strong>Version drift</strong> — “same link” can mean different factory weeks; ask if unsure.",),
        ("<strong>Insurance</strong> — decide whether you need add-ons before the parcel leaves China.",),
        ("<strong>Payment timing</strong> — know what triggers non-refundable charges on your agent.",),
    ],
    [
        ("<strong>Address &amp; contact</strong> — typos survive QC but fail at delivery.",),
        ("<strong>Restricted categories</strong> — some items are risky to ship to your country—research first.",),
        ("<strong>Weight estimates</strong> — rehearsal exists because guesses lie.",),
        ("<strong>Currency swings</strong> — your card issuer may add spreads beyond the item list price.",),
        ("<strong>Chargeback policy</strong> — agents may ban accounts if payment disputes are abused.",),
    ],
]

STEPS_LEAD_INS = [
    "How to use this site, then buy on {name} (or any agent)",
    "A practical flow: discover here, execute on {name}",
    "From grid to cart: a sane sequence",
    "Order of operations we recommend",
    "Seven steps before you ship internationally",
]

FAQ_AGENT_SPREADSHEET_ANSWER = [
    "A <strong>{name} spreadsheet</strong> in chat is usually a shared link list. This site gives you a searchable grid instead of a file, but checkout still happens on {name}.",
    "If you meant <strong>{name} spreadsheet</strong> as “how I browse before I paste links,” that is exactly what we describe—discovery here, payment on {name}’s site.",
    "<strong>{name} spreadsheet</strong> is not hosted here; the keyword describes the workflow. Use this catalog to research, then use {name} for warehouse steps and shipping.",
]

# Plain-text answers for JSON-LD (no HTML) — “What is a {Name} spreadsheet?”
FAQ_SPREADSHEET_JSONLD: list[str] = [
    "A {name} spreadsheet usually means a shared list of product links and notes passed around chats before you buy through an agent. This site replaces the static file with a live searchable catalog and image search.",
    "People say “{name} spreadsheet” to describe rows of finds and QC references. Here you browse a web grid instead of downloading Excel, then paste into {name} when ready.",
    "The phrase {name} spreadsheet is community slang for a curated link dump. We keep the same research pace but point you at current MaisonLooks listings when you click.",
    "If you expected a downloadable {name} spreadsheet, you will not find it here—this guide explains the same discovery goal using the home site’s grid and search.",
    "{name} spreadsheet workflows split into browse and checkout: we handle browse; {name} handles money, warehouse photos, and shipping lines.",
]

# Opening lead paragraphs — must stay distinct per slug (hash picks). Use {name}, {host_label}.
LEAD_OPENINGS: list[str] = [
    "Hunting for a <strong>{name} spreadsheet</strong> vibe—fast rows, loud photos, then paste into <a href=\"{official_url}\" target=\"_blank\" rel=\"noopener noreferrer\">{name}</a> when a SKU sticks? <strong>The best spreadsheet</strong> is a MaisonLooks-backed grid with text + image search; we are not {name}’s app, not their checkout, and not a file attachment.",
    "This page is for shoppers who describe their workflow as a <strong>{name} spreadsheet</strong> even when the “sheet” is really a Discord dump. We formalize the browse step: scroll the home grid, open listings in a new tab, then return to <strong>{host_label}</strong> to pay.",
    "You might be comparing agents while still wanting one calm discovery surface. Think of this as the shared front half—search and image search—before you split off to <a href=\"{official_url}\" target=\"_blank\" rel=\"noopener noreferrer\">{host_label}</a> for balances and parcels.",
    "Some folks collect links in Notes; others in Google Sheets. If your mental model is “<strong>{name} spreadsheet</strong> first, questions later,” you will recognize the rhythm: skim here, read the listing there, commit cash only on {name}.",
    "We built this for the tab hoarders: one window for MaisonLooks discovery, another for {name} logistics. No extension required—just discipline and a bookmark to <strong>{host_label}</strong> you verified yourself.",
    "Replica communities love spreadsheets until a seller renames a listing. This site reduces the archaeology: fewer dead URLs, more time comparing variants before you fund {name}.",
    "If your last haul started from a screenshot and a prayer, image search on the home site is the bridge. {name} still runs QC—this layer only helps you pick candidates worth submitting.",
    "International cards and Chinese checkout rarely meet; that is why {name} exists. Our job is narrower—surface items with modern search so you are not grepping column K at 2 a.m.",
    "Treat this domain as a reading room, not a warehouse. {name} stores boxes; we store attention—keyword search, image search, category hops on MaisonLooks.",
    "You do not need another macro. You need fewer 404s. The grid loads continuously, links resolve toward live product pages, and your wallet stays on {name}’s authenticated domain.",
    "Spreadsheets cannot upload a meme from TikTok; image search can. Pair that with {name}’s warehouse photos and you have two different kinds of truth—both matter.",
    "When batch talk moves faster than your filter, step out of the sheet and into site-wide search. Save {name} for the moment money leaves your account.",
    "We are not ranking “best agent.” We are speeding up “best link today.” Final judgment still happens on the listing page and in {name}’s ticket system.",
    "Some buyers want sneakers; others want desk gadgets. The mixed grid mirrors a mega-sheet’s chaos—category shortcuts exist for when you need a narrower lane before returning to {name}.",
    "If you already trust {name} with consolidation, trust this page only for discovery friction—less copy-paste, fewer “who edited this cell?” moments.",
    "The hardest part of a haul is often deciding what not to buy. A searchable catalog makes comparison cheaper than scrolling a frozen CSV from last season.",
    "We assume you know what QC means. We assume you do not want to juggle five outdated tabs. Hence: one grid, one agent login at <strong>{host_label}</strong>, one parcel plan.",
    "Language barriers live on the listing; payment barriers live on {name}. We stay in the shallow end—find, click, verify—before you swim into fees and freight.",
    "Bookmark hygiene matters: phishing sites mimic agents daily. Pair this discovery page with a {name} tab opened only from a URL you trust—not from random DMs.",
    "Your spreadsheet might track status; ours tracks curiosity. When you are ready for invoices and tracking numbers, the context switch to {name} is intentional.",
    "Fast fashion cycles punish static lists. A feed tied to storefront pages is less romantic than a community sheet, but more honest about what still exists.",
    "If you are new, read slowly: discovery is cheap, shipping mistakes are not. {name} publishes rules; we publish ways to browse without rage-quitting the hobby.",
    "Power users still share links in chats—this site simply gives you a second opinion machine: text search, image search, outfits for styling context.",
    "Nothing here auto-fills {name}’s order form. You copy with intent after you have compared photos and measurements on MaisonLooks.",
    "Think of {name} as the bank and this site as the library. Libraries do not ship boxes; they shorten the search for what to request.",
    "Seasonal sales in China still follow holidays you barely notice. A live grid adapts faster than a tab you have not touched since summer.",
    "We will repeat it until it is boring: passwords and parcels belong to {name}. This domain never asks for either.",
    "Some shoppers want a checklist; others want a river of SKUs. This grid leans river—use categories when you need banks instead of rapids.",
]

# Long-form catalog / angle pools (slug-keyed via pick_variant in build script).
CATALOG_A: list[str] = [
    "Community sheets won because they bundle social proof; they lose when maintainers vanish and URLs die. This build keeps the skim-fast habit but swaps the file for a live grid.",
    "Think of shared spreadsheets as fan zines—charming, uneven, often outdated. This catalog is closer to a store aisle wired to listing pages that update on the storefront side.",
    "If your Discord export still references a Taobao link from last season, you already know the pain. Here, scrolling loads more rows and cards resolve toward current MaisonLooks pages.",
    "The goal is not to recreate Excel online—it is to preserve the batch-browsing rhythm while reducing 404s and mismatched batch notes.",
    "Crowd sheets are democracy: noisy, unevenly moderated, occasionally brilliant. A web grid is oligarchy of UX: consistent search, consistent click-out behavior.",
    "You are not missing “community truth”—you are missing a maintainer. Automated feeds cannot gossip, but they also do not ghost you mid-season.",
    "Some collectors want rarity; haul browsers want throughput. This interface optimizes for the second group—scan wide, then tighten with categories.",
    "Spreadsheet columns rarely capture lighting conditions; listing pages sometimes do. We push you to the page where photography and text disagree less often.",
    "If your sheet has a “notes” column full of “RL?” you already understand uncertainty. We reduce uncertainty about whether the URL still resolves.",
    "Exports age like fish. A MaisonLooks-backed card stack ages like bread—stale sometimes, but easier to slice fresh.",
    "You can still screenshot our grid for friends. The difference is your screenshot points at a living listing, not a cell that will error tomorrow.",
    "The social layer stays in Discord. The inventory layer lives here—because inventory is what changes when sellers rotate stock.",
    "We do not promise every find is ethical or legal in your country—that is on you and your research. We promise less time hunting a working link.",
    "Mega-sheets feel infinite until they do not. Infinite scroll is honest about infinity—it admits the dataset is larger than your afternoon.",
    "Row 4,847 might be fire; you will never know if the file stops at 500. The grid does not stop at 500 unless you stop scrolling.",
    "Colorways shift; factories rename batches. A static row cannot argue with a seller who updated the title—only a live page can.",
    "If you miss the aesthetic of monospace fonts, we are sorry. If you miss fewer broken URLs, we are not.",
    "Think of categories as tabs you did not have to build—open sneakers, skim, return to mixed feed when you are bored of shoes.",
    "Browsing is not buying. We repeat it because spreadsheets blur the line when price columns sit next to checkout fantasies.",
    "Your past self’s spreadsheet is a time capsule. This grid is a newspaper—throwaway daily, useful when fresh.",
    "We like community wisdom; we dislike community link rot. This is the compromise: community habits, machine-maintained pointers.",
    "If you are here for spreadsheets as performance art, wrong venue. If you are here to find something worth paying {name} to touch, welcome.",
    "The thesis is simple: fewer hops between curiosity and a current listing. Everything else is commentary.",
    "You will still argue about batches in chat. We just want your argument to reference a page that loads.",
    "Catalogs used to be paper; then PDF; then CSV; now URLs. We are the URL era’s lazy index—good enough to start, serious enough to verify.",
]

CATALOG_B: list[str] = [
    "You still judge quality and sizing yourself; we simply remove friction between curiosity and a fresh product page.",
    "No algorithm promises authenticity—only less time wasted on dead links and renamed listings.",
    "Treat the grid as a compass, not a certificate: verify variants on the destination listing every time.",
    "Speed without verification is expensive. Slow down on the listing; speed up on discovery—that is the trade we enable.",
    "If something feels too cheap, the listing’s fine print is where reality lives—often in Chinese, often worth translating.",
    "We are allergic to guarantees; we are friendly to pointers. Pointers age; guarantees rot faster.",
    "Your eyes are still the QC layer before {name}’s warehouse QC. Two layers, two jobs.",
    "A pretty tile is marketing; a detailed listing is negotiation. Negotiate before you pay.",
    "When in doubt, open two listings side by side—batch differences hide in adjectives, not always in price.",
    "Measurements beat model names. Model names beat vibes. Vibes are not a return policy.",
    "The grid is neutral; your risk tolerance is not. Spend accordingly.",
    "If a seller’s English looks machine-translated, assume the numbers are the source of truth.",
    "Bookmarks beat memory. Screenshots beat bookmarks when colors are controversial.",
    "We will not tell you what to buy. We will tell you where to read before you buy.",
    "Silence in a chat is not approval; a loaded listing page is not approval either—only your payment is.",
    "Scroll fatigue is real. Use search when you have a clue; use image search when you do not.",
    "The best hauls mix planning with improvisation—too rigid a list misses restocks; too loose a list misses budgets.",
    "If you cannot explain why you want an item in one sentence, sleep on it—spreadsheets rarely include sleep.",
    "Community hype has a half-life. Listing photos have timestamps—check them.",
    "You are allowed to close the tab. You are also allowed to open it again tomorrow—prices move.",
    "This catalog does not know your customs limit. Your government does—read theirs, not ours.",
    "We bias toward clarity: fewer adjectives on our side, more on the seller’s side where they belong.",
    "If a category button saves you ten minutes, that is ten minutes you can spend reading reviews—if reviews exist.",
    "Finally: curiosity is cheap; international shipping is not. Act like it.",
]

FEATURE_H3_SETS: list[tuple[str, str, str]] = [
    ("1 · Catalog width", "2 · Search that matches how you think", "3 · Money stays on {name}"),
    ("1 · Range across categories", "2 · Text + image discovery", "3 · Agent boundary"),
    ("1 · Mixed SKUs, one stream", "2 · Research tools in the header", "3 · Checkout isolation"),
    ("1 · Breadth over boutique curation", "2 · Keywords + screenshots", "3 · No wallet on this domain"),
    ("1 · Endless-ish browsing", "2 · Image search for clueless moments", "3 · {name} owns QC and freight"),
    ("1 · Visual-first tiles", "2 · Search as a first-class citizen", "3 · Support tickets on {name} only"),
    ("1 · Haul-scale selection", "2 · Outfits optional, grid mandatory", "3 · Parcels and passwords elsewhere"),
    ("1 · Sneakers to gadgets", "2 · Two search modes", "3 · Hand-off, not replacement"),
]

COMPARE_TABLES: list[list[tuple[str, str, str]]] = [
    [
        ("Freshness", "Depends on whoever edits the file; easy to abandon.", "Continuous feed; scroll for new batches without re-downloading."),
        ("Search", "Ctrl+F in a tab or hope someone sorted columns.", "Site-wide text search + image search from the header."),
        ("Broken links", "Common when sellers change URLs or go private.", "Cards resolve through MaisonLooks; you still confirm on the listing."),
        ("Checkout", "You still open {name} (or another agent) yourself.", "Same—discovery here, payment and warehouse on the agent only."),
    ],
    [
        ("Maintenance", "Human editors, irregular updates.", "No merge conflicts—just load more rows."),
        ("Discovery", "Keyword luck + column sorting.", "Dedicated search + image upload."),
        ("Trust model", "Reputation of whoever shared the sheet.", "You verify on the live listing every time."),
        ("Payments", "Never on the sheet—should not be.", "Never on this site—must be on {name}."),
    ],
    [
        ("Versioning", "v12_final_REALLY.xlsx", "Always “today’s” storefront snapshot when you click through."),
        ("Mobile", "Pinch-zoom hell on tiny cells.", "Responsive grid + search built for phones."),
        ("Noise", "Off-topic rows and joke columns.", "Focused product tiles; chatter stays in your chats."),
        ("Scope", "Sometimes one seller, sometimes chaos.", "Wide mixed inventory like a public mega-sheet."),
    ],
]

CATEGORY_INTROS: list[str] = [
    "Pick a lane the same way you might jump between tabs in a spreadsheet—except each button opens the current category index on MaisonLooks, not a frozen list of URLs.",
    "Use these buttons when your brain wants “just sneakers today”—narrow first, wander the mixed grid later.",
    "Categories are training wheels for focus; the home grid is for when you want chaos and serendipity.",
    "If you already know the lane, click through; if not, stay on the home feed and let randomness help.",
    "Think of each button as a tab you did not have to build—except it opens a live index, not a saved column filter.",
]

CUSTOMS_P: list[str] = [
    "Your country’s rules beat anything in a blog. Budget for duties, read thresholds, and remember enforcement changes—{name} may offer guidance, but compliance stays with you.",
    "Customs is a local sport with different referees each year. {name} might explain options; you still own the declaration accuracy.",
    "VAT, GST, IOSS—acronyms vary. The constant is: under-declaring to save money can cost more later than paying upfront.",
    "If a line looks “too cheap to include insurance,” understand what you are risking before the box crosses the border.",
    "Some regions inspect fashion more than electronics; some the opposite. General guides cannot replace your country’s current enforcement mood.",
    "When in doubt, round duties up in your mental budget—surprises at the door are rarely pleasant surprises.",
]

MISTAKE_SETS: list[list[str]] = [
    [
        "<strong>Treating a sheet row as gospel</strong> — reopen the live listing the day you pay.",
        "<strong>Skipping measurements</strong> — flat-lay a favorite piece and compare numbers.",
        "<strong>Approving blurry QC</strong> — ask for clarity before the package leaves China.",
        "<strong>Ignoring fee stacks</strong> — domestic + international + insurance add up.",
        "<strong>DM support</strong> — tickets and payments belong inside {name}’s logged-in experience.",
    ],
    [
        "<strong>Assuming English titles match factory reality</strong> — read measurements and material lines.",
        "<strong>Chasing the lowest line price</strong> — shipping and service fees can erase the win.",
        "<strong>Shipping hype items with the slowest line</strong> — balance risk and speed deliberately.",
        "<strong>Ignoring seller processing times</strong> — pre-orders and holidays exist.",
        "<strong>Using the same password everywhere</strong> — isolate your agent credentials.",
    ],
    [
        "<strong>Buying blind off a single photo</strong> — scroll for more angles on MaisonLooks.",
        "<strong>Comparing batches from different years</strong> — community memory outlasts factory consistency.",
        "<strong>Rushing declarations</strong> — typos become expensive at customs.",
        "<strong>Skipping consolidation math</strong> — volume weight punishes random shapes.",
        "<strong>Trusting screenshots over warehouse QC</strong> — the warehouse is your last honest photo.",
    ],
    [
        "<strong>Letting chats set your risk tolerance</strong> — verify on the listing and with {name}.",
        "<strong>Ignoring return windows</strong> — they shrink once outbound shipping starts.",
        "<strong>Mixing up color names</strong> — “black” and “off-black” are different arguments.",
        "<strong>Underestimating holidays</strong> — China’s calendar moves your timeline.",
        "<strong>Bookmarking phishing domains</strong> — verify {host_label} character by character.",
    ],
]

# --- SEO: title, meta description, H1 — each page should rank for “{Name} spreadsheet” style queries (not only “finds spreadsheet”).
META_PAGE_TITLES: list[str] = [
    "{name} spreadsheet ({year}) · finds, W2C & link lists · {host_label} · The best spreadsheet",
    "{name} spreadsheet {year} guide · MaisonLooks grid · Taobao / Weidian / 1688 · {host_label}",
    "{name} spreadsheet · {year} browse tips · live catalog · image search · {host_label}",
    "{name} finds spreadsheet & keywords ({year}) · haul notes · {host_label}",
    "{name} spreadsheet hub · QC & customs ({year}) · pay on {host_label} only",
    "The “{name} spreadsheet” workflow ({year}) · keyword + image search · {host_label}",
    "{name} spreadsheet vs dead Excel rows · {year} · fresh links · {host_label}",
    "{name} spreadsheet for W2C & reps ({year}) · MaisonLooks · {host_label}",
]

# Keep under ~300 chars; include multiple long-tail phrases per variant.
META_DESCRIPTIONS: list[str] = [
    "{year} {name} spreadsheet guide: live grid (not a stale file)—{name} spreadsheet–style browsing, Taobao / Weidian / 1688 via MaisonLooks, image vs keyword search, haul & QC tips. Pay only on {host_label}; discovery-only.",
    "{name} spreadsheet {year}: shared downloads rot fast. Use this browser catalog instead—safe linking to {host_label}, broken-URL fewer than Excel, community-sheet rhythm without attachment chaos—The best spreadsheet.",
    "Searching “{name} spreadsheet {year}” or “{name} finds”? Same workflow: shortlist here, paste into {name}, warehouse QC on {host_label}. Image search when titles fail; keywords when you know the token.",
    "{name} spreadsheet keywords {year}: W2C lists, link hubs, QC mindset, customs reality—official checkout {host_label}; we are not {name}’s app.",
    "No mandatory {name} spreadsheet download—{year} listings move weekly. This page is the browse layer: search, image upload, MaisonLooks tabs, then {host_label} for money and parcels.",
    "Chat-export {name} spreadsheet vs this site: one freezes URLs, the other points at storefront pages. Taobao & Weidian context, fraud-aware habits, {year} shipping realism—still pay on {host_label}.",
    "{year} {name} spreadsheet meaning in plain English: how people use the phrase, what we provide instead of a Google Sheet, and when to trust warehouse photos on {name} at {host_label}.",
    "“{name} spreadsheet” tabs compared to this catalog—freshness, search quality, and why QC never lives in a cell—{year} guide; ship and insure through {host_label} after you buy.",
]

H1_TITLES: list[str] = [
    "{name} finds spreadsheet ({year})",
    "{name} spreadsheet · finds & links · {year}",
    "{name} spreadsheet ({year} live guide)",
    "{name} finds spreadsheet · W2C & link hub · {year}",
    "{name} spreadsheet guide · {year}",
    "{name} spreadsheet · {year} guide",
    "{name} spreadsheet & finds · {year}",
]

# Plain-text answers for extra JSON-LD FAQ entries (long-tail).
FAQ_LONGTAIL_DOWNLOAD: list[str] = [
    "No file download is required here—and a static {name} spreadsheet file is often outdated the week it is shared. This site gives you the same “{name} spreadsheet” research goal with a live grid and search; you still complete purchases on {name}’s official domain.",
    "We do not host an Excel or Google Sheet export. If you searched for a downloadable {name} spreadsheet, use this page as the browse layer and bookmark {name} for checkout—spreadsheets rot; listing pages update.",
    "A {name} spreadsheet in Discord is usually a screenshot or Drive link. This guide is the same intent with less link rot: search, image search, then paste into {name} when you are ready.",
]

FAQ_LONGTAIL_VS_SITE: list[str] = [
    "A shared {name} spreadsheet is a file or chat dump of URLs; this site is a discovery interface with search and image search tied to MaisonLooks. Both answer “{name} spreadsheet” workflows—only one stays current without manual edits.",
    "“{name} spreadsheet” often means rows of finds before you paste into the agent. That is exactly what we optimize here; the difference is live inventory pointers instead of frozen cells.",
    "Spreadsheets are great for notes; they are bad at staying synced with Chinese marketplace URLs. This page targets {name} spreadsheet searches with a catalog mindset—verify on {name} before you pay.",
]

# “Best spreadsheet in {year}?” — honest answer for FAQ + JSON-LD (no single canonical file).
FAQ_BEST_YEAR: list[str] = [
    "There is no one “best” {name} spreadsheet in {year} that stays true for everyone—links rot, batches change, and sellers rename listings. This site targets the same intent with a searchable catalog and image search; you still confirm on live pages and pay on {host_label}.",
    "Anyone promising a perfect {name} spreadsheet for {year} is selling nostalgia. Use this guide for browse-first research, then {name}’s authenticated domain for QC and shipping—fresh beats famous.",
    "The best {name} spreadsheet in {year} is the one you verify the same day you pay—not a file from last season. We bias toward always-on discovery; your agent account on {host_label} handles what spreadsheets cannot.",
]

H2_GUIDE_WHAT: list[str] = [
    "{name} spreadsheet in {year}: what this page is for",
    "Why this exists ({year} {name} spreadsheet guide)",
    "Reading this if you searched “{name} spreadsheet”",
    "{year} update: how we use the phrase “{name} spreadsheet” here",
]

P_GUIDE_WHAT: list[str] = [
    "People type “{name} spreadsheet” when they want fast rows of links before pasting into an agent. This page serves that habit with a live grid and search—not a downloadable file—so you spend less time on dead URLs and more time on listing details. Money and parcels still belong on {host_label}.",
    "If your mental model is a {name} spreadsheet tab, keep it: skim wide, click through, read variants. The difference in {year} is that storefront pages update while shared sheets don’t; we route you to current MaisonLooks listings before you commit on {name}.",
    "We are not publishing a ranked mega-list of SKUs—those go stale. We publish a {year}-ready browse layer that matches “{name} spreadsheet” intent: discovery here, checkout on {host_label}, skepticism everywhere else.",
]

H2_WORKFLOW: list[str] = [
    "First-time workflow ({year})",
    "From search to {host_label} ({year} checklist)",
    "New here? A sane {name} spreadsheet rhythm",
    "{year} order of operations before you pay {name}",
]

P_WORKFLOW: list[str] = [
    "Start on the home grid or search; open listings in a new tab; screenshot SKUs if needed; paste into {name} only after measurements make sense. In {year}, batch chatter moves faster than documents—trust live text on the listing over a screenshot from chat.",
    "One pass: browse → read listing → compare price bands → submit to {name} → fund on {host_label} → QC → ship. Skipping the listing read is how {year} hauls turn into return tickets.",
    "If you are chasing one grail link, image search first; if you know the product name, keyword search. Either way, the {name} spreadsheet fantasy ends when you verify stock language on the page—same as any {year} guide should tell you.",
]

H2_QC_BATCH: list[str] = [
    "QC & batch talk (without hype)",
    "Warehouse photos beat spreadsheet rumors",
    "How to read QC for {name} orders",
    "{year} reality check: batches and listings",
]

P_QC_BATCH: list[str] = [
    "Community spreadsheets often encode “batch” gossip; warehouse photos encode what you actually bought. Use {name}’s QC tools on {host_label} to zoom—if the photo disagrees with a row in an old sheet, trust the photo and ticket early.",
    "Batch codes are social objects; listings are legal-ish descriptions. When they conflict, the listing and your agent’s camera win. This {year}, assume renames happen weekly—spreadsheets rarely keep up.",
    "Red-light / green-light culture is fine for Discord; your wallet needs listing accuracy and agent-side photos. We mention this because “{name} spreadsheet” searches often come from people comparing batches—compare on fresh pages, not frozen cells.",
]

H2_SETS_COORD: list[str] = [
    "Sets & coordinated buys",
    "Matching tops and bottoms (same order mindset)",
    "When you buy two pieces that must match",
    "Outfits vs single-SKU hunting",
]

P_SETS_COORD: list[str] = [
    "Buying a coordinated set means two SKUs must match in dye lot and cut—not just size. Use category shortcuts and the Outfits lane for inspiration, then verify both listings reference the same season language before you paste into {name}.",
    "Sets fail when color names differ between items; screenshots fail when lighting lies. In {year}, treat “set” buys like mini hauls—one seller, one order batch when possible, and measure both pieces against a flat lay you trust.",
    "If you only need one item, ignore this block. If you want a head-to-toe look, browse like a spreadsheet user: lock the palette first, then hunt SKUs—still pay and QC through {host_label} on {name}.",
]


def meta_keywords_content(name: str, host_label: str, slug: str, year: str) -> str:
    """Comma-separated keywords for meta name=\"keywords\" (some engines still read it)."""
    base = name.replace(" ", "").lower()
    chunks = [
        f"{name} spreadsheet",
        f"{name} spreadsheet {year}",
        f"{name} finds spreadsheet",
        f"{slug} spreadsheet",
        f"{slug} spreadsheet {year}",
        f"{name} W2C",
        f"{name} finds",
        f"{year} shopping agent guide",
        "Taobao agent",
        "Weidian",
        "1688",
        "haul spreadsheet",
        "link list",
        host_label,
        "MaisonLooks",
        "shopping agent",
    ]
    if base != slug:
        chunks.insert(3, f"{base} spreadsheet")
    # de-dupe while preserving order
    seen: set[str] = set()
    out: list[str] = []
    for c in chunks:
        k = c.strip().lower()
        if k and k not in seen:
            seen.add(k)
            out.append(c.strip())
    return ", ".join(out)


def pick_variant(slug: str, key: str, options: list) -> object:
    """Deterministic pick: different key → different stream → less collision across sections."""
    if not options:
        raise ValueError("empty options")
    return options[_h(slug + "|" + key) % len(options)]


def format_lead(slug: str, name: str, host_label: str, official_url: str) -> str:
    tpl: str = pick_variant(slug, "lead", LEAD_OPENINGS)
    return tpl.format(name=name, host_label=host_label, official_url=official_url)


def faq_spreadsheet_jsonld_plain(slug: str, name: str) -> str:
    return pick_variant(slug, "faqjson1", FAQ_SPREADSHEET_JSONLD).format(name=name)


FEAT1_POOL: list[str] = [
    "Sneakers through electronics show up in one mixed stream—use MaisonLooks categories when you want a narrower lane than a mega-sheet’s stray columns.",
    "The feed spans footwear, apparel, bags, accessories, and more—closer to an endless haul tab than a single-seller worksheet.",
    "Wide SKUs mean you can wander like a mega-spreadsheet, then tighten focus with category hubs when fatigue hits.",
    "If you shop like you are flipping channels, the mixed grid matches; when you shop like a sniper, jump to a category hub.",
    "Rare pairs and common tees share the same river—sort mentally by price and vibe on the destination page.",
    "Discovery is allowed to be messy; checkout should not be—use categories when mess stops being fun.",
    "Think of the grid as a flea market aisle: loud, varied, occasionally cursed—categories are the stalls grouped by intent.",
    "Electronics and hoodies coexist because haul culture does not respect taxonomies—filters live on MaisonLooks, not in our moral judgment.",
    "Sometimes you want randomness to break filter bubbles; sometimes you want sneakers only—both modes are valid.",
    "Batch buyers and one-off experimenters share this feed; the difference is what you do after the click.",
    "If everything looks the same, you are tired—switch categories or switch days, not agents on impulse.",
    "Wide selection is a feature until it is noise; noise is your cue to search or image-search instead of scroll.",
    "The grid does not know your aesthetic; you do—use it to audition candidates, not to define taste.",
    "Seasonal drops still surface here; seasonality still hurts your wallet—plan accordingly.",
    "Nothing stops you from using this as inspiration board first and shopping list second—that is how many sheets started anyway.",
]

FEAT2_POOL: list[str] = [
    "Pair keyword search with image search when your only clue is a screenshot from a short video.",
    "Keywords for what you can name; image search for everything else—stolen memes, cropped IG posts, blurry factory photos.",
    "When text fails, drop an image into header search and chase the closest visual neighbors on MaisonLooks.",
    "Search rewards vocabulary; image search rewards hoarding screenshots—use the tool that matches your evidence.",
    "If you only know half a logo, image search is often faster than guessing pinyin.",
    "Sometimes the listing title is SEO spam; sometimes the image is honest—cross-check both.",
    "Reverse image search is not magic—it is triage. Triage still beats scrolling fifty wrong keywords.",
    "Combine discovery with the Outfits lane when you want silhouettes, not SKUs.",
    "If your keyword returns 8,000 hits, tighten the word or switch to image—breadth without signal is exhaustion.",
    "Good searches are iterative: start wide, read titles, refine, repeat—same as a good spreadsheet cleanup.",
    "Image search shines when sellers rename listings but keep the same photos—visual continuity beats textual chaos.",
    "If you are hunting a specific batch code, keywords win; if you are hunting a vibe, images win.",
    "Do not let perfect search be the enemy of good enough discovery—sometimes scrolling finds what language cannot.",
    "Search is a dialogue with the catalog; silence means try another query, not blame the agent.",
    "Remember: search finds candidates; listings decide truth.",
]

FEAT3_POOL: list[str] = [
    "Warehouse QC, freight choices, and refunds stay on {name}’s authenticated site—this domain never touches your card.",
    "Declarations, insurance, and ticket replies belong to {name} or whichever agent you picked; we stop at discovery.",
    "Keeping money and support on {name}’s real domain is deliberate—you mirror how serious shoppers separate browsing from buying.",
    "If it costs money or needs a ticket, it is not here—{name} signed up for that complexity.",
    "We refuse to cosplay customer support for {name}; their dashboard exists for a reason.",
    "Your card details should only ever touch {name}’s checkout flow you trust—not a spreadsheet macro, not a random DM.",
    "Disputes and insurance claims route through {name}; we do not have your order ID and do not want it.",
    "Think of this domain as read-only for commerce: you read listings; {name} writes charges.",
    "When something goes wrong in transit, {name}’s tools matter—our tools never shipped a box.",
    "The boundary is boring on purpose: boring saves you from phishing dressed as “helpful sheets.”",
    "Support staff at {name} train on their policies; we train on discovery—do not confuse the two.",
    "If a refund is possible, {name} knows the rules; we only know how to find another listing.",
    "Parcel photos belong in {name}’s UI; screenshot them from there, not from our grid.",
    "We like {name} enough to link out—just not enough to impersonate.",
    "Closing the loop: browse here, pay there, ship through {name}—three acts, three stages.",
]

WHAT_IS_POOL: list[str] = [
    "{name} is a shopping-agent workflow: you fund purchases from Chinese sellers who may not ship abroad, review domestic arrival photos, then pick an international line. This page only covers the research half—shortlisting items before you paste links.",
    "As a forwarding-style agent, {name} sits between you and domestic sellers—collecting parcels, shooting QC, staging consolidation. Use our grid to explore; use {name}’s dashboard to execute.",
    "{name} belongs to the same broad family as other agents: buy-for-me domestically, photograph, ship overseas. Discovery happens here; execution and disputes happen in your agent account.",
    "In one sentence: {name} moves goods from Chinese sellers to you through a warehouse you control with clicks, not forklifts.",
    "{name} is not a marketplace storefront in the Amazon sense—it is a service layer on top of Chinese marketplaces you cannot easily pay directly.",
    "Expect two wallets mentally: curiosity spends time here; reality spends currency on {name}.",
    "{name} exists because language, payment rails, and freight do not align across borders by default.",
    "If you understand “agent,” you understand {name}’s role—middle, not maker.",
    "Some agents emphasize QC photography; some emphasize lines—either way, {name} is where photos of *your* item should appear.",
    "Consolidation is {name}’s superpower; discovery is ours—division of labor.",
    "{name} cannot bless a listing’s ethics; neither can we—due diligence is distributed.",
    "You will hear “service fee” on {name}; you will not hear it here—no services beyond browsing.",
    "Think of {name} as logistics plus procurement insurance against “seller ghosted me.”",
    "The shortest version: {name} buys where you cannot, stores where you should not, ships where you live.",
    "If {name} ever feels slow, China’s domestic leg might be slow first—discovery cannot accelerate factories.",
]

WEIDIAN_POOL: list[str] = [
    "Yupoo albums, Weidian rumors, and Taobao bookmarks rarely stay in sync. This catalog gives you a visual runway when you want to browse without reconciling five outdated tabs.",
    "Most veterans mix Yupoo, Discord, and live listings. We do not replace those circles—we speed up the moment you need a clean grid instead of a CSV from 2023.",
    "When someone says “new batch,” trust the live listing and your agent’s QC—not a screenshot archived in a spreadsheet row.",
    "Discord is fast; spreadsheets are slow; listings are authoritative—rank your trust accordingly.",
    "Yupoo is a lookbook; Weidian is a storefront; your agent is a wallet—keep the roles separate.",
    "If a link dies, communities revive it sometimes faster than Google—this grid is not a replacement for friends, just a filter.",
    "Batch codes are social technology; QC photos are physical technology—both beat vibes.",
    "1688 prices seduce; MOQs punish—read carefully before you ask {name} to bridge the gap.",
    "Weidian titles are SEO theater; sometimes the theater is wrong—use photos and measurements.",
    "Spreadsheet screenshots age like milk; listing timestamps age like cheese—still check for mold.",
    "If your source is a TikTok, pause—image search might find the listing faster than comments.",
    "Community lists are collaborative fiction until a warehouse photo says otherwise.",
    "There is no substitute for opening the listing and reading the boring lines.",
    "Hype travels faster than inventory—verify stock language before you celebrate.",
    "Remember: a pretty Yupoo grid does not guarantee a pretty factory run.",
]

TIMELINE_POOL: list[str] = [
    "Track every milestone inside {name}; if something stalls, open a ticket there—this discovery layer has no order IDs.",
    "After you submit links to {name}, only their dashboard shows seller dispatch, warehouse arrival, and outbound tracking.",
    "Seasonal rushes and customs pauses show up in {name}’s UI, not on this site.",
    "Timelines are probability clouds—November and Chinese New Year widen the cloud.",
    "Domestic shipping is usually fast until it is not—factories miss dates too.",
    "If your parcel feels stuck, refresh tracking on {name}, not on this page—we do not have tracking.",
    "QC photos are a milestone: before them, hope; after them, decisions.",
    "International lines have personalities—some fast and expensive, some slow and bruised—{name} lists them, we do not rank them.",
    "Customs is a black box in every country—budget time, not miracles.",
    "Last-mile couriers lose packages sometimes—insurance exists for a reason.",
    "If you need a guaranteed date, buy locally; if you want price, accept variance.",
    "Your friend’s last haul timeline is anecdote, not contract.",
    "Clocks differ: seller clock, warehouse clock, freight clock—only {name} merges them for you.",
    "Patience is a strategy; anxiety is not—ticket politely if something looks wrong in {name}.",
    "End-to-end visibility ends at {name}’s tools—embrace that boundary.",
]

HAUL_POOL: list[str] = [
    "Plan batches in your head, in notes, or in screenshots—then paste groups of links into {name} when you are ready to consolidate.",
    "Group compatible pieces before you ship: volumetric weight punishes random one-offs more than a thought-through {name} parcel.",
    "Use rehearsal or pre-pack tools inside {name} when available—discovery here cannot estimate your final cube.",
    "A haul is a story; a parcel is a box—make sure the box matches the story’s weight class.",
    "Shoes and hoodies ship differently—mind volumetric vs actual weight when you bundle.",
    "If you fear duties, smaller parcels sometimes help—sometimes not; research your country.",
    "Impulse buys are fine until they share a box with fragile items—think packaging interactions.",
    "Spreadsheet tabs used to organize hauls; mental tabs still work—just write them down somewhere.",
    "Consolidation saves money until it delays everything—choose your poison.",
    "Sometimes splitting shipments reduces risk; sometimes it multiplies fees—{name}’s calculator is the referee.",
    "Holiday gifting? Start earlier than your optimism suggests.",
    "If you cannot lift the hypothetical box, neither can your mail carrier—split it.",
    "Haul culture rewards patience; shipping lines reward planning.",
    "Aesthetic cohesion is optional; freight cohesion is mandatory.",
    "Close the haul when the spreadsheet in your head feels complete—not when the grid runs out of scroll.",
]

WHEN_NOT_POOL: list[str] = [
    "Chargebacks, insurance, and account recovery route through {name} or your bank—this site cannot see your orders.",
    "Private sellers, niche categories, or bespoke quotes may still need forums; no single grid indexes the whole Chinese internet.",
    "If a listing vanishes, communities sometimes mirror replacements faster than any catalog—cross-check before you assume silence means denial.",
    "If you need legal advice, this is not it; if you need a link, maybe we are.",
    "Customs disputes belong to you and your government—agents advise, you sign.",
    "If a seller threatens you, that is between you, platforms, and law—not this FAQ.",
    "Niche hobby gear may never appear in a broad grid—specialist forums still win sometimes.",
    "If {name} bans an account, we cannot appeal on your behalf—we do not have accounts here.",
    "When data privacy questions arise, read {name}’s policy—ours is “we do not run checkout.”",
    "Medical claims, safety certifications, and compliance paperwork live on listings and regulators—not on discovery pages.",
    "If something feels like fraud, stop and verify domains—this page repeats that for a reason.",
    "Auctions, haggling, and offline deals are out of scope—we link to listings, not negotiate lives.",
    "Brand authenticity debates belong to communities and lawyers—here we only help you find a URL.",
    "If your country bans a category, do not ask us to help you skirt it—follow your laws.",
    "Finally: if you are unhappy with {name}, their ticket system is the right venue—we are not their HR department.",
]

GLOSSARY_AGENT_POOL: list[str] = [
    "A service that buys domestically in China and forwards internationally—{name} is one option among many.",
    "Forwarding intermediaries differ by fees and UI; {name} is one brand in that ecosystem.",
    "Agents compete on lines, QC clarity, and support—{name} is one entry you might pair with this discovery layer.",
    "Short definition: {name} is the paid layer between you and sellers who do not ship to your porch.",
    "Agents are not marketplaces; they are adapters—{name} adapts checkout and logistics for you.",
    "If “agent” sounds vague, think “procurement + warehouse + freight concierge”—{name} tries to bundle those.",
    "We describe agents generically; {name} implements specifics—read their help center for nuances.",
    "Not all agents serve all countries equally—{name}’s routes are their secret sauce, not ours.",
    "Choosing {name} is choosing a workflow—this page does not pick winners.",
    "Agents age; policies change—bookmark {name}’s official docs, not forum screenshots.",
    "An agent is not insurance against bad taste—only against some logistics failures, sometimes.",
    "You can switch agents; you cannot switch physics—boxes still weigh what they weigh.",
    "{name} is a tool; like any tool, misuse hurts—read fees before you click pay.",
    "Agents simplify China; they do not simplify your budget—plan accordingly.",
    "If {name} is wrong for your country, another agent might be—this grid stays the same either way.",
]

SVC_FEE_POOL: list[str] = [
    "What {name} charges to place the order—percent or flat—check their current fee page before you budget.",
    "Pricing models shift; read the agent’s own fee table instead of trusting a screenshot.",
    "Service fees stack on item cost—confirm the structure in {name}’s help center.",
    "Fees are the boring part of hauls—boring is where money leaks if you ignore it.",
    "Sometimes fees include photos; sometimes photos cost extra—{name} spells it out, we do not.",
    "Currency conversion can hide spreads—watch your card statement, not only the item line.",
    "If a fee looks new, it might be—agents update pricing; forum posts do not auto-update.",
    "Minimum fees exist sometimes—small orders hurt proportionally more.",
    "Payment processor charges may apply on top—read checkout carefully.",
    "Discount codes? Maybe—{name}’s site, not ours.",
    "Fee transparency is a feature—if you cannot find fees, pause before you pay.",
    "Hidden fees are often user error—read the breakdown slowly.",
    "Service fee vs shipping fee: two wallets, one headache—track both.",
    "If fees feel unfair, compare agents—but compare totals, not headline percentages.",
    "We mention fees often because surprises hurt worse than repetition.",
]

READ_LISTING_POOL: list[str] = [
    "Hero images lie; scroll for secondary shots, flat measurements, and stock status language before you trust a tile.",
    "If color names look translated oddly, trust numbers on the size chart more than adjectives in the title.",
    "Variant IDs matter: screenshot the exact SKU you want so warehouse photos can be compared apples to apples.",
    "Read the boring lines—material percentages, weight, pack contents—before you romanticize the hero shot.",
    "If the listing shows five colors but stock says three, trust stock.",
    "Sometimes “one size” means “one size fits nobody”—measure anyway.",
    "Seller badges and ratings are hints, not promises—especially on fast-moving fashion.",
    "If something is “random batch,” random is doing a lot of work—ask what it means in practice.",
    "Look for domestic shipping time estimates—your agent clock starts after the seller ships.",
    "Watermarks on photos can hide flaws—zoom like you mean it.",
    "If the listing mixes languages, numeric tables are the Rosetta stone.",
    "Returns language matters before you buy—after warehouse QC, rules tighten.",
    "Compare seller answers to listing text—contradictions are a red flag.",
    "If a detail is missing, assume worst case for sizing and timeline.",
    "The listing is the contract’s rough draft—your order details are the draft you sign.",
]

IMG_SEARCH_POOL: list[str] = [
    "Image search shines when vocabulary fails—upload the reference, scan neighbors, then read text on MaisonLooks carefully.",
    "When keywords return noise, a picture narrows candidates; still verify material and batch notes on the listing body.",
    "Think of image search as triage, not proof—lighting differs, so QC at the agent remains essential.",
    "Crop aggressively: less background, more product—search works better with signal.",
    "If you upload a meme, expect meme-adjacent results—humor is not a SKU.",
    "Similarity scores are fuzzy—human eyes still arbitrate taste.",
    "Reverse search can surface dupes and scams—cross-check seller reputation on the listing.",
    "Sometimes the best image is a side profile—angles matter for shoes.",
    "If results are too broad, add a keyword after the image pass—combine modes.",
    "Image search cannot read minds—only pixels.",
    "Blurry uploads yield blurry matches—get the clearest screenshot you can.",
    "If you find a visual twin, compare price deltas—too-good prices need extra scrutiny.",
    "Image search is great for “what is this called?”—bad for “is this legal here?”",
    "Use image search after TikTok, before impulse—still sleep on it.",
    "The best image search session ends on a listing with measurements—not on a tile alone.",
]

# Step lines: index 0..6, each pool has distinct micro-copy (same intent).
STEP_POOLS: list[list[str]] = [
    [
        "<strong>Start on the home grid</strong> — open <a href=\"index.html\">the spreadsheet home</a>, scroll, and let rows load; or start with search / image search if you already have a clue.",
        "<strong>Open the listing</strong> — click a card; MaisonLooks should open in a new tab with variants and seller copy.",
        "<strong>Read carefully</strong> — confirm measurements, color codes, batch language, and whether stock is live or pre-order.",
        "<strong>Copy what {name} expects</strong> — full URL, item ID, or notes—follow their submission form, not a chat screenshot.",
        "<strong>Pay on the agent</strong> — use <a href=\"{official_url}\" target=\"_blank\" rel=\"noopener noreferrer\">{host_label}</a> (logged-in balance or checkout); ignore payment requests in unsolicited messages.",
        "<strong>QC before international ship</strong> — zoom warehouse photos; ask for retakes while return windows still exist.",
        "<strong>Pick a freight line &amp; declare honestly</strong> — country rules differ; lean on {name} docs plus your local experience.",
    ],
    [
        "<strong>Land on the grid</strong> — <a href=\"index.html\">home</a> first; search if you are not in a scrolling mood.",
        "<strong>Click through</strong> — let MaisonLooks own the details; our card is only a preview.",
        "<strong>Interrogate the listing</strong> — size charts, stock flags, and fine print beat the tile’s vibe.",
        "<strong>Paste into {name}</strong> — match their expected format; screenshots are backup, not primary input.",
        "<strong>Fund on {host_label}</strong> — cards, wallets, top-ups—whatever {name} allows, inside their UI.",
        "<strong>Warehouse photos</strong> — approve or request retakes; this is your last cheap exit.",
        "<strong>Ship</strong> — choose a line, declare, pray to the customs gods responsibly.",
    ],
    [
        "<strong>Browse</strong> — infinite scroll until something stops your thumb.",
        "<strong>Deep-link</strong> — new tab, full context—no iframe cosplay.",
        "<strong>Verify</strong> — if the listing contradicts the tile, trust the listing.",
        "<strong>Submit</strong> — {name}’s form, not a Google Form from a stranger.",
        "<strong>Pay</strong> — only where SSL and your saved bookmark say {host_label}.",
        "<strong>Inspect QC</strong> — pixels cost money; zoom them.",
        "<strong>Export</strong> — pick a route, insure if needed, track like your money depends on it—because it does.",
    ],
]
