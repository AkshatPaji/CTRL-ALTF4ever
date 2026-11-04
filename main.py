import math 
import random
import pygame

# CTRL+ALTF4EVER
# I started this as a tiny popup simulator. It has since become a desktop problem.
# If something looks cursed, that's probably a feature. Probably.


pygame.init()
pygame.display.set_caption("CTRL+ALTF4EVER // questionable decisions")
clock = pygame.time.Clock()

info = pygame.display.Info()
SW, SH = info.current_w, info.current_h
# One SDL window, one size, for the whole session.
# Hyprland can get into a resize-feedback loop if Pygame recreates the
# display surface every time the compositor sends VIDEORESIZE.
GAME_SIZE = (min(SW, max(760, int(SW * 0.85))), min(SH, max(560, int(SH * 0.85))))
screen = pygame.display.set_mode(GAME_SIZE)

# Colours. Green text = hacker. I don't make the rules.
BLACK = (6, 10, 8)
PANEL = (13, 22, 17)
PANEL_2 = (19, 33, 25)
GREEN = (105, 255, 145)
DARK_GREEN = (35, 105, 58)
WHITE = (225, 235, 225)
GREY = (130, 145, 133)
RED = (255, 85, 85)
YELLOW = (255, 218, 105)
BLUE = (105, 185, 255)
PURPLE = (190, 145, 255)
WIN_TEXT = (25, 31, 27)


font = pygame.font.SysFont("monospace", 18)
small = pygame.font.SysFont("monospace", 15)
tiny = pygame.font.SysFont("monospace", 13)
title_font = pygame.font.SysFont("monospace", 22, bold=True)
big_font = pygame.font.SysFont("monospace", 34, bold=True)

# Boot screen fonts from the supplied v3.1 layout.
boot_header = pygame.font.SysFont("monospace", 25, bold=True)
boot_logo = pygame.font.SysFont("monospace", 23, bold=True)
boot_terminal = pygame.font.SysFont("monospace", 17)
boot_small = pygame.font.SysFont("monospace", 15)
boot_title = pygame.font.SysFont("monospace", 21, bold=True)
boot_dev = pygame.font.SysFont("monospace", 16)


phase = "boot"
popups = []
score = 0
popup_count = 0
start_time = 0
last_spawn = 0
last_input = pygame.time.get_ticks()
notice = ""
notice_until = 0
toast_queue = []
active_toasts = []
unlocked = set()
end_reason = ""
end_detail = ""

# Some windows are helpful. Some are absolutely not. Read the tiny labels, gamer.
WINDOW_TYPES = [
    # BAD: close these. Every single one is made up. The internet is not giving you $100.
    {"kind": "bad", "app": "BROWSER // TOTALLY LEGIT", "title": "CONGRATS, YOU GOT $100", "message": "You were selected by a website with 4 pixels and no privacy policy.", "extra": "CLAIM NOW button definitely does not lead anywhere good.", "accent": None},
    {"kind": "bad", "app": "MAIL // VERIFIED-ISH", "title": "MESSAGE FROM DONALD TRUMP", "message": "PARODY: 'Your code is tremendous. The biggest code. Believe me.'", "extra": "Not real. Not even close. Please close this fan mail.", "accent": None},
    {"kind": "bad", "app": "MESSAGES // 1 NEW", "title": "MESSAGE FROM YOUR CRUSH", "message": "hey... are you free? need help with something lol", "extra": "The game wrote this. Do not start planning the wedding.", "accent": None},
    {"kind": "bad", "app": "ANTIVIRUS // FREE EDITION", "title": "YOUR PC HAS 9,001 VIRUSES", "message": "9,000 are this popup. The last one is called confidence.exe.", "extra": "BUY PREMIUM TO REMOVE VIRUSES (premium is also fake).", "accent": None},
    {"kind": "bad", "app": "DOWNLOADS // TRUST ME", "title": "DOWNLOAD MORE RAM", "message": "Your computer is running low on imaginary memory.", "extra": "Download: 4 KB | RAM gained: emotionally significant.", "accent": None},
    {"kind": "bad", "app": "SYSTEM // URGENT-ish", "title": "YOUR MOUSE IS UNDER SURVEILLANCE", "message": "It has been moving around suspiciously. Very suspicious.", "extra": "Our investigation found: a hand. Case closed.", "accent": None},
  
  
    {"kind": "bad", "app": "GAMING // FREE REWARD", "title": "100,000 V-BUCKS UNLOCKED", "message": "Enter your password, shoe size and favourite motherboard.", "extra": "Terms: trust me bro. Close this before bro gets scammed.", "accent": None},
    {"kind": "bad", "app": "GIT // CONFLICT", "title": "MERGE CONFLICT DETECTED", "message": "main and your last braincell have diverged.", "extra": "Suggested fix: git blame yourself and close this window.", "accent": None},
    {"kind": "bad", "app": "GROUP CHAT // 47 UNREAD", "title": "BRO THE BUILD IS BROKEN", "message": "47 people have typed 'works on my machine'.", "extra": "Congratulations, you're now unpaid IT support.", "accent": None},
    {"kind": "bad", "app": "UPDATE // DEFINITELY REAL", "title": "CRITICAL UPDATE AVAILABLE", "message": "Installing update may take 3 to 5 business years.", "extra": "Progress: 0.0000001% | ETA: see you in 2031.", "accent": None},

    # GOOD: still fake. These are decoys, so leave them alone for the points.
    {"kind": "good", "app": "SYSTEM // SECURITY", "title": "SECURITY CHECK COMPLETE", "message": "No problems were found during the scheduled scan.", "extra": "The scan finished in the security app you already use.", "accent": None},
    {"kind": "good", "app": "SYSTEM // BACKUP", "title": "BACKUP COMPLETED", "message": "Your selected project folder was backed up successfully.", "extra": "The destination matches the backup location you selected.", "accent": None},
    {"kind": "good", "app": "GIT // BUILD", "title": "BUILD COMPLETED SUCCESSFULLY", "message": "The latest project build finished with no errors.", "extra": "The repository and commit match your recent build.", "accent": None},
    {"kind": "good", "app": "SYSTEM // PROTECTION", "title": "SCAN FINISHED", "message": "The scheduled scan found no threats.", "extra": "This is the security app already installed on your computer.", "accent": None},
    {"kind": "good", "app": "MESSAGES // REMINDER", "title": "NEW MESSAGE RECEIVED", "message": "You have a new message from a saved contact.", "extra": "The sender is already in your contacts. Open it when ready.", "accent": None},
    {"kind": "good", "app": "BROWSER // DOWNLOAD", "title": "DOWNLOAD COMPLETED", "message": "The file you selected has finished downloading.", "extra": "The file name and website match the download you started.", "accent": None},
    {"kind": "good", "app": "CALENDAR // REMINDER", "title": "UPCOMING EVENT", "message": "Your saved calendar event starts in 15 minutes.", "extra": "This reminder matches an event already in your calendar.", "accent": None},

    # More everyday desktop noise: realistic formats, fictional accounts/services.
    {"kind": "bad", "app": "NETWORK // WI-FI", "title": "NETWORK AUTHENTICATION REQUIRED", "message": "Your connection will expire unless you verify your account.", "extra": "The network name is misspelled and the page has no organisation details.", "accent": None},
    {"kind": "bad", "app": "FILES // DOWNLOAD", "title": "INVOICE_OCTOBER.PDF.exe", "message": "A document download arrived with an executable file extension.", "extra": "An invoice should not need to install an app. Nice try, download folder.", "accent": None},
    {"kind": "bad", "app": "BROWSER // SECURITY CHECK", "title": "URGENT: UPDATE YOUR PAYMENT DETAILS", "message": "Your subscription is on hold. Confirm billing information to avoid losing access.", "extra": "The sender domain does not match the service named in the message.", "accent": None},
    {"kind": "bad", "app": "SYSTEM // STORAGE", "title": "DISK SPACE CRITICALLY LOW", "message": "Click CLEAN NOW to recover 48 GB instantly.", "extra": "The storage panel shows 312 GB free. This alert came from a random webpage.", "accent": None},
    {"kind": "bad", "app": "NETWORK // VPN", "title": "VPN CONNECTION LOST", "message": "Reconnect using the attached configuration package.", "extra": "The file is from an unknown sender. The installed VPN is still connected.", "accent": None},
    {"kind": "bad", "app": "MAIL // DELIVERY", "title": "PACKAGE DELIVERY FAILED", "message": "A parcel could not be delivered. Pay a small redelivery fee.", "extra": "No courier name, tracking number, or matching order is provided.", "accent": None},
    {"kind": "bad", "app": "BROWSER // ACCOUNT", "title": "UNUSUAL SIGN-IN DETECTED", "message": "We noticed a sign-in attempt. Review activity to secure your account.", "extra": "The link points to a lookalike domain, not the account's official site.", "accent": None},
    {"kind": "bad", "app": "UPDATE // DRIVER", "title": "GRAPHICS DRIVER OUTDATED", "message": "Install this driver pack to unlock 900% more FPS.", "extra": "Publisher: Unknown. File: driver_booster_final_FINAL.exe.", "accent": None},
    {"kind": "bad", "app": "CHAT // WORKSPACE", "title": "YOUR ADMIN NEEDS A GIFT CARD", "message": "Can you buy gift cards urgently? I'll pay you back after this meeting.", "extra": "The request came from a new address, not the saved workspace contact.", "accent": None},
    {"kind": "bad", "app": "CALENDAR // INVITATION", "title": "MEETING INVITATION: REQUIRED", "message": "Join this meeting to avoid account suspension.", "extra": "The organiser is 'Support Team' using a free personal email address.", "accent": None},
    {"kind": "bad", "app": "BROWSER // REWARD", "title": "YOU ARE TODAY'S LUCKY VISITOR", "message": "A mystery prize is waiting. Spin now before the timer reaches zero.", "extra": "The countdown resets every time the page reloads. Classic.", "accent": None},
    {"kind": "bad", "app": "SYSTEM // CLIPBOARD", "title": "CLIPBOARD SYNC FAILED", "message": "Install this helper to restore clipboard history.", "extra": "The helper requests access to files and contacts. Why does it need those?", "accent": None},
    {"kind": "good", "app": "NETWORK // WI-FI", "title": "CONNECTED TO HOME-NETWORK", "message": "Internet access is available. Signal strength: excellent.", "extra": "Network name matches the saved connection. No action is required.", "accent": None},
    {"kind": "good", "app": "FILES // COPY COMPLETE", "title": "FILES COPIED SUCCESSFULLY", "message": "24 items copied to Projects/Backup.", "extra": "The destination and item count match the copy you started.", "accent": None},
    {"kind": "good", "app": "SYSTEM // UPDATE", "title": "UPDATE READY TO INSTALL", "message": "A system update is available from the configured software updater.", "extra": "Publisher and package source match the system's trusted repositories.", "accent": None},
    {"kind": "good", "app": "MAIL // SECURITY", "title": "PASSWORD RESET REQUEST RECEIVED", "message": "A password reset was requested for your account.", "extra": "You initiated this request from the account settings page. Keep this notice.", "accent": None},
    {"kind": "good", "app": "NETWORK // DOWNLOAD", "title": "DOWNLOAD COMPLETED", "message": "project-assets.zip finished downloading.", "extra": "The file name and source match the download you started.", "accent": None},
    {"kind": "good", "app": "CALENDAR // REMINDER", "title": "REMINDER: PROJECT REVIEW", "message": "Your project review starts in 15 minutes.", "extra": "This reminder matches an event in your calendar.", "accent": None},
    {"kind": "good", "app": "SYSTEM // BACKUP", "title": "BACKUP COMPLETED", "message": "Your scheduled backup finished successfully.", "extra": "Last run: today. Destination: your configured backup drive.", "accent": None},
    {"kind": "good", "app": "CHAT // WORKSPACE", "title": "BUILD STATUS: PASSED", "message": "Continuous integration completed successfully.", "extra": "Repository and commit match the project you pushed.", "accent": None},
 
 
    {"kind": "good", "app": "FILES // TRASH", "title": "RESTORE COMPLETED", "message": "The selected file was restored to its original folder.", "extra": "You requested this restore moments ago. All good.", "accent": None},
    {"kind": "good", "app": "BROWSER // DOWNLOAD", "title": "DOWNLOAD BLOCKED: UNSAFE FILE", "message": "The browser blocked a file that may be harmful.", "extra": "This warning came from the browser's built-in download protection.", "accent": None},
    {"kind": "good", "app": "NETWORK // CONNECTION", "title": "SECURE CONNECTION ESTABLISHED", "message": "The site connection is encrypted.", "extra": "The address is the exact site you entered and the certificate is valid.", "accent": None},
]

# Window colours are random decoration, never a clue to the answer.
WINDOW_PALETTES = [
    ((239, 226, 207), (126, 83, 61)),  # warm paper
    ((222, 231, 242), (67, 91, 125)),  # faded blue
    ((231, 224, 239), (105, 78, 126)), # dusty violet
    ((224, 236, 222), (77, 111, 75)),  # sage
    ((242, 226, 225), (137, 83, 82)),  # muted rose
    ((235, 232, 214), (119, 108, 65)), # sand
    ((220, 235, 233), (65, 112, 109)), # teal
    ((235, 228, 216), (112, 91, 69)),  # beige
]


REACTIONS = [
    "W click. the desktop is still fighting back.",
    "one less window, approximately 900 more.",
    "IT support called. they said good luck.",
    "okay okay, I see the mouse skills.",
    "the bugs have started a union.",
    "feature or bug? let's not investigate.",
    "you closed it. I made three more. fair trade.",
    "this is what the README warned us about.",
]

# Time achievements. The longer you stay, the more concerned I get.
TIME_ACHIEVEMENTS = [
    (600, "GO TOUCH GRASS", "10 minutes. the outside world misses you."),
    (1800, "SHE LEFT (THE DESKTOP DIDN'T)", "30 minutes. ur staying longer than she did."),
    (3600, "PLEASE SEEK SUNLIGHT", "one whole hour. this is not a benchmark."),
]


SCORE_ACHIEVEMENTS = [
    (1, "FIRST WINDOW DOWN", "wow. you clicked a rectangle. proud."),
    (10, "WINDOWS UPDATE", "you're getting suspiciously good at this."),
    (50, "CERTIFIED CLICKER", "your mouse deserves a day off."),
    (100, "WAIT, YOU'RE GOOD?", "wow you're good. I wasn't. I made the game."),
]


def draw_text(text, x, y, color=GREEN, f=None):
    if f is None:
        f = font
    image = f.render(str(text), True, color)
    screen.blit(image, (int(x), int(y)))


def centered(text, rect, color=GREEN, f=None):
    if f is None:
        f = font
    image = f.render(str(text), True, color)
    screen.blit(image, image.get_rect(center=rect.center))


def clipped_text(text, max_width, f):
    text = str(text)
    while text and f.size(text)[0] > max_width:
        text = text[:-2] + "…"
    return text


def set_notice(text, duration=2200):
    global notice, notice_until
    notice = text
    notice_until = pygame.time.get_ticks() + duration


def register_input():
    global last_input
    last_input = pygame.time.get_ticks()


def achievement_toast(name, desc):
    # Proper little achievement cards. The old single-line notice kept getting
    # overwritten, which is a very 2 AM bug to introduce.
    toast_queue.append({
        "title": name,
        "desc": desc,
        "created": pygame.time.get_ticks(),
    })

def update_toasts():
    now = pygame.time.get_ticks()
    # Keep a queue so unlocking two things quickly doesn't eat either toast.
    if toast_queue and (not active_toasts or now - active_toasts[-1]["created"] > 450):
        item = toast_queue.pop(0)
        item["created"] = now
        active_toasts.append(item)
    active_toasts[:] = [t for t in active_toasts if now - t["created"] < 4300]


def draw_toasts():
    now = pygame.time.get_ticks()
    w, _ = screen.get_size()
    for index, toast in enumerate(reversed(active_toasts[-3:])):
        age = now - toast["created"]
        width, height = 370, 76
        x = w - width - 18
        target_y = 58 + index * (height + 10)
        # Slide in, then gently fade out. Nothing fancy; no extra window.
        slide = min(1.0, age / 220)
        if age > 3800:
            slide *= max(0.0, (4300 - age) / 500)
        x += int((1.0 - slide) * 45)
        rect = pygame.Rect(x, target_y, width, height)
        pygame.draw.rect(screen, (8, 18, 12), rect.move(4, 4))
        pygame.draw.rect(screen, PANEL_2, rect)
        pygame.draw.rect(screen, YELLOW, rect, 2)
        pygame.draw.rect(screen, YELLOW, (rect.x, rect.y, 7, rect.height))
        draw_text("ACHIEVEMENT UNLOCKED", rect.x + 17, rect.y + 9, YELLOW, tiny)
        draw_text(clipped_text(toast["title"], width - 32, small), rect.x + 17, rect.y + 28, WHITE, small)
        draw_text(clipped_text(toast["desc"], width - 32, tiny), rect.x + 17, rect.y + 51, GREEN, tiny)

def draw_button(rect, label, mouse):
    hover = rect.collidepoint(mouse)
    pygame.draw.rect(screen, (25, 65, 39) if hover else PANEL_2, rect)
    pygame.draw.rect(screen, GREEN, rect, 2)
    centered(label, rect, GREEN, title_font)


def boot_screen(mouse):
    logo = [
        "  ____ ____   _    _____",
        " / ___|  _ \\ / \\  |  ___|",
        "| |   | |_) / _ \\ | |_   ",
        "| |___|  __/ ___ \\|  _|  ",
        " \\____|_| /_/   \\_\\_|    ",
    ]
    w, h = screen.get_size()
    screen.fill(BLACK)

    pygame.draw.rect(screen, PANEL, (0, 0, w, 48))
    draw_text("CPAF // BOOT LOADER", 20, 10, GREEN, boot_header)
    draw_text("v3.1", w - 75, 17, GREY, boot_small)

    logo_y = int(h * 0.09)
    for line in logo:
        draw_text(line, int(w * 0.04), logo_y, GREEN, boot_logo)
        logo_y += 27

    tx = int(w * 0.035)
    ty = int(h * 0.43)
    tw = int(w * 0.60)
    th = int(h * 0.43)
    terminal = pygame.Rect(tx, ty, tw, th)

    pygame.draw.rect(screen, PANEL, terminal)
    pygame.draw.rect(screen, DARK_GREEN, terminal, 1)
    draw_text("akshat@probably-not-a-hacker:~", tx + 17, ty + 13, WHITE, boot_small)
    pygame.draw.line(screen, DARK_GREEN, (tx + 17, ty + 40), (terminal.right - 17, ty + 40))
    draw_text("HOW TO PLAY", tx + 17, ty + 53, YELLOW, boot_title)
    instructions = [
        ("> read every popup before clicking.", GREEN),
        ("> suspicious offers / fake warnings = BAD.", YELLOW),
        ("> press X on BAD popups to close them.", WHITE),
        ("> normal system notices = GOOD.", GREEN),
        ("> press OK on GOOD popups to acknowledge.", WHITE),
        ("> bad X: +1 point. good OK: -10 points.", RED),
        ("> survive as the desktop gets more chaotic.", YELLOW),
    ]
    y = ty + 88
    for line, color in instructions:
        draw_text(line, tx + 17, y, color, boot_terminal)
        y += 26

    px = int(w * 0.68)
    draw_text("MESSAGE FROM THE DEV", px, int(h * 0.39), GREEN, boot_small)
    pygame.draw.line(screen, DARK_GREEN, (px, int(h * 0.43)), (w - 22, int(h * 0.43)))
    draw_text("DEV.LOG", px, int(h * 0.46), YELLOW, boot_title)

    dev_lines = [
        "I don't know how many",
        "windows I killed during",
        "development, but it crashed",
        "more than your kill count",
        "today.",
    ]
    dev_y = int(h * 0.52)
    for line in dev_lines:
        draw_text(line, px, dev_y, WHITE, boot_dev)
        dev_y += 22

    draw_text("- akshat", px, dev_y + 5, GREEN, boot_small)
    draw_text("// professional window", px, dev_y + 27, GREY, tiny)
    draw_text("destroyer", px, dev_y + 41, GREY, tiny)

    bw = int(w * 0.25)
    bh = 54
    bx = min(px, w - bw - 15)
    by = int(h * 0.79)
    start = pygame.Rect(bx, by, bw, bh)
    draw_button(start, "[ LETS GOO ]", mouse)
    draw_text("WARNING: skill issue may occur", px, by + 65, RED, tiny)

    pygame.draw.rect(screen, PANEL, (0, h - 35, w, 35))
    pygame.draw.line(screen, DARK_GREEN, (0, h - 35), (w, h - 35))
    draw_text("STATUS: SOMEHOW RUNNING", 15, h - 24, GREEN, tiny)
    draw_text("ESC = rage quit", w - 130, h - 24, GREY, tiny)
    return start

def choose_window_copy(template):
    """
    Titles and body text can lie. The symbol never does.
    Bad windows slowly get better at looking legit; good windows slowly
    get more suspicious body copy. The scoring kind never changes.
    """
    elapsed = max(0, (pygame.time.get_ticks() - start_time) / 1000) if start_time else 0
    ramp = min(1.0, elapsed / 1800.0)

    bad_pool = [item for item in WINDOW_TYPES if item["kind"] == "bad"]
    good_pool = [item for item in WINDOW_TYPES if item["kind"] == "good"]

    if template["kind"] == "bad":
        # Fake windows borrow a believable title more often as time passes:
        # 10% at the start -> 40% after two minutes.
        title_is_legit = random.random() < (0.10 + 0.30 * ramp)

        # Their body copy only gets a believable disguise 10% of the time.
        content_is_legit = random.random() < 0.10

        title_source = random.choice(good_pool) if title_is_legit else template
        content_source = random.choice(good_pool) if content_is_legit else template
    else:
        # Good windows keep their legitimate title 100% of the time.
        # Their body copy gets increasingly dodgy: 10% -> 50% over two minutes.
        title_source = template
        content_is_bad = random.random() < (0.10 + 0.40 * ramp)
        content_source = random.choice(bad_pool) if content_is_bad else template


    return {
        "title": title_source["title"],
        "message": content_source["message"],
        "extra": content_source["extra"],
    }


def make_popup():
    global popup_count
    popup_count += 1
    w, h = screen.get_size()
    # 9 times out of 10, the internet has sent you another problem.
    bad_windows = [item for item in WINDOW_TYPES if item["kind"] == "bad"]
    good_windows = [item for item in WINDOW_TYPES if item["kind"] == "good"]
    pool = bad_windows * 9 + good_windows
    template = random.choice(pool)
    palette_bg, palette_bar = random.choice(WINDOW_PALETTES)
    kind = template["kind"]
    copy = choose_window_copy(template)
    pw = min(random.randint(340, 470), w - 28)
    ph = min(random.randint(225, 255), h - 100)
    x = random.randint(12, max(12, w - pw - 12))
    y = random.randint(55, max(55, h - ph - 55))
    popups.append({
        "rect": pygame.Rect(x, y, pw, ph),
        "kind": kind,
        "app": template["app"].split(" // ", 1)[0],
        "title": copy["title"],
        "message": copy["message"],
        "extra": copy["extra"],
        "accent": palette_bar,
        "window_bg": palette_bg,
        "id": popup_count,
        "born": pygame.time.get_ticks(),
    })
    return kind

def make_popup_kind(template):
    global popup_count
    popup_count += 1
    w, h = screen.get_size()
    palette_bg, palette_bar = random.choice(WINDOW_PALETTES)
    copy = choose_window_copy(template)
    pw = min(random.randint(340, 470), w - 28)
    ph = min(random.randint(225, 255), h - 100)
    x = random.randint(12, max(12, w - pw - 12))
    y = random.randint(55, max(55, h - ph - 55))
    popups.append({
        "rect": pygame.Rect(x, y, pw, ph),
        "kind": template["kind"],
        "app": template["app"].split(" // ", 1)[0],
        "title": copy["title"],
        "message": copy["message"],
        "extra": copy["extra"],
        "accent": palette_bar,
        "window_bg": palette_bg,
        "id": popup_count,
        "born": pygame.time.get_ticks(),
    })

def close_top_window():
    global score
    if not popups:
        set_notice("no window selected. impressive.")
        return
    p = popups.pop()
    if p["kind"] == "bad":
        score += 1
        set_notice(random.choice(REACTIONS))
        check_score_achievements()
    else:
        score -= 10
        set_notice("THAT WAS A GOOD WINDOW. -10. READ THE LABELS.", 3000)
        if score < 0:
            end_game("SCORE COLLAPSE", "you closed the useful windows. outstanding work.")


def popup_click(pos):
    global score



    # Only the topmost popup under the cursor receives the click.
    # BAD: X is correct (+1), OK is wrong (-10).
    # GOOD: OK is correct (no penalty), X is wrong (-2).
    for i in range(len(popups) - 1, -1, -1):
        p = popups[i]
        r = p["rect"]

        close = pygame.Rect(r.right - 42, r.y + 4, 34, 27)
        ok = pygame.Rect(r.right - 92, r.bottom - 39, 78, 28)

        if not r.collidepoint(pos):
            continue

        if not (close.collidepoint(pos) or ok.collidepoint(pos)):
            return

        # Bring the clicked window to the front.
        popups.append(popups.pop(i))
        p = popups[-1]

        if p["kind"] == "bad":
            if close.collidepoint(pos):
                popups.pop()
                score += 5
                set_notice("BAD POPUP CLOSED. +5 POINTS.", 2000)
                check_score_achievements()
            else:
                popups.pop()
                score -= 10
                set_notice("YOU PRESSED OK ON A BAD POPUP. -10 POINTS.", 2800)
                if score < 0:
                    end_game("SCORE COLLAPSE", "you accepted the suspicious popup. classic.")
            return

        if p["kind"] == "good":
            if ok.collidepoint(pos):
                popups.pop()
                score += 1
                set_notice("GOOD NOTIFICATION ACKNOWLEDGED. +1 POINT.", 2200)
                check_score_achievements()
            else:
                popups.pop()
                score -= 2
                set_notice("YOU CLOSED A GOOD WINDOW. -2 POINTS.", 2500)
                if score < 0:
                    end_game("SCORE COLLAPSE", "you closed the useful notifications. outstanding.")
            return


def draw_browser_content(p, r):
    pygame.draw.rect(screen, (245, 247, 244), (r.x + 12, r.y + 43, r.width - 24, 30))
    draw_text("https://totally-safe-and-real.website", r.x + 22, r.y + 51, (55, 65, 58), tiny)
    pygame.draw.rect(screen, (235, 239, 234), (r.x + 12, r.y + 82, r.width - 24, 50))
    draw_text(p["message"], r.x + 22, r.y + 91, WIN_TEXT, small)
    draw_text(p["extra"], r.x + 22, r.y + 113, (80, 88, 81), tiny)


def draw_file_content(p, r):
    pygame.draw.rect(screen, (239, 242, 237), (r.x + 12, r.y + 43, r.width - 24, 95))
    for j, name in enumerate(["📁 projects", "📄 final_final_really.py", "📦 questionable_stuff.zip"]):
        draw_text(name, r.x + 24, r.y + 51 + j * 25, (55, 65, 58), tiny)



def draw_popup(p):
    r = p["rect"]
    bg = p["window_bg"]
    accent = p["accent"]
    ink = (34, 36, 39)
    muted_ink = (76, 79, 83)

    pygame.draw.rect(screen, (0, 0, 0), r.move(6, 6))
    pygame.draw.rect(screen, bg, r)
    pygame.draw.rect(screen, accent, (r.x, r.y, r.width, 35))
    pygame.draw.rect(screen, accent, r, 2)
    draw_text(clipped_text(p["app"], r.width - 100, tiny), r.x + 12, r.y + 11, (250, 250, 250), tiny)

    close_top = pygame.Rect(r.right - 42, r.y + 4, 34, 27)
    pygame.draw.rect(screen, (145, 35, 35), close_top)
    pygame.draw.rect(screen, (80, 20, 20), close_top, 1)
    centered("X", close_top, (255, 255, 255), small)

    # Each app gets its own familiar-looking surface. The UI style is random
    # decoration; it never tells you whether the message is good or bad.
    app = p["app"].upper()
    content = pygame.Rect(r.x + 12, r.y + 45, r.width - 24, r.height - 91)
    pygame.draw.rect(screen, (247, 248, 246), content)
    pygame.draw.rect(screen, (185, 190, 185), content, 1)

    if "BROWSER" in app:
        tabs = pygame.Rect(content.x, content.y, content.width, 23)
        pygame.draw.rect(screen, (224, 229, 225), tabs)
        draw_text("●  ●  ●", tabs.x + 7, tabs.y + 5, (105, 110, 105), tiny)
        address = pygame.Rect(content.x + 8, content.y + 29, content.width - 16, 23)
        pygame.draw.rect(screen, (255, 255, 255), address, border_radius=5)
        draw_text("⌕  https://account-check.example", address.x + 7, address.y + 5, muted_ink, tiny)
        body_y = content.y + 62
    elif "FILES" in app:
        pygame.draw.rect(screen, (232, 236, 232), (content.x, content.y, content.width, 24))
        draw_text("←   →    ↑     Home     Projects", content.x + 7, content.y + 5, muted_ink, tiny)
        for row, label in enumerate(("📁  Projects", "📄  project_notes.txt", "📦  download_item.zip")):
            yy = content.y + 31 + row * 21
            if row % 2 == 0:
                pygame.draw.rect(screen, (238, 242, 238), (content.x + 3, yy - 2, content.width - 6, 20))
            draw_text(label, content.x + 10, yy, ink, tiny)
        body_y = content.y + 99


    elif "NETWORK" in app:
        pygame.draw.rect(screen, (230, 237, 244), (content.x + 7, content.y + 7, content.width - 14, 38))
        draw_text("◉  Network status", content.x + 15, content.y + 15, (45, 70, 95), small)
        draw_text("Wi-Fi   |   Ethernet   |   VPN", content.x + 12, content.y + 52, muted_ink, tiny)
        body_y = content.y + 76
    elif "MAIL" in app or "CHAT" in app or "MESSAGES" in app:
        draw_text("From: notifications@service.example", content.x + 9, content.y + 8, muted_ink, tiny)
        pygame.draw.line(screen, (205, 210, 205), (content.x + 8, content.y + 28), (content.right - 8, content.y + 28))
        draw_text("Inbox  •  Message preview", content.x + 9, content.y + 35, (65, 75, 68), tiny)
        body_y = content.y + 58
    elif "SYSTEM" in app or "UPDATE" in app or "ANTIVIRUS" in app:
        draw_text("SYSTEM NOTIFICATION", content.x + 10, content.y + 9, (65, 75, 68), tiny)
        pygame.draw.line(screen, (205, 210, 205), (content.x + 8, content.y + 29), (content.right - 8, content.y + 29))
        body_y = content.y + 39
    elif "CALENDAR" in app:
        pygame.draw.rect(screen, (229, 235, 242), (content.x + 8, content.y + 8, 48, 48))
        centered("NOV", pygame.Rect(content.x + 8, content.y + 11, 48, 15), (65, 85, 110), tiny)
        centered("01", pygame.Rect(content.x + 8, content.y + 26, 48, 25), (45, 60, 80), title_font)
        body_y = content.y + 65
    else:
        body_y = content.y + 12

    draw_text(clipped_text(p["title"], content.width - 20, small), content.x + 10, body_y, ink, small)
    draw_text(clipped_text(p["message"], content.width - 20, tiny), content.x + 10, body_y + 27, ink, tiny)
    draw_text(clipped_text(p["extra"], content.width - 20, tiny), content.x + 10, body_y + 47, muted_ink, tiny)

    # Both controls are always present. X and OK are the only clues to act on.
    pygame.draw.line(screen, (165, 170, 165), (r.x + 10, r.bottom - 47), (r.right - 10, r.bottom - 47))
    ok_button = pygame.Rect(r.right - 92, r.bottom - 39, 78, 28)
    pygame.draw.rect(screen, (220, 235, 220), ok_button)
    pygame.draw.rect(screen, (65, 105, 70), ok_button, 2)
    centered("OK", ok_button, (20, 65, 30), small)


def make_bugs():
    bugs = []
    w, h = screen.get_size()
    for _ in range(9):
        bugs.append({
            "x": random.randint(8, w - 8),
            "y": random.randint(55, h - 55),
            "vx": random.uniform(-1.4, 1.4),
            "vy": random.uniform(-1.1, 1.1),
            "size": random.randint(2, 4),
            "phase": random.random() * math.tau,
        })
    return bugs


bugs = make_bugs()


def update_bugs(dt):
    w, h = screen.get_size()
    for bug in bugs:
        bug["phase"] += dt * 0.004
        bug["x"] += bug["vx"] * dt * 0.06 + math.sin(bug["phase"]) * 0.5
        bug["y"] += bug["vy"] * dt * 0.06 + math.cos(bug["phase"]) * 0.35
        if bug["x"] < 4 or bug["x"] > w - 4:
            bug["vx"] *= -1
        if bug["y"] < 50 or bug["y"] > h - 50:
            bug["vy"] *= -1


def draw_bugs():
    for bug in bugs:
        x, y, s = int(bug["x"]), int(bug["y"]), bug["size"]
        pygame.draw.circle(screen, (255, 95, 80), (x, y), s)
        pygame.draw.line(screen, (255, 130, 110), (x - s - 2, y - 2), (x - 1, y), 1)
        pygame.draw.line(screen, (255, 130, 110), (x + 1, y), (x + s + 2, y + 2), 1)


def check_score_achievements():
    for target, name, desc in SCORE_ACHIEVEMENTS:
        if score >= target and target not in unlocked:
            unlocked.add(target)
            achievement_toast(name, desc)
            break


def check_time_achievements(elapsed):
    for target, name, desc in TIME_ACHIEVEMENTS:
        if elapsed >= target and target not in unlocked:
            unlocked.add(target)

def end_game(reason, detail):
    global phase, end_reason, end_detail
    phase = "over"
    end_reason = reason
    end_detail = detail

def game_screen():
    w, h = screen.get_size()
    screen.fill(BLACK)
    for x in range(0, w, 42):
        pygame.draw.line(screen, (13, 26, 18), (x, 0), (x, h))
    for y in range(0, h, 42):
        pygame.draw.line(screen, (13, 26, 18), (0, y), (w, y))

    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    mins, secs = divmod(elapsed, 60)
    pygame.draw.rect(screen, PANEL, (0, 0, w, 48))
    draw_text("CPAF // questionable desktop", 14, 13, GREEN, title_font)
    draw_text(f"SCORE: {score}", int(w * 0.42), 16, WHITE, small)
    draw_text(f"ERRORS: {len(popups)}", int(w * 0.55), 16, RED, small)

    draw_text(f"UPTIME: {mins:02}:{secs:02}", w - 170, 16, GREEN, small)

    draw_text("SYSTEM STATUS: it's complicated", 25, 67, GREY, tiny)
    draw_text("[???]", 42, 100, GREEN, title_font)
    draw_text("definitely_not_a_virus.exe", 42, 130, GREY, tiny)
    draw_text("[gift]", 42, 178, YELLOW, title_font)
    draw_text("motivation.zip", 42, 208, GREY, tiny)

    draw_bugs()
    for p in popups:
        draw_popup(p)

    if pygame.time.get_ticks() < notice_until:
        box = pygame.Rect(20, 53, min(w - 40, 650), 34)
        pygame.draw.rect(screen, PANEL, box)
        pygame.draw.rect(screen, GREEN, box, 1)
        draw_text(clipped_text(notice, box.width - 18, tiny), box.x + 9, box.y + 10, YELLOW, tiny)

    pygame.draw.rect(screen, PANEL, (0, h - 43, w, 43))
    pygame.draw.line(screen, DARK_GREEN, (0, h - 43), (w, h - 43))
    draw_text("CPAF", 14, h - 30, GREEN, title_font)
    draw_text("CLICK THE X ON A WINDOW TO CLOSE IT", 105, h - 27, GREY, tiny)
    draw_text("QUIT", w - 72, h - 27, GREEN, tiny)


def draw_end_screen():
    w, h = screen.get_size()
    screen.fill(BLACK)
    pygame.draw.rect(screen, PANEL, (0, 0, w, 48))
    draw_text("CPAF // SESSION TERMINATED", 20, 13, RED, title_font)
    title = "HARDWARE MELTDOWN (SIMULATED)" if end_reason == "MELTDOWN" else end_reason
    centered(title, pygame.Rect(30, int(h * 0.25), w - 60, 60), RED, big_font)
    centered(end_detail, pygame.Rect(30, int(h * 0.39), w - 60, 45), WHITE, small)
    elapsed = max(0, (pygame.time.get_ticks() - start_time) // 1000)
    centered(f"FINAL SCORE: {score}     WINDOWS CLOSED: {popup_count - len(popups)}", pygame.Rect(30, int(h * 0.51), w - 60, 40), GREEN, title_font)
    centered(f"SESSION TIME: {elapsed // 60:02}:{elapsed % 60:02}", pygame.Rect(30, int(h * 0.59), w - 60, 35), GREY, small)
    centered("The fans are imaginary. Your choices were real.", pygame.Rect(30, int(h * 0.70), w - 60, 35), YELLOW, small)
    global restart_button, end_quit_button
    restart_button = pygame.Rect(int(w * 0.31), int(h * 0.80), int(w * 0.20), 48)
    end_quit_button = pygame.Rect(int(w * 0.55), int(h * 0.80), int(w * 0.16), 48)
    draw_button(restart_button, "[ RESTART ]", pygame.mouse.get_pos())
    draw_button(end_quit_button, "[ QUIT ]", pygame.mouse.get_pos())


def start_game():
    global phase, screen, score, popup_count, start_time, last_spawn, last_input, popups, unlocked, bugs, toast_queue, active_toasts, next_bad_spawn, next_good_spawn
    # Keep the original display surface. Do not recreate/resize the SDL window.
    pygame.display.set_caption("CTRL+ALTF4EVER // desktop.exe has concerns")
    phase = "game"
    score = 0
    popup_count = 0
    popups = []
    unlocked = set()
    toast_queue = []
    active_toasts = []
    now = pygame.time.get_ticks()
    start_time = now
    last_spawn = now
    last_input = now
    bugs = make_bugs()
    # No free pile-on at spawn; first alerts arrive quickly, then ramp up.
    next_bad_spawn = now + 1400
    next_good_spawn = now + 2800



# Mouse-only controls. The keyboard has been fired from this project.
running = True
last_mouse_pos = pygame.mouse.get_pos()
quit_button = None
restart_button = None
end_quit_button = None
next_bad_spawn = 0
next_good_spawn = 0

while running:
    dt = clock.tick(60)
    mouse = pygame.mouse.get_pos()

    # Moving the mouse counts as activity. AFK means AFK, not "forgot to click".
    if mouse != last_mouse_pos:
        register_input()
        last_mouse_pos = mouse

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            register_input()
            if event.button == 1:
                if phase == "boot":
                    if start_button.collidepoint(event.pos):
                        start_game()
                elif phase == "game":
                    # The taskbar quit target is intentionally mouse-only too.
                    w, h = screen.get_size()
                    if pygame.Rect(w - 90, h - 43, 90, 43).collidepoint(event.pos):
                        running = False
                    else:
                        popup_click(event.pos)
                elif phase == "over":
                    if restart_button and restart_button.collidepoint(event.pos):
                        start_game()
                    elif end_quit_button and end_quit_button.collidepoint(event.pos):
                        running = False



    if phase == "boot":
        start_button = boot_screen(mouse)

    elif phase == "game":
        now = pygame.time.get_ticks()
        elapsed = (now - start_time) // 1000
        idle = (now - last_input) // 1000

        # No mouse movement or clicks for 90 seconds? The imaginary fans give up.
        if idle >= 90:
            end_game("MELTDOWN", "90 seconds without mouse activity. CPU has filed a formal complaint.")
        else:
            check_time_achievements(elapsed)

            # It starts chill, then the desktop slowly remembers it's supposed
            # to be annoying. No instant popup apocalypse.
            ramp = min(1.0, elapsed / 1800.0)
            bad_min = int(1500 - (650 * ramp))
            bad_max = int(2300 - (900 * ramp))
            good_min = int(4200 - (1500 * ramp))
            good_max = int(6200 - (1900 * ramp))
            popup_limit = min(100, 8 + int(92 * ramp))

            due_bad = now >= next_bad_spawn
            due_good = now >= next_good_spawn
            spawn_order = ["bad", "good"]
            random.shuffle(spawn_order)

            for kind in spawn_order:
                if len(popups) >= popup_limit:
                    break
                if kind == "bad" and due_bad:
                    bad_pool = [item for item in WINDOW_TYPES if item["kind"] == "bad"]
                    make_popup_kind(random.choice(bad_pool))
                    next_bad_spawn = now + random.randint(bad_min, bad_max)
                elif kind == "good" and due_good:
                    good_pool = [item for item in WINDOW_TYPES if item["kind"] == "good"]
                    make_popup_kind(random.choice(good_pool))
                    next_good_spawn = now + random.randint(good_min, good_max)

            update_bugs(dt)
            update_toasts()
            game_screen()
            draw_toasts()

    if phase == "over":
        draw_end_screen()

    pygame.display.flip()


pygame.quit()
