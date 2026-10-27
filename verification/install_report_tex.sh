#!/usr/bin/env bash
# Linux x86_64: install the frozen final TeX Live 2025 used by the report.
set -euo pipefail

if [[ $# != 1 ]]; then
  echo "Usage: bash verification/install_report_tex.sh /new/toolchain/path" >&2
  exit 2
fi
tl_root=$(realpath -m -- "$1")
if [[ -e "$tl_root" || "$tl_root" =~ [[:space:]] ]]; then
  echo "Choose a new toolchain path without whitespace: $tl_root" >&2
  exit 2
fi
tl_repository=https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2025/tlnet-final
installer_sha512=a307d7d11bcbd1f054ad0b0d476f7f12bc1a40d07445020edef8713b44453831d18a2f1722c3d2b0ea2e4fe6c06183a79d1c4049495113f412a9f5a570a8614d
database_sha512=2fb7adc54cff58fa55c5b7c1bd3034e1efd849d0b73535c8dcdf0d8a36f66998b7a578ae036ef24354641be5f3738b0ad1323b7318581d88a0e271d1ac12cb2b
installer_work=$(mktemp -d)
trap 'rm -rf -- "$installer_work"' EXIT
cd "$installer_work"
curl --fail --location --retry 3 --max-time 180 "$tl_repository/install-tl-unx.tar.gz" -o install-tl-unx.tar.gz
curl --fail --location --retry 3 --max-time 180 "$tl_repository/tlpkg/texlive.tlpdb.xz" -o texlive.tlpdb.xz
xz --decompress --keep texlive.tlpdb.xz
printf '%s  %s\n' "$installer_sha512" install-tl-unx.tar.gz | sha512sum --check -
printf '%s  %s\n' "$database_sha512" texlive.tlpdb | sha512sum --check -
tar -xzf install-tl-unx.tar.gz
cat > report.profile <<EOF
selected_scheme scheme-basic
TEXDIR $tl_root
TEXMFCONFIG $tl_root/texmf-config
TEXMFHOME $tl_root/texmf-home
TEXMFLOCAL $tl_root/texmf-local
TEXMFSYSCONFIG $tl_root/texmf-config
TEXMFSYSVAR $tl_root/texmf-var
TEXMFVAR $tl_root/texmf-var
binary_x86_64-linux 1
instopt_adjustpath 0
instopt_adjustrepo 0
instopt_letter 0
instopt_portable 0
instopt_write18_restricted 1
tlpdbopt_autobackup 0
tlpdbopt_create_formats 1
tlpdbopt_desktop_integration 0
tlpdbopt_file_assocs 0
tlpdbopt_generate_updmap 1
tlpdbopt_install_docfiles 0
tlpdbopt_install_srcfiles 0
tlpdbopt_post_code 1
EOF
perl install-tl-20260301/install-tl -no-interaction -profile report.profile -repository "$tl_repository"
"$tl_root/bin/x86_64-linux/tlmgr" --repository "$tl_repository" install \
  amsmath amsfonts mathtools geometry microtype lm xcolor hyperref booktabs pgf pgfplots tools
"$tl_root/bin/x86_64-linux/pdflatex" --version
