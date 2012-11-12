
import pygame


class OnScreenKeyboard:

  class Row:
    def __init__( self, left, keys):
      self.left = left
      self.keys = keys

  def __init__( self, screen_dimensions, font):
    self.font = font
    self.color = 0, 0, 0
    self.background = 255, 255, 255
    # Work out the width of the widest row in characters
    #wwr = max( [len(r) for r in rows] )
    wwr = len("qwertyuiop")
    self.key_w = screen_dimensions.w / wwr
    self.key_h = self.key_w + 6
    self.rows = [
      OnScreenKeyboard.Row( 0,                         "qwertyuiop"),
      OnScreenKeyboard.Row( self.key_w/3,              "asdfghjkl"),
      OnScreenKeyboard.Row( self.key_w/3+self.key_w/2, "zxcvb nm"),
    ]
    self.top = screen_dimensions.h - self.key_h * len( self.rows)

  def render_to( self, surf):
    key_top = self.top
    for row in self.rows:
      key_left = row.left
      for ch in row.keys:
        #render_key( ch, key_top, key_left)
        # FIXME: Cache the rendered key cap surfs
        key_cap = self.font.render( ch, True, self.color, self.background)
        key_dims = key_cap.get_rect()
        ofs_x = ( self.key_w - key_dims.w) / 2
        ofs_y = ( self.key_h - (key_dims.h + 2)) / 2
        surf.blit( key_cap, (key_left+ofs_x, key_top+ofs_y) )
        # TODO: How to render a key that is held down?
        pygame.draw.rect( surf, (192,192,192), (key_left+1,key_top+1,self.key_w-2,self.key_h-2), 1)
        pygame.draw.rect( surf, self.color, (key_left+2,key_top+2,self.key_w-4,self.key_h-4), 1)
        key_left += self.key_w
      key_top += self.key_h

