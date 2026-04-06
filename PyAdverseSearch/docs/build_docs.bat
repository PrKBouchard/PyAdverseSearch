@echo off
echo Building English (default) documentation...
sphinx-build -a -b html -D language=en . _build/html/en

echo Building French documentation...
sphinx-build -a -b html -D language=fr . _build/html/fr

echo Creating index redirect...
echo ^<!DOCTYPE html^> > _build/html/index.html
echo ^<html^> >> _build/html/index.html
echo ^<head^> >> _build/html/index.html
echo ^<meta charset="utf-8"^> >> _build/html/index.html
echo ^<title^>Redirecting...^</title^> >> _build/html/index.html
echo ^<script^> >> _build/html/index.html
echo var lang = navigator.language ^|^| navigator.userLanguage; >> _build/html/index.html
echo if (lang.toLowerCase().startsWith('fr')) { >> _build/html/index.html
echo     window.location.href = "fr/index.html"; >> _build/html/index.html
echo } else { >> _build/html/index.html
echo     window.location.href = "en/index.html"; >> _build/html/index.html
echo } >> _build/html/index.html
echo ^</script^> >> _build/html/index.html
echo ^<!-- Fallback if JS is disabled --^> >> _build/html/index.html
echo ^<meta http-equiv="refresh" content="0; url=en/index.html"^> >> _build/html/index.html
echo ^</head^> >> _build/html/index.html
echo ^<body^> >> _build/html/index.html
echo ^<a href="en/index.html"^>Go to English documentation^</a^> ^<br^> >> _build/html/index.html
echo ^<a href="fr/index.html"^>Aller à la documentation française^</a^> >> _build/html/index.html
echo ^</body^> >> _build/html/index.html
echo ^</html^> >> _build/html/index.html

echo Done! The documentation is in _build/html/

