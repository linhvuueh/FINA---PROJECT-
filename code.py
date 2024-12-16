import pygame
import sys
from random import randint
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 102, 204)
GRAY = (150, 150, 150)
LIGHT_BLUE = (30,75,115)
BLACK = (0,0,0)
custom_font = "THINGS/SuperMario256.ttf"
custom_fontt = "THINGS/Comfortaa-Regular.ttf"
FONT_TITLE = pygame.font.Font(custom_font, 100)
FONT_BUTTONS = pygame.font.Font(custom_font, 30)
FONT_RULES = pygame.font.Font(custom_fontt, 30)
FONT_T_RULES = pygame.font.Font(custom_font, 50)
fire_img = pygame.transform.smoothscale(pygame.image.load("THINGS/fire.png").convert_alpha(), (150, 150))
background_img = pygame.image.load("THINGS/bg.jpg").convert()
background_img = pygame.transform.smoothscale(background_img, (WIDTH, HEIGHT))
rules_img=pygame.image.load("THINGS/2.png").convert()
rules_img = pygame.transform.smoothscale(rules_img, (WIDTH, HEIGHT))
npc_frames_run = [
    pygame.transform.smoothscale(pygame.image.load(f"THINGS/run_{i}.png").convert_alpha(), (650, 350))
    for i in range(1, 6)
]
npc_frames_jump = [
    pygame.transform.smoothscale(pygame.image.load(f"THINGS/jump_{i}.png").convert_alpha(), (650, 350))
    for i in range(1, 5)
]
ice_cream1_img = pygame.transform.smoothscale(pygame.image.load("THINGS/box.png").convert_alpha(), (120, 120))
ice_cream2_img = pygame.transform.smoothscale(pygame.image.load("THINGS/cone.png").convert_alpha(), (120, 120))
obstacle_img = pygame.transform.smoothscale(pygame.image.load("THINGS/bush.png").convert_alpha(), (150, 150))
npc = pygame.transform.smoothscale(pygame.image.load("THINGS/run_1.png").convert_alpha(), (650, 350))
bg_x1 = 0
bg_x2 = WIDTH
show_rules = False
in_game = False
game_over = False
npc_x, npc_y = 200, HEIGHT - 350
is_jumping = False
obstacles = []
fire=[]
SPAWN_O_INTERVAL = 3000  
last_o_spawn_time = 0
ice_creams = []
SPAWN_INTERVAL = 1500  
last_spawn_time = 0
bg_music = pygame.mixer.Sound("SOUND/loop.mp3")
#jump_sound = pygame.mixer.Sound("jump.wav")
collect_sound = pygame.mixer.Sound("SOUND/receive_ic.mp3")
#game_over_sound = pygame.mixer.Sound("game_over.wav")
hitbush_sound = pygame.mixer.Sound("SOUND/hit_bush.mp3")
gameover_sound = pygame.mixer.Sound("SOUND/game_over.mp3")
# Phát nhạc nền
pygame.mixer.Sound.set_volume(bg_music, 0.5)  
bg_music.play(-1)  
game_speed = 1.0  
speed_increment_interval = 20000  
last_speed_increment_time = pygame.time.get_ticks()  
def draw_scrolling_bg():
    global bg_x1, bg_x2
    screen.blit(background_img, (bg_x1, 0))
    screen.blit(background_img, (bg_x2, 0))
    bg_x1 -= 4 * game_speed
    bg_x2 -= 4 * game_speed
    if bg_x1 <= -WIDTH:
        bg_x1 = WIDTH
    if bg_x2 <= -WIDTH:
        bg_x2 = WIDTH
def draw_rules():
    screen.blit(rules_img,(0,0))  
    rules_title = FONT_T_RULES.render("THINGS/RULES", True, LIGHT_BLUE)
    rules_title_rect = rules_title.get_rect(center=(WIDTH//2, 100))
    screen.blit(rules_title, rules_title_rect)
    rules_text = [
        "- Press the 'Start' button to begin playing.",
        "- Within 2 minutes, use the keyboard to control the character:",
        "    + Press the W key to jump.",
        "    + Press the A key to collect a sundae.",
        "    + Press the D key to collect an ice cream cone.",
        "- Scoring system:",
        "    + Collecting ice cream: +2 points per time.",
        "    + Hitting a bush: -5 points per time.",
        "    + Hitting fire: Game over.",
    ]
    y_offset = 140
    for line in rules_text:
        text_surface = FONT_RULES.render(line, True, BLACK)
        screen.blit(text_surface, (120, y_offset))
        y_offset += 45
    got_it_button = pygame.Rect(WIDTH - 250, HEIGHT - 530, 100, 70)
    pygame.draw.rect(screen, RED, got_it_button, border_radius=10)
    got_it_text = FONT_BUTTONS.render("<", True, WHITE)
    got_it_rect = got_it_text.get_rect(center=got_it_button.center)
    screen.blit(got_it_text, got_it_rect)
    return got_it_button
def draw_signboard_with_panel(button_texts, button_positions, button_size, button_color, text_color, fonts):
    for text, (btn_x, btn_y) in zip(button_texts, button_positions):
        pygame.draw.rect(screen, button_color, (btn_x, btn_y, button_size[0], button_size[1]),border_radius=10)
        text_surface = FONT_BUTTONS.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(btn_x + button_size[0] // 2, btn_y + button_size[1] // 2))
        screen.blit(text_surface, text_rect)
def spawn_obstacle():
    x = WIDTH + randint(20, 200)
    y = HEIGHT - 180  
    obstacle_type = randint(1, 2)  
    obstacles.append({"x": x, "y": y, "type": obstacle_type})
def update_obstacles():
    global obstacles, game_over, score
    for obstacle in obstacles[:]:  
        obstacle["x"] -= 12 * game_speed
        npc_rect = pygame.Rect(npc_x + 250, npc_y + 10, 100, 300)
        obstacle_rect = pygame.Rect(obstacle["x"] + 20, obstacle["y"] + 15, 80, 100)
        if npc_rect.colliderect(obstacle_rect) and obstacle["type"]==1:  
            score-=5
            obstacles.remove(obstacle)
            hitbush_sound.play()
        if npc_rect.colliderect(obstacle_rect) and obstacle["type"]==2:
            gameover_sound.play()
            game_over=True
        if obstacle["x"] < -50:
            obstacles.remove(obstacle)
def draw_obstacles():
    for obstacle in obstacles:
        if obstacle["type"] == 1:
            screen.blit(obstacle_img, (obstacle["x"], obstacle["y"]))
        elif obstacle["type"] == 2:
            screen.blit(fire_img, (obstacle["x"], obstacle["y"]))                                                       
def spawn_ice_cream():
    y = randint(HEIGHT -350, HEIGHT - 200)  
    x = WIDTH + randint(20, 80)  
    ice_cream_type = randint(1, 2)  
    ice_creams.append({"x": x, "y": y, "type": ice_cream_type})
def update_ice_creams():
    global ice_creams, score
    keys = pygame.key.get_pressed()  
    for ice_cream in ice_creams[:]:  
        ice_cream["x"] -= 4 * game_speed
        grab_zone = pygame.Rect(npc_x + 220, npc_y + 1, 150, 300)  
        ice_cream_rect = pygame.Rect(ice_cream["x"], ice_cream["y"] - 100, 80, 200)  
        if grab_zone.colliderect(ice_cream_rect):
            if keys[pygame.K_a] and ice_cream["type"]==1:
                ice_creams.remove(ice_cream)  
                score+=2
                collect_sound.play()
            elif keys[pygame.K_d] and ice_cream["type"]==2:
                ice_creams.remove(ice_cream)  
                score+=2
                collect_sound.play()
        if ice_cream["x"] < -50:
            ice_creams.remove(ice_cream)
def draw_ice_creams():
    for ice_cream in ice_creams:
        if ice_cream["type"] == 1:
            screen.blit(ice_cream1_img, (ice_cream["x"], ice_cream["y"]))
        elif ice_cream["type"] == 2:
            screen.blit(ice_cream2_img, (ice_cream["x"], ice_cream["y"]))
def handle_jump():
    global npc_y, is_jumping
    if is_jumping:
        npc_y -= 6  
        if npc_y <= HEIGHT - 550:  
            is_jumping = False
    else:
        if npc_y < HEIGHT - 350:  
            npc_y += 6
        if npc_y >= HEIGHT - 350:  
            npc_y = HEIGHT - 350
start_time = pygame.time.get_ticks()
stop_all= False
score=0
best = score
def highest_score():
    global score, best  
    if score > best:
        best = score
    return best
def draw_game_over():
    screen.blit(background_img, (0, 0))
    final_score_text = FONT_TITLE.render(f"Your Score: {score}",True, BLACK)
    screen.blit(final_score_text, (WIDTH // 2 - 390, HEIGHT // 2 - 100))
    screen.blit(npc,(50, 230))  
def draw_score():
    score_text = FONT_RULES.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (50, 10))  
def draw_highest_score():
    best_text = FONT_RULES.render(f"Highest Score: {best}", True, BLACK)
    screen.blit(best_text, (50, 50))  
def play_again():
    play_again_button = pygame.Rect((WIDTH - 140) // 2, HEIGHT - 90, 180, 70)
    pygame.draw.rect(screen, RED, play_again_button, border_radius=10)
    play_again_text = FONT_BUTTONS.render("REPLAY", True, WHITE)
    play_again_rect = play_again_text.get_rect(center=play_again_button.center)
    screen.blit(play_again_text, play_again_rect)
    return play_again_button         
def reset():
    global obstacles, ice_creams, npc_x, npc_y, is_jumping, score
    global stop_all, show_rules, in_game, game_over
    global last_spawn_time, last_o_spawn_time, start_time, elapse_time, game_speed, last_speed_increment_time
    score = 0
    obstacles = []                
    ice_creams = []              
    npc_x, npc_y = 200, HEIGHT - 350  
    is_jumping = False          
    stop_all = False
    show_rules = False
    in_game = True                
    game_over = False
    start_time = pygame.time.get_ticks()  
    last_spawn_time = start_time
    last_o_spawn_time = start_time
    elapse_time = 0
    game_speed = 1.0 
    last_speed_increment_time = start_time  
def game_loop():
    global show_rules, in_game, last_spawn_time, last_o_spawn_time, is_jumping, game_over, stop_all, start_time, SPAWN_INTERVAL, SPAWN_O_INTERVAL, npc_x, npc_y
    global game_speed, last_speed_increment_time
    clock = pygame.time.Clock()
    running = True
    while running:
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()  
        elapse_time = (current_time - start_time) // 1000
        minutes = (120-elapse_time) // 60
        seconds = (120-elapse_time) % 60
        if current_time - last_speed_increment_time > speed_increment_interval:
            game_speed *= 1.1  
            last_speed_increment_time = current_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w and not is_jumping:
                is_jumping = True          
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if not in_game and not game_over:
                    if show_rules and draw_rules().collidepoint(mouse_x, mouse_y):
                        show_rules = False                      
                if show_rules:
                    if got_it_button.collidepoint(mouse_x, mouse_y):
                        show_rules = False
                elif not show_rules and not in_game and 525 <= mouse_x <= 675 and 350 <= mouse_y <= 400:
                    in_game = True
                elif not show_rules and not in_game and 525 <= mouse_x <= 675 and 460 <= mouse_y <= 510:
                    show_rules = True
        if game_over:
            draw_game_over()
            play_again_button=play_again()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if play_again_button.collidepoint(mouse_x, mouse_y):
                        reset()
        elif in_game:
            if not stop_all:
                draw_scrolling_bg()
                text_surface = FONT_T_RULES.render(f"time left: {f"{minutes:02}:{seconds:02}"}", True, RED)
                screen.blit(text_surface, (680, 30))
                draw_score()
                draw_highest_score()              
                if elapse_time < 120:
                    if current_time - last_spawn_time > SPAWN_INTERVAL:
                        spawn_ice_cream()
                        last_spawn_time = current_time
                    if current_time - last_o_spawn_time > SPAWN_O_INTERVAL:
                        spawn_obstacle()
                        last_o_spawn_time = current_time
                    update_obstacles()
                    draw_obstacles()
                    update_ice_creams()
                    draw_ice_creams()
                    highest_score()              
                else:
                    draw_game_over()
                    game_over=True
                handle_jump()
                if is_jumping:
                    current_frame = (pygame.time.get_ticks() // 200) % len(npc_frames_jump)
                    screen.blit(npc_frames_jump[current_frame], (npc_x, npc_y))
                else:
                    current_frame = (pygame.time.get_ticks() // 200) % len(npc_frames_run)
                    screen.blit(npc_frames_run[current_frame], (npc_x, npc_y))
        elif show_rules:
            got_it_button = draw_rules()
        elif not show_rules and not in_game and not game_over:
            draw_scrolling_bg()
            title_text = FONT_TITLE.render("ICE TO MEET YOU", True, BLUE)
            title_rect = title_text.get_rect(center=(WIDTH // 2, 200))
            screen.blit(title_text,title_rect)
            button_texts = ["Start", "Rules"]
            button_positions = [(525, 350), (525, 460)]
            button_size = (180, 60)
            draw_signboard_with_panel(
                button_texts, button_positions, button_size,
                RED, WHITE, FONT_BUTTONS
            )
        pygame.display.flip()
        clock.tick(60)
game_loop()
pygame.quit()
sys.exit()
