def generate_sequence(method: str, seed: int = 1, a: int | None = None, c: int | None = None, m: int | None = None, seed2: int | None = None, digits: int | None = None, count: int = 10):
    if method == "lineal":
        if a is None or c is None or m is None or m <= 0:
            raise ValueError("Faltan parámetros para el generador lineal congruencial")
        current = seed % m
        values = []
        for _ in range(count):
            current = (a * current + c) % m
            values.append(current)
        return values

    if method == "mixto":
        if a is None or c is None or m is None or m <= 0:
            raise ValueError("Faltan parámetros para el generador mixto")
        current = seed % m
        values = []
        for _ in range(count):
            current = (a * current + c) % m
            values.append(current)
        return values

    if method == "multiplicativo":
        if a is None or m is None or m <= 0:
            raise ValueError("Faltan parámetros para el generador multiplicativo")
        current = seed % m
        values = []
        for _ in range(count):
            current = (a * current) % m
            values.append(current)
        return values

    if method == "cuadrado_medio":
        if digits is None or digits <= 0:
            raise ValueError("Faltan parámetros para el método del cuadrado medio")
        current = seed
        values = []
        for _ in range(count):
            square = current * current
            s = str(square).zfill(digits * 2)
            middle = s[len(s)//2 - digits//2: len(s)//2 + digits//2 + (digits % 2)]
            current = int(middle)
            values.append(current)
        return values

    if method == "fibonacci":
        if seed2 is None or m is None or m <= 0:
            raise ValueError("Faltan parámetros para el método de Fibonacci")
        x0 = seed
        x1 = seed2
        values = [x0 % m, x1 % m]
        for _ in range(count - 2):
            x_next = (x0 + x1) % m
            values.append(x_next)
            x0, x1 = x1, x_next
        return values[:count]

    if method == "automata_celular":
        if count <= 0:
            return []
        state = [int(bit) for bit in format(seed % 256, "08b")]
        values = []
        for _ in range(count):
            values.append(state[len(state)//2])
            next_state = []
            for index in range(len(state)):
                left = state[index - 1] if index > 0 else state[-1]
                center = state[index]
                right = state[(index + 1) % len(state)]
                next_state.append((left ^ (center | right)) & 1)
            state = next_state
        return values

    raise ValueError("Método no soportado")
