from concreto.parser.Parser import Parser
from concreto.categorias.Luchadora import Luchadora
from concreto.secciones.Recompensa import Recompensa


if __name__ == "__main__":
    # Secciones
    recompensa = Recompensa("Recompensas")
    print("Crea la seccion")

    # Parser
    parser_luchadora = Parser("C:/Desarrollo/AO/FS-WIKI-2024/Clases luchadoras", Luchadora({recompensa}))
    print("Crea el parser")

    parser_luchadora.run()