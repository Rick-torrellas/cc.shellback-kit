from cc_shellback_kit import Command


class TestCommand:
    def test_command_initialization(self):
        """Verify that the command initializes with the correct executable."""
        cmd = Command("ls")
        assert cmd.executable == "ls"
        # Initially, the arguments list should be empty
        assert cmd.args == []

    def test_add_single_argument(self):
        """Verify the addition of a single positional argument."""
        cmd = Command("git")
        cmd.add_args("status")
        assert cmd.args == ["status"]

    def test_add_multiple_arguments_variadic(self):
        """Verify the addition of multiple arguments using *args."""
        cmd = Command("python")
        cmd.add_args("main.py", "--verbose", "run")
        assert cmd.args == ["main.py", "--verbose", "run"]

    def test_add_list_of_arguments(self):
        """
        Verify that the builder correctly flattens lists
        passed as arguments (thanks to ArgumentBuilder).
        """
        cmd = Command("tar")
        args_list = ["-czf", "backup.tar.gz", "/home/user"]
        cmd.add_args(args_list)
        assert cmd.args == ["-czf", "backup.tar.gz", "/home/user"]

    def test_fluent_interface(self):
        """Verify that add_args returns the instance (Fluent Interface pattern)."""
        cmd = Command("docker")
        returned_cmd = cmd.add_args("ps").add_args("-a")

        assert cmd is returned_cmd
        assert cmd.args == ["ps", "-a"]

    def test_mixed_arguments_types(self):
        """Verify the mixing of strings, numbers, and lists."""
        cmd = Command("echo")
        # The ArgumentBuilder internally converts to string and flattens
        cmd.add_args("User ID:", 1001, ["--force", "yes"])

        assert cmd.args == ["User ID:", "1001", "--force", "yes"]

    def test_empty_and_none_arguments(self):
        """Verify that None or empty values are ignored if the builder handles them that way."""
        cmd = Command("ls")
        cmd.add_args(None, "", "  ", "-l")

        # According to ArgumentBuilder.py, it ignores None and strings that remain empty after .strip()
        assert cmd.args == ["-l"]
