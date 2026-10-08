# Jetty-by-jetty review of 7 Oct 2026, read on USGS NAIP imagery (USGSNAIPPlus exportImage and
# USGSImageryOnly tiles) in the author's Chrome. One record per structure.
#   ways: OpenStreetMap way ids whose geometry was checked against the imagery and kept
#   add:  extra vertices read off the imagery ([lat, lon]), appended to the end of the named way
#         ('tip') or drawn as their own line ('line')
#   line: a polyline traced on the imagery ([lat, lon] vertices), used where OSM and ENC lack it
#   enc:  indexes into the ENC shoreline-construction extract (enc-jetties.json)
#   shore: where the structure meets today's shoreline, for the 1,500 yd long-jetty test
#   img: imagery the trace was read from (NAIP, or Esri World Imagery viewed where NAIP has no cover)
#   cls:  'closed' (jetty under r. 68B-20.003(2)(d)), 'warn' (structure that may be a jetty, or a
#         jetty whose exposure could not be seen), or 'none' (recorded, not drawn)
#   seen: what the imagery shows, in words
J = []
def rec(key, name, county, ways=(), enc=(), add=None, line=None, cls='closed', seen='', note='',
        fwc=None, shore=None, img='NAIP'):
    J.append(dict(key=key, name=name, county=county, ways=list(ways), enc=list(enc), add=add or {},
                  line=line, cls=cls, seen=seen, note=note, fwc=fwc, shore=shore, img=img))

rec('stmarys-s', 'St. Marys Entrance south jetty', 'Nassau', ways=[226293254],
    add={'tip': [[30.70830, -81.40265]]}, cls='closed',
    seen='Rock line runs from the Fort Clinch beach about 2.3 km ENE; the outer part shows only as a '
         'line of breaking water, so it is awash or just submerged at the time of the photograph. '
         'Breaking continues about 320 m past the end of the OSM line; drawn to there.',
    shore=[30.70047, -81.42839],
    note='Coast Pilot 4 describes both St. Marys jetties as almost entirely submerged at mean high '
         'water. The rule buffers only the unsubmerged portion; which parts uncover at low water '
         'cannot be told from one photograph, so the whole visible line is drawn (the reading that '
         'closes more water).')
rec('stmarys-n', 'St. Marys Entrance north jetty (Georgia)', 'Camden, GA', ways=[233046635], cls='none',
    seen='Roots on Cumberland Island, Georgia.',
    note='Georgia water; the Florida rule does not reach it. Not drawn.')

rec('stjohns-n', 'St. Johns River entrance north jetty', 'Duval',
    line=[[30.40483, -81.40355], [30.40387, -81.40075], [30.40281, -81.39479], [30.40181, -81.38662],
          [30.40095, -81.37774]], shore=[30.40342, -81.39876], img='NAIP; first read on Esri World Imagery offshore and confirmed on a later NAIP frame that covers the tip',
    seen='Continuous rock above water from the Huguenot spit to the tip, about 2.3 km seaward of the beach. '
         'The rock also runs west along the spit; traced to where it leaves the open beach.',
    note='Not in OpenStreetMap or the ENC shoreline-construction layers. The older westward extension '
         'toward Fort George Island along the north bank is not traced.')
rec('stjohns-s', 'St. Johns River entrance south jetty', 'Duval',
    line=[[30.39740, -81.39154], [30.39743, -81.38723], [30.39714, -81.38297], [30.39674, -81.37843],
          [30.39635, -81.37553]], shore=[30.39733, -81.39149],
    img='NAIP (re-traced in the check pass; the first trace on Esri imagery sat up to 40 m south of the rock)',
    seen='Continuous rock above water from the Mayport beach to the tip, about 1.4 km seaward of the beach.',
    note='The water around the tip is also closed at all times under 33 C.F.R. 334.500.')
rec('milepoint', 'St. Johns River, Mile Point training wall ("Little Jetties")', 'Duval', cls='warn',
    line=None, add={'marker': [[30.3925, -81.4245]]},
    seen='A straight rock training wall on the north bank at Mile Point, inside the river.',
    note='An inner-river training wall. Whether a training wall is a "jetty" is not settled; drawn as a '
         'marker with a warning, not traced.')
rec('staug-n', 'St. Augustine Inlet north terminal groin (Porpoise Point)', 'St. Johns',
    line=[[29.91391, -81.29027], [29.91433, -81.28891], [29.91468, -81.28760]], shore=[29.91391, -81.29027],
    seen='Short rock groin running ENE from the Porpoise Point beach, about 260 m, rock above water.',
    note='The Corps calls it a terminal groin; drawn as a jetty (the reading that closes more water).')
rec('staug-s', 'St. Augustine Inlet south jetty (Conch Island)', 'St. Johns', ways=[1204280171],
    seen='Rock line along the north shore of Conch Island, now largely the shoreline itself after accretion.',
    note='OpenStreetMap line matches the edge of the rock on the imagery.')
rec('ponce-n', 'Ponce de Leon Inlet north jetty and weir section', 'Volusia', ways=[984858414, 984853666, 984853664],
    seen='Rock jetty from the beach about 1 km seaward, above water to the tip; the old weir section runs '
         'west along the inlet shore to Lighthouse Point Park.',
    note='About 1,100 yd seaward of the beach on the imagery, under the 1,500 yd long-jetty threshold.')
rec('ponce-s', 'Ponce de Leon Inlet south jetty (Smyrna Dunes)', 'Volusia', ways=[456255017],
    seen='Only a short section, about 230 m, shows above water off the Smyrna Dunes beach.',
    note='The documented structure is about 4,000 ft; the rest is buried or submerged. Only the visible '
         'section is buffered, as the rule reaches the unsubmerged portion only.')
rec('canaveral-s', 'Port Canaveral south jetty (Jetty Park)', 'Brevard', enc=[454],
    line=[[28.40812, -80.59074], [28.40810, -80.58861], [28.40804, -80.58748], [28.40791, -80.58651]],
    shore=[28.40805, -80.58875],
    seen='Fishing walkway along the inner part, then rock above water to a rounded tip about 210 m past the beach.',
    note='OpenStreetMap carries only the park outline here; the ENC line covers part of the rock. Traced on NAIP.')
rec('canaveral-n', 'Port Canaveral north jetty', 'Brevard',
    line=[[28.41251, -80.58663], [28.41192, -80.58535], [28.41133, -80.58421], [28.41124, -80.58350],
          [28.41116, -80.58268]], shore=[28.41133, -80.58421],
    seen='Rock revetment along the inlet north shore joins the jetty at the beach; rock above water to the tip, '
         'about 150 m past the beach.',
    note='The revetment along the inlet shore is drawn as part of the jetty. Cape Canaveral Space Force Station '
         'restricted areas also apply near here.')
rec('sebastian-n', 'Sebastian Inlet north jetty', 'Brevard', ways=[42367225], enc=[822],
    seen='Curved fishing jetty with walkway from the beach about 230 m seaward; OSM and ENC lines match the structure.',
    fwc='Sebastian Inlet State Park - North Jetty')
rec('sebastian-s', 'Sebastian Inlet south jetty', 'Indian River', ways=[455483677],
    seen='Rock jetty from the south beach about 110 m seaward; OSM line matches.',
    fwc='Sebastian Inlet State Park - South Jetty')
rec('sebastian-inner', 'Sebastian Inlet, rock structures inside the inlet', 'Brevard / Indian River',
    ways=[455483671, 455483673], cls='warn',
    seen='Two straight rock lines inside the inlet west of the A1A bridge, mapped as breakwaters in OSM.',
    note='Inside the inlet rather than at its mouth; may be revetments. Drawn as may-be-a-jetty. State park '
         'water rules also apply in the park.')
rec('ftpierce-n', 'Fort Pierce Inlet north jetty', 'St. Lucie', ways=[988655846],
    seen='Rock jetty from the Fort Pierce Inlet State Park beach about 450 m seaward; OSM matches.',
    note='The state park water closure, r. 68B-20.003(2)(e), also applies along the park shore.')
rec('ftpierce-s', 'Fort Pierce Inlet south jetty and spur (Jetty Park)', 'St. Lucie', ways=[986788831, 986788830],
    seen='Rock jetty with fishing walkway and a short spur groin, plus the rock revetment where it joins the inlet shore.',
    fwc='Ft. Pierce Jetty Park')
rec('ftpierce-sshore', 'Fort Pierce Inlet south shore revetment', 'St. Lucie', ways=[986786515, 986786513], cls='warn',
    seen='Rock revetment along the inlet south shore west of Jetty Park.',
    note='A shoreline revetment rather than a jetty on the usual reading; drawn as may-be-a-jetty.')
rec('stlucie-n', 'St. Lucie Inlet north jetty (Sailfish Point) with weir section', 'Martin',
    ways=[979834682, 675885303, 979834683, 979835962],
    seen='Rock jetty from the Sailfish Point beach east then south-east (dog-leg), about 350 m; the weir '
         'section runs west along the inlet shore. The outer leg is faint on the imagery and may be awash.',
    note='Whole OSM line drawn; the outer leg may be below water at high tide (reading that closes more water).')
rec('stlucie-breakwater', 'St. Lucie Inlet detached breakwater', 'Martin', ways=[675885302], enc=[726, 297], cls='warn',
    seen='Detached rock breakwater south of the entrance channel, charted always dry.',
    note='Not attached to the shore. Whether a detached breakwater is a "jetty" is not settled; drawn as '
         'may-be-a-jetty.')
rec('stlucie-s', 'St. Lucie Inlet south jetty (Jupiter Island)', 'Martin', cls='none',
    seen='No rock above water visible at the north tip of Jupiter Island.',
    note='The documented south jetty (1978 to 1982) is buried or submerged. The adjoining St. Lucie Inlet '
         'Preserve State Park water is closed under r. 68B-20.003(2)(e) in any case.')
rec('jupiter-n', 'Jupiter Inlet north jetty', 'Palm Beach', ways=[],
    line=[[26.94500, -80.07310], [26.94484, -80.07232], [26.94472, -80.07146], [26.94462, -80.07061]],
    shore=[26.94472, -80.07146],
    seen='Rock jetty from inside the inlet past the Jupiter Inlet Colony beach to a tip about 85 m seaward.',
    note='OSM way 567630954 covers only the inner end; traced on NAIP.')
rec('jupiter-s', 'Jupiter Inlet south jetty (Jupiter Beach Park)', 'Palm Beach',
    line=[[26.94389, -80.07409], [26.94384, -80.07260], [26.94374, -80.07146], [26.94351, -80.07076],
          [26.94332, -80.07047]], shore=[26.94374, -80.07146],
    seen='Rock jetty along the inlet south shore with a walkway, curving to a tip about 120 m past the beach.',
    fwc='Jupiter Beach Park')
rec('jupiter-dubois', 'Jupiter Inlet, small breakwaters at DuBois Park', 'Palm Beach',
    ways=[558948388, 558948389, 558948398, 558948401, 558948407, 558948408, 558948418], enc=[280, 281, 293, 294, 296],
    cls='warn', seen='Short rock breakwaters around the DuBois Park swimming lagoon inside the inlet.',
    note='Small shore-attached breakwaters inside the inlet; drawn as may-be-a-jetty.')
rec('lakeworth-n', 'Lake Worth (Palm Beach) Inlet north jetty', 'Palm Beach', ways=[157406226, 757984529],
    seen='Rock jetty along the Singer Island inlet shore out to a tip about 120 m past the beach; OSM matches.',
    note='Also drawn in the Palm Beach layer (jettyN, 150 ft).')
rec('lakeworth-groin', 'Lake Worth Inlet ruined L-groin north of the jetty', 'Palm Beach', enc=[442], cls='closed',
    seen='Charted groin that covers and uncovers, just north of the north jetty tip.',
    note='Also drawn in the Palm Beach layer (groin).')
rec('lakeworth-s', 'Lake Worth (Palm Beach) Inlet south jetty', 'Palm Beach', ways=[757984530],
    seen='Rock jetty from the Palm Beach shore about 300 m to the tip; OSM matches.',
    note='Also drawn in the Palm Beach layer (jettyS).')
rec('peanut-breakwaters', 'Peanut Island east shore breakwaters', 'Palm Beach',
    ways=[924718905, 924718906, 924718907, 924718908, 924718910, 924718911, 924718912, 924718913, 924718914,
          924718915, 924718916, 924718917, 924718918, 924718919, 924718920, 924718928, 924718929],
    enc=[403, 404, 405, 406, 407, 408, 409, 410, 411, 412], cls='warn',
    seen='Row of short rock breakwaters protecting the Peanut Island swimming lagoon.',
    note='Inside the Peanut Island swim-area buffer already drawn in the Palm Beach layer.')
rec('boynton-n', 'South Lake Worth (Boynton) Inlet north jetty', 'Palm Beach',
    line=[[26.54569, -80.04329], [26.54562, -80.04261], [26.54556, -80.04197], [26.54541, -80.04155],
          [26.54496, -80.04119]], shore=[26.54556, -80.04197],
    seen='Rock jetty with walkway curving south to a tip about 110 m past the beach.',
    note='Not in OpenStreetMap or ENC as a jetty; traced on NAIP.', fwc='Ocean Inlet Park - North Jetty')
rec('boynton-s', 'South Lake Worth (Boynton) Inlet south jetty', 'Palm Beach',
    line=[[26.54523, -80.04325], [26.54518, -80.04261], [26.54510, -80.04221]], shore=[26.54519, -80.04275],
    seen='Short rock jetty with walkway, tip about 50 m past the beach.', fwc='Ocean Inlet Park- South Jetty')
rec('boynton-inner', 'South Lake Worth Inlet, breakwaters around Bird Island and in the lagoon', 'Palm Beach',
    ways=[1558544736, 630397572], enc=[213, 214, 223, 725, 820, 849], cls='warn',
    seen='Rock breakwaters edging the spoil island and a line in the lagoon west of the inlet.',
    note='Inside the Lake Worth Lagoon; drawn as may-be-a-jetty.')
rec('boca-n', 'Boca Raton Inlet north jetty and weir', 'Palm Beach', ways=[333543563, 333543564],
    seen='Rock jetty from the north beach with the weir section, tip about 60 m past the beach; OSM matches.',
    note='Boca Raton Code also closes the inlet to swimming and diving (loc-boca-inlet).')
rec('boca-s', 'Boca Raton Inlet south jetty (South Inlet Park)', 'Palm Beach', ways=[333543565],
    seen='Rock jetty with walkway, tip about 130 m past the beach; OSM matches.', fwc='South Inlet Park')
rec('hillsboro-n', 'Hillsboro Inlet north jetty with weir and detached extension', 'Broward',
    ways=[455118862, 455118863], enc=[658, 232],
    seen='Rock jetty off the lighthouse beach running south across the inlet mouth; the middle weir section '
         'is charted as covering and uncovering.',
    note='The weir section is drawn because it uncovers at low water (the reading that closes more water).')
rec('hillsboro-s', 'Hillsboro Inlet south jetty (Pompano Beach)', 'Broward', ways=[455118864, 989054442],
    seen='Rock jetty from the Pompano Beach side running south-east to a rounded tip; OSM matches.',
    note='Pompano Beach § 91.22 also closes the inlet to swimming and diving.')
rec('pe-n', 'Port Everglades north jetty', 'Broward', ways=[963614678],
    seen='Short rock jetty at the south end of Fort Lauderdale beach, tip about 60 m past the beach; OSM matches.')
rec('pe-n-barrier', 'Port Everglades north sand-tightening barrier', 'Broward', enc=[864], cls='warn',
    seen='Charted as covering and uncovering, running east from the beach north of the north jetty.',
    note='A boulder sand barrier rather than a jetty, but it uncovers at low water; drawn as may-be-a-jetty.')
rec('pe-s', 'Port Everglades south jetty (Dr. Von D. Mizell-Eula Johnson State Park)', 'Broward', ways=[381833682],
    seen='Rock jetty from the state park shore about 120 m east; OSM matches.',
    note='State park water closure also applies.', fwc='Dr. Von D. Mizell-Eula Johnson State Park')
rec('pe-inner', 'Port Everglades, shoreline breakwaters inside the port and along the park', 'Broward',
    ways=[485952337, 485952338, 1156546933, 1156546935, 963604797, 1156912577, 827740088], enc=[472, 473, 817],
    cls='warn', seen='Short rock breakwaters along the state park shore and inside the port.',
    note='Port security zones also apply inside the harbour.')
rec('pe-submerged', 'Port Everglades offshore breakwaters', 'Broward', enc=[458, 583, 584, 585, 586, 626, 657, 815],
    cls='none', seen='Charted as always under water.',
    note='No unsubmerged portion, so r. 68B-20.003(2)(d) does not attach. Not drawn.')
rec('haulover-n', 'Bakers Haulover Inlet north jetty (Haulover Park)', 'Miami-Dade',
    line=[[25.90070, -80.12352], [25.90065, -80.12246], [25.90068, -80.12161], [25.90084, -80.12121]],
    shore=[25.90066, -80.12189],
    seen='Rock jetty along the Haulover Park inlet shore, curving north at a tip about 70 m past the beach.',
    note='Not in OpenStreetMap or ENC; traced on NAIP.')
rec('haulover-s', 'Bakers Haulover Inlet south jetty (Bal Harbour)', 'Miami-Dade', ways=[1434893036],
    seen='Rock jetty from the Bal Harbour shore east, curving south at the tip; OSM matches.',
    note='Bal Harbour § 12-7 also bans discharging spearguns in village waters.')
rec('haulover-bridge', 'Bakers Haulover bridge fender lines', 'Miami-Dade', ways=[725423254, 725423255], cls='none',
    seen='Fender lines under the A1A bridge, tagged breakwater in OSM.', note='Not jetties. Not drawn.')
rec('govcut-n', 'Government Cut north jetty (South Pointe)', 'Miami-Dade', ways=[960144936],
    seen='Jetty from South Pointe Park, walkway at the root, then rock to a tip about 530 m out; the outer '
         'part is low and may be awash at high water.', fwc='South Pointe Park',
    note='Whole OSM line drawn (the reading that closes more water).')
rec('govcut-s', 'Government Cut south jetty (Fisher Island)', 'Miami-Dade', ways=[960144937],
    seen='Low rock jetty from Fisher Island to a tip about 570 m out; faint on the imagery, probably awash in part.',
    note='Whole OSM line drawn (the reading that closes more water).')
rec('govcut-marinas', 'Miami Beach Marina and Fisher Island breakwaters', 'Miami-Dade',
    ways=[336335287, 960135966, 960135967, 960139166, 960129558, 960129559], enc=[814, 750, 372, 382, 384, 386, 389, 395, 690, 691, 692],
    cls='warn', seen='Marina breakwaters and short groins along Fisher Island and the Miami Beach Marina.',
    note='Harbour structures; drawn as may-be-a-jetty.')
rec('govcut-submerged', 'Government Cut charted submerged breakwater', 'Miami-Dade', enc=[379], cls='none',
    seen='Charted always under water.', note='Not drawn.')
rec('miamibeach-groins', 'Miami Beach 29th to 33rd Street groins', 'Miami-Dade', cls='none',
    seen='No groin or jetty shows above the beach or water between 29th and 33rd Streets on the current NAIP; '
         'the old groins appear buried by beach fill.',
    note='Miami Beach § 82-441 still bans spearfishing in the "29th to 33rd Street jetty area" (loc-miamibeach); '
         'that local closure is unaffected.')
rec('blackpoint', 'Black Point Park jetty (Black Creek channel)', 'Miami-Dade', enc=[813, 260, 858, 580],
    seen='Rock jetty with walkway along the east side of the Black Point Marina channel, about 900 m into '
         'Biscayne Bay; a lower west-side rock line is charted as covering and uncovering.',
    fwc='Black Point Park',
    note='ENC lines match the structure. The charted always-submerged pieces (581, 857) are not drawn.')
rec('keywest-harbour', 'Key West harbour moles, breakwaters and Fort Zachary Taylor groins', 'Monroe', cls='warn',
    ways=[160036583, 281172097, 338225787, 339025510, 339027525, 339027532, 493317446, 493341260, 495083110,
          495083111, 495083112, 923188816, 1158814288, 1158814289, 1158814290, 1158814291, 1158814292, 1158814293,
          1158831715, 1158972904, 1158972905, 1158972907], enc=[92, 93, 99, 105, 110],
    seen='Truman Annex moles and breakwaters, Fort Zachary Taylor beach groins, Sunset Key and Key West Bight '
         'breakwaters; all rock above water.',
    note='Drawn as may-be-a-jetty. Fort Zachary Taylor is a state park (water closed under '
         'r. 68B-20.003(2)(e)); Truman Annex water is a naval restricted area (33 C.F.R. 334.610).')
rec('eastpass-w', 'East Pass (Destin) west jetty', 'Okaloosa',
    line=[[30.38759, -86.51623], [30.38722, -86.51591], [30.38490, -86.51369], [30.38306, -86.51199],
          [30.38110, -86.51057]], shore=[30.38524, -86.51430],
    seen='Rock jetty along the west side of the pass from the Okaloosa Island shore (Eglin land, masked on '
         'NAIP) to a tip about 500 m past the Gulf beach; rock above water throughout.',
    note='Not in OpenStreetMap or ENC; traced on NAIP. The inner weir section along the pass is included.')
rec('eastpass-e', 'East Pass (Destin) east jetty and spur groin', 'Okaloosa', enc=[604, 5],
    line=[[30.38409, -86.50626], [30.38281, -86.50688], [30.38115, -86.50750]], shore=[30.38237, -86.50699],
    seen='Rock jetty from the Holiday Isle shore south to a tip about 140 m past the beach, with a spur groin '
         'at its landward end.',
    note='The OSM feature "Jetty East" is a condominium and is not used.')
rec('eastpass-misc', 'East Pass charted submerged breakwaters', 'Okaloosa', enc=[7, 794], cls='none',
    seen='Charted always under water.', note='Not drawn.')
rec('standrews-w', 'St. Andrew Bay entrance west jetty (St. Andrews State Park)', 'Bay',
    line=[[30.12525, -85.73043], [30.12455, -85.73146], [30.12363, -85.73217], [30.12243, -85.73288],
          [30.12148, -85.73368], [30.12065, -85.73472]], shore=[30.12252, -85.73323],
    seen='Rock jetty from inside the pass past the park beach to a tip about 270 m out; rock above water.',
    note='Not in OSM or ENC as a jetty; traced on NAIP and re-traced at zoom 17 in the check pass (first trace sat up to 30 m west). Inside St. Andrews State Park, whose water is also '
         'closed under r. 68B-20.003(2)(e).')
rec('standrews-e', 'St. Andrew Bay entrance east jetty (Shell Island)', 'Bay', ways=[1175993853],
    seen='Rock jetty from the Shell Island shore south-west; OSM "East Jetty" matches the visible rock.')
rec('standrews-lagoon', 'St. Andrews State Park lagoon breakwaters', 'Bay', enc=[757], cls='warn',
    seen='Short breakwaters inside the park lagoon.', note='State park water; drawn as may-be-a-jetty.')
rec('mexicobeach-w', 'Mexico Beach canal inlet west jetty', 'Bay',
    line=[[29.95051, -85.43062], [29.95014, -85.43055], [29.94982, -85.43046]], shore=[29.95014, -85.43055],
    seen='Short rock jetty on the west side of the canal mouth, tip about 40 m past the beach.',
    note='Mexico Beach § 95.03 also closes the canal inlet and 100 ft each side of the jetties to swimming.')
rec('mexicobeach-e', 'Mexico Beach canal inlet east jetty (authorized 2023)', 'Bay', cls='none',
    seen='No rock above the sand or water on the east side of the canal mouth on the current NAIP.',
    note='Authorized in 2023 (FDEP permit 0416748-001-JC); not built on the imagery. Check on site.')
rec('sikes-e', 'Bob Sikes Cut north-east jetty', 'Franklin', ways=[481942391],
    seen='Rock jetty on the east side of the cut, about 230 m; OSM matches.')
rec('sikes-w', 'Bob Sikes Cut south-west jetty', 'Franklin', ways=[751098888],
    seen='Rock jetty on the west side of the cut, about 290 m; OSM matches.')
rec('pickens', 'Fort Pickens sound-side rock jetties', 'Escambia', ways=[335229915, 335229916],
    seen='Short rock jetties off the north (Pensacola Bay) shore near Fort Pickens; rock above water.',
    note='Inside Gulf Islands National Seashore (drawn amber pending the projectile-ban question). A '
         'secondhand report says FWC treats spearing here as a jetty violation (lead only).')
rec('pickens-fort', 'Fort Pickens fort walls tagged breakwater in OSM', 'Escambia',
    ways=[334541259, 334541260, 334541261, 334541264, 334541266, 358919561], cls='none',
    seen='The OSM lines trace the fort and its walls on land.', note='Not jetties. Not drawn.')
rec('clearwater-s', 'Clearwater Pass south jetty (Sand Key Park)', 'Pinellas', enc=[772, 561],
    seen='Rock jetty along the north shore of Sand Key Park from the Gulf beach to the bridge; ENC matches.')
rec('clearwater-n', 'Clearwater Pass north side groins (Clearwater Beach)', 'Pinellas',
    ways=[1150553542, 1150553543, 1150553544, 1150553545, 1150553546, 1150553547, 1150553548, 1150553549,
          1150553550, 1150553551, 184368000, 184368014, 184368035],
    seen='Row of short rock groins along the south shore of Clearwater Beach facing the pass.',
    note='Shore-attached structures at an inlet; drawn as jetties (the reading that closes more water).')
rec('clearwater-revet', 'Clearwater Beach shoreline structure tagged breakwater', 'Pinellas', ways=[1265232968],
    cls='warn', seen='Line along the beach face west of the groins.', note='Probably a revetment; may-be-a-jetty.')
rec('johnspass-n', "John's Pass north jetty (Madeira Beach)", 'Pinellas',
    line=[[27.78299, -82.78424], [27.78307, -82.78390], [27.78323, -82.78354], [27.78339, -82.78329]],
    seen='Curved rock jetty along the south tip of the Madeira Beach shore facing the pass; rock above water.',
    note='Not in OSM or ENC; traced on NAIP. Madeira Beach § 78-3 and Treasure Island § 58-34 close the pass itself.')
rec('johnspass-s', "John's Pass south jetty (Treasure Island terminal groin)", 'Pinellas', enc=[642, 520],
    seen='Rock terminal groin at the north end of Treasure Island; ENC matches.')
rec('blindpass-pin-n', 'Blind Pass (Pinellas) north jetty (Treasure Island south end)', 'Pinellas',
    line=[[27.73964, -82.75471], [27.73917, -82.75552], [27.73883, -82.75616], [27.73845, -82.75680]],
    seen='Rock jetty along the south shore of Treasure Island out to a tip on the Gulf side; rock above water.',
    note='Not in OSM or ENC; traced on NAIP.')
rec('blindpass-pin-s', 'Blind Pass (Pinellas) south jetty and pass revetment (Upham Beach)', 'Pinellas',
    line=[[27.73880, -82.75346], [27.73817, -82.75424], [27.73778, -82.75488], [27.73773, -82.75497],
          [27.73735, -82.75488], [27.73688, -82.75485]],
    seen='Rock revetment along the south side of the pass joining a rock jetty that runs south-south-west '
         'about 95 m off the Upham Beach tip.',
    note='Traced on NAIP. St. Pete Beach § 94-1 closes the waters of Blind Pass to swimming and skin diving (spb94).')
rec('upham-groin', 'Upham Beach rock groin', 'Pinellas', line=[[27.73644, -82.75421], [27.73610, -82.75389]],
    cls='warn', seen='Short rock groin on the Upham Beach face south of the jetty.',
    note='A beach groin near the inlet; drawn as may-be-a-jetty.')
rec('passagrille', 'Pass-a-Grille fishing jetty', 'Pinellas',
    line=[[27.68318, -82.73922], [27.68320, -82.73877], [27.68321, -82.73829]], shore=[27.68321, -82.73829],
    seen='Jetty with fishing deck off the south end of the Pass-a-Grille Gulf beach, about 90 m.',
    fwc='Pass-A-Grille Fishing Jetty', note='The 100 yd pier buffer around the FWC point also applies.')
rec('longboat-n', 'Longboat Pass north jetty (Coquina Beach)', 'Manatee', ways=[1266205572],
    seen='Rock and timber jetty off the south tip of Anna Maria Island (Coquina Beach); OSM matches.')
rec('longboat-s', 'Longboat Pass south side groin (Longboat Key north end)', 'Manatee', ways=[1266205565],
    seen='Short groin on the Longboat Key beach at the pass.', note='Drawn as a jetty: shore-attached at the inlet.')
rec('longboat-groins', 'Longboat Key and Coquina Beach groins near the pass', 'Manatee',
    ways=[1266205567, 1266205569], enc=[676, 702, 738], cls='warn',
    seen='Short beach groins either side of the pass.', note='Beach groins; may-be-a-jetty.')
rec('venice-n', 'Venice Inlet north jetty (North Jetty Park, Casey Key)', 'Sarasota',
    line=[[27.11337, -82.46703], [27.11321, -82.46838], [27.11305, -82.46916], [27.11289, -82.46984]],
    shore=[27.11314, -82.46873], fwc='North Jetty Park',
    seen='Rock jetty along the inlet north shore to a tip about 110 m past the Gulf beach.',
    note='OSM carries only the park outline; traced on NAIP. Venice § 46-114 bans spearfishing within or near city waters.')
rec('venice-s', 'Venice Inlet south jetty (Humphris Park)', 'Sarasota',
    line=[[27.11242, -82.46646], [27.11253, -82.46788], [27.11232, -82.46873], [27.11208, -82.46966]],
    shore=[27.11248, -82.46802], fwc='Humphris Park',
    seen='Rock jetty with walkway from Humphris Park to a tip about 170 m past the beach.')
rec('venice-island', 'Venice Inlet island breakwaters', 'Sarasota', ways=[1058106447, 1058106448, 1058106450],
    enc=[30, 31, 719, 797], cls='warn', seen='Short rock breakwaters on the small island inside the inlet.',
    note='May-be-a-jetty.')
rec('stump', 'Stump Pass terminal groin', 'Charlotte', enc=[47], cls='none',
    seen='No rock above water at the pass; the charted groin is always under water.',
    note='Stump Pass Beach State Park adjoins the north side; its water is closed under r. 68B-20.003(2)(e).')
rec('blindpass-lee', 'Blind Pass (Lee) terminal groin and Sanibel shore structures', 'Lee', ways=[1116334298, 1116334299],
    cls='warn', seen='The pass mouth is shoaled; the Turner Beach terminal groin does not show clearly above the sand. '
    'Two short structures on the Sanibel side are mapped as breakwaters.',
    note='May-be-a-jetty. Lee County park waters carry their own spear ban (Lee County § 20-25).')
rec('doctors-n', 'Doctors Pass north jetty', 'Collier', ways=[169915310],
    seen='Rock jetty on the north side of the pass, about 115 m past the beach; OSM outline matches.')
rec('doctors-s', 'Doctors Pass south jetty', 'Collier', ways=[1114792655],
    seen='L-shaped rock jetty on the south side of the pass; OSM outline matches.')
rec('doctors-bw', 'Doctors Pass detached breakwater', 'Collier', ways=[1114792656], enc=[619], cls='warn',
    seen='Short detached rock breakwater off the beach south of the pass, charted always dry.',
    note='Detached; may-be-a-jetty.')
rec('gordon-n', 'Gordon Pass north jetty (Port Royal)', 'Collier', ways=[169915309],
    seen='Short rock jetty at the Port Royal tip on the north side of the pass; OSM matches.')
rec('gordon-s', 'Gordon Pass south jetty (Keewaydin Island)', 'Collier', ways=[169915313],
    seen='Rock jetty along the north shore of Keewaydin Island to a tip on the Gulf side; OSM matches.',
    note='ENC 682 at its tip is charted always under water and is not drawn.')
rec('naples-groins', 'Naples and Keewaydin beach groins either side of Gordon Pass', 'Collier',
    ways=[903940583, 903940584, 903940585, 903940586, 903940587, 903940588, 903940589, 492627077, 492627078,
          1113038961, 169915316, 169915303, 169915320, 999061999, 1113400125],
    enc=[805, 834, 775, 833, 617, 616, 615, 36, 37, 38, 39, 40, 41, 42], cls='warn',
    seen='Rows of short rock groins on the beaches north and south of the pass.',
    note='Beach groins; may-be-a-jetty. Charted always-submerged groins are not drawn.')
rec('cocohatchee', 'Cocohatchee River Park "fishing jetty"', 'Collier', cls='none', fwc='Cocohatchee River Park',
    seen='Boardwalk and docks along the river at the county boat-ramp park; no rock jetty.',
    note='Covered by the 100 yd fishing-pier circle drawn from the FWC point. Not drawn as a jetty.')
rec('palmvalley', 'Palm Valley "fishing jetty" (ICW)', 'St. Johns', cls='none', fwc='Palm Valley',
    seen='Fishing docks on the Intracoastal Waterway at the Palm Valley bridge; no rock jetty.',
    note='Covered by the pier circle and the bridge buffer. Not drawn as a jetty.')
rec('ozello', 'Ozello Fishing Deck', 'Citrus', cls='none', fwc='Ozello Fishing Deck',
    seen='A small wooden deck at the shore of the St. Martins River backcountry; no rock jetty.',
    note='Covered by the pier circle from the FWC point. Not drawn as a jetty.')
rec('hernando', 'Hernando Beach channel jetty and fill spit', 'Hernando', cls='warn',
    add={'marker': [[28.48573, -82.66544]]},
    seen='A low fill spit runs out beside the Hernando Beach approach channel; no distinct rock jetty can be '
         'separated from the fill on the NAIP.',
    note='Coast Pilot 5 names "the jetty and fill spit". Marker only; not traced.')
rec('bargecanal', 'Cross Florida Barge Canal Gulf spoil berm', 'Citrus / Levy', cls='none',
    seen='Five-mile spoil berm along the canal channel.',
    note='A dredge-spoil peninsula rather than a jetty. Not drawn as a jetty.')
rec('kw-nwchannel', 'Key West Northwest Channel jetties', 'Monroe', cls='none',
    seen='Not attached to any shore; Coast Pilot 5 describes them as submerged.',
    note='No unsubmerged portion documented; not drawn. FKNMS rules apply in the area.')
