from searchbar import SearchBar
from firstLogin import FirstLogin
import util

if util.path_exists():
	sb = SearchBar.makeSearchBar()
	sb.display()
else:
	fl = FirstLogin.makeFirstLogin()
	fl.display()
