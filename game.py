import time
import os
import random

# Warna terminal (ANSI)
class C:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


# Default pause (seconds) used after each printed line to add drama
DEFAULT_LINE_PAUSE = 0.5
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_pause(text="", delay=DEFAULT_LINE_PAUSE, end="\n"):
    print(text, end=end, flush=True)
    time.sleep(delay)


def print_slow(text, char_delay=0.02, end_delay=DEFAULT_LINE_PAUSE):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(char_delay)
    print()
    time.sleep(end_delay)


def print_line(text="", pause=DEFAULT_LINE_PAUSE, end="\n"):
    """Print a full line then pause for `pause` seconds."""
    print(text, end=end, flush=True)
    time.sleep(pause)


def input_prompt(prompt="", pause=DEFAULT_LINE_PAUSE):
    """Print a prompt, pause `pause` seconds, then read input from the user."""
    print(prompt, end='', flush=True)
    time.sleep(pause)
    return input()


def header():
        print_pause(C.OKCYAN + """
  *************************************************
  *          PETUALANGAN DI HUTAN MISTERIUS       *
  *************************************************
    """ + C.ENDC)


# Entitas pemain / musuh dan fungsi pertempuran
class Entity:
    def __init__(self, name, hp, attack_range, difficulty=1.0):
        self.name = name
        self.hp = hp
        self.attack_range = attack_range
        self.difficulty = difficulty
        self.base_hp = hp

    def attack(self):
        return random.randint(*self.attack_range)


def combat(player: Entity, enemy: Entity):
    print_pause()
    print_slow(f"Tiba-tiba, {enemy.name} muncul dari balik bayangan! (Level musuh ~{int(enemy.difficulty*player.level)})", 0.02)
    while enemy.hp > 0 and player.hp > 0:
        print_pause(f"\nNyawamu: {player.hp}  |  {enemy.name} HP: {enemy.hp}")
        aksi = input_prompt("Pilih aksi: 1) Serang   2) Lari  -> ").strip().lower()
        if aksi in ("1", "serang", "s"):
            dmg = player.attack()
            enemy.hp -= dmg
            print_slow(C.OKGREEN + f"Kau menyerang dan memberi {dmg} kerusakan!" + C.ENDC, 0.01)
            if enemy.hp <= 0:
                print_slow(C.OKCYAN + f"{enemy.name} tumbang. Kau menang!" + C.ENDC, 0.02)
                return 'victory'
            edmg = enemy.attack()
            player.hp -= edmg
            print_slow(C.FAIL + f"{enemy.name} menyerang balik dan memberikan {edmg} kerusakan!" + C.ENDC, 0.01)
        elif aksi in ("2", "lari", "l"):
            print_slow(C.WARNING + "Kau memilih mundur dengan cepat, selamat... untuk sekarang." + C.ENDC, 0.02)
            return 'escaped'
        else:
            print_slow(C.WARNING + "Aksi tidak dikenali. Ketik '1' atau '2'." + C.ENDC, 0.01)

    if player.hp <= 0:
        print_slow(C.FAIL + "Kau roboh. Petualangan berakhir..." + C.ENDC, 0.02)
        return 'dead'
    return 'unknown'


def create_enemy(name: str, base_hp: int, base_attack: tuple, difficulty_str: str, player_level: int):
    # difficulty_str: 'normal'|'hard'|'elite'
    mult_map = {'normal': 1.0, 'hard': 1.25, 'elite': 1.6}
    mult = mult_map.get(difficulty_str, 1.0)
    # scale with player level
    lvl_scale = 1.0 + (player_level - 1) * 0.05
    hp = max(1, int(base_hp * mult * lvl_scale))
    low = max(1, int(base_attack[0] * mult * lvl_scale))
    high = max(low + 1, int(base_attack[1] * mult * lvl_scale))
    enemy = Entity(name, hp, (low, high), difficulty=mult)
    enemy.base_hp = base_hp
    return enemy


def award_xp_and_maybe_level(player: Entity, enemy: Entity):
    # simple XP: 10 * difficulty
    xp_gain = int(10 * enemy.difficulty + (enemy.base_hp // 5))
    player.xp = getattr(player, 'xp', 0) + xp_gain
    print_slow(C.OKGREEN + f"[XP +{xp_gain}] Sekarang XP: {player.xp}" + C.ENDC, 0.02)
    # level up threshold
    leveled = False
    while player.xp >= player.level * 15:
        player.xp -= player.level * 15
        player.level += 1
        player.base_hp = getattr(player, 'base_hp', player.hp) + 5
        player.hp = min(player.hp + 8, player.base_hp)
        # increase attack max
        low, high = player.attack_range
        player.attack_range = (low, high + 1)
        print_slow(C.OKCYAN + f"== LEVEL UP! Sekarang level {player.level}. HP dan serangan meningkat! ==" + C.ENDC, 0.03)
        leveled = True
    return leveled


def scene_meet_local_and_first_battle(player: Entity, inventory: dict):
    clear()
    header()
    # Pertemuan dengan penduduk lokal
    print_slow("🌲 Arden memasuki Hutan Misterius, di mana udara dipenuhi suara burung dan pohon-pohon tinggi...", 0.01)
    time.sleep(0.3)
    print_slow("Seorang penduduk lokal muncul—seorang wanita tua berjubah yang ramah. 🧓✨", 0.02)
    print_pause()
    print_slow("'Sumber kehidupan ada di dalam hutan, tetapi kamu harus berhati-hati.'", 0.02)
    print_slow("'Ada banyak bahaya di sini, termasuk monster-monster yang mengancam nyawa.'", 0.02)
    print_pause()
    print_slow("Wanita itu memberikanmu peta kecil dan sebotol ramuan penyembuh. 🗺️🧪", 0.02)
    inventory.setdefault('potions', 0)
    inventory['potions'] += 1
    print_slow(C.OKGREEN + "[Dapat] 1x Ramuan Penyembuh" + C.ENDC, 0.02)
    print_pause()

    # Pertemuan pertama: serigala bermata merah
    print_slow("Di sela-sela semak, mata merah menyala menatapmu... 🐺🔥", 0.02)
    enemy = create_enemy("Red-Eyed Wolf 🐺", 22, (5, 9), 'normal', player.level)
    result = combat(player, enemy)

    if result == 'victory' and player.hp > 0:
        award_xp_and_maybe_level(player, enemy)
        print_slow(C.OKCYAN + "Dengan kemampuan dan strategimu, Arden berhasil mengalahkan monster itu." + C.ENDC, 0.02)
        # Reward: obat-obatan (potion sudah diberikan) dan upgrade kemampuan
        print_slow("Kau menemukan beberapa obat-obatan dan sebuah kristal yang meningkatkan seranganmu. ✨⚔️", 0.02)
        inventory['potions'] = inventory.get('potions', 0) + 1
        # naikkan attack max
        low, high = player.attack_range
        player.attack_range = (low, high + 2)
        print_slow(C.OKGREEN + f"[Upgrade] Serangan maksimum bertambah menjadi {player.attack_range[1]}" + C.ENDC, 0.02)
        # sedikit penyembuhan
        player.hp = min(player.hp + 10, getattr(player, 'base_hp', 40))
        print_slow(C.OKGREEN + f"Arden sembuh sedikit: Nyawa sekarang {player.hp}" + C.ENDC, 0.02)
    else:
        print_slow(C.WARNING + "Pertempuran berakhir tanpa hadiah." + C.ENDC, 0.02)


def trap_encounter(player: Entity):
    print_slow("Saat berjalan pelan, tanah di hadapanmu terasa rapuh...", 0.02)
    print_slow("Kau melihat ada jebakan tersembunyi.", 0.02)
    pilihan = input_prompt("Apa yang kau lakukan? ('periksa'/'lewati'): ").strip().lower()
    if pilihan in ("periksa", "p"):
        success = random.random() < 0.75
        if success:
            print_slow(C.OKGREEN + "Kau berhasil menemukan dan menjauh dari jebakan." + C.ENDC, 0.02)
            return True
        else:
            dmg = random.randint(3, 7)
            player.hp -= dmg
            print_slow(C.FAIL + f"Ups! Sebuah panah menyentuhmu. Kau kehilangan {dmg} nyawa." + C.ENDC, 0.02)
            return False
    else:
    # langsung lewat -> lebih berisiko
     success = random.random() < 0.5
    if success:
        print_slow(C.OKGREEN + "Dengan cekatan kau melompati jebakan." + C.ENDC, 0.02) 
        return True
    else:
        dmg = random.randint(5, 12)
        player.hp -= dmg
        print_slow(C.FAIL + f"Tanah runtuh! Kau terkena {dmg} kerusakan." + C.ENDC, 0.02)
        return False


def puzzle_riddle(player: Entity):
    print_slow("Sebuah ukiran di batu memancarkan cahaya—sebuah teka-teki muncul:", 0.02)
    print_slow("'Apa yang selalu bertambah, tapi tak pernah berkurang?'", 0.02)
    attempts = 3
    answers = ("umur", "usia")
    while attempts > 0:
        jawaban = input_prompt(f"Jawabanmu ({attempts} percobaan tersisa): ").strip().lower()
        if jawaban in answers:
            print_slow(C.OKGREEN + "Benar! Batu itu bergetar dan memberimu energi." + C.ENDC, 0.02)
            heal = 8
            player.hp = min(player.hp + heal, 40)
            print_slow(C.OKGREEN + f"Nyawamu bertambah {heal}. Sekarang {player.hp}." + C.ENDC, 0.02)
            return True
        else:
            attempts -= 1
            print_slow(C.WARNING + "Bukan itu jawaban yang benar." + C.ENDC, 0.02)
    print_slow(C.FAIL + "Ukiran padam. Tidak ada hadiah." + C.ENDC, 0.02)
    return False


def maybe_elite_encounter(path_name: str, player: Entity):
    # 25% chance muncul musuh elit berbeda berdasarkan jalur
    if random.random() < 0.25:
        if "lembah" in path_name.lower():
            elite = create_enemy("Magma Drake 🔥", 30, (8, 13), 'elite', player.level)
        else:
            elite = create_enemy("Ancient Ent 🌳", 28, (7, 12), 'elite', player.level)
        print_slow(C.HEADER + "! Musuh Elit Muncul !" + C.ENDC, 0.02)
        res = combat(player, elite)
        if res == 'victory':
            award_xp_and_maybe_level(player, elite)
            return True
        if res == 'escaped':
            return True
        return False
    return True



def game_utama():
   
    clear()
    header()
    # Pembukaan cerita (lanjutan dari teks pengguna)
    intro = (
        "Selama berabad-abad, Hutan Misterius telah menjadi tempat yang penuh dengan keajaiban dan bahaya. "
        "Banyak petualang telah memasuki hutan ini, tetapi hanya sedikit yang berhasil kembali. "
        "Arden, seorang petualang muda dan berani, telah menerima panggilan untuk mencari sumber kehidupan yang tersembunyi di dalam hutan. "
        "Dengan kemampuan dan keberaniannya, Arden memasuki Hutan Misterius, siap menghadapi apa pun yang ada di depannya."
    )
    print_slow(intro, 0.01)

    nama = input_prompt(C.OKGREEN + "Siapa namamu, petualang? " + C.ENDC).strip()
    if not nama:
        nama = "Arden"

    # Buat entitas pemain dan inventory di awal, agar persistent selama sesi
    player = Entity(nama, 30, (5, 9))
    player.level = 1
    player.xp = 0
    player.base_hp = 30
    inventory = {}

    print_slow(f"Selamat datang, {nama}. Di depanmu terbentang dua jalur berbahaya namun memikat...", 0.03)
    print_pause()

    # Tampilkan pilihan dengan gaya
    print_pause(C.HEADER + "Pilih jalurmu:" + C.ENDC)
    print_pause(C.WARNING + "1) Lembah fire   - Lembah berapi, panas dan berkilau dengan kristal magma." + C.ENDC)
    print_pause(C.OKBLUE + "2) Gunung Bug     - Gunung tinggi yang dipenuhi makhluk-makhluk aneh dan teka-teki." + C.ENDC)
    print_pause()

    # Ambil input dan gunakan if-else untuk menentukan jalur
    pilihan = input_prompt("Ketik 'Lembah fire' atau 'Gunung Bug' (atau 1/2): ").strip().lower()

    # Sisipkan scene singkat pertemuan lokal dan pertempuran pertama sebelum memilih jalur
    scene_meet_local_and_first_battle(player, inventory)

    if pilihan in ("1", "lembah fire", "lembah", "lembah fire"):
        clear()
        header()
        print_slow(C.FAIL + "Kau memilih Lembah fire..." + C.ENDC, 0.03)
        time.sleep(0.6)
        print_slow("Asap dan panas menyambut langkahmu. Batu-batu menyala dan aliran magma memantulkan bayanganmu.", 0.02)
        print_slow("Di kejauhan, sebuah cahaya biru menyala - sumber kehidupan? Namun untuk mencapainya, kau harus menyeberangi sungai lava yang berbahaya.", 0.02)
        print_pause()
        print_pause(C.OKGREEN + "Keputusan berat menanti: mencari alat penyeberangan atau mencoba melompat dengan keberanian." + C.ENDC)
        # Tantangan: jebakan sebelum pertempuran
        trap_encounter(player)
        enemy = create_enemy("Flame Warden", 20, (4, 8), 'hard', player.level)
        res = combat(player, enemy)
        if res == 'dead':
            return
        if res == 'victory':
            award_xp_and_maybe_level(player, enemy)
        # Mungkin ada musuh elit setelah pertempuran
        if not maybe_elite_encounter('lembah', player):
            return
    elif pilihan in ("2", "gunung bug", "gunung", "bug"):
        clear()
        header()
        print_slow(C.OKBLUE + "Kau memilih Gunung Bug..." + C.ENDC, 0.03)
        time.sleep(0.6)
        print_slow("Angin dingin memotong wajahmu saat kau menaiki jalur berbatu. Suara gemerisik makhluk kecil bergema di celah-celah batu.", 0.02)
        print_slow("Sebuah gerbang kayu tertutup oleh akar raksasa—di baliknya mungkin ada petunjuk sumber kehidupan yang kau cari.", 0.02)
        print_pause()
        print_pause(C.OKGREEN + "Pilihan bijak: merapal mantra membuka gerbang atau mencari jalan memanjat sampingnya." + C.ENDC)
        # Tantangan: teka-teki di Gunung Bug sebelum pertempuran
        puzzle_riddle(player)
        enemy = create_enemy("Bugling", 18, (3, 6), 'normal', player.level)
        res = combat(player, enemy)
        if res == 'dead':
            return
        if res == 'victory':
            award_xp_and_maybe_level(player, enemy)
        # Mungkin ada musuh elit setelah pertempuran
        if not maybe_elite_encounter('gunung', player):
            return
    else:
        print_slow(C.WARNING + "Pilihan tidak dikenali. Silakan jalankan ulang dan pilih 'Lembah fire' atau 'Gunung Bug'." + C.ENDC)

    # Jika pemain masih hidup setelah semua tantangan, tampilkan ending
    if player.hp > 0:
        time.sleep(0.6)
        clear()
        header()
        print_slow("🌟 Akhir Kisah 🌟", 0.02)
        print_pause()
        print_slow("Arden berhasil menyelesaikan misinya dan menemukan sumber kehidupan yang tersembunyi di dalam Hutan Misterius.", 0.02)
        print_slow("Dengan hati penuh kebanggaan dan keberanian, ia kembali ke desa. Penduduk menyambutnya sebagai pahlawan.", 0.02)
        print_slow("Hutan Misterius kini menjadi tempat yang lebih aman berkat tindakannya.", 0.02)
        print_pause()
        potions = inventory.get('potions', 0)
        if potions:
            print_slow(C.OKGREEN + f"Hadiah yang dibawa pulang: {potions} ramuan penyembuh." + C.ENDC, 0.02)
        print_slow(C.OKCYAN + "=== SELAMAT! Misi Terselesaikan ===" + C.ENDC, 0.03)


if __name__ == "__main__":
    game_utama()