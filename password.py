import pygame
import json
import os

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BookBeat")

# Load images
background2 = pygame.image.load("images/background2.png")
vector_image = pygame.image.load("images/vector2.png")
username_icon = pygame.image.load("images/username_icon.png")
password_icon = pygame.image.load("images/password_icon.png")
bookbeat_icon = pygame.image.load("images/bookbeat_icon.png")
mail_icon = pygame.image.load("images/mail.png")
btn2_img = pygame.image.load("images/btn2.png")
btnR_img = pygame.image.load("images/backgroundReg.png")
pygame.display.set_icon(bookbeat_icon)

# Fonts
FONT = pygame.font.SysFont("Zapf Renaissance Book", 20, bold=True)
BIG_FONT = pygame.font.SysFont("Zapf Renaissance Book", 36, bold=True)
FONTSMALL = pygame.font.SysFont("fonnts.com-Neue_Haas_Grotesk_Display_Pro_65_Medium", 20, bold=True)
FONTSNONBOLD = pygame.font.SysFont("fonnts.com-Neue_Haas_Grotesk_Display_Pro_65_Medium", 20)
FONTARIAL = pygame.font.SysFont("Arial", 15)

# Colors
WHITE = (255, 255, 255)
GRAY = (107, 106, 105)
BLUE = (48, 71, 255)
BLACK = (0, 0, 0)
PURPLE = (205, 150, 255)
LIGHTGRAY = (242, 242, 242)

# User data
users_file = "users.json"
if os.path.exists(users_file):
    with open(users_file, "r") as f:
        users_dict = json.load(f)
else:
    users_dict = {}

# State
username_input = ""
password_input = ""
email_input = ""
active_field = None
feedback = ""
is_register_screen = False

# Rectangles (login screen)
username_rect = pygame.Rect(550, 330, 300, 35)
password_rect = pygame.Rect(550, 410, 300, 35)
login_button_rect = pygame.Rect(550, 470, 300, 45)
top_register_button_rect = pygame.Rect(WIDTH - 190, 10, 120, 40)

# Rectangles (register screen)
email_rect = pygame.Rect(550, 490, 250, 35)
username_rect_reg = pygame.Rect(550, 330, 250, 35)
password_rect_reg = pygame.Rect(550, 410, 250, 35)
skapa_konto_rect = pygame.Rect(550, 550, 250, 45)

def draw_text(text, pos, font=FONTSMALL, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, pos)

def check_login():
    global feedback
    if username_input in users_dict:
        if users_dict[username_input] == password_input:
            feedback = f"Välkommen Tillbaka, {username_input}!"
        else:
            feedback = "Fel lösenord eller användarnamn."
    else:
        feedback = "Användaren finns inte."

clock = pygame.time.Clock()
cursor_visible = True
cursor_timer = 0
cursor_interval = 500  # milliseconds

running = True
while running:
    dt = clock.tick(60)
    cursor_timer += dt
    if cursor_timer >= cursor_interval:
        cursor_visible = not cursor_visible
        cursor_timer %= cursor_interval

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not is_register_screen:
                if username_rect.collidepoint(event.pos):
                    active_field = "username"
                elif password_rect.collidepoint(event.pos):
                    active_field = "password"
                elif login_button_rect.collidepoint(event.pos):
                    check_login()
                elif top_register_button_rect.collidepoint(event.pos):
                    is_register_screen = True
                    username_input = ""
                    password_input = ""
                    email_input = ""
                    feedback = ""
                else:
                    active_field = None
            else:
                # Register screen mouse clicks
                if username_rect_reg.collidepoint(event.pos):
                    active_field = "username"
                elif password_rect_reg.collidepoint(event.pos):
                    active_field = "password"
                elif email_rect.collidepoint(event.pos):
                    active_field = "email"
                elif skapa_konto_rect.collidepoint(event.pos):
                    if username_input and password_input and email_input:
                        if username_input in users_dict:
                            feedback = "Användarnamnet är redan taget."
                        else:
                            users_dict[username_input] = password_input
                            with open(users_file, "w") as f:
                                json.dump(users_dict, f)
                            feedback = f"User {username_input} Välkommen!."
                            username_input = ""
                            password_input = ""
                            email_input = ""
                            is_register_screen = False
                    else:
                        feedback = "Alla fält måste fyllas i."
                elif bookbeat_text_rect.collidepoint(event.pos):  # Back button
                    is_register_screen = False
                    username_input = ""
                    password_input = ""
                    email_input = ""
                    feedback = ""
                else:
                    active_field = None

        elif event.type == pygame.KEYDOWN:
            if active_field == "username":
                if event.key == pygame.K_BACKSPACE:
                    username_input = username_input[:-1]
                elif len(event.unicode) == 1:
                    username_input += event.unicode
            elif active_field == "password":
                if event.key == pygame.K_BACKSPACE:
                    password_input = password_input[:-1]
                elif len(event.unicode) == 1:
                    password_input += event.unicode
            elif active_field == "email":
                if event.key == pygame.K_BACKSPACE:
                    email_input = email_input[:-1]
                elif len(event.unicode) == 1:
                    email_input += event.unicode

    # Draw interface
    if is_register_screen:
        screen.blit(btnR_img, (0, 0))
        bookbeat_text = BIG_FONT.render("BookBeat", True, BLACK)
        bookbeat_text_rect = bookbeat_text.get_rect(topleft=(80, 10))
        screen.blit(bookbeat_text, bookbeat_text_rect)

        headline_label = BIG_FONT.render("Kom igång med ett konto", True, BLACK)
        screen.blit(headline_label, headline_label.get_rect(center=(WIDTH // 2, 200)))

        pygame.draw.rect(screen, GRAY, username_rect_reg, 2)
        pygame.draw.rect(screen, GRAY, password_rect_reg, 2)
        pygame.draw.rect(screen, GRAY, email_rect, 2)

        skapa_konto_color = PURPLE if username_input and password_input and email_input else LIGHTGRAY
        pygame.draw.rect(screen, skapa_konto_color, skapa_konto_rect)

        draw_text("Användarnamn", (username_rect_reg.x, username_rect_reg.y - 30), FONTSMALL, BLACK)
        draw_text("Lösenord", (password_rect_reg.x, password_rect_reg.y - 30), FONTSMALL, BLACK)
        draw_text("Mailadress", (email_rect.x, email_rect.y - 30), FONTSMALL, BLACK)
        draw_text("Skapa konto", (skapa_konto_rect.x + 80, skapa_konto_rect.y + 14), FONTSMALL, BLACK)

        screen.blit(username_icon, (520, 335))
        screen.blit(password_icon, (520, 415))
        screen.blit(mail_icon, (520, 495))

        draw_text(username_input or "Skriv användarnamn", (username_rect_reg.x + 10, username_rect_reg.y + 10), FONTARIAL, BLACK if username_input else (180, 180, 180))
        draw_text("*" * len(password_input) if password_input else "Skriv lösenord", (password_rect_reg.x + 10, password_rect_reg.y + 10), FONTARIAL, BLACK if password_input else (180, 180, 180))
        draw_text(email_input or "Skriv mailadress", (email_rect.x + 10, email_rect.y + 10), FONTARIAL, BLACK if email_input else (180, 180, 180))

        if active_field in ["username", "password", "email"] and cursor_visible:
            input_map = {
                "username": (username_input, username_rect_reg),
                "password": ("*" * len(password_input), password_rect_reg),
                "email": (email_input, email_rect),
            }
            text_val, rect = input_map[active_field]
            text_surface = FONTARIAL.render(text_val, True, GRAY)
            cursor_x = rect.x + 10 + text_surface.get_width() + 1
            cursor_y = rect.y + 8
            cursor_height = FONTARIAL.get_height()
            pygame.draw.line(screen, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

    else:
        screen.blit(background2, (0, 0))
        screen.blit(username_icon, (520, 335))
        screen.blit(password_icon, (520, 415))

        pygame.draw.rect(screen, PURPLE, top_register_button_rect)
        draw_text("Prova gratis", (top_register_button_rect.x + 20, top_register_button_rect.y + 13), FONTSMALL, BLACK)

        draw_text("BookBeat", (80, 10), BIG_FONT, BLACK)
        draw_text("Logga in", (630, 200), BIG_FONT, BLACK)
        draw_text("Användarnamn", (550, 300), FONTSMALL, BLACK)
        draw_text("Lösenord", (550, 380), FONTSMALL, BLACK)

        pygame.draw.rect(screen, GRAY, username_rect, 2)
        pygame.draw.rect(screen, GRAY, password_rect, 2)

        draw_text(username_input or "Skriv användarnamn", (username_rect.x + 10, username_rect.y + 10), FONTARIAL, BLACK if username_input else (180, 180, 180))
        draw_text("*" * len(password_input) if password_input else "Skriv lösenord", (password_rect.x + 10, password_rect.y + 10), FONTARIAL, BLACK if password_input else (180, 180, 180))

        if active_field in ["username", "password"] and cursor_visible:
            input_text = username_input if active_field == "username" else "*" * len(password_input)
            rect = username_rect if active_field == "username" else password_rect
            text_surface = FONTARIAL.render(input_text, True, GRAY)
            cursor_x = rect.x + 10 + text_surface.get_width() + 1
            cursor_y = rect.y + 8
            cursor_height = FONTARIAL.get_height()
            pygame.draw.line(screen, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

        login_button_color = PURPLE if username_input and password_input else LIGHTGRAY
        pygame.draw.rect(screen, login_button_color, login_button_rect)
        draw_text("Logga in", (login_button_rect.x + 115, login_button_rect.y + 14), FONTSMALL, BLACK)

        

        feedback_label = FONTSMALL.render(feedback, True, GRAY)
        screen.blit(feedback_label, feedback_label.get_rect(center=(login_button_rect.centerx, 640)))

    pygame.display.update()

pygame.quit()
