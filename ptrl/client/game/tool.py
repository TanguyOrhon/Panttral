import pygame


class Tool:

    @staticmethod
    def split_image(spritesheet : pygame.surface, x : int, y : int, width : int, heigth : int) -> pygame.surface:
        """_summary_

        Args:
            spritesheet (pygame.surface)
            x (int)
            y (int)
            width (int)
            heigth (int)

        Returns:
            pygame.surface
        """
        return spritesheet.subsurface(pygame.Rect(x, y, width, heigth))