# ============================================================================
# games_seed.py — Danh sách 121 tựa game THẬT cho Vapor Game Store.
# Được init_db.py import để nạp vào bảng Games.
#
# Format mỗi phần tử (đúng 9 trường):
#   (title, category_slug, price_vnd, description, developer,
#    release_date, rating, platforms, tags)
#
# category_slug khớp với 12 thể loại trong init_db.py:
#   action, rpg, strategy, shooter, horror, adventure, racing, sports,
#   puzzle, simulation, indie, mmo
#
# Giá là giá demo của store sinh viên (VND) — game free-to-play giá 0.
# ============================================================================

GAMES = [
    # ---------------- ACTION (12) ----------------
    ("God of War", "action", 700000, "Kratos bước vào realms Bắc Âu — combat rìu Leviathan nặng nề, câu chuyện cha con chạm cảm xúc nhất series.", "Santa Monica Studio", "2018-04-20", 4.9, "PC, PS4, PS5", "nordic, epic, story-rich"),
    ("Devil May Cry 5", "action", 400000, "Hack and slash chuẩn mực: combo hàng trăm hit, phong cách switch liên tục và boss design khó quên. Pure adrenaline.", "Capcom", "2019-03-08", 4.7, "PC, PS4, Xbox", "stylish, combo, demon"),
    ("Sekiro: Shadows Die Twice", "action", 450000, "FromSoftware bắt bạn học cách deflection — mỗi pha parry kim loại vang như chuông, phần thưởng là cảm giác bất khả chiến bại.", "FromSoftware", "2019-03-22", 4.8, "PC, PS4, Xbox", "samurai, hardcore, posture"),
    ("Marvel's Spider-Man Remastered", "action", 415000, "Treo mình trên mạng nhện bay qua Manhattan đúng nghĩa tự do — combat fluid, story Peter Parker trưởng thành rất đã.", "Insomniac Games", "2022-08-12", 4.8, "PC, PS5", "web-swinging, open-world, superhero"),
    ("Bayonetta 2", "action", 350000, "Witch time, combo trên giày cao gót và sân khấu boss như concert rock — platinum games ở đỉnh cao flair.", "PlatinumGames", "2018-02-16", 4.6, "Switch", "witch, stylish, over-the-top"),
    ("Grand Theft Auto V", "action", 500000, "Ba góc nhìn, một Los Santos rộng tới developer còn chẳng đi hết — heist, xe cộ và chaos sandbox kinh điển.", "Rockstar North", "2015-04-14", 4.9, "PC, PS4, PS5, Xbox", "open-world, heist, crime"),
    ("Star Wars Jedi: Fallen Order", "action", 400000, "Lightsaber parry metroidvania trong vũ trụ Star Wars — thế giới đẹp, combat satisfy, không microtransaction.", "Respawn Entertainment", "2019-11-15", 4.4, "PC, PS4, Xbox", "jedi, metroidvania, sci-fi"),
    ("Shadow of the Tomb Raider", "action", 350000, "Lara kết thúc trilogy trong rừng Amazon — puzzle mồ mộ hoành tráng, stealth bụi rậm và survivor craft đủ cay.", "Crystal Dynamics", "2018-09-14", 4.2, "PC, PS4, Xbox", "tomb, stealth, adventure-action"),
    ("A Plague Tale: Innocence", "action", 250000, "Hai đứa trẻ và bầy chuột đen Paris thế kỷ 14 — stealth giải đố nhẹ nhàng nhưng căng thẳng từng hơi thở.", "Asobo Studio", "2019-11-05", 4.5, "PC, PS4, Xbox, Switch", "stealth, dark-fairytale, narrative"),
    ("God of War Ragnarök", "action", 750000, "Ragnarök bùng nổ — Atreus lớn tiếng riêng, combat nhiều vũ khí hơn, mỗi realm một ý tưởng visual khó quên.", "Santa Monica Studio", "2024-09-19", 4.9, "PC, PS4, PS5", "nordic, saga, boss-fight"),
    ("Mad Max", "action", 200000, "The Magnum Opus của bạn là chiếc xe — chiến đấu gắn giáo, nốc rượu và đập xe đối thủ trong sa mạc muối.", "Avalanche Studios", "2015-09-04", 3.9, "PC, PS4, Xbox", "post-apocalyptic, vehicular, wasteland"),
    ("Darksiders: Warmastered Edition", "action", 150000, "War cưỡi ngựa đỏ chém dọc địa ngục — God of War gặp Zelda trong câu chuyện tận thế bốn kỵ sĩ.", "Vigil Games", "2016-11-22", 4.3, "PC, PS4, Xbox, Switch", "apocalypse, hack-n-slash, puzzle"),

    # ---------------- RPG (12) ----------------
    ("The Witcher 3: Wild Hunt", "rpg", 400000, "Kiếm sĩ già tìm con gái nuôi khắp war-torn continent — side quest đời thường còn hay hơn plot chính nhiều game AAA.", "CD Projekt Red", "2015-05-19", 5.0, "PC, PS4, Xbox, Switch", "fantasy, story-rich, choices"),
    ("Elden Ring", "rpg", 1200000, "Toàn bộ Souls được mở into open world — bạn cưỡi ngựa phi qua lâu đài, hang động và boss lớn bằng màn hình.", "FromSoftware", "2022-02-25", 4.9, "PC, PS4, Xbox", "open-world, dark-fantasy, souls"),
    ("Cyberpunk 2077", "rpg", 1200000, "Night City rực neon và phản bội — bản cập nhật 2.0 cùng Edgerunners đưa RPG cyberpunk này về đúng tiềm năng.", "CD Projekt Red", "2020-12-10", 4.5, "PC, PS5, Xbox", "cyberpunk, neon, fps-rpg"),
    ("Baldur's Gate 3", "rpg", 500000, "Dungeons and Dragons mà mỗi màn cứu đều là một plot twist — branching narrative sâu nhất thập kỷ.", "Larian Studios", "2023-08-03", 4.9, "PC, PS5, Xbox", "dnd, turn-based, party"),
    ("Final Fantasy XVI", "rpg", 690000, "Eikon collision như kaiju đánh nhau — FF chuyển hẳn sang real-time combat và không hối hận.", "Square Enix", "2023-06-22", 4.3, "PC, PS5", "dark-fantasy, action-rpg, eikon"),
    ("Persona 5 Royal", "rpg", 450000, "Ban ngày là học sinh, ban đêm là phantom thief cướp cung điện — UI cool nhất lịch sử JRPG.", "Atlus", "2022-10-21", 4.9, "PC, PS4, Xbox, Switch", "jrpg, school, stylish-ui"),
    ("Dragon Quest XI S: Echoes of an Elusive Age", "rpg", 350000, "JRPG truyền thống làmPerfect — 100 giờ phiêu lưu ấm áp với party khó ai nỡ bỏ.", "Square Enix", "2021-09-27", 4.5, "PC, PS4, Xbox, Switch", "classic-jrpg, turn-based, cozy"),
    ("Final Fantasy VII Remake", "rpg", 500000, "Midgar sống lại giữa hybrid combat — đoạn đi dạo phố với Aerith đủ khiến cả fandom xúc động.", "Square Enix", "2021-05-18", 4.6, "PC, PS4, PS5", "jrpg, noir, action-hybrid"),
    ("The Elder Scrolls V: Skyrim Special Edition", "rpg", 250000, "Lần thứ bao nhiêu bạn lại bắt đầu lại — Skyrim vẫn là open world sandbox để mod vô tận.", "Bethesda Game Studios", "2016-10-28", 4.6, "PC, PS4, Xbox, Switch", "open-world, modding, nordic"),
    ("Divinity: Original Sin 2", "rpg", 300000, "Turn-based CRPG nơi mọi câu trả lời đều thay đổi thế giới — combat theo element tương tác thiên tài.", "Larian Studios", "2017-08-25", 4.8, "PC, PS4, Xbox, Switch", "crpg, tactical, co-op"),
    ("Hogwarts Legacy", "rpg", 400000, "Bạn là phù thủy thế kỷ 19 khám phá Hogwarts bản đồ mở — bay chổi qua Hogsmeade snow đáng giá cả game.", "Avalanche Software", "2023-02-10", 4.4, "PC, PS5, Xbox", "wizarding, open-world, spells"),
    ("Dragon Age: The Veilguard", "rpg", 450000, "Party ba người đồng hànhแน่น — combat nhịp nhanh và quyết định tình cảm khiến bạn save liên tục.", "BioWare", "2024-10-31", 4.0, "PC, PS5, Xbox", "fantasy, squad, romance"),

    # ---------------- STRATEGY (11) ----------------
    ("Age of Empires II: Definitive Edition", "strategy", 200000, "RTS bất tử với bản đồ random, villager ping và tiếng chiêng cổ điển — 25 năm vẫn không game thủ nào bỏ.", "World's Edge, Hidden Path", "2019-11-15", 4.7, "PC, Xbox, Switch", "rts, classic, medieval"),
    ("Age of Empires IV", "strategy", 800000, "Bài học lịch sử dạng RTS — cinematic như documentary, siege machine tàn phá công trình vật lý thật.", "Relic Entertainment", "2021-10-28", 4.1, "PC, Xbox", "rts, siege, medieval"),
    ("Sid Meier's Civilization VI", "strategy", 350000, "One more turn là câu thần chú nguy hiểm nhất ngành game — từ Stone Age lên Mars với năng lượng văn minh.", "Firaxis Games", "2016-10-21", 4.5, "PC, PS4, Xbox, Switch", "4x, turn-based, empire"),
    ("Total War: WARHAMMER III", "strategy", 690000, "Chiến dịch map cộng nhất series — ma thuật, daemon và 8000 đơn vị hỗn chiến trên một battle map.", "Creative Assembly", "2023-02-16", 4.3, "PC", "grand-campaign, fantasy-war, real-time"),
    ("XCOM 2", "strategy", 250000, "Du kích trên hành tinh bị chiếm — mỗi soldier chết là mất thật, miss 95% hit chance là đau cả đời.", "Firaxis Games", "2016-02-05", 4.6, "PC, PS4, Xbox, Switch", "turn-based, squad, permadeath"),
    ("Into the Breach", "strategy", 150000, "Puzzle chiến thuật siêu gọn: mech chống kaiju, mọi nước đi đối phương đều hiện sẵn — chỉ cần bạn thông minh enough.", "Subset Games", "2018-08-28", 4.5, "PC, Switch", "grid, minimal, puzzle-strategy"),
    ("Company of Heroes 3", "strategy", 300000, "Chiến trường Địa Trung Hải Thế chiến II — destructible cover, campaign chiến dịch kiểu grand map mới.", "Relic Entertainment", "2023-02-23", 3.6, "PC, PS5, Xbox", "wwii, tactical, destructible"),
    ("Stellaris", "strategy", 250000, "Từ một con tàu explorer đến empire thiên hà — event text hài hước nhất thể loại 4X sci-fi.", "Paradox Development Studio", "2016-05-09", 4.3, "PC", "grand-strategy, sci-fi, 4x"),
    ("Frostpunk", "strategy", 200000, "Thành phố cuối cùng trên địa cầu đóng băng — law book của bạn sẽ bắt trẻ em đào than, hoặc chết.", "11 bit studios", "2018-04-24", 4.4, "PC, PS4, Xbox", "survival-city, moral-choices, steampunk"),
    ("Crusader Kings III", "strategy", 300000, "Hoàng gia drama engine — liên minh, phản bội và gen di truyền quan trọng hơn cả quân đội.", "Paradox Development Studio", "2020-09-01", 4.6, "PC, PS5, Xbox", "dynasty, roleplay, medieval"),
    ("They Are Billions", "strategy", 150000, "Zombie RTS tàn bạo — một con bài lẻn vào thành phố là 20.000 dân thành zombie trong 30 giây.", "Numantian Games", "2019-08-14", 3.9, "PC", "zombie, tower-defense, colony"),

    # ---------------- SHOOTER (10) ----------------
    ("DOOM Eternal", "shooter", 400000, "Heavy metal đúng nghĩa — chainsaw để lấy máu, glory kill để lấy giáp, bạn không được phép đứng yên.", "id Software", "2020-03-20", 4.8, "PC, PS4, Xbox, Switch", "fps, fast, demon-slaying"),
    ("Borderlands 3", "shooter", 300000, "Hàng triệu khẩu súng và giọng thoại Badass — co-op looter shooter buồn cười nhất hệ mặt trời.", "Gearbox Software", "2019-09-13", 4.2, "PC, PS4, Xbox", "looter, cel-shaded, co-op"),
    ("Halo Infinite", "shooter", 350000, "Master Chief trở lại với open-zone — grappling hook biến mỗi trận bắn súng thành parkour.", "343 Industries", "2021-12-08", 4.1, "PC, Xbox", "sci-fi, arena, sandbox"),
    ("Titanfall 2", "shooter", 250000, "Campaign ngắn mà_dense như phim — wall-run, titan cockpit và màn time-travel level design vô đối.", "Respawn Entertainment", "2016-10-28", 4.7, "PC, PS4, Xbox", "mech, movement, sci-fi"),
    ("Helldivers 2", "shooter", 400000, "Dân chủ galactic dạng co-op — friendly fire bật sẵn nên mỗi pha orbital strike là canh bạc.", "Arrowhead Game Studios", "2024-02-08", 4.6, "PC, PS5", "co-op, extraction, satirical"),
    ("Valorant", "shooter", 0, "Tactical shooter 5v5 nơi ability chỉ mở đường — aim mới là vua, free-to-play cạnh tranh khốc liệt nhất.", "Riot Games", "2020-06-02", 4.2, "PC", "tactical, hero, competitive"),
    ("Counter-Strike 2", "shooter", 0, "Huyền thoại 20 năm nâng cấp Source 2 — economy, spray pattern và một quả AWP giữa map.", "Valve", "2023-09-27", 4.4, "PC", "tactical, esports, classic"),
    ("Apex Legends", "shooter", 0, "Movement shooter với ping system thay đổi cả thể loại — 60 fps fluid như trượt trên băng.", "Respawn Entertainment", "2019-02-04", 4.1, "PC, PS4, Xbox, Switch", "battle-royale, movement, squad"),
    ("War Thunder", "shooter", 0, "Tank, máy bay, tàu chiến cùng một trận — meta game của lịch sử quân sự thế chiến đến hiện đại.", "Gaijin Entertainment", "2016-08-15", 4.0, "PC, PS5, Xbox", "vehicles, historical, pvp"),
    ("Tom Clancy's Rainbow Six Siege", "shooter", 149000, "Mọi bức tường đều phá được — attacker vs defender mà mỗi round là một bài toán hình học.", "Ubisoft Montreal", "2015-12-01", 4.3, "PC, PS4, Xbox", "breach, tactical, destructible"),

    # ---------------- HORROR (10) ----------------
    ("Resident Evil Village", "horror", 400000, "Làng snow Romania, Lady Dimitrescu 2m14 và một minotaur maze — survival horror showcase thế hệ mới.", "Capcom", "2021-05-07", 4.6, "PC, PS4, PS5, Xbox", "gothic, survival, first-person"),
    ("Resident Evil 2 Remake", "horror", 400000, "Raccoon City police station tái sinh — ammo quý hơn vàng và Mr. X gõ cửa đúng lúc nhất gaming.", "Capcom", "2019-01-25", 4.8, "PC, PS4, Xbox", "zombie, survival, remake"),
    ("Silent Hill 2 Remake", "horror", 500000, "Bản remake đẹp và đau — James đi tìm vợ trong fog tâm lý mà monster nào cũng là một ẩn dụ.", "Bloober Team", "2024-10-08", 4.5, "PC, PS5", "psychological, fog, story-heavy"),
    ("Outlast 2", "horror", 200000, "Camcorder là tất cả những gì bạn có — cult rural Arizona mà mỗi cutscene đều khiến bạn regret.", "Red Barrels", "2017-04-25", 4.2, "PC, PS4, Xbox, Switch", "found-footage, chase, no-combat"),
    ("The Forest", "horror", 200000, "Crash máy bay, dựng camp, rồi nghe tiếng hú trong rừng khi mặt trời lặn — survival horror cân bằng hoàn hảo.", "Endnight Games", "2018-04-30", 4.4, "PC, PS4", "survival, cave, cannibal"),
    ("Alien: Isolation", "horror", 250000, "Một con Alien, một station — AI không học theo pattern của bạn nhưng luôn tìm được bạn.", "Creative Assembly", "2014-10-07", 4.5, "PC, PS4, Xbox", "sci-fi, stealth, retro-future"),
    ("Dead Space Remake", "horror", 500000, "USG Ishimaur trở lại với limb targeting vẫn tàn bạo — audio design hay nhất thể loại sci-fi horror.", "Motive Studio", "2023-01-27", 4.6, "PC, PS5, Xbox", "sci-fi, dismemberment, remake"),
    ("Layers of Fear (2023)", "horror", 150000, "Painting, guilt và một con rết mẹ — walking sim horror mà mỗi cánh cửa đổi cả bố cục nhà.", "Bloober Team", "2023-06-15", 3.8, "PC, PS5, Xbox", "psychological, walking-sim, art-horror"),
    ("The Evil Within 2", "horror", 250000, "Shinji Mikami trở lại — STEM thế giới méo mó, crafting tense và một bé Lily đáng sợ hơn boss.", "Tango Gameworks", "2017-10-13", 4.3, "PC, PS4, Xbox", "surreal, survival, mind-bend"),
    ("Signalis", "horror", 200000, "Reactor unit Eter mở mắt trong tuyết — survival horror retro pixel Đông Âu đẹp và buồn như một bài thơ.", "rose-engine", "2022-10-27", 4.5, "PC, PS4, Xbox, Switch", "retro, sci-fi, dystopia"),

    # ---------------- ADVENTURE (11) ----------------
    ("Red Dead Redemption 2", "adventure", 150000, "Sự sụp đổ của Wild West qua mắt Arthur Morgan — chi tiết đến mức snow MELT theo từng bước ngựa.", "Rockstar Games", "2019-11-05", 4.9, "PC, PS4, Xbox", "western, open-world, narrative"),
    ("Uncharted 4: A Thief's End", "adventure", 450000, "Indiana Jones phiên bản AAA — set piece như phim, và đoạn kết khiến cả party im lặng.", "Naughty Dog", "2022-10-19", 4.7, "PC, PS4, PS5", "treasure, cinematic, climbing"),
    ("The Last of Us Part I", "adventure", 500000, "Joel và Ellie đi xuyên nước Mỹ sụp đổ — story-driven stealth mà mỗi clicker encounter đều nín thở.", "Naughty Dog", "2022-03-28", 4.8, "PC, PS5", "post-apocalyptic, story-rich, stealth"),
    ("Ghost of Tsushima Director's Cut", "adventure", 500000, "Samurai cuối cùng của Tsushima — wind-guided exploration đẹp đến mức bạn quên cả chiến đấu.", "Sucker Punch Productions", "2024-05-16", 4.7, "PC, PS4, PS5", "samurai, open-world, cinematic"),
    ("Life is Strange", "adventure", 200000, "Nữ sinh chụp ảnh và rewind thời gian — indie narrative mà mỗi save bạn chọn là một vết thương.", "Dontnod Entertainment", "2015-01-30", 4.6, "PC, PS4, Xbox, Switch", "episodic, time-power, emotional"),
    ("Kena: Bridge of Spirits", "adventure", 350000, "Giả như Pixar làm game — Rot đoàn quân nhỏ dễ thương trong combat Zeldalite gọn gàng.", "Ember Lab", "2021-09-21", 4.5, "PC, PS4, PS5", "animation-style, puzzle, spirits"),
    ("Firewatch", "adventure", 150000, "Lính cứu hỏa Wyoming và chiếc bộ đàm — dialogue mà cả game chỉ nói chuyện vẫn không nhàm chán.", "Campo Santo", "2016-02-09", 4.2, "PC, PS4, Xbox, Switch", "walking-sim, mystery, dialogue"),
    ("Metroid Dread", "adventure", 300000, "Samus đối mặt E.M.M.I. — metroidvania tốc độ cao mà bản đồ khiến bạn đi lạc một cách hạnh phúc.", "MercurySteam", "2021-10-08", 4.6, "Switch", "metroidvania, isolation, sci-fi"),
    ("Prince of Persia: The Lost Crown", "adventure", 300000, "Persian metroidvania hồi sinh series — combat combo mượt, time power và map design thông minh.", "Ubisoft Montpellier", "2024-01-18", 4.5, "PC, PS4, Xbox, Switch", "2.5d, acrobatic, myth"),
    ("A Plague Tale: Requiem", "adventure", 350000, "Amicia và Hugo trên con đường phía nam — bầy chuột như sóng thần, puzzle light và stealth đẫm nước mắt.", "Asobo Studio", "2022-10-18", 4.5, "PC, PS5, Xbox, Switch", "dark-fairytale, stealth, sequel"),
    ("Journey", "adventure", 100000, "Đi về ngọn núi dưới ánh nắng — game không một dòng text mà khiến người lớn rơi nước mắt.", "thatgamecompany", "2019-06-18", 4.7, "PC, PS4", "art-game, wordless, cooperative-spirit"),

    # ---------------- RACING (9) ----------------
    ("Forza Horizon 5", "racing", 500000, "Mexico bản đồ mở — từ volcano đến jungle, drift sang cả sa mạc, car list hơn 500 chiếc.", "Playground Games", "2021-11-09", 4.7, "PC, Xbox", "open-world, arcade-sim, festival"),
    ("Need for Speed Unbound", "racing", 450000, "Grafitti effect bay theo xe — street racing underground với soundtrack và style đúng văn hóa hip-hop.", "Criterion Games", "2022-12-02", 4.1, "PC, PS5, Xbox", "street, stylish, police-chase"),
    ("F1 24", "racing", 550000, "Mùa giải công thức 1 chính thức — career mode 15 năm và handling cân giữa sim và arcade.", "Codemasters, EA Sports", "2024-05-31", 3.9, "PC, PS5, Xbox", "simulation-sport, licensed, grand-prix"),
    ("Mario Kart 8 Deluxe", "racing", 500000, "48 course phản trọng lực — party game mà một con blue shell thay đổi cả tình bạn.", "Nintendo EPD", "2017-04-28", 4.8, "Switch", "kart, party, classic"),
    ("Assetto Corsa", "racing", 200000, "Sim racing với mod cộng đồng vô hạn — drift đêm trên đường đua Nürburgring lúc 2 giờ sáng.", "Kunos Simulazioni", "2014-12-19", 4.3, "PC, PS4, Xbox", "simulation, modding, track-day"),
    ("DiRT Rally 2.0", "racing", 250000, "Rally thật sự: một Pebble bug là 30 giây bay ra khỏi đường — punishment game đúng nghĩa.", "Codemasters", "2019-02-26", 4.4, "PC, PS4, Xbox", "rally, punishing, offroad"),
    ("Neon Drive", "racing", 90000, "Racing rhythm với synthwave — đường hầm neon, beat rơi theo từng góc cua, ngắn nhưng aesthetic cực mạnh.", "Fraoula", "2016-07-15", 4.2, "PC, Switch", "synthwave, retro, tunnel"),
    ("Wreckfest", "racing", 250000, "Derby demolisher — mỗi chiếc xe móp méo vật lý thật, bay nóc mà vẫn vui.", "Bugbear Entertainment", "2018-06-14", 4.3, "PC, PS4, Xbox", "destruction, demolition-derby, physics"),
    ("Burnout Paradise Remastered", "racing", 200000, "Thành phố Paradise không barrier — takedown 10 chiếc rồi crash chính mình cũng là một nghệ thuật.", "Criterion Games", "2018-03-16", 4.4, "PC, PS4, Xbox", "arcade, crash, open-world"),

    # ---------------- SPORTS (7) ----------------
    ("EA Sports FC 24", "sports", 500000, "FIFA kỷ nguyên mới — HyperMotion mang bóng và người về cùng nhịp, Ultimate Team vẫn hút thời gian.", "EA Vancouver", "2023-09-29", 3.9, "PC, PS4, PS5, Xbox", "football, ultimate-team, simulation"),
    ("NBA 2K24", "sports", 450000, "Roster đầy sao và MyCareer bóng rổ — nhưng VC lại là miniboss khó nhất game.", "Visual Concepts", "2023-09-08", 4.0, "PC, PS4, PS5, Xbox", "basketball, career, licensed"),
    ("Rocket League", "sports", 0, "FIFA gặp Forza — bóng đá bằng xe bay, skill ceiling cao tới tận stratossphere, free-to-play hoàn hảo.", "Psyonix", "2015-07-07", 4.5, "PC, PS4, Xbox, Switch", "car-soccer, competitive, physics"),
    ("Tony Hawk's Pro Skater 1+2", "sports", 350000, "Remake của hai huyền thoại — combo rail + grab vẫn khiến bạn tự hỏi tại sao game này 20 tuổi.", "Vicarious Visions", "2020-09-04", 4.7, "PC, PS4, Xbox", "skate, nostalgic, soundtrack"),
    ("WWE 2K24", "sports", 450000, "MyRise, universe mode và roster đô vật đô nhất — wrestling simulator không cần xin lỗi.", "Visual Concepts", "2024-03-08", 4.0, "PC, PS4, PS5, Xbox", "wrestling, showmanship, roster"),
    ("Golf With Your Friends", "sports", 150000, "Mini golf physics cho 12 người — đặt club mạnh tay một là bóng bay lên Mặt Trăng.", "Blacklight Intensive, Team17", "2020-05-19", 3.8, "PC, PS4, Xbox, Switch", "party, physics, multiplayer"),
    ("Football Manager 2024", "sports", 300000, "Excel spreadsheet đẹp nhất thế giới — bạn sẽ bỏ job interview thật để giữ job virtual.", "Sports Interactive", "2023-11-06", 4.4, "PC, Xbox, Switch", "management, tactics, data-heavy"),

    # ---------------- PUZZLE (9) ----------------
    ("Portal 2", "puzzle", 200000, "GLaDOS, Weighted Companion Cube và coop hai người — writing hài hước nhất lịch sử puzzle game.", "Valve", "2011-04-19", 4.9, "PC, PS3, Xbox", "portal-gun, comedy, test-chamber"),
    ("The Witness", "puzzle", 250000, "Một hòn đảo, 650 bức tường line puzzle — game dạy bạn nhìn thế giới bằng quy tắc im lặng.", "Thekla Inc", "2016-01-26", 4.5, "PC, PS4, Xbox, Switch", "line-drawing, island, minimalist"),
    ("Tetris Effect: Connected", "puzzle", 250000, "Tetris như concert — mỗi dòng clear là một burst ánh sáng và nhạc, Zone mode gây nghiện nặng.", "Enhance Games", "2021-07-27", 4.6, "PC, PS4, Xbox, Switch", "synesthesia, music, hypnosis"),
    ("Baba Is You", "puzzle", 150000, "Bạn đẩy chính rule của game — khi nào hiểu WALL IS STOP không còn là sự thật, bạn đã thông minh hơn.", "Hempuli", "2019-01-13", 4.7, "PC, Switch", "rule-bending, clever, indie-classic"),
    ("The Talos Principle", "puzzle", 150000, "Portal gặp triết học — puzzle laser và debate với tiếng nói về nhân tính trong ruins nhân loại.", "Croteam", "2014-12-11", 4.4, "PC, PS4, Xbox, Switch", "philosophy, first-person, laser"),
    ("Superliminal", "puzzle", 150000, "Perspective là mechanic — đồng xu to bằng building nếu bạn nhìn đúng góc.", "Pillow Castle", "2019-11-05", 4.2, "PC, PS4, Xbox, Switch", "forced-perspective, dream, clever"),
    ("Patrick's Parabox", "puzzle", 150000, "Box trong box trong bạn — recursion puzzle mà mỗi room là một fractal tâm trí.", "Patrick Traynor", "2022-05-26", 4.4, "PC, Switch", "recursion, Sokoban-like, meta"),
    ("It Takes Two", "puzzle", 400000, "Game bắt buộc hai người — mỗi level một mechanic mới và một màn boss absurd dễ thương.", "Hazelight Studios", "2021-03-26", 4.8, "PC, PS4, PS5, Xbox", "co-op-only, variety, relationship"),
    ("Antichamber", "puzzle", 100000, "Não của bạn là puzzle chính — hành lang loop và lời hint trắng đen đánh lừa mọi trực giác.", "Alexander Bruce", "2013-01-31", 4.1, "PC", "non-euclidean, mindbend, abstract"),

    # ---------------- SIMULATION (10) ----------------
    ("The Sims 4", "simulation", 199000, "Đời người bản sandbox — build house 6 tiếng, để pool ladder biến mất 1 phút.", "Maxis", "2014-09-02", 4.1, "PC, PS4, Xbox", "life-sim, build-mode, drama"),
    ("Cities: Skylines II", "simulation", 500000, "Thành phố 75k dân — traffic AI thật, utility depth mới và laptop bạn bắt đầu khóc.", "Colossal Order", "2023-10-24", 3.6, "PC, Xbox", "city-builder, traffic, infrastructure"),
    ("Farming Simulator 22", "simulation", 300000, "Tractor mô-tơ hóa đầy đủ — bạn sẽ lên Reddit hỏi cách cắt cỏ lúc 1 giờ sáng.", "Giants Software", "2021-11-22", 4.2, "PC, PS5, Xbox", "farming, machinery, chill"),
    ("Microsoft Flight Simulator", "simulation", 500000, "Trái Đất bản 1:1 bằng satellite và AI — bay từ Nội Bài vào Tân Sơn Nhất nhìn đúng sông Hồng.", "Asobo Studio", "2020-08-18", 4.5, "PC, Xbox", "aviation, earth-scale, weather"),
    ("Planet Coaster", "simulation", 250000, "Công viên giải trí tự tay dựng từng rail — rồi đứng xem guests xếp hàng 40 phút vì một roller.", "Frontier Developments", "2016-11-17", 4.4, "PC, PS4, Xbox", "park-tycoon, creative, management"),
    ("Two Point Hospital", "simulation", 200000, "Hài hước tycoon — chữa H2O Overdose và Large Head bằng phòng ban sắp xếp như puzzle.", "Two Point Studios", "2018-08-30", 4.5, "PC, PS4, Xbox, Switch", "hospital, comedic, management"),
    ("Euro Truck Simulator 2", "simulation", 200000, "Bán nhà mua cabin DLC — 12 tiếng virtual drive radio Europe là relaxation trị liệu.", "SCS Software", "2013-10-19", 4.6, "PC", "truck, relaxation, convoy"),
    ("House Flipper", "simulation", 150000, "Dọn rác, sơn tường, bán nhà —ASMR lao động khiến bạn quên đời thật đang bừa.", "Empyrean", "2018-05-17", 4.0, "PC, PS4, Xbox, Switch", "cleaning, renovation, cozy"),
    ("Oxygen Not Included", "simulation", 200000, "Colony trên asteroid — khí, nhiệt, nước bẩn và stress khiến mọi kế hoạch của bạn fail beautiful.", "Klei Entertainment", "2019-07-30", 4.5, "PC", "colony, survival, engineering"),
    ("Stardew Valley", "simulation", 200000, "Bỏ job văn phòng về nông trại — 24 giờ đầu là plant, 240 giờ sau là mining và marriage route.", "ConcernedApe", "2016-02-26", 4.9, "PC, PS4, Xbox, Switch, mobile", "cozy, farming, pixel-art"),

    # ---------------- INDIE (12) ----------------
    ("Hades", "indie", 350000, "Roguelike mà chết là cách thúc đẩy story — mỗi escape attempt từ House of Hades là một run combat hoàn hảo.", "Supergiant Games", "2020-09-17", 4.7, "PC, PS4, Xbox, Switch", "rogue-lite, greek, narrative-run"),
    ("Hollow Knight", "indie", 200000, "Bug metroidvania trong kingdom mục ruỗng — 2D combat chuẩn Souls với map hơn 100 giờ khám phá.", "Team Cherry", "2017-02-24", 4.8, "PC, PS4, Xbox, Switch", "metroidvania, hand-drawn, tough"),
    ("Celeste", "indie", 150000, "Climb mountain against anxiety — platformer frame-perfect mà assist mode cũng là một ending đẹp.", "Maddy Makes Games", "2018-01-25", 4.8, "PC, PS4, Xbox, Switch", "precision-platformer, mental-health, speedrun"),
    ("Dead Cells", "indie", 200000, "Rogue-vania 60 fps — weapon mutates, you mutate, run again with better muscles.", "Motion Twin", "2018-08-06", 4.6, "PC, PS4, Xbox, Switch, mobile", "rogue-lite, fast-combat, pixel"),
    ("Undertale", "indie", 100000, "RPG mà không ai phải chết — hoặc mọi người đều. Meta narrative nhỏ game gây bão lớn nhất 2015.", "Toby Fox", "2015-09-15", 4.7, "PC, PS4, Switch", "rpg, no-kill-route, quirky"),
    ("Hotline Miami", "indie", 150000, "Neon Miami massacre 30 giây một màn — music drop mạnh như cú beatdown của mặt nạ.", "Dennaton Games", "2012-10-23", 4.8, "PC, PS4, Switch, mobile", "synthwave, ultra-violent, top-down"),
    ("Vaporwave Simulator", "indie", 50000, "Aesthetic idle game — statue Hydrant, sunset grid và music loop đúng hệ tư tưởng Vaporwave.", "VaporDev", "2023-01-01", 3.9, "PC", "vaporwave, aesthetic, idle"),
    ("Balatro", "indie", 150000, "Poker là roguelike — joker, tarot và số điểm vượt vũ trụ khiến bạn 3 giờ sáng vẫn one more hand.", "LocalThunk", "2024-02-20", 4.7, "PC, PS4, Xbox, Switch", "card-game, deckbuilder, hypnotic"),
    ("Cuphead", "indie", 200000, "Cartoon 1930 chuyển động — run-and-gun khó cay nhưng mỗi boss là một tập phim hoạt hình.", "StudioMDHR", "2017-09-29", 4.6, "PC, PS4, Xbox, Switch", "1930s-cartoon, run-gun, hand-drawn"),
    ("Inside", "indie", 150000, "Cậu bé vào dystopian facility — 2 giờ im lặng mà dread hơn mọi game kinh dị 20 giờ.", "Playdead", "2016-06-29", 4.7, "PC, PS4, Xbox", "atmospheric, puzzle-platformer, dystopia"),
    ("Terraria", "indie", 150000, "2D sandbox 10 năm không hết content — khai khoáng, boss, build house và một cục moon lord cuối game.", "Re-Logic", "2011-05-16", 4.7, "PC, PS4, Xbox, Switch, mobile", "sandbox, crafting, boss-rush"),
    ("The Binding of Isaac: Repentance", "indie", 150000, "Roguelike giải phẫu Kinh Thánh với hàng trăm item tương tác khó tin.", "Nicalis, Edmund McMillen", "2021-03-31", 4.6, "PC, PS4, Xbox, Switch", "roguelike, dark, item-synergy"),

    # ---------------- MMO (8) ----------------
    ("World of Warcraft", "mmo", 155000, "Hai thập kỷ raiding ở Azeroth — Dragonflight đưa class trở lại, housing là tương lai hứa hẹn.", "Blizzard Entertainment", "2004-11-23", 4.4, "PC", "raiding, fantasy, subscription"),
    ("Final Fantasy XIV Online", "mmo", 400000, "From disastrous launch to best story in any MMO — Endwalker viết tiếp sử thi Hydaelyn hoàn hảo.", "Square Enix", "2013-08-27", 4.7, "PC, PS4, PS5", "story-rich, raid, fantasy"),
    ("Guild Wars 2", "mmo", 300000, "Event-based world mà không ai grind với ai — expansion End of Dragons đẹp và martial arts đã.", "ArenaNet", "2012-08-28", 4.3, "PC", "buy-once, dynamic-events, fantasy"),
    ("Old School RuneScape", "mmo", 200000, "Cày 1000 quest từ 2007 đến giờ — MMO sandbox mà một con green dragon giết bạn cả tháng.", "Jagex", "2013-02-14", 4.5, "PC, mobile", "grind, nostalgia, sandbox"),
    ("Black Desert Online", "mmo", 149000, "Combat action MMO đẹp nhất — nhân vật tạo như ảnh thời trang, nhưng AFK horse grinding là thật.", "Pearl Abyss", "2016-05-03", 3.8, "PC, PS4, Xbox", "action-combat, sandbox, grind"),
    ("Albion Online", "mmo", 200000, "Sandbox you-are-what-you-wear — economy do người chơi, PvP zerg và one server toàn thế giới.", "Sandbox Interactive", "2021-07-18", 4.0, "PC, mobile, Switch", "player-economy, pvp, cross-platform"),
    ("Phantasy Star Online 2: New Genesis", "mmo", 250000, "PSO2 nâng cấp open sky — flashy combo action và customization nhân vật vô tận.", "Sega", "2021-06-09", 4.1, "PC, Xbox", "anime, action-mmo, co-op"),
    ("New World: Enhanced", "mmo", 200000, "Aeternum colonial MMO — PvP territory war và crafting hệ thống sâu, graphics đẹp nhất thể loại.", "Amazon Games", "2023-04-18", 3.8, "PC", "territory-war, crafting, colonial"),
]
