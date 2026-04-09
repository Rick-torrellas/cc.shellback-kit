from CapsuleCore_shellback import ArgumentBuilder


class TestArgumentBuilder:
    def test_default_initialization(self):
        """Verifica que por defecto use estilo unix y empiece vacío."""
        builder = ArgumentBuilder()
        assert builder.style == "unix"
        assert builder.build() == []

    def test_add_flag_unix_style(self):
        """Verifica el formato de flags en estilo Unix (--flag)."""
        builder = ArgumentBuilder(style="unix")
        builder.add_flag("verbose")
        assert builder.build() == ["--verbose"]

    def test_add_flag_ms_style(self):
        """Verifica el formato de flags en estilo MS (/flag)."""
        builder = ArgumentBuilder(style="ms")
        builder.add_flag("help")
        assert builder.build() == ["/help"]

    def test_add_flag_with_value(self):
        """Verifica que los valores se añadan como elementos separados en la lista."""
        builder = ArgumentBuilder(style="unix")
        builder.add_flag("output", "file.txt")
        # El resultado esperado es que el valor siga al flag
        assert builder.build() == ["--output", "file.txt"]

    def test_method_chaining(self):
        """Verifica que se puedan encadenar llamadas a add_flag."""
        builder = ArgumentBuilder()
        result = builder.add_flag("quiet").add_flag("log", "debug.log").build()
        assert result == ["--quiet", "--log", "debug.log"]

    def test_mixed_flags_and_values(self):
        """Prueba una combinación compleja de flags con y sin valores."""
        builder = ArgumentBuilder(style="ms")
        builder.add_flag("force")
        builder.add_flag("user", "admin")
        builder.add_flag("retry", 3)

        expected = ["/force", "/user", "admin", "/retry", "3"]
        assert builder.build() == expected

    def test_value_conversion_to_string(self):
        """Verifica que valores no-string (int, float) se conviertan a string."""
        builder = ArgumentBuilder()
        builder.add_flag("timeout", 500)
        builder.add_flag("ratio", 0.5)

        assert builder.build() == ["--timeout", "500", "--ratio", "0.5"]

    def test_internal_args_access(self):
        """Verifica que la manipulación directa de _args (usada en Command.py) funcione."""
        builder = ArgumentBuilder()
        builder._args.append("positional_arg")
        builder.add_flag("flag")

        assert builder.build() == ["positional_arg", "--flag"]
