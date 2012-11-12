
import pygame


class TextBox:

  def __init__( self, font):
    self.font = font
    self.background = 255, 255, 255
    self.shadow = 224, 224, 224
    self.color = 0, 0, 0
    self.cursor_color = 192, 0, 0
    self.bounds = pygame.Rect( 0, 14, 240, 100)
    self.show_from_line = 0
    self.text = ""
    self.cursor = 0
    self.lines = [""]

  def insert( self, character):
    self.text = self.text[0:self.cursor] + character + self.text[self.cursor:]
    self.cursor += 1
    self.break_lines()

  def delete( self):
    if 0 < self.cursor:
      self.text = self.text[0:self.cursor-1] + self.text[self.cursor:]
      self.cursor -= 1
      self.break_lines()

  def render_to( self, surf):
    surf.lock()
    surf.fill( self.background, self.bounds)
    pygame.draw.rect( surf, self.color, self.bounds, 1)
    x = self.bounds.left
    y = self.bounds.top
    w = self.bounds.w
    h = self.bounds.h
    points = ( (x+1,y+h-2), (x+1,y+1), (x+w-2,y+1) )
    pygame.draw.lines( surf, self.shadow, False, points, 1)
    surf.unlock()
    line_height = self.font.get_linesize()
    lines_shown = ( self.bounds.h - 3) / line_height
    line_topleft = pygame.rect.Rect( self.bounds.topleft, (0,0))
    line_topleft.x += 2
    line_topleft.y += 2
    for line_no in range( self.show_from_line, self.show_from_line+ lines_shown):
      try: line = self.lines[ line_no]
      except IndexError: break
      line = self.font.render( line, True, self.color, self.background)
      surf.blit( line, line_topleft)
      line_topleft.y += line_height
    # render the cursor
    # Locate the line and col of the cursor within the text document
    cursor_line = 0 # line number
    sol = 0 # the index in text of the start of the line
    #print "lines:",self.lines
    #print "line:",cursor_line
    while True:
      #print "cursor_line", cursor_line
      line_len = len( self.lines[ cursor_line] ) + 1 # + 1 for the space at the end that was ripped off by break_lines()
      if self.cursor <= sol + line_len: break
      cursor_line += 1
      sol += line_len
    cursor_column = self.cursor - sol  # The number of characters between the beginning of the line and the cursor
    #print "line:",line, " col:", cursor_column
    # Scroll the view ( always only once I hope) to show the cursor
    while cursor_line - self.show_from_line < 0:
      self.show_from_line -= 1
    while lines_shown <= cursor_line - self.show_from_line:
      self.show_from_line += 1
    y = self.bounds.y + 2 + line_height * ( cursor_line - self.show_from_line)
    line_under_cursor = self.lines[ cursor_line] # The line within the document on which the cursor is resting
    x = self.bounds.x + 2 + self.font.size(line_under_cursor[0:cursor_column])[0]
    pygame.draw.line( surf, self.cursor_color, (x,y), (x,y+line_height-1), 1)

  def break_lines( self):
    pixels_across = self.bounds.w - 3
    pixels_across = 30
    lines = [""]
    cs = 0 # start at the beginning of the text
    while True:
      # Look for a space from the cursor onwards:
      i = self.text.find(" ", cs)
      #print "i:",i
      next_word = self.text[ cs:i] if i != -1 else self.text[ cs:]
      #print "nw:",next_word
      extended_line = next_word if "" == lines[-1] else lines[-1]+ " "+ next_word
      #print "el:",extended_line
      line_width, ignore = self.font.size( extended_line)
      # If the extended_line fits within the text box, or if the last line is
      # blank so far:
      if line_width <= pixels_across or "" == lines[-1]:
        lines[-1] = extended_line
      else:
        # Start a new line for the word that would have made the line too wide:
        lines.append( next_word)
      if -1 == i: break
      else: cs = i + 1
    self.lines = lines
    #print "lines",lines

