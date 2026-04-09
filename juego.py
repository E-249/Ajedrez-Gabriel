from enum import Enum

unicode = True

def tablero():
	side = 8
	tablero = [[Casilla(Pieza.VACIO, Equipo.VACIO)] * side for _ in range(side)]
	
	for (equipo, f) in [(Equipo.BLANCAS, lambda y: y), (Equipo.NEGRAS, lambda y: side-1 - y)]:
		for x in range(side):
			tablero[x][f(1)] = Casilla(Pieza.PEON, equipo)
			y = f(0)
			tablero[0][y] = Casilla(Pieza.TORRE, equipo)
			tablero[1][y] = Casilla(Pieza.CABALLO, equipo)
			tablero[2][y] = Casilla(Pieza.ALFIL, equipo)
			tablero[3][y] = Casilla(Pieza.DAMA, equipo)
			tablero[4][y] = Casilla(Pieza.REY, equipo)
			tablero[5][y] = Casilla(Pieza.ALFIL, equipo)
			tablero[6][y] = Casilla(Pieza.CABALLO, equipo)
			tablero[7][y] = Casilla(Pieza.TORRE, equipo)
	
	return tablero

def print_tablero():
	for y in range(8):
		for x in range(8):
			print(repr(tablero[x][7-y]), '', end='')
		print()

class Pieza(Enum):
	VACIO = '_'
	PEON = 'P'
	CABALLO = 'C'
	ALFIL = 'A'
	TORRE = 'T'
	DAMA = 'D'
	REY = 'R'
	
	def __repr__(self):
		return str(self.value)

class Equipo(Enum):
	BLANCAS = +1
	NEGRAS = -1
	VACIO = 0

	def __repr__(self):
		match self:
			case Equipo.BLANCAS:
				return 'b'
			case Equipo.NEGRAS:
				return 'n'
			case Equipo.VACIO:
				return '_'
		return str(self.value)

	def enemigo(self):
		match self:
			case Equipo.BLANCAS:
				return Equipo.NEGRAS
			case Equipo.NEGRAS:
				return Equipo.BLANCAS

class Casilla:
	def __init__(self, pieza: Pieza, equipo: Equipo):
		self.pieza = pieza
		self.equipo = equipo
	
	def as_tup(self) -> tuple[Pieza, Equipo]:
		return (self.pieza, self.equipo)
	
	def __repr__(self):
		if not unicode:
			return repr(self.pieza) + repr(self.equipo)

		match self.equipo:
			case Equipo.VACIO:
				return ' '
			case Equipo.BLANCAS:
				match self.pieza:
					case Pieza.PEON:
						return '♙'
					case Pieza.CABALLO:
						return '♘'
					case Pieza.ALFIL:
						return '♗'
					case Pieza.TORRE:
						return '♖'
					case Pieza.DAMA:
						return '♕'
					case Pieza.REY:
						return '♔'
				
			case Equipo.NEGRAS:
				match self.pieza:
					case Pieza.PEON:
						return '♟'
					case Pieza.CABALLO:
						return '♞'
					case Pieza.ALFIL:
						return '♝'
					case Pieza.TORRE:
						return '♜'
					case Pieza.DAMA:
						return '♛'
					case Pieza.REY:
						return '♚'

tablero = tablero()

def incr(dx, dy):
	if dx > 0: ix = +1
	elif dx < 0: ix = -1
	else: ix = 0

	if dy > 0: iy = +1
	elif dy < 0: iy = -1
	else: iy = 0

	return (ix, iy)

def puede_mover(x0: int, y0: int, xF: int, yF: int) -> bool:
	(dx, dy) = (xF - x0, yF - y0)
	(pieza_origen, equipo_origen) = tablero[x0][y0].as_tup()
	(pieza_destino, equipo_destino) = tablero[xF][yF].as_tup()
	sentido = equipo_origen.value
	
	match pieza_origen:
		case Pieza.VACIO:
			return False
		
		case Pieza.PEON:
			
			def avanzar() -> bool:
				# Casilla destino ocupada
				if pieza_destino != Pieza.VACIO:
					return False
				
				# Casila no al alcance [TODO: añadir dos pasos]
				if (dx, sentido*dy) != (0, 1):
					return False
				
				# Cumple
				return True
			
			def atacar() -> bool:
				# Casilla destino no es enemiga
				if equipo_destino != equipo_origen.enemigo():
					return False
				
				# Casilla no al alcance
				if (abs(dx), sentido*dy) != (1, 1):
					return False

				# Cumple
				return True
			
			# Cumple
			return avanzar() or atacar()

		case Pieza.CABALLO:

			# Casilla destino ocupada por una pieza aliada
			if equipo_destino == equipo_origen:
				return False
			
			# Casilla destino no al alcance
			if (abs(dx), abs(dy)) not in [(1, 2), (2, 1)]:
				return False
			
			# Cumple
			return True
		
		case Pieza.ALFIL:

			# Casilla destino ocupada por una pieza aliada
			if equipo_destino == equipo_origen:
				return False
			
			# Casilla destino no al alcance
			if abs(dx) != abs(dy):
				return False
			
			# Camino obstruido hacia destino

			# (calcular incremento)
			ix, iy = incr(dx, dy)

			# (recorrer camino)
			x, y = x0 + ix, y0 + iy
			while (x, y) != (xF, yF):
				pieza_camino, _ = tablero[x][y].as_tup()

				# (camino obstruido)
				if pieza_camino != Pieza.VACIO:
					return False
				
				# (siguiente casilla del camino)
				x += ix
				y += iy
			
			# Cumple
			return True
	
		case Pieza.TORRE:

			# Casilla destino ocupada por una pieza aliada
			if equipo_destino == equipo_origen:
				return False
			
			# Casilla destino no al alcance
			if abs(dx) != 0 and abs(dy) != 0:
				return False
			
			# Camino obstruido hacia destino

			# (calcular incremento)
			ix, iy = incr(dx, dy)

			# (recorrer camino)
			x, y = x0 + ix, y0 + iy
			while (x, y) != (xF, yF):
				pieza_camino, _ = tablero[x][y].as_tup()

				# (camino obstruido)
				if pieza_camino != Pieza.VACIO:
					return False
				
				# (siguiente casilla del camino)
				x += ix
				y += iy
			
			# Cumple
			return True
		
		case Pieza.DAMA:

			# Casilla destino ocupada por una pieza aliada
			if equipo_destino == equipo_origen:
				return False
			
			# Casilla destino no al alcance
			if (abs(dx) != abs(dy)) and (abs(dx) != 0 and abs(dy) != 0):
				return False

			# Camino obstruido hacia destino

			# (calcular incremento)
			ix, iy = incr(dx, dy)

			# (recorrer camino)
			x, y = x0 + ix, y0 + iy
			while (x, y) != (xF, yF):
				pieza_camino, _ = tablero[x][y].as_tup()

				# (camino obstruido)
				if pieza_camino != Pieza.VACIO:
					return False
				
				# (siguiente casilla del camino)
				x += ix
				y += iy
			
			# Cumple
			return True
		
		case Pieza.REY:

			# Casilla destino ocupada por una pieza aliada
			if equipo_destino == equipo_origen:
				return False
			
			# Casilla destino no al alcance
			if (abs(dx), abs(dy)) not in [(0, 1), (1, 1), (1, 0)]:
				return False
			
			# Cumple
			return True

def mover(x0: int, y0: int, xF: int, yF: int):
	if puede_mover(x0, y0, xF, yF):
		casilla = tablero[x0][y0]
		tablero[x0][y0] = Casilla(Pieza.VACIO, Equipo.VACIO)
		tablero[xF][yF] = casilla
	else:
		print(tablero[x0][y0], 'NOPE!', tablero[xF][yF])
	print_tablero()
	print('----------------')

if __name__ == "__main__":
	mover(4, 4, 4, 4)

	mover(1, 1, 1, 2)
	mover(1, 0, 2, 2)
	mover(2, 0, 0, 2)
	mover(0, 0, 1, 0)

	mover(1, 2, 1, 3)
	mover(1, 3, 1, 4)
	mover(1, 4, 1, 5)
	mover(1, 5, 2, 6)
	mover(1, 0, 1, 6)

	mover(3, 0, 1, 0)
	mover(1, 0, 1, 4)
	mover(1, 4, 3, 6)

	mover(4, 0, 3, 0)
	mover(3, 0, 2, 0)
	mover(2, 0, 1, 1)
	mover(1, 1, 1, 2)
	mover(1, 2, 1, 3)
	mover(1, 3, 1, 4)
	mover(1, 4, 1, 5)

	mover(0, 6, 1, 5)