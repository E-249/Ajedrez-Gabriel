from enum import Enum

unicode = True # cómo se dibujar el tablero. True: usar iconos, False: usar letras

SIDE = 8 # tamaño (en casillas) de cada lado del tablero


# [Principal] Crea el tablero y lo inicia con la posición por defecto de las piezas.
def tablero():
	tablero = [[Casilla(Pieza.VACIO, Equipo.VACIO)] * SIDE for _ in range(SIDE)]
	
	for (equipo, f) in [(Equipo.BLANCAS, lambda y: y), (Equipo.NEGRAS, lambda y: SIDE-1 - y)]:
		for x in range(SIDE):
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

# [Principal] Imprime el tablero.
def print_tablero():
	for y in range(SIDE):
		for x in range(SIDE):
			casilla = tablero[x][SIDE-1 - y]
			_, equipo = casilla.as_tup()
			match equipo:

				# Fondo
				case Equipo.VACIO:
					if (x + y) % 2 == 0:
						icon = '□'
					else:
						icon = '■'

				# Piezas
				case _:
					icon = repr(casilla)

			print(icon + ' ', end='')
		print()

# [Clase] Piezas, con su respectiva sigla.
class Pieza(Enum):
	VACIO = '_'
	PEON = 'P'
	CABALLO = 'C'
	ALFIL = 'A'
	TORRE = 'T'
	DAMA = 'D'
	REY = 'R'

	# La representación de una pieza es su sigla.
	def __repr__(self):
		return str(self.value)

# [Clase] Equipos, con su respectivo valor.
class Equipo(Enum):
	BLANCAS = +1
	NEGRAS = -1
	VACIO = 0

	# Representación del equipo.
	def __repr__(self):
		match self:
			case Equipo.BLANCAS:
				return '□Blancas□'
			case Equipo.NEGRAS:
				return '■Negras■'
			case Equipo.VACIO:
				return '_'

	# Equipo enemigo de 'self'
	def enemigo(self):
		match self:
			case Equipo.BLANCAS:
				return Equipo.NEGRAS
			case Equipo.NEGRAS:
				return Equipo.BLANCAS
			case Equipo.VACIO:
				return Equipo.VACIO

# [Auxiliar] Indica la altura respecto al equipo.
# Donde '0' es la fila de las piezas mayores de su equipo.
def altura(y: int, equipo: Equipo) -> int:
	match equipo:
		case Equipo.VACIO:
			return y
		case Equipo.BLANCAS:
			return y
		case Equipo.NEGRAS:
			return SIDE-1 - y

# [Clase] Casillas, compuestas por pieza y equipo.
class Casilla:
	def __init__(self, pieza: Pieza, equipo: Equipo):
		self.pieza = pieza
		self.equipo = equipo

	# [Auxiliar] Simplifica una Casilla como '(pieza, equipo)'
	def as_tup(self) -> tuple[Pieza, Equipo]:
		return (self.pieza, self.equipo)

	# Representación
	def __repr__(self):

		# Con letras
		if not unicode:
			match self.equipo:
				case Equipo.VACIO:
					return '_'
				case Equipo.BLANCAS:
					return repr(self.pieza).lower()
				case Equipo.NEGRAS:
					return repr(self.pieza).upper()

		# Con iconos
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

# [Lanzador] Inicia el tablero y turno
tablero = tablero()
turno = Equipo.BLANCAS

# [Auxiliar] Siguiente turno.
def siguiente_turno():
	global turno
	turno = turno.enemigo()

# [Auxiliar] Limita un vector.
# El máximo por cada lado será |1|, es decir, absoluto de 1.
def incr(dx, dy):
	if dx > 0: ix = +1
	elif dx < 0: ix = -1
	else: ix = 0

	if dy > 0: iy = +1
	elif dy < 0: iy = -1
	else: iy = 0

	return (ix, iy)

# [Principal] Indica si un movimiento es posible.
# - x0, y0: la casilla de origen.
# - xF, yF: la casilla de destino.
def puede_llegar(x0: int, y0: int, xF: int, yF: int) -> bool:
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

				s_dy = sentido * dy

				# Casilla destino al alcance
				if (dx, s_dy) == (0, 1):
					return True

				# Casilla destino al alcance (fila 2, avanzar dos casillas)
				if altura(y0, equipo_origen) == 1 and (dx, s_dy) == (0, 2):

					# (calcular incremento)
					ix, iy = incr(dx, dy)

					# (que no haya piezas en medio)
					pieza_en_camino, _ = tablero[x0+ix][y0+iy].as_tup()
					if pieza_en_camino == Pieza.VACIO:
						return True
				
				# No cumple
				return False
			
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

# [Auxiliar] Encuentra al rey.
def dónde_estáis_alteza(equipo: Equipo) -> tuple[int, int]:
	for x in range(SIDE):
		for y in range(SIDE):
			esta_pieza, este_equipo = tablero[x][y].as_tup()
			if esta_pieza == Pieza.REY and este_equipo == equipo:
				return (x, y)

	raise ValueError("¡No! ¡Os maldigo, equipo rival!")

# [Auxiliar] Dada una casilla, devuelve las casillas que le hacen jaque.
# - x, y: la casilla objetivo.
def en_jaque(x: int, y: int) -> list[tuple[int, int]]:
	casillas: list[tuple[int, int]] = []

	for x0 in range(SIDE):
		for y0 in range(SIDE):
			if puede_llegar(x0, y0, x, y):
				casillas.append((x0, y0))

	return casillas

# [Principal] Indica si un movimiento es legal.
# - x0, y0: la casilla de origen.
# - xF, yF: la casilla de destino.
def puede_mover(x0: int, y0: int, xF: int, yF: int) -> bool:

	# Casilla destino al alcance
	if not puede_llegar(x0, y0, xF, yF):
		return False

	# Guardar estado del tablero
	casilla_origen = tablero[x0][y0]
	casilla_destino = tablero[xF][yF]

	# Realizar movimiento
	tablero[x0][y0] = Casilla(Pieza.VACIO, Equipo.VACIO)
	tablero[xF][yF] = casilla_origen

	# Buscar al rey
	_, equipo = casilla_origen.as_tup()
	x, y = dónde_estáis_alteza(equipo)

	# Rey en jaque
	if en_jaque(x, y):
		# (reestablecer tablero)
		tablero[x0][y0] = casilla_origen
		tablero[xF][yF] = casilla_destino
		return False

	# Cumple
	return True

# [Principal] Realiza un movimiento si es legal; si no lo es, imprime un error
# - x0, y0: la casilla de origen.
# - xF, yF: la casilla de destino.
def mover(x0: int, y0: int, xF: int, yF: int) -> bool:
	if puede_mover(x0, y0, xF, yF):
		siguiente_turno()
		return True
	else:
		print(tablero[x0][y0], 'NOPE!', tablero[xF][yF])
		return False

# [Principal] Bucle del juego. Gestiona los turnos y el input.
# En caso de error, vuelve a pedir el input.
def loop():
	print_tablero()
	print('----------------')
	while True:
		print(repr(turno))

		while True:
			try:
				x0 = int(input('x0: '))
				y0 = int(input('y0: '))

				casilla = tablero[x0][y0]
				_, equipo_origen = casilla.as_tup()
				if equipo_origen != turno:
					print('Pieza incorrecta:', repr(casilla))
					continue

				print('Pieza seleccionada:', repr(casilla))

				xF = int(input('xF: '))
				yF = int(input('yF: '))

				if mover(x0, y0, xF, yF):
					print_tablero()
					print('----------------')
					break
			except Exception as e:
				print(f"Error occurred: {e}")
				continue


# [Test] Para testear jugadas sin tener que replicarlas a mano.
def recipe1():
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

	mover(6, 1, 6, 3)

# [Test] Para testear jugadas sin tener que replicarlas a mano.
def recipe2():
	mover(4, 1, 4, 3)
	mover(4, 6, 4, 4)

	mover(3, 0, 5, 2)
	mover(4, 7, 4, 6)
	mover(3, 1, 3, 3)

	# mover(4, 0, 4, 1)
	# mover(3, 7, 5, 5)


# [Lanzador] Inicia el juego.
loop()