#!/usr/bin/env -S perl -0777pi
BEGIN {
  $template = << 'EOF';
[tool.setuptools.dynamic.optional-dependencies.color]
file = "requirements/color.txt"
EOF
  while ($#ARGV > 0) {
    $name = shift;
    $name =~ s=.*requirements/(.+?)\.txt=$1=;
    $temp = $template;
    $temp =~ s/color/$name/g;
    push @temps, $temp;
  }
}
$dependencies = join "\n", @temps;
s=(# begin: scripts/generate-pyproject\.toml\.pl\n).*?(# end: scripts/generate-pyproject\.toml\.pl)=$1$dependencies$2=s;
