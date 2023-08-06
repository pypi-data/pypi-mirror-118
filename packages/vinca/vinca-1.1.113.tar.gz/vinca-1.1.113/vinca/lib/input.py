#TODO d2w not just 2dw
import re
import string

from vinca.lib import ansi
from vinca.lib import terminal
from vinca.lib.readkey import readkey, keys

line_history = []
yank = ''
# by making the line_history and the yank history module level variables
# they are preserved for the duration of the python session

class VimEditor:
	modes = ('normal','insert','motion_pending')
	operators = ['d','c','y','~','z']
	motions = ['w','e','b','f','t','F','T',';',',','h','l','(',')','0','$','_','^',keys.LEFT, keys.RIGHT]  # TODO capital letters
	actions = ['s','S','r','u','.','x','X','D','C','p','P','Y','a','i','A','I','j','k']
	BOW = re.compile(	# BEGINNING OF WORD
		'((?<=\s)|^)'	# pattern is preceded by whitespace or the beginning of the line
		'\w')		# the beginning of the word is any alphanumeric character.
	EOW = re.compile(	# END OF WORD
		'\w'		# any alphanumeric character
		'(\s|$)')	# succeeded by whitespace or the end of the line.
	EOS = re.compile('[.!?]')  # EDGE OF SENTENCE

	def __init__(self, text, mode, pos, completions):
		self.text = text
		self.mode = mode
		self.pos = pos
		self.completions = completions
		self.multiplier = 1
		self.undo_stack = self.redo_stack = []
		self.operator = None
		self.current_insertion = ''
		self.prev_insertion = ''
		self.prev_multiplier = 1
		self.prev_action = None
		self.prev_operation = None
		self.line_history_idx = 0
		self.search_char = None

	def process_key(self, key):
		if mode == 'insert':
			if key == keys.ESC:
				self.prev_insertion = self.current_insertion
				self.current_insertion = ''
				self.mode = 'normal'
			self.do_insert(key)
			return
		if key in string.digits:
			self.multiplier = int(key)
			return
		if mode == 'normal':
			if key in ACTIONS:
				for _ in range(self.multiplier):
					self.do_action(key)
				self.reset_multiplier()
			if key in OPERATORS:
				self.mode = 'motion_pending'
				self.operator = key
			if key in MOTIONS:
				for _ in range(self.multiplier):
					self.do_motion(key)
				self.reset_multiplier()
		if mode == 'motion_pending':
			motion = key
			for _ in range(self.multiplier):
				start = self.pos
				self.do_motion(motion)
				end = self.pos
				self.pos = start
				self.do_operation(self.operator, start, end)
			self.reset_multiplier()
			self.operator = None
			self.prev_action = self.prev_insertion = None
			self.prev_operation = (self.operator, motion)

	def reset_multiplier(self):
		self.prev_multiplier = self.multiplier
		self.multiplier = 1

	def idx(self, pattern, back = False):
		'''Return the index of a match of the pattern in the text.
		If we find no match we return pos.'''
		indices = [m.start() for m in re.finditer(pattern, self.text)]  # list of matching indices
		if not back:
			return min([i for i in indices if i > self.pos], default = self.pos)
		if back:
			return max([i for i in indices if i < self.pos], default = self.pos)

	def do_insert(self, key):
		if key == '\t' and self.completions:
			raise NotImplementedError
		if key not in string.printable:
			return
		self.text = self.text[:self.pos] + key + self.text[self.pos:]
		self.current_insertion += key
		
		

	def do_operation(self, key, start, end):
		if k in ('d','c'):
			self.text = self.text[:start] + self.text[end+1:]
		if k == 'y':
			yank = self.text[start:end]
		if k == '~':
			self.text = self.text[:start] + self.text[start:end].swapcase() + self.text[end+1:]
		if k == 'z':
			yank = self.text[start:end]
			self.text = self.text[:start] + '_'*(end-start) + self.text[end+1:]
		self.mode = 'insert' if k =='c' else 'normal'

	def do_motion(self, key):
		k = key
		# jump to character
		if k in ('f','F','t','T'):
			sc = self.search_char = readkey()
			self.pos = {'f': idx(sc),
				    'F': idx(sc, back = True),
				    't': idx(f'.(?={sc})'),
				    'T': idx(f'(?<={sc}).', back = True)}[k]
			return
		# other motions
		self.pos = {
			# jump by word
			'w': idx(BOW), 'e': idx(EOW), 'b': idx(BOW, back = True),
			# repeat character jumps
			';': idx(self.search_char), ',': idx(self.search_char, back = True),
			# left / right navigation
			'h': max(0, self.pos-1), keys.LEFT: max(0, self.pos-1),
			'l': min(len(self.text), self.pos+1) keys.RIGHT: min(len(self.text), self.pos+1)
			# sentence jumping
			')': idx(EOS), '(': idx(EOS, back = True),
			# jump to beginning or end of line
			'0': 0, '^': 0, '_': 0, '$': len(self.text)}[k]

	def do_action(self, key): 
		text, pos = self.text, self.pos
		k = key
		# substitution
		if k in ('s','S','C'):
			self.mode = 'insert'
			text = {'S': '', 's': text[:pos + text[pos+1], 'C': text[:pos]}[k]
		# reversion and redoing
		if k == 'u' and self.undo_stack:
			self.redo_stack.append({'text': text, 'pos': pos})  # save current state
			prev_state = self.undo_stack.pop() # retrieve previous state
			text, pos = prev_state['text'], prev_state['pos']
		if k == keys.CTRL_R and self.redo_stack:
			self.undo_stack.append({'text': text, 'pos': pos})
			new_state = self.redo_stack.pop()
			text, pos = new_state['text'], new_state['pos']
		if k == '.' and (self.prev_action or self.prev_operation):
			if self.prev_action:
				for _ in range(self.prev_multiplier):
					self.do_action(self.prev_action)
					if self.mode == 'insert':
						self.text = self.text[:self.pos] + self.prev_insertion + self.text[self.pos:]
					self.mode = 'normal'
			elif self.prev_operation:
				operator, motion = self.prev_operation
				for _ in range(self.prev_multiplier):
					self.do_operation(operator, motion)
		# deletion
		if k in ('x','X','D'):
			text = {'D': text[:pos],
				'x': text[:pos] + text[pos+1:],
				'X': text[:pos-1] + text[pos:]}[k]
			pos -= (k == 'X')
		# copy and paste
		if k == 'Y': yank = text[pos:]
		if k == 'p': text = text[:pos+1] + yank + text[pos+1:]
		if k == 'P': text = text[:pos] + yank + text[pos:]; pos += len(yank)
		# enter insert mode
		if k in ('i','I','a','A'):
			self.mode = 'insert'
			pos = 0 if k=='I' else pos+1 if k=='a' else len(text) if k=='A' else pos
		# history scrolling
		if k in ('j','k',keys.DOWN, keys.UP):
			self.line_history_idx -= 1 if k in ('k', keys.UP) else -1
			lhi = self.line_history_idx
			if lhi == 0: text = ''
			elif lhi <= -len(text): text = line_history[0]
			else: text = line_history[lhi]
		self.text, self.pos = text, pos
	

normal_prompt = f'{ansi.codes["red"]}[N]{ansi.codes["reset"]} '
insert_prompt = f'{ansi.codes["green"]}[I]{ansi.codes["reset"]} '

def input(vi_mode = False, starting_mode = 'insert', multiline = False, prompt = '', text = '', completions = None):

	vim = VimState(text = text, mode = starting_mode, pos = 0, completions = completions)
	with terminal.NoCursor(), terminal.LineWrapOff():
		while True:
			text = vim.text
			prefix = (normal_prompt if mode == 'normal' else insert_prompt) * vi_mode
			cursor = ansi.codes['reverse'] + (text[pos] if pos<len(text) else ' ') + ansi.codes['reset']
			end_buffer = ' '*terminal.COLUMNS
			print('\r', prefix, text[:pos], cursor, text[pos+1:], end_buffer, end='', sep='', flush=True)

			key = readkey()
			if key in ('\n','\r'):
				line_history.append(vim.text)
				return vim.text
			else:
				vim.process_key(key)
