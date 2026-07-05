from flask import Flask, redirect, render_template, request, session, url_for
from database import authenticate_user, create_tables, get_default_db_path, register_user
from simulation_calculator import simulate_binomial
from covid_simulation import simulate_covid
from random_generators import generate_sequence
from roulette_simulation import RouletteSimulator
from statistical_tests import generate_and_test_sequence


def create_app(db_path: str | None = None):
    app = Flask(__name__, template_folder="templates")
    app.secret_key = "simulacion-secret-key"
    app.config["db_path"] = db_path or get_default_db_path()
    create_tables(app.config["db_path"])

    @app.route("/", methods=["GET", "POST"])
    def login_page():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            if authenticate_user(username, password, db_path=app.config["db_path"]):
                session["user"] = username
                return redirect(url_for("dashboard"))
            return render_template("login.html", title="Iniciar sesión", message="Usuario o contraseña incorrectos")
        return render_template("login.html", title="Iniciar sesión", message=None)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        return login_page()

    @app.route("/register", methods=["GET", "POST"])
    def register_page():
        if request.method == "POST":
            full_name = request.form.get("full_name", "").strip()
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")
            if password != confirm_password:
                return render_template("register.html", title="Registro", message="Las contraseñas no coinciden")
            if register_user(full_name, username, email, password, db_path=app.config["db_path"]):
                return render_template("login.html", title="Iniciar sesión", message="Cuenta creada correctamente")
            return render_template("register.html", title="Registro", message="No se pudo crear la cuenta")
        return render_template("register.html", title="Registro", message=None)

    @app.route("/dashboard")
    def dashboard():
        if "user" not in session:
            return redirect(url_for("login_page"))
        return render_template("dashboard.html", title="Panel principal", message=None)

    @app.route("/calculator", methods=["GET", "POST"])
    def calculator():
        if "user" not in session:
            return redirect(url_for("login_page"))
        result = None
        if request.method == "POST":
            try:
                trials = int(request.form.get("trials", 0))
                probability = float(request.form.get("probability", 0))
                seed = int(request.form.get("seed", 0)) if request.form.get("seed", "").strip() else None
                result = simulate_binomial(trials=trials, probability=probability, seed=seed)
            except ValueError as exc:
                return render_template("calculator.html", title="Calculadora", message=str(exc), result=None)
        return render_template("calculator.html", title="Calculadora", message=None, result=result)

    @app.route("/covid", methods=["GET", "POST"])
    def covid_simulation():
        if "user" not in session:
            return redirect(url_for("login_page"))
        summary = None
        if request.method == "POST":
            try:
                size = int(request.form.get("size", 0))
                infected = int(request.form.get("infected", 0))
                steps = int(request.form.get("steps", 0))
                summary = simulate_covid(size=size, infected=infected, steps=steps)
            except ValueError as exc:
                return render_template("covid.html", title="Simulación COVID", message=str(exc), summary=None)
        return render_template("covid.html", title="Simulación COVID", message=None, summary=summary)

    @app.route("/random-generators", methods=["GET", "POST"])
    def random_generators():
        if "user" not in session:
            return redirect(url_for("login_page"))
        sequence = None
        method = "lineal"
        method_label = "Lineal congruencial"
        if request.method == "POST":
            try:
                method = request.form.get("method", "lineal")
                method_labels = {
                    "lineal": "Lineal congruencial",
                    "mixto": "Mixto",
                    "multiplicativo": "Multiplicativo",
                    "cuadrado_medio": "Cuadrado medio",
                    "fibonacci": "Fibonacci",
                    "automata_celular": "Autómata celular",
                }
                method_label = method_labels.get(method, method)
                seed = int(request.form.get("seed", 1))
                a = int(request.form.get("a", 0)) if request.form.get("a", "").strip() else None
                c = int(request.form.get("c", 0)) if request.form.get("c", "").strip() else None
                m = int(request.form.get("m", 0)) if request.form.get("m", "").strip() else None
                seed2 = int(request.form.get("seed2", 0)) if request.form.get("seed2", "").strip() else None
                digits = int(request.form.get("digits", 0)) if request.form.get("digits", "").strip() else None
                count = int(request.form.get("count", 10))
                sequence = generate_sequence(method=method, seed=seed, a=a, c=c, m=m, seed2=seed2, digits=digits, count=count)
            except ValueError as exc:
                return render_template("random_generators.html", title="Generadores aleatorios", message=str(exc), sequence=None, method=method, method_label=method_label)
        return render_template("random_generators.html", title="Generadores aleatorios", message=None, sequence=sequence, method=method, method_label=method_label)

    @app.route("/statistical-tests", methods=["GET", "POST"])
    def statistical_tests():
        if "user" not in session:
            return redirect(url_for("login_page"))
        result = None
        frequency_bars = []
        method = "lineal"
        method_label = "Lineal congruencial"
        if request.method == "POST":
            try:
                method = request.form.get("method", "lineal")
                method_labels = {
                    "lineal": "Lineal congruencial",
                    "mixto": "Mixto",
                    "multiplicativo": "Multiplicativo",
                    "cuadrado_medio": "Cuadrado medio",
                    "fibonacci": "Fibonacci",
                    "automata_celular": "Autómata celular",
                }
                method_label = method_labels.get(method, method)
                seed = int(request.form.get("seed", 1))
                a = int(request.form.get("a", 0)) if request.form.get("a", "").strip() else None
                c = int(request.form.get("c", 0)) if request.form.get("c", "").strip() else None
                m = int(request.form.get("m", 0)) if request.form.get("m", "").strip() else None
                seed2 = int(request.form.get("seed2", 0)) if request.form.get("seed2", "").strip() else None
                digits = int(request.form.get("digits", 0)) if request.form.get("digits", "").strip() else None
                count = int(request.form.get("count", 20))
                generated = generate_and_test_sequence(method=method, seed=seed, a=a, c=c, m=m, seed2=seed2, digits=digits, count=count)
                result = generated
                if generated.get("values"):
                    bins = 10
                    counts = [0] * bins
                    max_value = max(generated["values"])
                    scale = max(max_value, 1)
                    for value in generated["values"]:
                        index = min(int((value / scale) * bins), bins - 1)
                        counts[index] += 1
                    max_count = max(counts) if counts else 1
                    frequency_bars = [{"label": f"Intervalo {index + 1}", "value": count, "width": (count / max_count) * 100 if max_count else 0} for index, count in enumerate(counts)]
            except ValueError as exc:
                return render_template("statistical_tests.html", title="Pruebas estadísticas", message=str(exc), result=None, frequency_bars=[], method=method, method_label=method_label)
        return render_template("statistical_tests.html", title="Pruebas estadísticas", message=None, result=result, frequency_bars=frequency_bars, method=method, method_label=method_label)

    @app.route("/roulette", methods=["GET", "POST"])
    def roulette():
        if "user" not in session:
            return redirect(url_for("login_page"))
        result = None
        if request.method == "POST":
            try:
                simulations = int(request.form.get("simulations", 0))
                initial_capital = float(request.form.get("initial_capital", 0))
                bet_amount = float(request.form.get("bet_amount", 0))
                bet_type = request.form.get("bet_type", "Rojo")
                selected_number = int(request.form.get("selected_number", 0)) if request.form.get("selected_number", "").strip() else None
                docena = int(request.form.get("docena", 1)) if request.form.get("docena", "").strip() else None
                column = int(request.form.get("column", 1)) if request.form.get("column", "").strip() else None
                simulator = RouletteSimulator()
                result = simulator.run_simulation(
                    simulations=simulations,
                    initial_capital=initial_capital,
                    bet_amount=bet_amount,
                    bet_type=bet_type,
                    selected_number=selected_number,
                    docena=docena,
                    column=column,
                )
            except ValueError as exc:
                return render_template("roulette.html", title="Ruleta Monte Carlo", message=str(exc), result=None)
        return render_template("roulette.html", title="Ruleta Monte Carlo", message=None, result=result)

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        return redirect(url_for("login_page"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
