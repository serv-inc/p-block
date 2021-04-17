for i in $(find . -name "*gif"); do optipng -snip $i; rm $i; done
