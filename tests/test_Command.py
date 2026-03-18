from unittest.mock import MagicMock, patch

# Ajusta 'tu_paquete' al nombre de la carpeta/módulo donde está tu código
from CapsuleCore_shellback import Command


class TestCommand:
    def test_initialization(self):
        """Verifica que el ejecutable se asigne correctamente."""
        cmd = Command("git")
        assert cmd.executable == "git"
        assert cmd.builder is not None

    def test_add_args_chaining(self):
        """Verifica que add_args retorne self para permitir el encadenamiento."""
        cmd = Command("docker")
        result = cmd.add_args("run", "-it")
        assert result is cmd

    @patch("CapsuleCore_shellback.capsule.Command.ArgumentBuilder")
    def test_add_args_logic(self, mock_builder_class):
        """Verifica que los argumentos se agreguen a la lista interna del builder."""
        # Configuramos el mock
        mock_instance = mock_builder_class.return_value
        mock_instance._args = []

        cmd = Command("python")
        cmd.add_args("main.py", "--version")

        assert mock_instance._args == ["main.py", "--version"]

    def test_args_property_delegation(self):
        """Verifica que cmd.args llame al método .build() del builder."""
        cmd = Command("ls")
        # Inyectamos un mock en la instancia existente
        cmd.builder = MagicMock()
        cmd.builder.build.return_value = ["-l", "-a"]

        # Ejecutamos
        resultado = cmd.args

        # Validamos
        assert resultado == ["-l", "-a"]
        cmd.builder.build.assert_called_once()

    def test_add_multiple_calls(self):
        """Verifica que las llamadas sucesivas a add_args sigan acumulando."""
        cmd = Command("grep")
        cmd.builder._args = []  # Usamos el builder real para este test si es simple

        cmd.add_args("-r").add_args("pattern")

        assert cmd.args == ["-r", "pattern"]
