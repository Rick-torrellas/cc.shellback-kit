from CapsuleCore_shellback import ArgumentBuilder  # Asegúrate de importar correctamente


def test_unix_style_builder():
    builder = ArgumentBuilder(style="unix")
    args = builder.add_flag("verbose").add_flag("output", "file.txt").build()

    assert args == ["--verbose", "--output", "file.txt"]


def test_ms_style_builder():
    builder = ArgumentBuilder(style="ms")
    args = builder.add_flag("verbose").add_flag("output", "file.txt").build()

    assert args == ["/verbose", "/output", "file.txt"]


def test_empty_builder():
    builder = ArgumentBuilder()
    assert builder.build() == []


def test_method_chaining():
    builder = ArgumentBuilder()
    # Verificamos que el retorno sea la misma instancia
    result = builder.add_flag("a")
    assert result is builder
