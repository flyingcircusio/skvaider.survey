{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  env.GREET = "skvaider.survey";

  # https://devenv.sh/packages/
  packages = [ pkgs.git ];

  # https://devenv.sh/languages/
  languages.python.enable = true;
  languages.python.uv.enable = true;

  # https://devenv.sh/processes/
  processes.dev.exec = "${lib.getExe pkgs.watchexec} --restart -w src -w uv.lock -w pyproject.toml -- uv run skvaider-survey web";

  # https://devenv.sh/services/
  # services.postgres.enable = true;

  # https://devenv.sh/tasks/
  # tasks = {
  #   "myproj:setup".exec = "mytool build";
  #   "devenv:enterShell".after = [ "myproj:setup" ];
  # };

  # https://devenv.sh/tests/
  enterTest = ''
    echo "Running tests"
    git --version | grep --color=auto "${pkgs.git.version}"
    uv run pytest
  '';

  # https://devenv.sh/git-hooks/
  # git-hooks.hooks.shellcheck.enable = true;

  # See full reference at https://devenv.sh/reference/options/
}
