################################################################################
# Copyright (C) 2020 Abstract Horizon
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License v2.0
# which accompanies this distribution, and is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
#  Contributors:
#    Daniel Sendula - initial API and implementation
#
#################################################################################


import pygame
from pygame import Rect


class ALIGNMENT:
    LEFT = 1
    CENTER = 2
    RIGHT = 3
    TOP = 4
    MIDDLE = 5
    BOTTOM = 6


class Component:
    def __init__(self, rect):
        self.rect = rect
        self.mouse_is_over = False
        self.font = None
        self._visible = True

    def _font(self):
        if self.font is None:
            self.font = pygame.font.SysFont('Arial', 30)
        return self.font

    def is_visible(self):
        return self._visible

    def set_visible(self, visible):
        self._visible = visible

    def draw(self, surface):
        pass

    def redefine_rect(self, rect):
        self.rect = rect

    def mouse_over(self, mouse_pos):
        self.mouse_is_over = True

    def mouse_left(self, mouse_pos):
        self.mouse_is_over = False

    def mouse_down(self, mouse_pos):
        pass

    def mouse_up(self, mouse_pos):
        pass

    def size(self):
        return self.rect.width, self.rect.height

    def key_down(self, code):
        return False

    def key_up(self, code):
        return False


class BaseLayout:
    def arrange(self, rect, components):
        for component in components:
            component.redefine_rect(rect)


class TopDownLayout(BaseLayout):
    def __init__(self, margin=0):
        self.margin = margin

    def arrange(self, rect, components):
        y = rect.y
        for component in components:
            if component.rect is not None and component.rect.height != 0:
                height = component.rect.height
            else:
                height = (rect.height - self.margin * (len(components) - 1)) // len(components)
            component.redefine_rect(Rect(rect.x, y, rect.width, height))
            y += self.margin + height


class LeftRightLayout(BaseLayout):
    def __init__(self, margin=0):
        self.margin = margin

    def arrange(self, rect, components):
        x = rect.x
        for component in components:
            if component.rect is not None and component.rect.width != 0:
                width = component.rect.width
            else:
                width = (rect.width - self.margin * (len(components) - 1)) // len(components)
            component.redefine_rect(Rect(x, rect.y, width, rect.height))
            x += self.margin + width


class Collection(Component):
    def __init__(self, rect, layout=None):
        super(Collection, self).__init__(rect)  # Call super constructor to store rectable
        self.components = []
        self.layout = layout
        self._selected_component = None

    def add_component(self, component, ):
        self.components.append(component)

    def remove_component(self, component):
        i = self.components.index(component)
        if i > 0:
            del self.components[i]

    def draw(self, surface):
        for component in self.components:
            if component.is_visible():
                component.draw(surface)

    def find_component(self, pos):
        for component in reversed(self.components):
            if component.is_visible() and component.rect is not None and component.rect.collidepoint(pos):
                return component
        return None

    def redefine_rect(self, rect):
        self.rect = rect
        if self.layout is not None:
            self.layout.arrange(rect, self.components)
        else:
            for component in self.components:
                component.redefine_rect(rect)

    def mouse_over(self, mouse_pos):
        self.mouse_is_over = True
        component = self.find_component(mouse_pos)
        if component != self._selected_component and self._selected_component is not None:
            self._selected_component.mouse_left(mouse_pos)
        if component is not None:
            component.mouse_over(mouse_pos)
            self._selected_component = component

    def mouse_left(self, mouse_pos):
        self.mouse_is_over = False
        if self._selected_component is not None:
            self._selected_component.mouse_left(mouse_pos)

    def mouse_down(self, mouse_pos):
        component = self.find_component(mouse_pos)
        if component != self._selected_component and self._selected_component is not None:
            self._selected_component.mouse_left(mouse_pos)
        if component is not None:
            component.mouse_down(mouse_pos)
            self._selected_component = component

    def mouse_up(self, mouse_pos):
        if self._selected_component is not None:
            self._selected_component.mouse_up(mouse_pos)
            if not self._selected_component.rect.collidepoint(mouse_pos):
                # we released button outside of component - it would be nice to let it know mouse is not inside of it any more
                self._selected_component.mouse_left(mouse_pos)
        component = self.find_component(mouse_pos)
        if component is not None:
            # we released mouse over some other component - now it is turn for it to receive mouse over
            component.mouse_over(mouse_pos)


class Panel(Collection):
    def __init__(self, rect, background_colour=None, decoration=None):
        super(Panel, self).__init__(rect)
        self.bacground_colour = background_colour
        self.decoration = decoration

    def redefine_rect(self, rect):
        super(Panel, self).redefine_rect(rect)
        if self.decoration is not None:
            self.decoration.redefine_rect(rect)

    def draw(self, surface):
        if self.bacground_colour is not None:
            pygame.draw.rect(surface, self.bacground_colour, self.rect)
        super(Panel, self).draw(surface)


class Menu(Panel):
    def __init__(self, rect, ui_factory, background_colour=None, decoration=None):
        super(Menu, self).__init__(ui_factory.ui_adapter.get_screen().get_rect())
        self.draw_rect = rect
        self.ui_factory = ui_factory
        self.bacground_colour = background_colour
        self.decoration = decoration
        self.menu_items = []
        self.set_visible(False)
        self._key_selected = -1

    def redefine_rect(self, rect):
        self.draw_rect = rect
        self.rect = self.ui_factory.ui_adapter.get_screen().get_rect()
        self.calculate_height()
        if self.decoration is not None:
            self.decoration.redefine_rect(rect)

    def draw(self, surface):
        if self.bacground_colour is not None:
            pygame.draw.rect(surface, self.bacground_colour, self.draw_rect)
        if self._key_selected >= 0:
            for i in range(len(self.menu_items)):
                item = self.menu_items[i]

                item.mouse_is_over = i == self._key_selected

        super(Panel, self).draw(surface)
        if self.decoration is not None:
            self.decoration.draw(surface)

    def mouse_down(self, mouse_pos):
        if not self.draw_rect.collidepoint(mouse_pos):
            self.hide()
        else:
            super(Menu, self).mouse_over(mouse_pos)

    def show(self):
        self.set_visible(True)
        self._clean_key_selected()

    def hide(self):
        self.set_visible(False)
        self._clean_key_selected()

    def size(self):
        return self.draw_rect.width, self.draw_rect.height

    def _clean_key_selected(self):
        for item in self.menu_items:
            item.mouse_is_over = False

    def calculate_height(self):
        y = 5
        for item in self.menu_items:
            item.redefine_rect(Rect(self.draw_rect.x, y + self.draw_rect.y, self.draw_rect.width, item.rect.height))
            y += item.rect.height
        y += 5
        self.draw_rect.height = y

    def add_menu_item(self, label, callback=None, height=30):
        component = self.ui_factory.menu_item(Rect(0, 0, 0, height), label, callback)
        self.menu_items.append(component)
        self.add_component(component)
        self.calculate_height()

    def clear_menu_items(self):
        del self.menu_items[:]
        del self.components[:]
        self._key_selected = -1

    def key_down(self, code):
        if len(self.menu_items) > 0:
            if code == pygame.K_UP:
                if self._key_selected <= 0:
                    self._key_selected = len(self.menu_items) - 1
                else:
                    self._key_selected -= 1
                return True

            if code == pygame.K_DOWN:
                self._key_selected += 1
                if self._key_selected >= len(self.menu_items):
                    self._key_selected = 0
                return True

            if code == pygame.K_RETURN or code == pygame.K_KP_ENTER or code == pygame.K_SPACE:
                item = self.menu_items[self._key_selected]
                if isinstance(item, Button):
                    item.on_click(item, None)
                return True

        return False

    def key_up(self, code):
        return False


class CardsCollection(Collection):
    def __init__(self, rect):
        super(CardsCollection, self).__init__(rect)
        self.cards = {}
        self.selected_card_name = None
        self.selectedCardComponent = None

    def add_card(self, name, component):
        self.cards[name] = component
        component._visible = False
        super(CardsCollection, self).add_component(component)

    def select_card(self, name):
        if name in self.cards:
            if self.selectedCardComponent is not None:
                self.selectedCardComponent.set_visible(False)
            self.selectedCardComponent = self.cards[name]
            self.selectedCardComponent.set_visible(True)
            self.selected_card_name = name
            return self.selectedCardComponent
        return None

    def selectedCardName(self):
        return self.selected_card_name


class Image(Component):
    def __init__(self, rect, surface, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP):
        super(Image, self).__init__(rect)  # Call super constructor to store rectable
        self._surface = surface
        self.h_alignment = h_alignment
        self.v_alignment = v_alignment

    def getImage(self):
        return self._surface

    def setImage(self, surface):
        self._surface = surface

    def draw(self, surface):
        if self._surface is not None:
            x = self.rect.x
            y = self.rect.y

            if self.h_alignment == ALIGNMENT.CENTER:
                x = self.rect.centerx - self._surface.get_width() // 2
            elif self.h_alignment == ALIGNMENT.RIGHT:
                x = self.rect.right - self._surface.get_width()

            if self.v_alignment == ALIGNMENT.MIDDLE:
                y = self.rect.centery - self._surface.get_height() // 2
            elif self.v_alignment == ALIGNMENT.BOTTOM:
                y = self.rect.bottom - self._surface.get_height()

            surface.blit(self._surface, (x, y))


class Label(Image):
    def __init__(self, rect, text, colour=None, font=None, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP):
        super(Label, self).__init__(rect, None, h_alignment, v_alignment)  # Call super constructor to store rectable
        self._text = text
        self.font = font
        self.colour = colour if colour is not None else pygame.color.THECOLORS['white']

    def get_text(self):
        return self._text

    def set_text(self, text):
        if self._text != text:
            self._text = text
            self.invalidate_surface()

    def get_colour(self):
        return self.colour

    def set_colour(self, colour):
        self.colour = colour
        self.invalidate_surface()

    def invalidate_surface(self):
        self._surface = None

    def draw(self, surface):
        if self._surface is None:
            self._surface = self._font().render(self._text, 0, self.colour)

        super(Label, self).draw(surface)


class Button(Component):
    def __init__(self, rect, on_click=None, on_hover=None, label=None, background_decoration=None, mouse_over_decoration=None):
        super(Button, self).__init__(rect)  # Call super constructor to store rectable
        self.on_click = on_click
        self.on_hover = on_hover
        self._label = label
        self.background_decoration = background_decoration
        self.mouse_over_decoration = mouse_over_decoration
        self.redefine_rect(rect)

    def get_label(self):
        return self._label

    def set_label(self, label):
        self._label = label
        self._label.redefine_rect(self.rect)

    def redefine_rect(self, rect):
        super(Button, self).redefine_rect(rect)
        if self._label is not None:
            self._label.redefine_rect(rect)  # set label's position to buttons
        if self.background_decoration is not None:
            self.background_decoration.redefine_rect(rect)
        if self.mouse_over_decoration is not None:
            self.mouse_over_decoration.redefine_rect(rect)

    def draw(self, surface):
        if self.mouse_is_over:
            if self.mouse_over_decoration is not None:
                self.mouse_over_decoration.draw(surface)
        else:
            if self.background_decoration is not None:
                self.background_decoration.draw(surface)

        if self._label is not None:  # this way 'label' can be anything - text, image or something custom drawn
            self._label.draw(surface)

    def mouse_up(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.on_click is not None:
            self.on_click(self, mouse_pos)


class UIAdapter:
    def __init__(self, screen=None, screen_size=None, freq=30, do_init=True):
        self.screen = screen
        self.screen_size = None if screen_size is None else screen_size
        self.top_component = None
        self.mouse_is_down = False
        self.freq = freq
        self.frameclock = pygame.time.Clock()
        if self.screen is None and do_init:
            self.init()

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)

    def get_screen(self):
        return self.screen

    def set_top_component(self, component):
        self.top_component = component

    def process_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            self.mouse_moved(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            self.mouse_down(mouse_pos)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            self.mouse_up(mouse_pos)

    def mouse_moved(self, mouse_pos):
        if self.top_component is not None:
            self.top_component.mouse_over(mouse_pos)

    def mouse_down(self, mouse_pos):
        self.mouse_is_down = True
        if self.top_component is not None:
            self.top_component.mouse_down(mouse_pos)

    def mouse_up(self, mouse_pos):
        self.mouse_is_down = False
        if self.top_component is not None:
            self.top_component.mouse_up(mouse_pos)

    def draw(self, surface):
        if self.top_component is not None:
            self.top_component.draw(surface)

    def frame_end(self):
        pygame.display.flip()
        self.frameclock.tick(self.freq)


class UiHint:
    NO_DECORATION = 0
    NORMAL = 1
    WARNING = 2
    ERROR = 3


class BorderDecoration(Component):
    def __init__(self, rect, colour):
        super(BorderDecoration, self).__init__(rect)  # Call super constructor to store rectable
        self.colour = colour

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, self.rect, 1)


class BaseUIFactory:
    def __init__(self, ui_adapter, font=None, small_font=None, colour=None, background_colour=None, mouse_over_colour=None):
        self.ui_adapter = ui_adapter
        self.font = font if font is not None else pygame.font.SysFont('Arial', 14)
        self.small_font = small_font if small_font is not None else pygame.font.SysFont('Arial', 9)
        self.colour = colour if colour is not None else pygame.color.THECOLORS['white']
        self.background_colour = background_colour if background_colour is not None else pygame.color.THECOLORS['black']
        self.mouse_over_colour = mouse_over_colour

    def get_ui_adapter(self):
        return self.ui_adapter

    def get_font(self):
        return self.font

    def get_small_font(self):
        return self.small_font

    def label(self, rect, text, font=None, colour=None, h_alignment=ALIGNMENT.LEFT, v_alignment=ALIGNMENT.TOP, hint=UiHint.NORMAL):
        return None

    def image(self, rect, image, hint=UiHint.NORMAL):
        return None

    def button(self, rect, on_click=None, on_hover=None, label=None, hint=UiHint.NORMAL):
        return None

    def text_button(self, rect, text, on_click=None, on_hover=None, hint=UiHint.NORMAL, font=None):
        return self.button(rect, on_click, on_hover, self.label(None, text, h_alignment=ALIGNMENT.CENTER, v_alignment=ALIGNMENT.MIDDLE, font=font), hint=hint)

    def panel(self, rect, background_colour=None, hint=UiHint.NORMAL):
        return None

    def menu(self, rect, background_colour=None, hint=UiHint.NORMAL):
        return None

    def _menu_item_text_button(self, rect, label, callback):
        return self._menu_item_button(self, rect, self.label(None, label, h_alignment=ALIGNMENT.CENTER, v_alignment=ALIGNMENT.MIDDLE))

    def _menu_item_button(self, rect, label, callback):
        return Button(rect, callback, label=label)

    def menu_item(self, rect, label, callback):
        if isinstance(label, str):
            component = self._menu_item_text_button(rect, label, callback)
        elif isinstance(label, Label):
            component = self._menu_item_button(rect, label, callback)
        else:
            component = label

        return component

    def border(self, rect, colour=pygame.color.THECOLORS['white']):
        return BorderDecoration(rect, colour)
