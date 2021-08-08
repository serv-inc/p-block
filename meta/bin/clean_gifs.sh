for i in $(identify * | grep " GIF "| cut -d ':' -f 1); do optipng -snip $i; rm $i; done
