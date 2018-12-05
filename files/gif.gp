
set datafile separator ","
set key autotitle columnheader
set xrange [1:100]
set yrange [1:100]
set key outside

# More visually agreable
# set output 'grid_t'.i.'.png'

set title 'Time Step number '.i

plot 'grid_t'.i.'.csv' u 1:2 w p lc rgb 'green' pt 7 t 'Prey', '' u 3:4 w p lc rgb 'red' pt 7 t 'Predator'
i = i + 1
if (i <= 9) reread
