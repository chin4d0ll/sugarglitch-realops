# Hacker Aliases and Environment
# Add these to your ~/.bashrc

# Navigation shortcuts
alias ll='ls -la'
alias la='ls -A' 
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias workspace='cd /workspaces/sugarglitch-realops'
alias results='cd /workspaces/sugarglitch-realops/results'
alias targets='cd /workspaces/sugarglitch-realops/targets'

# Network and web analysis
alias ports='netstat -tuln'
alias processes='ps aux | grep'
alias myip='curl -s ifconfig.me'
alias headers='curl -I'
alias follow='curl -L -I'

# File operations
alias grep='grep --color=auto'
alias tree='find . -type d | sed -e "s/[^-][^\/]*\//  |/g" -e "s/|\([^ ]\)/|-\1/"'
alias sizeof='du -sh'
alias bigfiles='find . -type f -size +10M'

# Professional workflow
alias targets='cat /workspaces/sugarglitch-realops/targets.txt'
alias edittar='nano /workspaces/sugarglitch-realops/targets.txt'
alias sessions='ls -la /workspaces/sugarglitch-realops/sessions/'
alias database='sqlite3 /workspaces/sugarglitch-realops/alx_trading_database.sqlite'

# Quick analysis
alias jsonpp='python3 -m json.tool'
alias urldecode='python3 -c "import sys, urllib.parse; print(urllib.parse.unquote(sys.argv[1]))"'
alias urlencode='python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.argv[1]))"'
alias base64d='python3 -c "import sys, base64; print(base64.b64decode(sys.argv[1]).decode())"'
alias base64e='python3 -c "import sys, base64; print(base64.b64encode(sys.argv[1].encode()).decode())"'

# Git workflow
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline'

# Hacker-style prompt
export PS1='\[\e[1;31m\]┌[\[\e[1;33m\]\u\[\e[1;31m\]@\[\e[1;32m\]\h\[\e[1;31m\]]\[\e[1;34m\]─[\[\e[1;37m\]\w\[\e[1;31m\]]\n\[\e[1;31m\]└─\[\e[1;33m\]\$\[\e[0m\] '
