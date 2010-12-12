require 'uri'
require 'rake/clean'
require 'nokogiri'
references  = 'references.csv'
imdb_mirror =  URI.parse('ftp://ftp.fu-berlin.de/pub/misc/movies/database/')
movie_links =  URI.parse(imdb_mirror.to_s + 'movie-links.list.gz')

CLEAN.include('graph.dot', 'graph.svg', 'temp.svg')

def mirror(uri, verbose = false)
  sh "wget #{verbose ? '-v' : '-q'} -c --no-host-directories -N -r -l 1 --no-remove-listing #{uri}"
end

desc "perform a full imdb mirror"
task :mirror do
  mirror imdb_mirror
end

file movie_links.path do
  mirror movie_links
end

file references => movie_links.path do
  sh "zcat < #{movie_links.path} | ./links.rb references"
end

task :rank => references do
  sh "./rank.py #{references} --rank"
end

file 'graph.dot' => references do
  sh "./rank.py #{references} --graph --max=#{ENV['MAX'] || 100} > graph.dot"
end

file 'temp.svg' => 'graph.dot' do
 sh "dot -Tsvg graph.dot -o temp.svg"
end

file 'graph.svg' => [ 'temp.svg', file('styles.xml') ] do
  g = Nokogiri::XML(IO.read('temp.svg'))
  styles = Nokogiri::XML(IO.read('styles.xml'))

  styles.root.children.each { |c| g.root.add_child(c) }
  File.open('graph.svg', 'w') { |f| f << g.to_s }
end
