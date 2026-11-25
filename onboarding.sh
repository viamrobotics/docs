#!/bin/bash

# Homebrew
if [ -x /opt/homebrew/bin/brew ] || command -v brew >/dev/null 2>&1; then
  echo "Homebrew already installed, skipping."
else
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

if grep -qF 'brew shellenv' "$HOME/.zprofile" 2>/dev/null; then
  echo "Homebrew shellenv already in ~/.zprofile, skipping."
else
  echo >> "$HOME/.zprofile"
  echo 'eval "$(/opt/homebrew/bin/brew shellenv zsh)"' >> "$HOME/.zprofile"
fi
eval "$(/opt/homebrew/bin/brew shellenv zsh)"


# uv
export PATH="$HOME/.local/bin:$PATH"
if command -v uv >/dev/null 2>&1; then
  echo "uv already installed, skipping."
else
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

if uv python find 3.10 >/dev/null 2>&1; then
  echo "Python 3.10 already installed, skipping."
else
  uv python install 3.10
fi


#hugo
if command -v hugo >/dev/null 2>&1 && hugo version | grep -q 'v0.152.2.*extended'; then
  echo "Hugo extended 0.152.2 already installed, skipping."
else
  mkdir -p ~/bin/hugo-0.152.2 && cd ~/bin/hugo-0.152.2
  curl -LO https://github.com/gohugoio/hugo/releases/download/v0.152.2/hugo_extended_0.152.2_darwin-universal.tar.gz
  tar -xzf hugo_extended_0.152.2_darwin-universal.tar.gz
  xattr -d com.apple.quarantine hugo 2>/dev/null
  sudo ln -sf ~/bin/hugo-0.152.2/hugo /usr/local/bin/hugo
  cd - >/dev/null
fi


#npm
export NVM_DIR="$HOME/.nvm"
if [ -s "$NVM_DIR/nvm.sh" ]; then
  echo "nvm already installed, skipping."
else
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.41.0/install.sh | bash
fi

[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

if nvm ls 'lts/*' >/dev/null 2>&1; then
  echo "Node LTS already installed, skipping."
else
  nvm install --lts
fi

npm install


#go
if command -v go >/dev/null 2>&1; then
  echo "Go already installed, skipping."
else
  brew install go
fi

#flake8
if command -v flake8 >/dev/null 2>&1; then
  echo "flake8 already installed, skipping."
else
  brew install flake8
  uv tool install flake8-markdown
fi


#htmltest
if command -v htmltest >/dev/null 2>&1; then
  echo "htmltest already installed, skipping."
else
  brew install htmltest
fi


#markdownlint
if command -v markdownlint >/dev/null 2>&1; then
  echo "markdownlint already installed, skipping."
else
  brew install markdownlint-cli
fi


