for i in $(identify * | grep "GIF image data, version 89a"| cut -d ':' -f 1); do optipng -snip $i; rm $i; done
