import pygame
import sys
import time

from button import Button
from target import Target



def draw(window: pygame.Surface, window_width: int, number_of_generated_targets: int, number_of_clicks: int,
         number_of_clicked_targets: int, elapsed_time_in_seconds: int, elapsed_time_in_minutes: int) -> None:

    window.fill((0, 0, 0))

    rectangle: pygame.rect.Rect = pygame.rect.Rect(0,0,1280,30)
    pygame.draw.rect(window, "grey", rectangle)

    # Afișarea timpului petrecut în joc:
    if elapsed_time_in_minutes:
        time: pygame.Surface = pygame.font.SysFont("cambria", 20).render(f"Timp: {elapsed_time_in_minutes}m " + "{:.0f}s".format(elapsed_time_in_seconds), True, "black")
    else:
        time: pygame.Surface = pygame.font.SysFont("cambria", 20).render("Timp: {:.0f}s".format(elapsed_time_in_seconds - 60 * elapsed_time_in_minutes), True, "black")
    rectangle: pygame.rect.Rect = time.get_rect(topleft = (5, 5))
    window.blit(time, rectangle)

    # Afișarea numărului de ținte generate
    copy_of_generated_targets: int = number_of_generated_targets
    number_of_generated_targets = pygame.font.SysFont("cambria", 20).render(f"Ținte generate: {number_of_generated_targets}", True, "black")
    rectangle = number_of_generated_targets.get_rect(topleft = (200, 5))
    window.blit(number_of_generated_targets, rectangle)

    # Afișarea numărului de apăsări
    number_of_clicks = pygame.font.SysFont("cambria", 20).render(f"Click-uri: {number_of_clicks}", True, "black")
    rectangle: pygame.rect.Rect = number_of_clicks.get_rect(topleft = (400, 5))
    window.blit(number_of_clicks, rectangle)

    # Afișarea numărului de ținte nimerite
    copy_of_number_of_clicked_targets = number_of_clicked_targets
    number_of_clicked_targets =  pygame.font.SysFont("cambria", 20).render(f"Ținte nimerite: {number_of_clicked_targets}", True, "black")
    rectangle: pygame.rect.Rect = number_of_clicked_targets.get_rect(topleft = (600, 5))
    window.blit(number_of_clicked_targets, rectangle)

    if elapsed_time_in_seconds >= 1:
        number_of_clicked_targets_per_second: float = copy_of_number_of_clicked_targets / elapsed_time_in_seconds
        number_of_clicked_targets_per_second: str = "{:.2f}".format(number_of_clicked_targets_per_second)
    else:
        number_of_clicked_targets_per_second: str = "0.00"

    # Afișarea numărului de ținte nimerite pe secundă
    number_of_clicked_targets =  pygame.font.SysFont("cambria", 20).render(f"Ținte nimerite pe secundă: {number_of_clicked_targets_per_second}", True, "black")
    rectangle: pygame.rect.Rect = number_of_clicked_targets.get_rect(topleft = (800, 5))
    window.blit(number_of_clicked_targets, rectangle)

    # Afișarea numărului de vieți
    lives = pygame.font.SysFont("cambria", 20).render(f"Vieți: {100 - copy_of_generated_targets + copy_of_number_of_clicked_targets}", True, "black")
    rectangle: pygame.Rect = lives.get_rect(topright = (window_width - 5, 5))
    window.blit(lives, rectangle)


def end_screen(window: pygame.Surface, window_width: int, mouse_position: tuple, retry_button: Button, number_of_clicked_targets: int,
               elapsed_time_in_minutes: int, elapsed_time_in_seconds: int) -> None:
    
    window.fill((0, 0, 0))

    if elapsed_time_in_minutes:
        time: pygame.Surface = pygame.font.SysFont("cambria", 50).render(f"Timp: {elapsed_time_in_minutes}m " + "{:.0f}s".format(elapsed_time_in_seconds), True, "white")
    else:
        time: pygame.Surface = pygame.font.SysFont("cambria", 50).render("Timp: {:.0f}s".format(elapsed_time_in_seconds - 60 * elapsed_time_in_minutes), True, "white")
    rectangle: pygame.rect.Rect = time.get_rect(center = (window_width // 2, 100))
    window.blit(time, rectangle)

    copy_of_number_of_clicked_targets = number_of_clicked_targets
    number_of_clicked_targets =  pygame.font.SysFont("cambria", 50).render(f"Numărul de ținte nimerite: {number_of_clicked_targets}", True, "white")
    rectangle: pygame.rect.Rect = number_of_clicked_targets.get_rect(center = (window_width // 2, 200))
    window.blit(number_of_clicked_targets, rectangle)

    number_of_clicked_targets_per_second: float = copy_of_number_of_clicked_targets / elapsed_time_in_seconds
    number_of_clicked_targets_per_second: str = "{:.2f}".format(number_of_clicked_targets_per_second)

    # Afișarea numărului de ținte nimerite pe secundă
    number_of_clicked_targets =  pygame.font.SysFont("cambria", 50).render(f"Ținte nimerite pe secundă: {number_of_clicked_targets_per_second}", True, "white")
    rectangle: pygame.rect.Rect = number_of_clicked_targets.get_rect(center = (window_width // 2, 300))
    window.blit(number_of_clicked_targets, rectangle)

    retry_button.hover(pygame.mouse.get_pos())
    retry_button.draw(window)


def main(fps: int, window_dimensions: tuple, window: pygame.Surface) -> None:

    # Crearea unui obiect ce ajută la monitorizarea timpului
    clock: pygame.time.Clock = pygame.time.Clock()

    run: bool = True
    previous_time: float = time.time()

    # Crearea unui eveniment
    TARGET_SPAWN: int = pygame.USEREVENT + 1

    # Setarea apariției evenimentului în coada de evenimente la un anumit număr de milisecunde
    pygame.time.set_timer(TARGET_SPAWN, 500)

    # Grupul țintelor
    target_group: pygame.sprite.Group = pygame.sprite.Group()

    number_of_generated_targets: int = 0
    number_of_clicks: int = 0
    number_of_clicked_targets: int = 0

    start_time: int = pygame.time.get_ticks()

    retry_button = Button((window_dimensions[0] // 2, 500), "Reîncercare", pygame.font.SysFont("cambria", 50), "white", "red")


    # Bucla jocului
    while run:

        dt: float = time.time() - previous_time
        previous_time: float = time.time()

        mouse_position: tuple = (0, 0)

        # Gestionarea evenimentelor
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == TARGET_SPAWN and len(target_group) < 10 and number_of_generated_targets - number_of_clicked_targets < 100:
                Target(window_dimensions, target_group)
                number_of_generated_targets += 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position: tuple = pygame.mouse.get_pos()
                number_of_clicks += 1
        

        if number_of_generated_targets - number_of_clicked_targets < 100:

            current_time: int = pygame.time.get_ticks()
            elapsed_time_in_seconds: int = current_time - start_time
            elapsed_time_in_minutes: int = elapsed_time_in_seconds // 60000
            
            # Afișarea informațiilor în bara superioară
            draw(window,  window_dimensions[0], number_of_generated_targets, number_of_clicks, number_of_clicked_targets,
                 elapsed_time_in_seconds / 1000, elapsed_time_in_minutes)

            for target in target_group:
                if target.click_collision(mouse_position):
                    number_of_clicked_targets += 1
                    target.kill()
                
                else:
                    target.update(dt)
                    target.draw(window)
        
        else:
            end_screen(window, window_dimensions[0], mouse_position, retry_button, number_of_clicked_targets,
                       elapsed_time_in_minutes, elapsed_time_in_seconds / 1000)
            
            for target in target_group:
                target.kill()

            if retry_button.input(mouse_position):
                number_of_generated_targets: int = 0
                number_of_clicks: int = 0
                number_of_clicked_targets: int = 0
                start_time: int = pygame.time.get_ticks()


        pygame.display.update()

        # Limitarea rulării buclei la fps ori pe secundă/rularea jocului la fps cadre pe secundă
        clock.tick(fps)


    pygame.quit()
    sys.exit()


if __name__ == "__main__":

    # Inițializare pygame
    pygame.init()

    # Proprietățile ferestrei
    window_dimensions: tuple = (1280, 720) # dimensiule inițiale ale ferestrei

    # Inițializarea ferestrei de lucru
    window: pygame.Surface = pygame.display.set_mode(window_dimensions)#), pygame.RESIZABLE)

    # Numele ferestrei
    pygame.display.set_caption("Joc") # Numele ferestrei

    fps: int = 60

    main(fps, window_dimensions, window)