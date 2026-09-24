from graph.builder import build_graph


def main() -> None:
    graph = build_graph()

    incident = input(
        "\nDescreva o incidente:\n> "
    )

    initial_state = {
        "incident": incident,
        "retry_count": 0,
    }

    result = graph.invoke(initial_state)

    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)

    for key, value in result.items():
        print(f"\n{key}:")
        print(value)


if __name__ == "__main__":
    main()
