require 'uri'
require 'rake/clean'
references  = 'references.csv'
imdb_mirror =  URI.parse('ftp://ftp.fu-berlin.de/pub/misc/movies/database/')
movie_links =  URI.parse(imdb_mirror.to_s + 'movie-links.list.gz')

CLEAN.include(references)

def mirror(uri, verbose = false)
  sh "wget #{verbose ? '-v' : '-q'} -c --no-host-directories -N -r -l 1 --no-remove-listing #{uri}"
end

file movie_links.path do
  mirror movie_links
end

task :mirror do
  mirror imdb_mirror
end

file references => movie_links.path do
  unless uptodate?(references, [movie_links.path])
    sh "zcat < #{movie_links.path} | ./links.rb references"
  end
end

task :rank => references do
  sh "./graph.py #{references}"
end
