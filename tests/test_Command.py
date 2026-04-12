from cc_shellback_kit import Command


class TestCommand:
    def test_command_initialization(self):
        """Verifica que el comando se inicializa con el ejecutable correcto."""
        cmd = Command("ls")
        assert cmd.executable == "ls"
        # Al inicio, la lista de argumentos debe estar vacía
        assert cmd.args == []

    def test_add_single_argument(self):
        """Verifica la adición de un único argumento posicional."""
        cmd = Command("git")
        cmd.add_args("status")
        assert cmd.args == ["status"]

    def test_add_multiple_arguments_variadic(self):
        """Verifica la adición de múltiples argumentos usando *args."""
        cmd = Command("python")
        cmd.add_args("main.py", "--verbose", "run")
        assert cmd.args == ["main.py", "--verbose", "run"]

    def test_add_list_of_arguments(self):
        """
        Verifica que el builder aplane correctamente las listas
        pasadas como argumentos (gracias a ArgumentBuilder).
        """
        cmd = Command("tar")
        args_list = ["-czf", "backup.tar.gz", "/home/user"]
        cmd.add_args(args_list)
        assert cmd.args == ["-czf", "backup.tar.gz", "/home/user"]

    def test_fluent_interface(self):
        """Verifica que add_args devuelva la instancia (patrón Fluent Interface)."""
        cmd = Command("docker")
        returned_cmd = cmd.add_args("ps").add_args("-a")

        assert cmd is returned_cmd
        assert cmd.args == ["ps", "-a"]

    def test_mixed_arguments_types(self):
        """Verifica la mezcla de strings, números y listas."""
        cmd = Command("echo")
        # El ArgumentBuilder convierte internamente a string y aplana
        cmd.add_args("User ID:", 1001, ["--force", "yes"])

        assert cmd.args == ["User ID:", "1001", "--force", "yes"]

    def test_empty_and_none_arguments(self):
        """Verifica que se ignoren valores None o vacíos si el builder así lo gestiona."""
        cmd = Command("ls")
        cmd.add_args(None, "", "  ", "-l")

        # Según ArgumentBuilder.py, ignora None y strings que queden vacíos tras .strip()
        assert cmd.args == ["-l"]
