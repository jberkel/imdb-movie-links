movie_links = 'pub/misc/movies/database/movie-links.list.gz'
references  = 'references.csv'
mirror      = 'ftp://ftp.fu-berlin.de/pub/misc/movies/database/'

task :mirror do
  sh "wget  -c --no-host-directories -v -N -r -l 1 --no-remove-listing #{mirror}"
end

file references do
  unless uptodate?(references, [movie_links])
    sh "zcat < #{movie_links} | ./links.rb references"
  end
end

task :rank => references do
  sh "./graph.py #{references}"
end
