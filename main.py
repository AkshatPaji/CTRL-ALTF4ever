
import pygame
import random

pygame.init()

info = pygame.display.Info()
SW, SH = info.current_w, info.current_h

BOOT_SIZE = (int(SW * 0.60), int(SH * 0.60))
GAME_SIZE = (int(SW * 0.85), int(SH * 0.85))

screen = pygame.display.set_mode(BOOT_SIZE)
pygame.display.set_caption("CTRL+ALTF4EVER")
clock = pygame.time.Clock()

# green text = hacker, trust me bro
BLACK = (7, 12, 9)
PANEL = (13, 23, 16)
GREEN = (100, 255, 140)
DARK_GREEN = (35, 100, 55)
WHITE = (220, 235, 220)
RED = (255, 75, 75)
GREY = (90, 105, 95)
YELLOW = (255, 220, 100)
WIN_BG = (215, 220, 214)
WIN_TEXT = (25, 30, 25)

font = pygame.font.SysFont("monospace", 17)
small = pygame.font.SysFont("monospace", 13)
tiny = pygame.font.SysFont("monospace", 11)
title_font = pygame.font.SysFont("monospace", 21, bold=True)
logo_font = pygame.font.SysFont("monospace", 16, bold=True)

phase = "boot"
popups = []
score = 0
popup_count = 0
start_time = 0
last_spawn = 0
start_button = pygame.Rect(0, 0, 0, 0)
restart_button = pygame.Rect(0, 0, 0, 0)

logo = [
    "  ____ ____   _    _____",
    " / ___|  _ \\ / \\  |  ___|",
    "| |   | |_) / _ \\ | |_   ",
    "| |___|  __/ ___ \\|  _|  ",
    " \\____|_| /_/   \\_\\_|    ",
]

# if any of these sound familiar, no they dont
messages = [
    ("SKILL ISSUE", "Have you tried being less bad?", "skill issue detected"),
    ("FATAL ERROR", "bro really clicked run 💀", "this is literally your fault"),
    ("DEV MODE", "who let bro cook", "the kitchen is closed"),
    ("MEMORY LEAK", "your last braincell left", "it had a good run"),
    ("GIT ERROR", "works on my machine lol", "ship it anyway"),
    ("PYTHON.EXE", "indentation? never heard of her", "four spaces of pain"),
    ("CERTIFIED DEV", "made with 3 braincells", "and one questionable idea"),
    ("SYSTEM WARNING", "bro thinks he's in Mr Robot", "bro is in a python file"),
    ("NOT RESPONDING", "me when someone says touch grass", "request denied"),
    ("404 BRAIN", "brain.exe was not found", "try turning it off and on"),
    ("CRITICAL THINKING", "thinking... thinking...", "yeah nothing happened"),
    ("UPDATE FAILED", "new skill issue just dropped", "patch notes unavailable"),
    ("GITHUB MOMENT", "pushed straight to main 💀", "no tests were harmed"),
    ("SUDO ERROR", "permission denied. get good.", "sudo make me competent"),
    ("FINAL BOSS", "you named it final_final_v3", "and still lost the file"),
    ("FREE GIFT", "i am NOT a dev btw", "but the gift is mine now"),
    ("REALITY.EXE", "it works. dont ask why.", "we are NOT touching that code"),
    ("BUG REPORT", "feature or bug? yes.", "close the issue and move on"),
    ("TOUCH GRASS", "grass.exe not installed", "try going outside manually"),
    ("IMPOSTER SYNDROME", "bro actually wrote this code", "character development??"),
]

# tiny achievements because why not
achievements = [
    (1, "FIRST BLOOD", "closed a window. proud of u."),
    (5, "WINDOW SHOPPER", "five errors gone. 900 more to go."),
    (10, "ACTUAL DEVELOPER??", "okay wait ur kinda cooking"),
    (20, "NO LIFER MODE", "the grass is getting concerned"),
    (35, "FINAL BOSS ENERGY", "this is not a productive use of time"),
]

unlocked = set()
notice = ""
notice_until = 0


def draw_text(msg, x, y, color=GREEN, f=None):
    if f is None:
        f = font

    img = f.render(str(msg), True, color)
    screen.blit(img, (int(x), int(y)))


def centered(msg, rect, color=GREEN, f=None):
    if f is None:
        f = font

    img = f.render(str(msg), True, color)
    screen.blit(img, img.get_rect(center=rect.center))


def draw_button(rect, label, mouse):
    hover = rect.collidepoint(mouse)
    color = (30, 75, 42) if hover else PANEL

    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, GREEN, rect, 2)
    centered(label, rect, GREEN, title_font)


def boot_screen(mouse):
    w, h = screen.get_size()
    screen.fill(BLACK)

    pygame.draw.rect(screen, PANEL, (0, 0, w, 42))
    draw_text("CPAF // BOOT LOADER", 20, 11, GREEN, title_font)
    draw_text("v0.1-dev-ish", w - 125, 14, GREY, tiny)

    # logo
    logo_y = int(h * 0.10)
    for line in logo:
        draw_text(line, int(w * 0.04), logo_y, GREEN, logo_font)
        logo_y += 21

    # terminal panel
    tx = int(w * 0.035)
    ty = int(h * 0.44)
    tw = int(w * 0.60)
    th = int(h * 0.41)

    terminal = pygame.Rect(tx, ty, tw, th)
    pygame.draw.rect(screen, PANEL, terminal)
    pygame.draw.rect(screen, DARK_GREEN, terminal, 1)

    draw_text("akshat@probably-not-a-hacker:~", tx + 15, ty + 12, WHITE, tiny)
    pygame.draw.line(
        screen, DARK_GREEN,
        (tx + 15, ty + 34), (terminal.right - 15, ty + 34)
    )

    y = ty + 49
    for line, color in [
        ("> booting up questionable decisions...", GREEN),
        ("> checking if the code actually runs...", GREEN),
        ("> confidence level: 100%", YELLOW),
        ("> skill level: still loading...", RED),
        ("> yeah we're probably fine_", WHITE),
    ]:
        draw_text(line, tx + 15, y, color, small)
        y += 27

    px = int(w * 0.70)
    draw_text("YO.", px, int(h * 0.48), WHITE, title_font)
    draw_text("you made this.", px, int(h * 0.55), GREY, small)
    draw_text("you tell me if it works.", px, int(h * 0.59), GREY, tiny)

    bw = int(w * 0.23)
    bh = 54
    bx = min(px, w - bw - 15)
    by = int(h * 0.70)

    start = pygame.Rect(bx, by, bw, bh)
    draw_button(start, "[ LETS GOO ]", mouse)

    draw_text("WARNING: skill issue may occur", px, by + 70, RED, tiny)

    pygame.draw.rect(screen, PANEL, (0, h - 35, w, 35))
    pygame.draw.line(screen, DARK_GREEN, (0, h - 35), (w, h - 35))
    draw_text("STATUS: SOMEHOW RUNNING", 15, h - 24, GREEN, tiny)
    draw_text("ESC = rage quit", w - 130, h - 24, GREY, tiny)

    return start


def make_popup():
    global popup_count
    popup_count += 1

    w, h = screen.get_size()

    pw = min(random.randint(330, 440), w - 30)
    ph = min(random.randint(155, 205), h - 90)

    x = random.randint(15, max(15, w - pw - 15))
    y = random.randint(50, max(50, h - ph - 50))

    title, message, extra = random.choice(messages)

    popups.append({
        "rect": pygame.Rect(x, y, pw, ph),
        "title": title,
        "message": message,
        "extra": extra,
        "id": popup_count,
    })


def draw_popup(p):
    r = p["rect"]

    pygame.draw.rect(screen, (0, 0, 0), r.move(5, 5))

    pygame.draw.rect(screen, WIN_BG, r)

    bar = pygame.Rect(r.x, r.y, r.width, 31)
    pygame.draw.rect(screen, (25, 65, 40), bar)
    pygame.draw.rect(screen, GREEN, r, 2)

    draw_text(p["title"], r.x + 10, r.y + 7, WHITE, tiny)

    # red close button
    close = pygame.Rect(r.right - 29, r.y + 4, 23, 22)
    pygame.draw.rect(screen, (110, 25, 25), close)
    pygame.draw.rect(screen, RED, close, 1)
    centered("X", close, WHITE, tiny)

    # message
    draw_text("!", r.x + 17, r.y + 48, RED, title_font)
    draw_text(p["message"], r.x + 50, r.y + 49, WIN_TEXT, small)
    draw_text(p["extra"], r.x + 50, r.y + 75, (75, 80, 75), tiny)

    draw_text("this is a you problem btw", r.x + 17, r.bottom - 32,
              (70, 75, 70), tiny)

    ok = pygame.Rect(r.right - 88, r.bottom - 35, 68, 24)
    pygame.draw.rect(screen, (230, 234, 228), ok)
    pygame.draw.rect(screen, (50, 60, 50), ok, 1)
    centered("OK", ok, WIN_TEXT, tiny)


def popup_click(pos):
    global score, notice, notice_until
    for i in range(len(popups) - 1, -1, -1):
        p = popups[i]
        r = p["rect"]

        close = pygame.Rect(r.right - 29, r.y + 4, 23, 22)
        ok = pygame.Rect(r.right - 88, r.bottom - 35, 68, 24)

        if close.collidepoint(pos) or ok.collidepoint(pos):
            popups.pop(i)
            score += 1

            for target, name, desc in achievements:
                if score >= target and target not in unlocked:
                    unlocked.add(target)
                    notice = name + " // " + desc
                    notice_until = pygame.time.get_ticks() + 3000
                    return

            reactions = [
                "W move. unfortunately there are more.",
                "bro thinks its over 💀",
                "one less problem. like 400 more.",
                "closing windows is ur new personality",
                "okay dev, calm down.",
                "this is basically IT support now.",
                "the bugs are multiplying btw",
                "goated click. mid life choices.",
            ]

            notice = random.choice(reactions)
            notice_until = pygame.time.get_ticks() + 1800
            return


def game_screen():
    w, h = screen.get_size()
    screen.fill(BLACK)

    for x in range(0, w, 40):
        pygame.draw.line(screen, (13, 28, 18), (x, 0), (x, h))
    for y in range(0, h, 40):
        pygame.draw.line(screen, (13, 28, 18), (0, y), (w, y))

    pygame.draw.rect(screen, PANEL, (0, 0, w, 46))
    draw_text("CPAF // questionable desktop", 15, 13, GREEN, title_font)
    draw_text(f"CLOSED: {score}", int(w * 0.42), 15, WHITE, small)
    draw_text(f"ERRORS: {len(popups)}", int(w * 0.55), 15, RED, small)

    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    draw_text(f"UPTIME: {elapsed}s", w - 125, 16, GREEN, tiny)

    draw_text("SYSTEM STATUS: its complicated", 28, 70, GREY, tiny)
    draw_text("[???]", 48, 100, GREEN, title_font)
    draw_text("definitely_not_a_virus.exe", 48, 128, GREY, tiny)

    draw_text("[gift]", 48, 180, YELLOW, title_font)
    draw_text("motivation.zip", 48, 208, GREY, tiny)

    for p in popups:
        draw_popup(p)
        
    if pygame.time.get_ticks() < notice_until:
        box = pygame.Rect(20, 53, min(w - 40, 480), 32)
        pygame.draw.rect(screen, PANEL, box)
        pygame.draw.rect(screen, GREEN, box, 1)
        draw_text(notice[:55], box.x + 8, box.y + 9, YELLOW, tiny)

    pygame.draw.rect(screen, PANEL, (0, h - 42, w, 42))
    pygame.draw.line(screen, DARK_GREEN, (0, h - 42), (w, h - 42))

    draw_text("CPAF", 15, h - 29, GREEN, title_font)
    draw_text("made with questionable decisions", 100, h - 26, GREY, tiny)
    draw_text("ESC: QUIT", w - 90, h - 26, GREEN, tiny)


running = True

while running:
    clock.tick(60)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if phase == "boot":
                if start_button.collidepoint(event.pos):
                    phase = "game"
                    screen = pygame.display.set_mode(GAME_SIZE)
                    pygame.display.set_caption("CTRL+ALTF4EVER")

                    start_time = pygame.time.get_ticks()
                    last_spawn = start_time
                    make_popup()

            elif phase == "game":
                popup_click(event.pos)

    if phase == "boot":
        start_button = boot_screen(mouse)

    elif phase == "game":
        now = pygame.time.get_ticks()

        # each close makes the next one arrive faster
        delay = max(450, 1800 - score * 35)

        if now - last_spawn >= delay:
            make_popup()
            last_spawn = now

        game_screen()

    pygame.display.flip()

pygame.quit()
 