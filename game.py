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


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_slow(text, delay=0.02):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()


def header():
    print(C.OKCYAN + """
  *************************************************
  *          PETUALANGAN DI HUTAN MISTERIUS       *
  *************************************************
    """ + C.ENDC)


# Entitas pemain / musuh dan fungsi pertempuran
class Entity:
    def __init__(self, name, hp, attack_range):
        self.name = name
        self.hp = hp
        self.attack_range = attack_range

    def attack(self):
        return random.randint(*self.attack_range)


def combat(player: Entity, enemy: Entity):
    print()
    print_slow(f"Tiba-tiba, {enemy.name} muncul dari balik bayangan!", 0.02)
    while enemy.hp > 0 and player.hp > 0:
        print(f"\nNyawamu: {player.hp}  |  {enemy.name} HP: {enemy.hp}")
        aksi = input("Pilih aksi: 1) Serang   2) Lari  -> ").strip().lower()
        if aksi in ("1", "serang", "s"):
            dmg = player.attack()
            enemy.hp -= dmg
            print_slow(C.OKGREEN + f"Kau menyerang dan memberi {dmg} kerusakan!" + C.ENDC, 0.01)
            if enemy.hp <= 0:
                print_slow(C.OKCYAN + f"{enemy.name} tumbang. Kau menang!" + C.ENDC, 0.02)
                return True
            edmg = enemy.attack()
            player.hp -= edmg
            print_slow(C.FAIL + f"{enemy.name} menyerang balik dan memberikan {edmg} kerusakan!" + C.ENDC, 0.01)
        elif aksi in ("2", "lari", "l"):
            print_slow(C.WARNING + "Kau memilih mundur dengan cepat, selamat... untuk sekarang." + C.ENDC, 0.02)
            return True
        else:
            print_slow(C.WARNING + "Aksi tidak dikenali. Ketik 'serang' atau 'lari'." + C.ENDC, 0.01)

    if player.hp <= 0:
        print_slow(C.FAIL + "Kau roboh. Petualangan berakhir..." + C.ENDC, 0.02)
        return False
    return True


def scene_meet_local_and_first_battle(player: Entity, inventory: dict):
    clear()
    header()
    # Pertemuan dengan penduduk lokal
    print_slow("🌲 Arden memasuki Hutan Misterius, di mana udara dipenuhi suara burung dan pohon-pohon tinggi...", 0.01)
    time.sleep(0.3)
    print_slow("Seorang penduduk lokal muncul—seorang wanita tua berjubah yang ramah. 🧓✨", 0.02)
    print()
    print_slow("'Sumber kehidupan ada di dalam hutan, tetapi kamu harus berhati-hati.'", 0.02)
    print_slow("'Ada banyak bahaya di sini, termasuk monster-monster yang mengancam nyawa.'", 0.02)
    print()
    print_slow("Wanita itu memberikanmu peta kecil dan sebotol ramuan penyembuh. 🗺️🧪", 0.02)
    inventory.setdefault('potions', 0)
    inventory['potions'] += 1
    print_slow(C.OKGREEN + "[Dapat] 1x Ramuan Penyembuh" + C.ENDC, 0.02)
    print()

    # Pertemuan pertama: serigala bermata merah
    print_slow("Di sela-sela semak, mata merah menyala menatapmu... 🐺🔥", 0.02)
    enemy = Entity("Red-Eyed Wolf 🐺", 22, (5, 9))
    won = combat(player, enemy)

    if won and player.hp > 0 and enemy.hp <= 0:
        print_slow(C.OKCYAN + "Dengan kemampuan dan strategimu, Arden berhasil mengalahkan monster itu." + C.ENDC, 0.02)
        # Reward: obat-obatan (potion sudah diberikan) dan upgrade kemampuan
        print_slow("Kau menemukan beberapa obat-obatan dan sebuah kristal yang meningkatkan seranganmu. ✨⚔️", 0.02)
        inventory['potions'] = inventory.get('potions', 0) + 1
        # naikkan attack max
        low, high = player.attack_range
        player.attack_range = (low, high + 2)
        print_slow(C.OKGREEN + f"[Upgrade] Serangan maksimum bertambah menjadi {player.attack_range[1]}" + C.ENDC, 0.02)
        # sedkit penyembuhan
        player.hp = min(player.hp + 10, 40)
        print_slow(C.OKGREEN + f"Arden sembuh sedikit: Nyawa sekarang {player.hp}" + C.ENDC, 0.02)
    else:
        print_slow(C.WARNING + "Pertempuran berakhir tanpa hadiah." + C.ENDC, 0.02)


def trap_encounter(player: Entity):
    print_slow("Saat berjalan pelan, tanah di hadapanmu terasa rapuh...", 0.02)
    print_slow("Kau melihat ada jebakan tersembunyi.", 0.02)
    pilihan = input("Apa yang kau lakukan? ('periksa'/'lewati'): ").strip().lower()
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
        jawaban = input(f"Jawabanmu ({attempts} percobaan tersisa): ").strip().lower()
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
            elite = Entity("Magma Drake 🔥", 30, (8, 13))
        else:
            elite = Entity("Ancient Ent 🌳", 28, (7, 12))
        print_slow(C.HEADER + "! Musuh Elit Muncul !" + C.ENDC, 0.02)
        return combat(player, elite)
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

    nama = input(C.OKGREEN + "Siapa namamu, petualang? " + C.ENDC).strip()
    if not nama:
        nama = "Arden"

    # Buat entitas pemain dan inventory di awal, agar persistent selama sesi
    player = Entity(nama, 30, (5, 9))
    inventory = {}

    print_slow(f"Selamat datang, {nama}. Di depanmu terbentang dua jalur berbahaya namun memikat...", 0.03)
    print()

    # Tampilkan pilihan dengan gaya
    print(C.HEADER + "Pilih jalurmu:" + C.ENDC)
    print(C.WARNING + "1) Lembah fire   - Lembah berapi, panas dan berkilau dengan kristal magma." + C.ENDC)
    print(C.OKBLUE + "2) Gunung Bug     - Gunung tinggi yang dipenuhi makhluk-makhluk aneh dan teka-teki." + C.ENDC)
    print()

    # Ambil input dan gunakan if-else untuk menentukan jalur
    pilihan = input("Ketik 'Lembah fire' atau 'Gunung Bug' (atau 1/2): ").strip().lower()

    # Sisipkan scene singkat pertemuan lokal dan pertempuran pertama sebelum memilih jalur
    scene_meet_local_and_first_battle(player, inventory)

    if pilihan in ("1", "lembah fire", "lembah", "lembah fire"):
        clear()
        header()
        print_slow(C.FAIL + "Kau memilih Lembah fire..." + C.ENDC, 0.03)
        time.sleep(0.6)
        print_slow("Asap dan panas menyambut langkahmu. Batu-batu menyala dan aliran magma memantulkan bayanganmu.", 0.02)
        print_slow("Di kejauhan, sebuah cahaya biru menyala - sumber kehidupan? Namun untuk mencapainya, kau harus menyeberangi sungai lava yang berbahaya.", 0.02)
        print()
        print(C.OKGREEN + "Keputusan berat menanti: mencari alat penyeberangan atau mencoba melompat dengan keberanian." + C.ENDC)
            # Pertempuran singkat di Lembah fire (menggunakan Entity & combat)
        enemy = Entity("Flame Warden", 20, (4, 8))
        combat(player, enemy)
    elif pilihan in ("2", "gunung bug", "gunung", "bug"):
        clear()
        header()
        print_slow(C.OKBLUE + "Kau memilih Gunung Bug..." + C.ENDC, 0.03)
        time.sleep(0.6)
        print_slow("Angin dingin memotong wajahmu saat kau menaiki jalur berbatu. Suara gemerisik makhluk kecil bergema di celah-celah batu.", 0.02)
        print_slow("Sebuah gerbang kayu tertutup oleh akar raksasa—di baliknya mungkin ada petunjuk sumber kehidupan yang kau cari.", 0.02)
        print()
        print(C.OKGREEN + "Pilihan bijak: merapal mantra membuka gerbang atau mencari jalan memanjat sampingnya." + C.ENDC)
        # Pertempuran singkat di Gunung Bug (menggunakan Entity & combat)
        enemy = Entity("Bugling", 18, (3, 6))
        combat(player, enemy)
    else:
        print_slow(C.WARNING + "Pilihan tidak dikenali. Silakan jalankan ulang dan pilih 'Lembah fire' atau 'Gunung Bug'." + C.ENDC)


if __name__ == "__main__":
    game_utama()