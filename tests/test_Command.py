from CapsuleCore_shellback import Command

## --- Tests de Inicialización ---


def test_command_initialization():
    """Verifica que el comando se inicialice con el ejecutable correcto."""
    cmd = Command("ls")
    assert cmd.executable == "ls"
    assert cmd.args == []


## --- Tests de Argumentos Posicionales ---


def test_command_add_single_arg():
    """Verifica la adición de un único argumento posicional."""
    cmd = Command("mkdir")
    cmd.add_args("my_folder")
    assert cmd.args == ["my_folder"]


def test_command_add_multiple_args():
    """Verifica la adición de múltiples argumentos en una sola llamada."""
    cmd = Command("rm")
    cmd.add_args("-rf", "/tmp/test")
    assert cmd.args == ["-rf", "/tmp/test"]


def test_command_method_chaining():
    """Verifica que add_args permita encadenamiento (fluent interface)."""
    cmd = Command("git")
    # El método debe retornar self para permitir esto
    result = cmd.add_args("commit").add_args("-m", "feat: initial")

    assert result is cmd
    assert cmd.args == ["commit", "-m", "feat: initial"]


## --- Tests de Integración con ArgumentBuilder (Flags) ---


def test_command_with_flags():
    """Verifica que se pueden mezclar argumentos posicionales y flags usando el builder interno."""
    cmd = Command("curl")
    cmd.add_args("-X", "POST")
    # Accediendo directamente al builder para usar flags
    cmd.builder.add_flag("header", "Content-Type: application/json")
    cmd.add_args("http://localhost:8080")

    expected = [
        "-X",
        "POST",
        "--header",
        "Content-Type: application/json",
        "http://localhost:8080",
    ]
    assert cmd.args == expected


def test_command_flag_style_persistence():
    """Verifica que el estilo de los flags se mantiene a través del builder."""
    cmd = Command("netstat")
    # Cambiamos el estilo del builder interno
    cmd.builder.style = "ms"
    cmd.builder.add_flag("a")

    assert cmd.args == ["/a"]
