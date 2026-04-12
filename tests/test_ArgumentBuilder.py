from cc_shellback_kit import ArgumentBuilder

class TestArgumentBuilder:

    def test_add_single_argument(self):
        """Verifica que se añadan argumentos simples correctamente."""
        builder = ArgumentBuilder()
        builder.add_arg("ls")
        builder.add_arg("-la")
        assert builder.build() == ["ls", "-la"]

    def test_flatten_list_arguments(self):
        """Verifica que las listas y tuplas se aplanen automáticamente."""
        builder = ArgumentBuilder()
        builder.add_arg(["git", "commit"])
        builder.add_arg("-m")
        builder.add_arg(["Mensaje con espacios"])
        
        assert builder.build() == ["git", "commit", "-m", "Mensaje con espacios"]

    def test_ignore_none_and_empty_values(self):
        """Verifica que los valores None o strings vacíos no se añadan."""
        builder = ArgumentBuilder()
        builder.add_arg(None)
        builder.add_arg("")
        builder.add_arg("  ") # Espacios en blanco
        builder.add_arg("python")
        
        assert builder.build() == ["python"]

    def test_fluent_interface(self):
        """Verifica que los métodos sean encadenables (return self)."""
        builder = ArgumentBuilder()
        result = builder.add_arg("cmd").add_flag("v").add_arg("file.txt")
        
        assert isinstance(result, ArgumentBuilder)
        assert builder.build() == ["cmd", "--v", "file.txt"]

    def test_unix_style_flags(self):
        """Verifica el prefijo '--' para el estilo unix por defecto."""
        builder = ArgumentBuilder(style="unix")
        builder.add_flag("force")
        builder.add_flag("output", "results.txt")
        
        expected = ["--force", "--output", "results.txt"]
        assert builder.build() == expected

    def test_windows_style_flags(self):
        """Verifica el prefijo '/' para el estilo windows."""
        builder = ArgumentBuilder(style="windows")
        builder.add_flag("all")
        builder.add_flag("limit", 10)
        
        expected = ["/all", "/limit", "10"]
        assert builder.build() == expected

    def test_flag_name_cleaning(self):
        """Verifica que los espacios en los nombres de flags se conviertan en underscores."""
        builder = ArgumentBuilder()
        builder.add_flag("ignore case")
        
        assert builder.build() == ["--ignore_case"]

    def test_complex_nesting(self):
        """Verifica un caso complejo con anidación profunda de listas."""
        builder = ArgumentBuilder()
        builder.add_arg(["docker", ["run", ["-d", "--name"]], "my_container"])
        
        expected = ["docker", "run", "-d", "--name", "my_container"]
        assert builder.build() == expected