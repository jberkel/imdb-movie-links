require 'uri'
require 'rake/clean'
require 'nokogiri'
require 'json'

references  = 'references.csv'
imdb_mirror =  URI.parse('ftp://ftp.fu-berlin.de/pub/misc/movies/database/')
movie_links =  URI.parse(imdb_mirror.to_s + 'movie-links.list.gz')
ratings     =  URI.parse(imdb_mirror.to_s + 'ratings.list.gz')

CLEAN.include('graph.dot', 'graph.svg', 'temp.svg')

def mirror(uri, verbose = false)
  sh "wget #{verbose ? '-v' : '-q'} -c --no-host-directories -N -r -l 1 --no-remove-listing #{uri}"
end

desc "perform a full imdb mirror"
task :mirror do
  mirror imdb_mirror
end

[movie_links, ratings].each do |f|
  file(f.path) { mirror f }
end

file references => movie_links.path do
  ref = ENV['REF'] || 'references'
  sh "zcat < #{movie_links.path} | ./links.rb #{ref} > #{references}"
end

task :rank => references do
  sh "./rank.py #{references} --pagerank"
end

file 'graph.dot' => references do
  max = ENV['MAX'] || 100
  max_edge = ENV['MAX_EDGE'] || -1
  sh "./rank.py #{references} --graph --max-edge-distance=#{max_edge} --max=#{max} > graph.dot"
end

file 'temp.svg' => 'graph.dot' do
 sh "dot -Tsvg graph.dot -o temp.svg"
end

file 'graph.svg' => [ 'temp.svg', file('styles.xml') ] do
  imdb_data = JSON.parse(IO.read('imdb_cache.json'))

  g = Nokogiri::XML(IO.read('temp.svg'))
  styles = Nokogiri::XML(IO.read('styles.xml'))

  # merge stylesheet
  styles.root.children.each { |c| g.root.add_child(c) }

  # add node metadata
  g.search('g.node').each do |node|
    title = node.search('title').text
    _class = ['node']
    if data = imdb_data[title]
      case data['kind']
        when 'tv series'
          _class << 'tv'
        when 'movie'
          _class << 'movie'
      end
      _class << 'top250' if data['top_250_rank'].to_i > 0

      node.set_attribute('class', _class.join(' '))
    end
  end

  # linkify text
  g.search('text').each do |text|
    if text.text =~ %r{(http://[^\s]+)}
      link = Nokogiri::XML::Node.new("a", g)
      link.set_attribute("xlink:href", $1)
      link.add_child(text.clone)
      text.replace(link)
    end
  end
  File.open('graph.svg', 'w') { |f| f << g.to_s }
end
