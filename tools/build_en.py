"""Build en/index.html from index.html by replacing each French string with its English version.
Every French string must be found exactly once (or the listed count), so the build fails loudly
if the French page changes and a translation goes stale. Run: python3 tools/build_en.py
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
fr = (ROOT / "index.html").read_text(encoding="utf-8")

PAIRS = [
    # document & meta
    ('<html lang="fr">', '<html lang="en">'),
    ("<title>Coach Agile à Lille | Mattieu Bernard-Guêle</title>", "<title>Agile Coach in Lille | Mattieu Bernard-Guêle</title>"),
    ('content="Coach agile freelance à Lille. Transformation à l\'échelle, passage du projet au produit, SAFe, PI Planning et pilotage de la delivery. MBG Consulting."',
     'content="Freelance agile coach in Lille, France. Large-scale transformation, project-to-product shift, SAFe, PI Planning and delivery steering. MBG Consulting."'),
    ('<meta property="og:locale" content="fr_FR">', '<meta property="og:locale" content="en_GB">'),
    ('content="Coach Agile à Lille | Mattieu Bernard-Guêle"', 'content="Agile Coach in Lille | Mattieu Bernard-Guêle"'),
    ('content="Coach agile freelance à Lille. Transformation à l\'échelle, passage du projet au produit, SAFe, PI Planning et pilotage de la delivery."',
     'content="Freelance agile coach in Lille, France. Large-scale transformation, project-to-product shift, SAFe, PI Planning and delivery steering."'),
    ('content="assets/mattieu', 'content="../assets/mattieu'),
    ('<link rel="stylesheet" href="assets/site.css?v=2">', '<link rel="stylesheet" href="../assets/site.css">'),
    ('<link rel="alternate" hreflang="fr" href="./">\n<link rel="alternate" hreflang="en" href="en/">',
     '<link rel="alternate" hreflang="fr" href="../">\n<link rel="alternate" hreflang="en" href="./">'),
    # header
    ('Aller au contenu', 'Skip to content'),
    ('<a href="#a-propos"><b>01</b>À propos</a>', '<a href="#a-propos"><b>01</b>About</a>', 2),
    ('<a href="#expertises"><b>02</b>Expertises</a>', '<a href="#expertises"><b>02</b>Expertise</a>', 2),
    ('<a href="#parcours"><b>03</b>Parcours</a>', '<a href="#parcours"><b>03</b>Background</a>', 2),
    ('aria-label="Sections"', 'aria-label="Sections"', 2),
    ('<div class="lang"><a href="./" aria-current="page" lang="fr" title="Français">FR</a><span>/</span><a href="en/" lang="en" hreflang="en" title="English">EN</a></div>',
     '<div class="lang"><a href="../" lang="fr" hreflang="fr" title="Français">FR</a><span>/</span><a href="./" aria-current="page" lang="en" title="English">EN</a></div>'),
    ('aria-label="LinkedIn (nouvelle fenêtre)"', 'aria-label="LinkedIn (new window)"'),
    ('aria-label="Ouvrir le menu"', 'aria-label="Open menu"'),
    ("btn.setAttribute('aria-label',open?'Fermer le menu':'Ouvrir le menu');", "btn.setAttribute('aria-label',open?'Close menu':'Open menu');"),
    # hero
    ("— Coach agile, transformation à l'échelle &amp; entrepreneur · Lille", "— Agile coach, large-scale transformation &amp; entrepreneur · Lille"),
    ('<p class="tagline">Je fais <mark>bouger les lignes</mark>.</p>', '<p class="tagline">I get things <mark>moving</mark>.</p>'),
    ("<u>Planification qui ne tient pas</u>, <u>transformation qui s'essouffle</u>, <u>équipes en silos</u>, <u>delivery imprévisible</u> : j'aide les organisations à embarquer leurs équipes et à livrer de la valeur, durablement.",
     "<u>Plans that don't hold</u>, <u>a transformation running out of steam</u>, <u>siloed teams</u>, <u>unpredictable delivery</u>: I help organisations bring their teams on board and deliver value, for the long run."),
    ('Me contacter sur LinkedIn</a>', 'Contact me on LinkedIn</a>', 2),
    ('<a class="btn btn-ghost" href="#expertises">Voir mes expertises</a>', '<a class="btn btn-ghost" href="#expertises">See my expertise</a>'),
    ('<dd>Lille · Hauts-de-France</dd>', '<dd>Lille · Northern France</dd>'),
    ('<dt class="mono">Statut</dt>', '<dt class="mono">Status</dt>'),
    ('src="assets/mattieu', 'src="../assets/mattieu'),
    ('alt="Mattieu Bernard-Guêle, coach agile à Lille, portrait en noir et blanc, assis sur des marches en pierre"',
     'alt="Mattieu Bernard-Guêle, agile coach in Lille, black and white portrait, sitting on stone steps"'),
    # about
    ('<h2>À propos</h2>', '<h2>About</h2>'),
    ("Coach agile freelance basé à Lille, j'accompagne des organisations dans leur transformation à grande échelle : passage du mode projet au mode produit, agilité à l'échelle avec SAFe, pilotage par la valeur et par les indicateurs de delivery. Je travaille au plus près des équipes, des Product Owners et des managers, avec une conviction : une transformation tient quand les gens ont envie d'y prendre part.",
     "I'm a freelance agile coach based in Lille, helping organisations through large-scale transformation: moving from projects to products, scaling agility with SAFe, and steering by value and delivery metrics. I work closely with teams, Product Owners and managers, with one conviction: a transformation lasts when people want to be part of it."),
    ("Et je vis de l'intérieur ce que j'accompagne : entrepreneur dans l'âme, je me suis aussi lancé il y a quelques mois dans une nouvelle aventure, la location de matériel événementiel.",
     "And I live what I coach from the inside: an entrepreneur at heart, a few months ago I also started a new venture in event equipment rental."),
    ("Origines tech : formé à Epitech, j'ai été développeur .NET avant de basculer vers l'agilité en 2019. Je parle le langage des équipes que j'accompagne.",
     "Tech roots: trained at Epitech, I worked as a .NET developer before moving into agility in 2019. I speak the language of the teams I coach."),
    ("J'interviens à Lille, dans sa métropole et plus largement dans les Hauts-de-France.",
     "I work in Lille, its metropolitan area and across the Hauts-de-France region."),
    ('➿ projets accompagnés', '➿ projects supported'),
    ('👥 équipes accompagnées', '👥 teams coached'),
    ('🍖 ROTI demandés', '🍖 ROTI votes collected'),
    ('❤️ sourires distribués', '❤️ smiles shared'),
    # expertise
    ('<h2>Expertises</h2>', '<h2>Expertise</h2>'),
    ("Six terrains d'intervention, rarement isolés : un Program Increment qui ne tient pas cache souvent des dépendances mal pilotées, et un delivery imprévisible, une priorisation qui ne parle pas de valeur. Chaque carte indique ses dépendances.",
     "Six areas of work, rarely isolated: a Program Increment that doesn't hold often hides poorly managed dependencies, and unpredictable delivery often hides prioritisation that ignores value. Each card shows its dependencies."),
    ("<h3>Agilité à l'échelle</h3>", "<h3>Agility at scale</h3>"),
    ("Mise en place et animation d'un Agile Release Train : PI Planning, synchronisation multi-équipes, Inspect &amp; Adapt.",
     "Setting up and running an Agile Release Train: PI Planning, cross-team synchronisation, Inspect &amp; Adapt."),
    ('<p class="deps">Dépend de', '<p class="deps">Depends on', 5),
    ('<h3>Du projet au produit</h3>', '<h3>From project to product</h3>'),
    ("Faire passer une organisation d'une logique projet à une logique produit : rôles, gouvernance, communautés de pratique.",
     "Moving an organisation from project thinking to product thinking: roles, governance, communities of practice."),
    ('<li>Rôles</li><li>Gouvernance</li>', '<li>Roles</li><li>Governance</li>'),
    ("<h3>Coaching d'équipes et de leaders</h3>", "<h3>Coaching teams and leaders</h3>"),
    ("Accompagnement des équipes, Scrum Masters, Product Owners et managers, sur leurs vrais sujets et dans la durée.",
     "Supporting teams, Scrum Masters, Product Owners and managers on their real issues, over time."),
    ('<li>Équipes</li><li>PO &amp; SM</li><li>Managers</li><li>Changement</li>', '<li>Teams</li><li>PO &amp; SM</li><li>Managers</li><li>Change</li>'),
    ('<h3>Risques et dépendances</h3>', '<h3>Risks and dependencies</h3>'),
    ("Rendre visibles les risques et les dépendances entre équipes, puis les traiter avant qu'ils ne bloquent la delivery.",
     "Making risks and cross-team dependencies visible, then handling them before they block delivery."),
    ('<li>Dépendances</li>', '<li>Dependencies</li>'),
    ('<h3>Priorisation par la valeur</h3>', '<h3>Value-based prioritisation</h3>'),
    ("Relier la stratégie aux équipes et arbitrer sur la valeur métier plutôt que sur l'urgence du moment.",
     "Connecting strategy to teams and deciding on business value rather than on whatever feels urgent."),
    ('<h3>Delivery et performance</h3>', '<h3>Delivery and performance</h3>'),
    ("Mesurer pour progresser : fiabilité des engagements, prévisibilité, indicateurs DORA, avec Jira comme source de vérité.",
     "Measuring to improve: commitment reliability, predictability, DORA metrics, with Jira as the single source of truth."),
    ('<li>Prévisibilité</li><li>Jira</li><li>Amélioration continue</li>', '<li>Predictability</li><li>Jira</li><li>Continuous improvement</li>'),
    ('<p class="deps">Alimente', '<p class="deps">Feeds'),
    # background
    ('<h2>Parcours</h2>', '<h2>Background</h2>'),
    ("Version condensée. Le détail, mission par mission, est sur LinkedIn.", "The short version. Mission-by-mission detail is on LinkedIn."),
    ('<p class="when">Depuis fin 2024</p>', '<p class="when">Since late 2024</p>'),
    ('<h3>Fondateur &amp; Coach Agile - Produit <span>· MBG Consulting</span></h3>', '<h3>Founder &amp; Agile - Product Coach <span>· MBG Consulting</span></h3>'),
    ("Missions freelance de coaching agile et d'accompagnement de transformations à l'échelle.",
     "Freelance missions in agile coaching and large-scale transformation support."),
    ('<p class="when">Depuis oct. 2024</p>', '<p class="when">Since Oct. 2024</p>'),
    ("Transformation agile à l'échelle, du mode projet vers une culture produit : facilitation du PI Planning, de l'ART Sync et de l'Inspect &amp; Adapt, pilotage des dépendances et des risques, suivi du respect des engagements PI et des indicateurs DORA.",
     "Agile transformation at scale, from project mode to a product culture: facilitating PI Planning, ART Sync and Inspect &amp; Adapt, managing dependencies and risks, tracking PI commitment reliability and DORA metrics."),
    ('<h3>Scrum Master puis Coach Agile <span>· Decathlon (via sumit, puis en indépendant)</span></h3>',
     '<h3>Scrum Master then Agile Coach <span>· Decathlon (via sumit, then freelance)</span></h3>'),
    ("Scrum Master d'une équipe front e-commerce passée de 7 à environ 50 personnes, cofondateur du collectif agile qui accompagnait les 20 équipes e-commerce, puis coach des équipes Cloud Platform Engineering.",
     "Scrum Master for an e-commerce front-end team that grew from 7 to about 50 people, co-founder of the agile collective supporting all 20 e-commerce teams, then coach for the Cloud Platform Engineering teams."),
    ("Garant du cadre agile de la direction projet et référent de l'offre agile : formation et accompagnement des collaborateurs.",
     "Guardian of the project department's agile framework and lead for the agile offer: training and coaching colleagues."),
    ('<h3>Origines tech <span>· Epitech, sumit</span></h3>', '<h3>Tech roots <span>· Epitech, sumit</span></h3>'),
    ("Formation d'ingénierie logicielle à Epitech, puis développeur .NET / C#.", "Software engineering training at Epitech, then .NET / C# developer."),
    ('>Parcours complet sur LinkedIn</a>', '>Full background on LinkedIn</a>'),
    ("<p>« Il ne se contente pas d'accompagner le changement : il donne envie d'y prendre part. »</p>",
     "<p>“He doesn't just support change: he makes people want to be part of it.”</p>"),
    ('Simon Aubry · recommandation LinkedIn', 'Simon Aubry · LinkedIn recommendation (translated)'),
    ("<h3 class=\"subhead\">Ils m'ont fait confiance</h3>", '<h3 class="subhead">They trusted me</h3>'),
    ('<h3 class="subhead">Transmission et communauté</h3>', '<h3 class="subhead">Community and sharing</h3>'),
    ("Vice-trésorier puis secrétaire de l'association de 2019 à 2025, organisation de meetups.",
     "Vice-treasurer then secretary of the association from 2019 to 2025, organising meetups."),
    ("Co-organisation du congrès agile annuel de Lille, en charge de la communication.",
     "Co-organiser of Lille's annual agile conference, in charge of communication."),
    ("Cofondateur de ces rencontres informelles entre praticiens de l'agilité.",
     "Co-founder of these informal meetups for agile practitioners."),
    # venture
    ("Il y a quelques mois, j'ai repris Puzzl Event, une entreprise de location de matériel et de prestations événementielles dans la métropole lilloise : photobooths, tentes, DJ, décoration. Mariages, soirées d'entreprise, anniversaires : un seul interlocuteur pour tout l'événement.",
     "A few months ago I took over Puzzl Event, an event equipment rental and services company in the Lille area: photobooths, tents, DJs, decoration. Weddings, corporate parties, birthdays: one point of contact for the whole event."),
    ("Reprendre une entreprise m'apprend ce qu'aucun framework n'enseigne : arbitrer avec peu de moyens, tenir une promesse client un samedi soir, et décider vite quand le plan ne se déroule pas comme prévu.",
     "Running a business teaches me what no framework does: making trade-offs with limited means, keeping a promise to a client on a Saturday night, and deciding fast when the plan falls apart."),
    ("C'est cette réalité terrain que j'apporte dans mes missions.", "I bring that field reality into every mission."),
    ('<h3>Expérience client</h3><p>Chaque événement est unique, et le client ne voit que le résultat. Tout le reste doit suivre.</p>',
     '<h3>Customer experience</h3><p>Every event is unique, and the client only sees the result. Everything else has to follow.</p>'),
    ('<h3>Réalité terrain</h3><p>Logistique, équipes, imprévus : la stratégie se vérifie le jour J, pas dans un tableau.</p>',
     '<h3>Field reality</h3><p>Logistics, people, the unexpected: strategy gets tested on the day, not in a spreadsheet.</p>'),
    ('Une entreprise construite sur le terrain : offre, clients, équipes et logistique.', 'A business built in the field: offer, clients, people and logistics.'),
    ('>Découvrir puzzl-event.fr</a>', '>Visit puzzl-event.fr</a>'),
    # consulting
    ("Ma société de conseil, basée à Lille : la structure de mes missions freelance de coaching agile et d'accompagnement de transformations. Trois piliers : les personnes, la performance collective, l'impact business.",
     "My consulting company, operating from Lille: the structure behind my freelance agile coaching and transformation missions. Three pillars: people, collective performance, business impact."),
    ('<h3>Coaching agile</h3><p>Équipes, Scrum Masters, Product Owners et managers, sur le terrain.</p>',
     '<h3>Agile coaching</h3><p>Teams, Scrum Masters, Product Owners and managers, on the ground.</p>'),
    ("<h3>Accompagnement de transformations</h3><p>Du projet au produit, agilité à l'échelle, PI Planning et synchronisation des équipes.</p>",
     "<h3>Transformation support</h3><p>From project to product, agility at scale, PI Planning and team synchronisation.</p>"),
    ('<h3>Pilotage et performance</h3><p>Indicateurs de delivery, prévisibilité, DORA et outillage Jira au service des décisions.</p>',
     '<h3>Steering and performance</h3><p>Delivery metrics, predictability, DORA and Jira tooling that support decisions.</p>'),
    ('<dt class="mono">Forme</dt>', '<dt class="mono">Legal form</dt>'),
    ('<dt class="mono">Activité</dt>', '<dt class="mono">Based in</dt>'),
    ('<dt class="mono">Depuis</dt>', '<dt class="mono">Since</dt>'),
    ('<a href="mentions-legales.html">Mentions légales →</a>', '<a href="../mentions-legales.html">Legal notice (French) →</a>'),
    # faq
    ('<h2>Questions fréquentes</h2>', '<h2>Frequently asked questions</h2>'),
    ("Ce que l'on me demande le plus souvent avant de démarrer une mission de coaching agile.",
     "What I'm asked most often before starting an agile coaching mission."),
    ("<h3>Qu'est-ce qu'un coach agile ?</h3>", "<h3>What does an agile coach do?</h3>"),
    ("Un coach agile aide une organisation à mieux travailler ensemble pour livrer de la valeur : clarifier les rôles, installer des rituels qui servent vraiment, synchroniser les équipes, rendre visibles les risques et les dépendances, et mesurer les progrès. Je travaille aux côtés des équipes, des Product Owners, des Scrum Masters et des managers, sur leurs vrais sujets.",
     "An agile coach helps an organisation work better together to deliver value: clarifying roles, setting up rituals that are actually useful, synchronising teams, making risks and dependencies visible, and measuring progress. I work alongside teams, Product Owners, Scrum Masters and managers, on their real issues."),
    ("<h3>Quelle différence entre un coach agile et un Scrum Master ?</h3>", "<h3>How is an agile coach different from a Scrum Master?</h3>"),
    ("Le Scrum Master accompagne une équipe au quotidien. Le coach agile intervient à l'échelle de plusieurs équipes et de l'organisation : agilité à l'échelle, transformation du mode projet vers le mode produit, coaching des managers et des Scrum Masters eux-mêmes. Les blocages se situent presque toujours entre les équipes, c'est là que j'interviens.",
     "A Scrum Master supports one team day to day. An agile coach works across several teams and the wider organisation: agility at scale, the shift from projects to products, coaching managers and Scrum Masters themselves. The blockers almost always sit between teams, and that's where I step in."),
    ("<h3>Où intervenez-vous ?</h3>", "<h3>Where do you work?</h3>"),
    ('<dt class="mono">Origines</dt>', '<dt class="mono">Roots</dt>'),
    ("Je suis basé à Lille et j'interviens sur site dans la métropole lilloise et dans les Hauts-de-France. Pour une autre région ou un format à distance, parlons-en.",
     "I'm based in Lille and work on site across the Lille area and the Hauts-de-France region. For another region or a remote setup, let's talk."),
    ("<h3>Quels types de missions proposez-vous ?</h3>", "<h3>What kinds of missions do you take on?</h3>"),
    ("Des missions freelance de coaching agile via MBG Consulting, l'accompagnement de transformations à l'échelle (SAFe, PI Planning, passage au mode produit), le coaching de Scrum Masters, de Product Owners et de managers, et la mise en place d'indicateurs de pilotage de la delivery.",
     "Freelance agile coaching through MBG Consulting, large-scale transformation support (SAFe, PI Planning, the move to product mode), coaching Scrum Masters, Product Owners and managers, and setting up delivery steering metrics."),
    ("<h3>Accompagnez-vous les petites structures comme les grands groupes ?</h3>", "<h3>Do you work with small companies as well as large groups?</h3>"),
    ("Oui. J'ai accompagné de grandes organisations comme Decathlon, avec ses 20 équipes e-commerce, ou WayKonect et son train agile, et je vis au quotidien la réalité d'une petite entreprise en tant qu'entrepreneur. Je connais la coordination de dizaines d'équipes autant que les arbitrages avec peu de moyens.",
     "Yes. I've supported large organisations such as Decathlon and its 20 e-commerce teams, or WayKonect and its agile release train, and as an entrepreneur I live the reality of a small business every day. I know how to coordinate dozens of teams as well as how to make trade-offs with limited means."),
    ("<h3>Comment démarrer ?</h3>", "<h3>How do we get started?</h3>"),
    ("Appelez-moi, écrivez-moi par email ou sur LinkedIn. On fait le point sur votre contexte et sur ce qui coince, sans engagement.",
     "Call me, email me or message me on LinkedIn. We'll look at your context and what's getting stuck, with no commitment."),
    ('<dt class="mono">Téléphone</dt><dd><a href="tel:+33627321270">06 27 32 12 70</a></dd>', '<dt class="mono">Phone</dt><dd><a href="tel:+33627321270">+33 6 27 32 12 70</a></dd>'),
    # contact & footer
    ("<h2>Une transformation à relancer, des équipes à embarquer ? Parlons-en.</h2>",
     "<h2>A transformation to restart, teams to bring on board? Let's talk.</h2>"),
    ("Par téléphone, par email ou sur LinkedIn : je réponds rapidement. Pas de formulaire sur ce site.",
     "By phone, by email or on LinkedIn: I reply quickly. No form on this site."),
    ("© 2026 MBG Consulting · Site statique, sans cookie.", "© 2026 MBG Consulting · Static site, no cookies."),
    ('aria-label="Liens"', 'aria-label="Links"'),
    ('<a href="mentions-legales.html">Mentions légales</a>', '<a href="../mentions-legales.html">Legal notice</a>'),
    ('<a href="#top">Haut de page ↑</a>', '<a href="#top">Back to top ↑</a>'),
]

out = fr
errors = []
for p in PAIRS:
    src, dst = p[0], p[1]
    n = p[2] if len(p) > 2 else 1
    found = out.count(src)
    if found != n:
        errors.append(f"expected {n}x, found {found}x: {src[:80]!r}")
        continue
    out = out.replace(src, dst)

if errors:
    print("Translation build failed:\n  " + "\n  ".join(errors))
    sys.exit(1)

(ROOT / "en").mkdir(exist_ok=True)
(ROOT / "en" / "index.html").write_text(out, encoding="utf-8")
print("en/index.html written")
